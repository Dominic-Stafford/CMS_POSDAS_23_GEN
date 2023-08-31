# CMS_POSDAS_23_GEN

##  Setting up CMSSW 
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW_9_3_9_patch2
cd CMSSW_12_4_4_patch2
cmsenv
cd -

## Setting up MadGraph
wget https://cms-project-generators.web.cern.ch/cms-project-generators/MG5_aMC_v2.6.0.tar.gz
tar xf MG5_aMC_v2.6.0.tar.gz
rm MG5_aMC_v2.6.0.tar.gz
cd MG5_aMC_v2_6_0

# Run with interactive command shell
./bin/mg5

## Using MadGraph to generate parton-level events 

### Standalone Madgraph syntax LO, NLO, decays...
### Structure of a Les Houches Event file 
### Uncertainty weights
### Running in CMSSW

## Showering events using Pythia8
### Standalone Pythia8 run
### Structure of an HepMC file
### Showering LHE events
### Shower settings (switch off QCD ISR, hadronisation, ..QED FSR)
### Shower uncertainties

## Analyse and plot events with Rivet
