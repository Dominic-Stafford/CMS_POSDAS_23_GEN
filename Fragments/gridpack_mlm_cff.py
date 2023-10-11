import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

externalLHEProducer = cms.EDProducer('ExternalLHEProducer',
  scriptName = cms.FileInPath("GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh"),
  outputFile = cms.string("cmsgrid_final.lhe"),
  numberOfParameters = cms.uint32(1),
  args = cms.vstring('/path/to/POSDAS23_genproductions/bin/MadGraph5_aMCatNLO/ttbar_LO_slc7_amd64_gcc900_CMSSW_12_0_2_tarball.tar.xz'),
  nEvents = cms.untracked.uint32(10000)
)

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
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = 50.', #this is the actual merging scale
            'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
            'JetMatching:nJetMax = 1', #number of partons in born matrix element for highest multiplicity
            'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

from GeneratorInterface.RivetInterface.rivetAnalyzer_cfi import rivetAnalyzer

rivetAnalyzer.AnalysisNames = cms.vstring(
    'MC_TTBAR', # MC analysis for lepton+jets
    'MC_PARTONICTOPS', # MC parton level top analysis
    'MC_TOPMASS_LJETS', # MC analysis for lepton+jets top mass
    'MC_FSPARTICLES', # MC generic analysis
    'MC_XS', # MC xs analysis
    'CMS_2016_I1491950',  # diff xs lepton+jets (2015 paper)
    'CMS_2018_I1620050',  # diff xs dilepton (2015 paper)
    'CMS_2018_I1663958',  # ttbar lepton+jets 13 TeV
)
rivetAnalyzer.OutputFile = cms.string("ttbar_gridpack.yoda")

ProductionFilterSequence = cms.Sequence(generator*rivetAnalyzer)
