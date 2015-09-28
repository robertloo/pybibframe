# -*- coding: utf-8 -*-
'''
Test some small, simple MARC snippets.

Requires http://pytest.org/ e.g.:

pip install pytest

Each test case is a triple of e.g. [SNIPPET_1, CONFIG_1, EXPECTED_1]

You must have matched series each with all 3 components matched up, otherwise the entire test suite will fall over like a stack of dominoes

----

Recipe for regenerating the test case expected outputs:

python -i test/test_marc_snippets3.py #Ignore the SystemExit

Then:

all_snippets = sorted([ sym for sym in globals() if sym.startswith('SNIPPET') ])
all_config = sorted([ sym for sym in globals() if sym.startswith('CONFIG') ])
all_expected = sorted([ sym for sym in globals() if sym.startswith('EXPECTED') ])

for s, c, e in zip(all_snippets, all_config, all_expected):
    sobj, cobj, eobj = globals()[s], globals()[c], globals()[e]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    m = memory.connection()
    instream = BytesIO(sobj.encode('utf-8'))
    outstream = StringIO()
    bfconvert(instream, model=m, out=outstream, config=cobj, canonical=True, loop=loop)
    print('EXPECTED from {0}:'.format(s))
    print(outstream.getvalue()) #This output becomes the EXPECTED stanza

'''

import sys
import logging
import asyncio
import difflib
from io import StringIO, BytesIO
import tempfile

from amara3.inputsource import factory

from versa.driver import memory
from versa.util import jsondump, jsonload

from bibframe.reader import bfconvert
import bibframe.plugin
from bibframe.util import hash_neutral_model

import pytest

#Bits from http://www.loc.gov/standards/marcxml/Sandburg/sandburg.xml

#XXX Add test for 8a subfield code warning
SNIPPET_21 = '''<collection xmlns="http://www.loc.gov/MARC21/slim">
<record>
  <leader>02143nam a22004218a 4500</leader>
  <!-- Note the following 2 ISBNs, once normalized, are the same -->
  <datafield ind2=" " ind1=" " tag="020"><subfield code="a">9781615302550</subfield></datafield>
  <datafield ind2=" " ind1=" " tag="020"><subfield code="a">1615302557</subfield></datafield>
  <datafield ind2="4" ind1="0" tag="245">
    <!-- Note: should issue somethig like: WARNING:root:Invalid subfield code "8a" in record "record-2:0", tag "245" -->
    <subfield code="8a">The eye</subfield>
    <subfield code="h">[downloadable ebook] :</subfield>
    <subfield code="b">the physiology of human perception /</subfield>
    <subfield code="c">edited by Kara Rogers</subfield>
  </datafield>
  <datafield ind2=" " ind1="0" tag="776">
    <subfield code="c">Original</subfield>
    <subfield code="z">9781615301164</subfield>
    <subfield code="w">sky235195071</subfield>
  </datafield>
</record>
</collection>
'''

CONFIG_21 = None

