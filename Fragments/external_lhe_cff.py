import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    #'processParameters',
                                    )
    )
)

from GeneratorInterface.RivetInterface.rivetAnalyzer_cfi import rivetAnalyzer

rivetAnalyzer.AnalysisNames = cms.vstring(
    'CMS_2015_I1370682', # diff xs particle->parton level
    'CMS_2015_I1370682_internal', # diff xs parton level
    'CMS_2015_I1397174', # jet multiplicity dilepton
    'CMS_2016_I1454211', # boosted top
    'CMS_2016_I1473674', # HT, MET, ST, WPT
    'CMS_TOP_15_006', # jet multiplicity lepton+jets
    'MC_TTBAR', # MC analysis for lepton+jets
    'MC_TOPMASS_LJETS', # MC analysis for lepton+jets top mass
    'CMS_LesHouches2015', # MC analysis for dilepton
    'MC_GENERIC', # MC generic analysis
    'MC_XS', # MC xs analysis
)

ProductionFilterSequence = cms.Sequence(generator*rivetAnalyzer)
