'''
'''

import asyncio
import logging
from collections import defaultdict, OrderedDict
import warnings
import zipfile

from bibframe import g_services
from bibframe import BF_INIT_TASK, BF_MARCREC_TASK, BF_FINAL_TASK
from bibframe.reader.marcextra import transforms as extra_transforms

import rdflib

from versa import I, VERSA_BASEIRI, ORIGIN, RELATIONSHIP, TARGET, ATTRIBUTES
from versa import util
from versa.driver import memory

from bibframe import BFZ, BFLC, BL, register_service
from bibframe.reader import marc
from bibframe.writer import rdf
from bibframe.reader.marcpatterns import TRANSFORMS
from bibframe.reader.util import AVAILABLE_TRANSFORMS

from bibframe.reader.marcxml import handle_marcxml_source

BFNS = rdflib.Namespace(BFZ)
BFCNS = rdflib.Namespace(BFZ + 'cftag/')
BFDNS = rdflib.Namespace(BFZ + 'dftag/')

#VNS = rdflib.Namespace(VERSA_BASEIRI)

NSSEP = ' '

#PYTHONASYNCIODEBUG = 1


def bfconvert(inputs, handle_marc_source=handle_marcxml_source, entbase=None, model=None,
                out=None, limit=None, rdfttl=None, rdfxml=None, config=None,
                verbose=False, logger=logging, loop=None, canonical=False,
                lax=False, zipcheck=False):
    '''
    inputs - List of MARC/XML files to be parsed and converted to BIBFRAME RDF (Note: want to allow singular input strings)
    entbase - Base IRI to be used for creating resources.
    model - model instance for internal use
    out - file where raw Versa JSON dump output should be written (default: write to stdout)
    limit - Limit the number of records processed to this number. If omitted, all records will be processed.
    rdfttl - stream to where RDF Turtle output should be written
    rdfxml - stream to where RDF/XML output should be written
    config - configuration information
    verbose - If true show additional messages and information (default: False)
    logger - logging object for messages
    loop - optional asyncio event loop to use
    canonical - output Versa's canonical form?
    zipcheck - whether to check for zip files among the inputs
    '''
    #if stats:
    #    register_service(statsgen.statshandler)

    config = config or {}
    #if hasattr(inputs, 'read') and hasattr(inputs, 'close'):
        #It's a file type?
    #    inputs = [inputs]
    if limit is not None:
        try:
            limit = int(limit)
        except ValueError:
            logger.debug('Limit must be a number, not "{0}". Ignoring.'.format(limit))

    if 'marc_record_handler' in config:
        handle_marc_source = AVAILABLE_MARC_HANDLERS[config['marc_record_handler']]

    ids = marc.idgen(entbase)
    if model is None: model = memory.connection(logger=logger)
    g = rdflib.Graph()
    if canonical: global_model = memory.connection(attr_cls=OrderedDict)

    extant_resources = None
    #extant_resources = set()
    def postprocess():
        #No need to bother with Versa -> RDF translation if we were not asked to generate Turtle
        if any((rdfttl, rdfxml)): rdf.process(model, g, to_ignore=extant_resources, logger=logger)
        if canonical: global_model.add_many([(o,r,t,a) for (rid,(o,r,t,a)) in model])

        model.create_space()

    #Set up event loop if not provided
    if not loop:
        loop = asyncio.get_event_loop()

    #Allow configuration of a separate base URI for vocab items (classes & properties)
    #XXX: Is this the best way to do this, or rather via a post-processing plug-in
    vb = config.get('vocab-base-uri', BL)

    transform_iris = config.get('transforms', {})
    if transform_iris:
        transforms = {}
        for tiri in transform_iris:
            try:
                transforms.update(AVAILABLE_TRANSFORMS[tiri])
            except KeyError:
                raise Exception('Unknown transforms set {0}'.format(tiri))
    else:
        transforms = TRANSFORMS

    marcextras_vocab = config.get('marcextras-vocab')

    #Initialize auxiliary services (i.e. plugins)
    plugins = []
    for pc in config.get('plugins', []):
        try:
            pinfo = g_services[pc['id']]
            plugins.append(pinfo)
            pinfo[BF_INIT_TASK](pinfo, config=pc)
        except KeyError:
            raise Exception('Unknown plugin {0}'.format(pc['id']))

    limiting = [0, limit]
    #logger=logger,
    
    if zipcheck:
        warnings.warn("The zipcheck option is not working yet.", RuntimeWarning)
    
    for source_fname in inputs:
        #Note: 
        def input_fileset(sf):
            if zipcheck and zipfile.is_zipfile(sf):
                zf = zipfile.ZipFile(sf, 'r')
                for info in list(zf.infolist()):
                    #From the doc: Note If the ZipFile was created by passing in a file-like object as the first argument to the constructor, then the object returned by open() shares the ZipFile’s file pointer. Under these circumstances, the object returned by open() should not be used after any additional operations are performed on the ZipFile object.
                    sf.seek(0, 0)
                    zf = zipfile.ZipFile(sf, 'r')
                    yield zf.open(info, mode='r')
            else:
                if zipcheck:
                    #Because zipfile.is_zipfile fast forwards to EOF
                    sf.seek(0, 0)
                yield sf

        for infname in input_fileset(source_fname):
            @asyncio.coroutine
            #Wrap the parse operation to make it a task in the event loop
            def wrap_task(infname=infname):
                sink = marc.record_handler( loop,
                                            model,
                                            entbase=entbase,
                                            vocabbase=vb,
                                            limiting=limiting,
                                            plugins=plugins,
                                            ids=ids,
                                            postprocess=postprocess,
                                            out=out,
                                            logger=logger,
                                            transforms=transforms,
                                            extra_transforms=extra_transforms(marcextras_vocab),
                                            canonical=canonical)

                def resolve_class(fullname):
                    import importlib
                    modpath, name = fullname.rsplit('.', 1)
                    module = importlib.import_module(modpath)
                    cls = getattr(module, name)
                    return cls

                attr_cls = resolve_class(config.get('versa-attr-cls', 'collections.OrderedDict'))
                attr_list_cls = resolve_class(config.get('versa-attr-list-cls', 'builtins.list'))

                args = dict(lax=lax)
                handle_marc_source(infname, sink, args, attr_cls, attr_list_cls)
                sink.close()
                yield
            task = asyncio.async(wrap_task(), loop=loop)

    try:
        loop.run_until_complete(task)
    except Exception as ex:
        raise ex
    finally:
        loop.close()

    if canonical:
        out.write(repr(global_model))

    if vb == BFZ:
        g.bind('bf', BFNS)
        g.bind('bfc', BFCNS)
        g.bind('bfd', BFDNS)
    else:
        g.bind('vb', rdflib.Namespace(vb))
    if entbase:
        g.bind('ent', entbase)

    if rdfttl is not None:
        logger.debug('Converting to RDF.')
        rdfttl.write(g.serialize(format="turtle"))

    if rdfxml is not None:
        logger.debug('Converting to RDF.')
        rdfxml.write(g.serialize(format="pretty-xml"))
    return


AVAILABLE_MARC_HANDLERS = {
    "http://bibfra.me/tool/pybibframe/marchandler#marcjson": handle_marcxml_source
}

def register_marc_handler(iri, func):
    AVAILABLE_MARC_HANDLERS[iri] = func
