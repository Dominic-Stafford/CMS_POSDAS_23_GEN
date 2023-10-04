# CMS_POSDAS_23_GEN

##  Preliminaries

###  Setting up CMSSW 

We will first activate a CMSSW environment to ensure everyone has a consistent set of enviroment variables. Make a new directory for this exercise and execute the following commands:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW_12_5_0
cd CMSSW_12_5_0/src
cmsenv
```

### Setting up [Rivet in CMSSW](https://twiki.cern.ch/twiki/bin/view/CMS/Rivet#Setting_Rivet_in_CMSSW)

We will use [Rivet](https://rivet.hepforge.org/) to analyse events. A version of Rivet has been designed to be run in CMSSW, which can be set up as follows:

```
git clone https://gitlab.cern.ch/cms-gen/Rivet.git
cd Rivet
source rivetSetup.sh
scram b -j8
cd ../../..
```

### Setting up [MadGraph](https://launchpad.net/mg5amcnlo)

```
wget https://cms-project-generators.web.cern.ch/cms-project-generators/MG5_aMC_v2.9.13.tar.gz
tar xf MG5_aMC_v2.9.13.tar.gz
rm MG5_aMC_v2.9.13.tar.gz
```

## Exercise 1
### 1a.: Using MadGraph to generate parton-level events 

...Briefly descirbe ME generators...

Madgraph comes with an interactive shell, which is very helpful for learning the syntax of the commands. To start this, type:

```
./bin/mg5_aMC
```

This will show a splash screen, a few warnings related to additional packages not being installed (which you can ignore), and a list of predefined multiparticles such the proton. You will then see a command prompt. Two useful commands are `help`, to list all possible commands, or `tutorial`, which gives an interactive walk through of how to generate events. For this tutorial one can generate a ttbar event with the following commands: (Or should we ge them to run the interactive tutorial? It's also ttbar)

```
generate p p > t t~
output LO_ttbar
launch
```

You will then see some switches for additional options, which can be left off for now. Then you will get the option to edit the cards which control the run: open these in turn (by default madgraph will open these with vim, after you've finished looking enter :quit! to exit without saving). The param card contains the parameters for the currently used physics model- by default this contains all of the SM interactions. The proc card contains speicfic cuts and other settings for madgraph when running. After you have looked at these cards, madgraph will compile some code to compute the process, then generate some events (by default 10000).

Look in lhe file

To add: script for looking at lhe events

Extensions:
- Add decays (with madspin?)
- Redefine the proton to include b quarks (and set b mass to 0)
- Produce tt+1j mlm
- Uncertainty weights?

### 1b. Showering events using [Pythia8](https://www.pythia.org//latest-manual/Welcome.html)

...Briefly reiterate the concept of a PS, give introduction to pythia...

In CMSSW generation (and most other processes) is controlled by python configuration files, which typically end in `cfg.py`. These contain all of the options required to produce events, including generator information and information related to the specific year being produced. To ensure portability of processes between years, the generator information is factorised into a more light weight format called a "fragment", which typically end in `cff.py`. We have provided one such simple fragment designed to shower a LO madgraph lhe file with pythia in `CMS_POSDAS_23_GEN/Fragments/external_lhe_cff.py`. This imports a set of common settings and the dedicated CMS UE Tune, CP5. To turn this fragment into a full configuration file that can produce events, one must first put it in a specific place within CMSSW, and recompile so CMSSW knows where to find it:

```
cd /PATH/TO/CMSSW_12_4_14_patch2/src
mkdir Configuration
mkdir Configuration/GenProduction
mkdir Configuration/GenProduction/python
cp /PATH/TO/CMS_POSDAS_23_GEN/Fragments/external_lhe_cff.py Configuration/GenProduction/python
scram b -j 4
```

The command that converts fragments to full configurations is cmsDriver.py this has many options, however generally one can take a pre-existing command from a previous generator request in the same campaign, so does not need to memorise all the options. For this tutorial run the following command:

```
cmsDriver.py Configuration/GenProduction/python/external_lhe_cff.py --python_filename external_lhe_cfg.py --eventcontent RAWSIM --datatier GEN --filein file:/nfs/dust/cms/user/stafford/POSDAS_23/tmp/cmsgrid_final.lhe --fileout file:ttbar.root --conditions 124X_mcRun3_2022_realistic_postEE_v1 --beamspot Realistic25ns13p6TeVEarly2022Collision --step GEN --geometry DB:Extended --era Run3 --no_exec --mc --customise_commands process.MessageLogger.cerr.FwkReport.reportEvery="int(1000)" -n 10000
```

One can then run the config thus produced using the following command:

```
cmsRun external_lhe_cfg.py
```

Look at printed event output

Look at rivet plots

(### Rivet routines for top)
https://rivet.hepforge.org/analyses/MC_TTBAR.html
https://rivet.hepforge.org/analyses/MC_PARTONICTOPS.html

Extensions:
- Look at effects of turning on and off MPI, had, FSR, ISR, QED, etc.
- Do run with shower uncertainties? (quite slow)

## Exercise 2: Generating gridpacks

Start with ttbar+1jet (mlm)
Then move to FxFx

## Exercise 3: Modify rivet routines
