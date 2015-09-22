# -*- coding: utf-8 -*-
'''
'''
# These two lines are required at the top
from bibframe import BL, BA, REL, MARC, RBMS, AV
from bibframe.reader.util import *

LL = 'http://library.link/vocab/'

WORK_HASH_TRANSFORMS = {
    # Key creator info
    '100$a': onwork.rename(rel=LL + 'creatorName'),
    '100$d': onwork.rename(rel=LL + 'creatorDate'),

    '110$a': onwork.rename(rel=BL + 'organizationName'),
    '110$d': onwork.rename(rel=BL + 'organizationDate'),

    '111$a': onwork.rename(rel=BL + 'meetingName'),
    '111$d': onwork.rename(rel=BL + 'meetingDate'),

    '130$a': onwork.rename(rel=BL + 'collectionName'),

    # key uniform title info
    '240a': oninstance.rename(rel=LL + 'collectionTitle'),
    # '240f': oninstance.rename(rel=LL + 'collectionDate'),
    # '240n': oninstance.rename(rel=LL + 'collectionPartCount'),
    # '240o': oninstance.rename(rel=LL + 'collectionMusicArrangement'),
    # '240p': oninstance.rename(rel=LL + 'collectionPartName'),
    # '240l': oninstance.rename(rel=LL + 'collectionLanguage'),

    # Title info
    '245$a': onwork.rename(rel=BL + 'title'),
    '245$b': onwork.rename(rel=MARC + 'titleRemainder'),
    '245$c': onwork.rename(rel=MARC + 'titleStatement'),
    '245$n': onwork.rename(rel=MARC + 'titleNumber'),
    '245$p': onwork.rename(rel=MARC + 'titlePart'),
    '245$f': onwork.rename(rel=MARC + 'inclusiveDates'),
    '245$k': onwork.rename(rel=MARC + 'formDesignation'),

    # Title variation info
    '246$a': onwork.rename(rel=MARC + 'titleVariation'),
    '246$b': onwork.rename(rel=MARC + 'titleVariationRemainder'),
    '246$f': onwork.rename(rel=MARC + 'titleVariationDate'),

    # # Key edition info
    # '250$a': onwork.rename(rel=MARC + 'edition'),
    # '250$b': onwork.rename(rel=MARC + 'edition'),

    # Key subject info
    '600$a': onwork.rename(rel=LL + 'subjectName'),
    '610$a': onwork.rename(rel=LL + 'subjectName'),
    '611$a': onwork.rename(rel=LL + 'subjectName'),
    '650$a': onwork.rename(rel=LL + 'subjectName'),
    '651$a': onwork.rename(rel=LL + 'subjectName'),

    # Key contributor info
    '700$a': onwork.rename(rel=LL + 'relatedWorkOrContributorName'),
    '700$d': onwork.rename(rel=LL + 'relatedWorkOrContributorDate'),

    '710$a': onwork.rename(rel=LL + 'relatedWorkOrContributorName'),
    '710$d': onwork.rename(rel=LL + 'relatedWorkOrContributorDate'),

    '711$a': onwork.rename(rel=LL + 'relatedWorkOrContributorName'),
    '711$d': onwork.rename(rel=LL + 'relatedWorkOrContributorDate'),

    '730$a': onwork.rename(rel=BL + 'collectionName'),
}

