import sys
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing ('standard')
options.register('runOnly', '', VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string, "Run only specified analysis")
options.register('yodafile', 'test.yoda', VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string, "Name of yoda output file")
if(hasattr(sys, "argv")):
    options.parseArguments()
print (options)

process = cms.Process("runRivetAnalysis")

process.load('Configuration.StandardSequences.Services_cff')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))

process.source = cms.Source("LHESource",
    fileNames = cms.untracked.vstring('file:../test/standalone_MG_ttbar.lhe')
)

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    #'processParameters',
                                    )
    )
)

process.load("GeneratorInterface.RivetInterface.rivetAnalyzer_cfi")

if options.runOnly:
    process.rivetAnalyzer.AnalysisNames = cms.vstring(options.runOnly)
else:
    process.rivetAnalyzer.AnalysisNames = cms.vstring(
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
process.rivetAnalyzer.OutputFile      = options.yodafile
process.rivetAnalyzer.HepMCCollection = cms.InputTag("generator:unsmeared")
process.rivetAnalyzer.CrossSection    = 252.89 # NNLO (arXiv:1303.6254)

process.p = cms.Path(process.generator*process.rivetAnalyzer)

