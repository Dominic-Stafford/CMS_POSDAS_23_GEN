# CMS_POSDAS_23_GEN

##  Preliminaries

###  Setting up CMSSW 

We will first activate a CMSSW environment to ensure everyone has a consistent set of enviroment variables. Make a new directory for this exercise and execute the following commands:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW_12_4_14_patch2
cd CMSSW_12_4_14_patch2
cmsenv
```

## Setting up [Rivet in CMSSW](https://twiki.cern.ch/twiki/bin/view/CMS/Rivet#Setting_Rivet_in_CMSSW)

We will use [Rivet](https://rivet.hepforge.org/) to analyse events. A version of Rivet has been designed to be run in CMSSW, which can be set up as follows:

```
git-init-cms
git-cms-addpkg GeneratorInterface/RivetInterface
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

### Installing [pylhe](https://github.com/scikit-hep/pylhe/tree/main)

We will use pylhe to analyse the lhe files produced by Madgraph. This can be simply installed with pip:

```
python3 -m pip install --user pylhe
```

### Mounting a file system

This last step is optional, but will make inspecting the output easier. Provided you are working on a linux machine, you can use ssh to mount the directories on naf on your local machine. To do this run the follow commands in a terminal on your local machine (i.e. without doing an ssh to your school account). You will need to exchange `schoolXX` for your account

```
mkdir my_das_school_dir
sshfs schoolXX@naf-cms.desy.de:/afs/desy.de/user/s/schoolXX my_das_school_dir
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

A folder called LO_ttbar will be created in the MG5_aMC_v2_9_13 directory, containing all of the information from this run. If you managed to mount your file system as described in the preliminaries, you can navigate to this directory and open `index.html` with your web browser, which gives an overview of the information. Clicking on "Process Information " shows the information about the different sub-processes considered, including the corresponding Feynmann diagrams. Clicking on "Results and Event Database" then "LHE" will show the LHE file containing the generated events. If you are unable to open the html file, you can instead unzip the lhe file and view it in the terminal:

```
gunzip LO_ttbar/Events/run_01/unweighted_events.lhe.gz
less LO_ttbar/Events/run_01/unweighted_events.lhe
```

Looking at the file, the first lines contains the log of the commands in the madgraph console and copies of the run, proc and automatically generated param cards used in the run (keeping a record of the settings used together with the generated run). After this there is some general information enclosed in an <init>...<\init> block, then each event is in its own block, enclosed by <event>...</event> tags. The first line contains general information about the event, then there is one line per particle, after which comes some reweighting information, enclosed in <mgrwt>...</mgrwt> tags, which can be used for a number purposes, including evaluating the effect of pdf variations. This is a standardised format used by all matrix element generators, documented [here](https://arxiv.org/abs/hep-ph/0609017) or in a somewhat more inteligible format [here](https://hugonweb.com/lheref/). This is obviously not the easiest format to read, however a number of packages are available to process this. We have provided a script to read this and produce some plots of different distibutions [scripts/plot_lhe.py](scripts/plot_lhe.py). Run this script:

```
python3 scripts/plot_lhe.py path/to/your/mgdir/LO_ttbar/Events/run_01/unweighted_events.lhe.gz lhe_plots
```

This will produce plots of the mass and pt of the tops, as well as the invariant mass of the ttbar system. Try modifying this script to also produce the pt of the ttbar system. Have a look at the plots. Are these what you would expect?

#### Extension:

- Add decays?
- Produce tt+1j mlm?

### 1b. Showering events using [Pythia8](https://www.pythia.org//latest-manual/Welcome.html)

...Briefly reiterate the concept of a PS, give introduction to pythia...

In CMSSW generation (and most other processes) is controlled by python configuration files, which typically end in `cfg.py`. These contain all of the options required to produce events, including generator information and information related to the specific year being produced. To ensure portability of processes between years, the generator information is factorised into a more light weight format called a "fragment", which typically end in `cff.py`. We have provided one such simple fragment designed to shower a LO madgraph lhe file with pythia in [Fragments/external_lhe_cff.py](Fragments/external_lhe_cff.py). This imports a set of common settings and the dedicated CMS UE Tune, CP5. To turn this fragment into a full configuration file that can produce events, one must first put it in a specific place within CMSSW, and recompile so CMSSW knows where to find it:

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
cmsDriver.py Configuration/GenProduction/python/external_lhe_cff.py --python_filename external_lhe_cfg.py --eventcontent RAWSIM --datatier GEN --filein file:/nfs/dust/cms/user/stafford/POSDAS_23/tmp/cmsgrid_final.lhe --fileout file:ttbar.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN --geometry DB:Extended --era Run2_2018 --no_exec --mc --customise_commands process.MessageLogger.cerr.FwkReport.reportEvery="int(1000)" -n 10000
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

## Exercise 2: Generating gridpacks

While running madgraph interactively is useful for smaller tests, it is rather cumbersome for large scale production, since the intial set-up would have to be repeated in each job. In CMS we therefore use "gridpacks", which are tarballs containing all of the information necessary to generate events. These can be produced using the [CMS genproductions repository](https://github.com/cms-sw/genproductions/tree/master), which contains cards for all of the different physics processes in CMS, and the code to make gridpacks of these for different generators. However since this is a very large repository, we will use a [lightweight version](https://github.com/Dominic-Stafford/POSDAS23_genproductions) for this exercise. In a new terminal session (without CMSSW active) check out this repository and navigate to the madgraph directory:

```
git clone https://github.com/Dominic-Stafford/POSDAS23_genproductions.git
cd POSDAS23_genproductions/bin/MadGraph5_aMCatNLO
```

We have already provided cards for ttbar production in [cards/examples/ttbar_LO](https://github.com/Dominic-Stafford/POSDAS23_genproductions/tree/master/bin/MadGraph5_aMCatNLO/cards/examples/ttbar_LO). These are the same as the run and proc cards you generated in the first section. To make a gridpack from these cards, execute the following command:

```
./gridpack_generation.sh ttbar_LO cards/examples/ttbar_LO
```

This will generate the feynmann diagrams, code and integration grid to produce events, perform a test run and then store all necessary files in a tarball. One can then generate lhe events from this gridpack within CMSSW using the externalLHEProducer class. We provide a fragment to do this and shower the event with pythia in [Fragments/gridpack_cff.py](Fragments/gridpack_cff.py). Open this and change the path on line 10 to point to the gridpack you just created. Then in your first terminal session (with the CMSSW environment set up) copy this to your CMSSW release, use cmsDriver to produce a cfg and run it:

```
cd /PATH/TO/CMSSW_12_4_14_patch2/src
cp /PATH/TO/CMS_POSDAS_23_GEN/Fragments/external_lhe_cff.py Configuration/GenProduction/python
scram b -j 4
cmsDriver.py Configuration/GenProduction/python/gridpack_cff.py --python_filename gridpack_cfg.py --eventcontent RAWSIM,LHE --datatier GEN,LHE --fileout file:ttbar_1j.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN --geometry DB:Extended --era Run2_2018 --no_exec --mc --customise_commands process.MessageLogger.cerr.FwkReport.reportEvery="int(1000)" -n 10000
cmsRun gridpack_cfg.py
```



## Exercise 3: Modify rivet routines