# special thanks to UCD, NLM, GW
WORK_HASH_INPUT = [
    # Stuff derived from leader, 006 & 008
    VTYPE_REL,
    LL + 'date',
    LL + 'language',
    # MARC + 'literaryForm',
    # MARC + 'illustrations',
    # MARC + 'index',
    # MARC + 'natureOfContents',
    # MARC + 'formOfItem',
    # MARC + 'governmentPublication',
    # MARC + 'biographical',
    # MARC + 'formOfComposition',
    # MARC + 'formatOfMusic',
    # MARC + 'musicParts',
    # MARC + 'targetAudience',
    # MARC + 'accompanyingMatter',
    # MARC + 'literaryTextForSoundRecordings',
    # MARC + 'transpositionAndArrangement',
    # MARC + 'relief',
    # MARC + 'projection',
    # MARC + 'characteristic',
    # MARC + 'specialFormatCharacteristics',
    # MARC + 'runtime',
    # MARC + 'technique',
    # MARC + 'frequency',
    # MARC + 'regularity',
    # MARC + 'formOfOriginalItem',
    # MARC + 'natureOfEntireWork',
    # MARC + 'natureOfContents',
    # MARC + 'originalAlphabetOrScriptOfTitle',
    # MARC + 'entryConvention',
    # MARC + 'specificMaterialDesignation',
    # MARC + 'color',
    # MARC + 'physicalMedium',
    # MARC + 'typeOfReproduction',
    # MARC + 'productionReproductionDetails',
    # MARC + 'positiveNegativeAspect',
    # MARC + 'sound',
    # MARC + 'dimensions',
    # MARC + 'imageBitDepth',
    # MARC + 'fileFormat',
    # MARC + 'qualityAssuranceTargets',
    # MARC + 'antecedentSource',
    # MARC + 'levelOfCompression',
    # MARC + 'reformattingQuality',
    # MARC + 'typeOfReproduction',
    # MARC + 'classOfBrailleWriting',
    # MARC + 'levelOfContraction',
    # MARC + 'brailleMusicFormat',
    # MARC + 'specialPhysicalCharacteristics',
    # MARC + 'baseOfEmulsion',
    # MARC + 'soundOnMediumOrSeparate',
    # MARC + 'mediumForSound',
    # MARC + 'secondarySupportMaterial',
    # MARC + 'positiveNegativeAspect',
    # MARC + 'reductionRatioRange',
    # MARC + 'reductionRatio',
    # MARC + 'emulsionOnFilm',
    # MARC + 'generation',
    # MARC + 'baseOfFilm',
    # MARC + 'motionPicturePresentationFormat',
    # MARC + 'configurationOfPlaybackChannels',
    # MARC + 'productionElements',
    # MARC + 'refinedCategoriesOfColor',
    # MARC + 'kindOfColorStockOrPrint',
    # MARC + 'deteriorationStage',
    # MARC + 'completeness',
    # MARC + 'filmInspectionDate',
    # MARC + 'altitudeOfSensor',
    # MARC + 'cloudCover',
    # MARC + 'platformConstructionType',
    # MARC + 'platformUseCategory',
    # MARC + 'sensorType',
    # MARC + 'dataType',
    # MARC + 'speed',
    # MARC + 'configurationOfPlaybackChannels',
    # MARC + 'grooveWidthPitch',
    # MARC + 'tapeWidth',
    # MARC + 'tapeConfiguration',
    # MARC + 'kindOfDiscCylinderOrTape',
    # MARC + 'kindOfMaterial',
    # MARC + 'kindOfCutting',
    # MARC + 'specialPlaybackCharacteristics',
    # MARC + 'captureAndStorageTechnique',
    # MARC + 'videorecordingFormat',

    LL + 'collectionTitle',
    LL + 'collectionName',

    BL + 'title',
    MARC + 'titleRemainder',
    MARC + 'titleStatement',
    MARC + 'titleNumber',
    MARC + 'titlePart',
    MARC + 'inclusiveDates',
    MARC + 'formDesignation',

    MARC + 'titleVariation',
    MARC + 'titleVariationRemainder',
    MARC + 'titleVariationDate',

    # MARC + 'edition',

    LL + 'creatorName',
    LL + 'creatorDate',

    BL + 'organizationName',
    BL + 'organizationDate',

    BL + 'meetingName',
    BL + 'meetingNate',

    LL + 'subjectName',

    LL + 'relatedWorkOrContributorName',
    LL + 'relatedWorkOrContributorDate',
]
