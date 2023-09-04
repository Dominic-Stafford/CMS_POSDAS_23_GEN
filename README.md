# CMS_POSDAS_23_GEN

##  Setting up CMSSW 
`source /cvmfs/cms.cern.ch/cmsset_default.sh`\
`scram p CMSSW_12_4_14_patch2`\
`cd CMSSW_12_4_14_patch2`\
`cmsenv`\
`cd -`

## Setting up MadGraph
`wget https://cms-project-generators.web.cern.ch/cms-project-generators/MG5_aMC_v2.9.13.tar.gz`\
`tar xf MG5_aMC_v2.9.13.tar.gz`\
`rm MG5_aMC_v2.9.13.tar.gz`\
`cd MG5_aMC_v2_9_13`

### Run with interactive command shell and install libraries and Pythia8 (~50min)
`./bin/mg5`\
`install lhapdf`\
`install zlib`\
`install hepmc`\
`install pythia8`\
`install collier`\
`install oneloop`\
`install ninja`

### Soft link the LHPDF data 
`change in /pathto/MG5_aMC_v2_9_13/HEPTools/lhapdf6_py3/share`\
`ln -s /pathto/lhapdf/share/LHAPDF .`


## Setting up [Rivet in CMSSW](https://twiki.cern.ch/twiki/bin/view/CMS/Rivet#Setting_Rivet_in_CMSSW)
`cmsrel CMSSW_12_5_0`\
`cd CMSSW_12_5_0/src`\
`cmsenv`\

`git-init-cms`\
`git-cms-addpkg GeneratorInterface/RivetInterface`\
`git-cms-addpkg Configuration/Generator`
`git clone https://gitlab.cern.ch/cms-gen/Rivet.git`\
`cd Rivet`\
`git remote add cmsgen https://gitlab.cern.ch/cms-gen/Rivet.git`\
`source rivetSetup.sh`\
`scram b -j8`\


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
