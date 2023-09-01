# CMS_POSDAS_23_GEN

##  Setting up CMSSW 
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW_9_3_9_patch2
cd CMSSW_12_4_4_patch2
cmsenv
cd -

## Setting up MadGraph
wget https://cms-project-generators.web.cern.ch/cms-project-generators/MG5_aMC_v2.9.16.tar.gz
tar xf MG5_aMC_v2.9.16.tar.gz
rm MG5_aMC_v2.9.16.tar.gz
cd MG5_aMC_v2.9.16

# Run with interactive command shell and install libraries (~1h)
./bin/mg5_aMC
install lhapdf
install zlib
install hepmc
install pythia8
install collier
install oneloop
install ninja

### Soft link the LHPDF data
change in ~/scratch-dust/cvs/madgraph/MG5_aMC_v2_9_16/HEPTools/lhapdf6_py3/share
ln -s /nfs/dust/cms/user/jung/cvs/lhapdf/share/LHAPDF .

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