EXPECTED_21 = '''
[
    [
        "3f9AOY8U7fg",
        "http://bibfra.me/purl/versa/type",
        "http://bibfra.me/vocab/lite/Instance",
        {
            "@target-type": "@iri-ref"
        }
    ],
    [
        "3f9AOY8U7fg",
        "http://bibfra.me/vocab/lite/instantiates",
        "tVaxKHAonKQ",
        {
            "@target-type": "@iri-ref"
        }
    ],
    [
        "3f9AOY8U7fg",
        "http://bibfra.me/vocab/lite/medium",
        "[downloadable ebook] :",
        {}
    ],
    [
        "3f9AOY8U7fg",
        "http://bibfra.me/vocab/marc/isbn",
        "9781615302550",
        {}
    ],
    [
        "3f9AOY8U7fg",
        "http://bibfra.me/vocab/marc/titleRemainder",
        "the physiology of human perception /",
        {}
    ],
    [
        "3f9AOY8U7fg",
        "http://bibfra.me/vocab/marc/titleStatement",
        "edited by Kara Rogers",
        {}
    ],
    [
        "3f9AOY8U7fg",
        "http://bibfra.me/vocab/relation/hasOtherPhysicalFormat",
        "GxDFRy2DEyA",
        {
            "@target-type": "@iri-ref"
        }
    ],
    [
        "GxDFRy2DEyA",
        "http://bibfra.me/purl/versa/type",
        "http://bibfra.me/vocab/lite/Instance",
        {
            "@target-type": "@iri-ref"
        }
    ],
    [
        "GxDFRy2DEyA",
        "http://bibfra.me/vocab/lite/authorityLink",
        "http://bibfra.me/vocab/marcext/authrec/sky235195071",
        {
            "@target-type": "@iri-ref"
        }
    ],
    [
        "GxDFRy2DEyA",
        "http://bibfra.me/vocab/lite/instantiates",
        "tVaxKHAonKQ",
        {
            "@target-type": "@iri-ref"
        }
    ],
    [
        "GxDFRy2DEyA",
        "http://bibfra.me/vocab/lite/medium",
        "[downloadable ebook] :",
        {}
    ],
    [
        "GxDFRy2DEyA",
        "http://bibfra.me/vocab/lite/note",
        "Original",
        {}
    ],
    [
        "GxDFRy2DEyA",
        "http://bibfra.me/vocab/marc/isbn",
        "9781615301164",
        {}
    ],
    [
        "GxDFRy2DEyA",
        "http://bibfra.me/vocab/marc/titleRemainder",
        "the physiology of human perception /",
        {}
    ],
    [
        "GxDFRy2DEyA",
        "http://bibfra.me/vocab/marc/titleStatement",
        "edited by Kara Rogers",
        {}
    ],
    [
        "GxDFRy2DEyA",
        "http://bibfra.me/vocab/marcext/sf-c",
        "Original",
        {}
    ],
    [
        "GxDFRy2DEyA",
        "http://bibfra.me/vocab/marcext/sf-w",
        "sky235195071",
        {}
    ],
    [
        "GxDFRy2DEyA",
        "http://bibfra.me/vocab/marcext/sf-z",
        "9781615301164",
        {}
    ],
    [
        "tVaxKHAonKQ",
        "http://bibfra.me/purl/versa/type",
        "http://bibfra.me/vocab/lite/Work",
        {
            "@target-type": "@iri-ref"
        }
    ],
    [
        "tVaxKHAonKQ",
        "http://bibfra.me/purl/versa/type",
        "http://bibfra.me/vocab/marc/Books",
        {
            "@target-type": "@iri-ref"
        }
    ],
    [
        "tVaxKHAonKQ",
        "http://bibfra.me/purl/versa/type",
        "http://bibfra.me/vocab/marc/LanguageMaterial",
        {
            "@target-type": "@iri-ref"
        }
    ],
    [
        "tVaxKHAonKQ",
        "http://bibfra.me/vocab/marc/titleRemainder",
        "the physiology of human perception /",
        {}
    ],
    [
        "tVaxKHAonKQ",
        "http://bibfra.me/vocab/marc/titleStatement",
        "edited by Kara Rogers",
        {}
    ],
    [
        "tVaxKHAonKQ",
        "http://bibfra.me/vocab/marcext/tag-020-XX-a",
        "1615302557",
        {}
    ],
    [
        "tVaxKHAonKQ",
        "http://bibfra.me/vocab/marcext/tag-020-XX-a",
        "9781615302550",
        {}
    ]
]
'''

all_snippets = sorted([ sym for sym in globals() if sym.startswith('SNIPPET') ])
all_config = sorted([ sym for sym in globals() if sym.startswith('CONFIG') ])
all_expected = sorted([ sym for sym in globals() if sym.startswith('EXPECTED') ])

all_snippets = [ (sym, globals()[sym]) for sym in all_snippets ]
all_config = [ (sym, globals()[sym]) for sym in all_config ]
all_expected = [ (sym, globals()[sym]) for sym in all_expected ]

def file_diff(s_orig, s_new):
    diff = difflib.unified_diff(s_orig.split('\n'), s_new.split('\n'))
    return '\n'.join(list(diff))


def run_one(snippet, expected, desc, entbase=None, config=None, loop=None, canonical=True):
    m = memory.connection()
    m_expected = memory.connection()
    infile = tempfile.NamedTemporaryFile()
    infile.write(snippet.encode('utf-8'))
    infile.seek(0)
    outstream = StringIO()
    bfconvert([infile], model=m, out=outstream, config=config, canonical=canonical, loop=loop)
    #bfconvert(factory(infile), model=m, out=outstream, config=config, canonical=canonical, loop=loop)
    infile.close()
    outstream.seek(0)
    hashmap, m = hash_neutral_model(outstream)
    hashmap = '\n'.join(sorted([ repr((i[1], i[0])) for i in hashmap.items() ]))

    expected_stream = StringIO(expected)
    hashmap_expected, m_expected = hash_neutral_model(expected_stream)
    hashmap_expected = '\n'.join(sorted([ repr((i[1], i[0])) for i in hashmap_expected.items() ]))

    assert hashmap == hashmap_expected, "Changes to hashes found ({0}):\n{1}\n\nActual model structure diff:\n{2}".format(desc, file_diff(hashmap_expected, hashmap), file_diff(repr(m_expected), repr(m)))
    assert m == m_expected, "Discrepancies found ({0}):\n{1}".format(desc, file_diff(repr(m_expected), repr(m)))


@pytest.mark.parametrize('snippet, config, expected', zip(all_snippets, all_config, all_expected))
def test_snippets(snippet, config, expected):
    #Use a new event loop per test instance, and so one call of bfconvert per test
    desc = '|'.join([ t[0] for t in (snippet, config, expected) ])
    snippet, config, expected = [ t[1] for t in (snippet, config, expected) ]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)

    run_one(snippet, expected, desc, config=config, loop=loop)


if __name__ == '__main__':
    raise SystemExit("use py.test")
