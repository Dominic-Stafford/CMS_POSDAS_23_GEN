import sys
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing ('standard')
options.register('runOnly', '', VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string, "Run only specified analysis")
options.register('yodafile', 'test.yoda', VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string, "Name of yoda output file")
options.setDefault('maxEvents', 1000)
if(hasattr(sys, "argv")):
    options.parseArguments()
print (options)

process = cms.Process("runRivetAnalysis")

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))

process.source = cms.Source("EmptySource")

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.generator = cms.EDFilter("Pythia8GeneratorFilter",
     comEnergy = cms.double(13000.0),
     crossSection = cms.untracked.double(421.1),
     filterEfficiency = cms.untracked.double(1),
     maxEventsToPrint = cms.untracked.int32(0),
     pythiaHepMCVerbosity = cms.untracked.bool(False),
     pythiaPylistVerbosity = cms.untracked.int32(1),
     PythiaParameters = cms.PSet(
         processParameters = cms.vstring(
             'Main:timesAllowErrors = 10000',
             'ParticleDecays:limitTau0 = on',
             'ParticleDecays:tauMax = 10',
             'Tune:ee 7',
             'Tune:pp 14',      # Monash tune
             'Top:gg2ttbar    = on', # switch on g g -> t tbar 
             'Top:qqbar2ttbar = on', # switch on q qbar -> t tbar
             'PartonLevel:FSR = on', #Turn off FS parton Shower
             'PartonLevel:MPI = on', #Turn off Multiparton interactions
             'PartonLevel:ISR = on',
             '6:m0 = 172.5',    # top mass'
         ),
         parameterSets = cms.vstring('processParameters')
     )
)

process.load("GeneratorInterface.RivetInterface.rivetAnalyzer_cfi")

if options.runOnly:
    process.rivetAnalyzer.AnalysisNames = cms.vstring(options.runOnly)
else:
    process.rivetAnalyzer.AnalysisNames = cms.vstring(
        'CMS_2016_I1434354', # diff xs lepton+jets
        'MC_TTBAR', # MC analysis for lepton+jets
        'MC_TOPMASS_LJETS', # MC analysis for lepton+jets top mass
        #'CMS_LesHouches2015', # MC analysis for dilepton
        'MC_GENERIC', # MC generic analysis
        'MC_XS', # MC xs analysis
        'CMS_2016_I1491950',  # diff xs lepton+jets (2015 paper)
        'CMS_2018_I1620050',  # diff xs dilepton (2015 paper)
        #'CMS_2018_I1703993',  # diff xs dilepton (2016 paper)
    )
process.rivetAnalyzer.OutputFile      = options.yodafile
process.rivetAnalyzer.HepMCCollection = cms.InputTag("generator:unsmeared")
process.rivetAnalyzer.CrossSection    = 831.76 # NNLO (arXiv:1303.6254)

process.p = cms.Path(process.generator*process.rivetAnalyzer)


