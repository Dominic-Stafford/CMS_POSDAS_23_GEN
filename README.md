# CMS_POSDAS_23_GEN

##  Preliminaries

###  Setting up [CMSSW](https://github.com/cms-sw/cmssw) 

We will first configure a CMSSW release to ensure everyone has a consistent environment and set of enviroment variables. 
Create a new directory for this exercise and execute the following commands:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW_12_5_0
cd CMSSW_12_5_0/src
cmsenv
```

### Setting up [Rivet in CMSSW](https://twiki.cern.ch/twiki/bin/view/CMS/Rivet#Setting_Rivet_in_CMSSW)

We will use the [Rivet](https://rivet.hepforge.org/) program to analyse events. 
Rivet can be run from within CMSSW. To set it up run the following commands:

```
git clone https://gitlab.cern.ch/cms-gen/Rivet.git
cd Rivet
source rivetSetup.sh
scram b -j8
cd ../../..
```

### Setting up [MG5_aMC](https://launchpad.net/mg5amcnlo)
For the first exercise we will run the standalone madgraph5_aMC@NLO program. 
Download the program and extract the tarball using these commands:
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
### 1a.: Using madgraph5_aMC@NLO to generate parton-level events 

The first kind of program we will look at is a matrix-element (ME) generator, which produces “parton-level events”.
These codes take as input the Feynman rules of a given Lagrangian (typically the SM)
and use them to compute the ME and produce events for a given process using MC integrations (e.g. e+ e- -> mu+ mu-, p bar -> q qbar, p p > Z0 b, …).
These events will contain the fields present in the Lagrangian (leptons, quarks, gluons, photons),
which however do not usually correspond to the same particles produced in collider events (due to QCD confinement and other details we will discuss later on).
There are three codes specialized in producing parton-level events for (almost) arbitrary processes: Powheg, mg5_aMC and Sherpa.
They can all produce events ar leading- and next-to-leading and, for Powheg, also at next-to-next-to-leading order.
The madgraph5_aMC@NLO (in short MG5_aMC) program we will use in this tutorial is a flexible and powerful parton-level event generator.
It can perform the automatic computation of  parton-level events for arbitrary Standard Model processes
and for many theories Beyond the Standard Model at leading-order (LO) and next-to-leading-order (NLO) in the strong coupling.



MG5_aMC comes with an interactive shell, which is very helpful for learning the syntax of the commands. To start this, type:

```
./bin/mg5_aMC
```

This will show a splash screen, a few warnings related to additional packages not being installed (which you can ignore), and a list of predefined multiparticles such the proton. You will then see a command prompt. Two useful commands are `help`, to list all possible commands, or `tutorial`, which gives an interactive walk through of how to generate events. 

We will first need to specify the model we want to use. This specifies the particles considered and their interactions, and is implemented in Universal Feynrules Output (or UFO) format. A list of many models can be found at this link [Model Database](https://feynrules.irmp.ucl.ac.be/wiki/ModelDatabaseMainPage)
We can display the particle content of the model with this command:
```
import model sm
display multiparticles
```
For this tutorial we will  generate top quark pair production events at LO in QCD with the following commands: (Or should we ge them to run the interactive tutorial? It's also ttbar)

```
generate p p > t t~
output LO_ttbar
```

Starting from the Feynman rules of the SM MG5_aMC has now computed all of the feynman diagrams for the production of top quark pairs at LO and Fortran code to evaluate the squared matrix-elements. Have a look at the Feynman diagrams of the process (need X11 forwarding) by typing:

```
display diagrams
```

Now let's begin to integrate the process and generate the actual events with the following command:

```
launch
```


You will then see some switches for additional options, which can be left off for now. Then you will get the option to edit the cards which control the run: open these in turn (by default MG5_aMC will open these with vim, after you've finished looking enter :quit! to exit without saving). The param card contains the parameters for the currently used physics model- by default this contains all of the SM interactions. The proc card contains speicfic cuts and other settings for madgraph when running. After you have looked at these cards, MG5_aMC will compile some code to compute the process, then generate some events (by default 10000).

A folder called LO_ttbar will be created in the MG5_aMC_v2_9_13 directory, containing all of the information from this run. If you managed to mount your file system as described in the preliminaries, you can navigate to this directory and open `index.html` with your web browser, which gives an overview of the information. Clicking on "Process Information " shows the information about the different sub-processes considered, including the corresponding Feynmann diagrams. Clicking on "Results and Event Database" then "LHE" will point to the  file containing the generated events in Les Houches Event format. If you are unable to open the html file, you can instead unzip the lhe file and view it in the terminal:

```
gunzip LO_ttbar/Events/run_01/unweighted_events.lhe.gz
less LO_ttbar/Events/run_01/unweighted_events.lhe
```

Looking at the file, the first lines contains the log of the commands in the madgraph console and copies of the run, proc and automatically generated param cards used in the run (keeping a record of the settings used together with the generated run). After this there is some general information enclosed in an <init>...<\init> block, then each event is in its own block, enclosed by <event>...</event> tags. The first line contains general information about the event, then there is one line per particle, after which comes some reweighting information, enclosed in <mgrwt>...</mgrwt> tags, which can be used for a number purposes, including evaluating the effect of pdf variations. This is a standardised format used by all matrix element generators, documented [here](https://arxiv.org/abs/hep-ph/0609017) or in a somewhat more inteligible format [here](https://hugonweb.com/lheref/). This is obviously not the easiest format to read, however a number of packages are available to process this. We have provided a script to read this and produce some plots of different distibutions [scripts/plot_lhe.py](scripts/plot_lhe.py). Run this script:

```
python3 scripts/plot_lhe.py path/to/your/mgdir/LO_ttbar/Events/run_01/unweighted_events.lhe.gz lhe_plots
```

This will produce plots of the mass and transverse momentum, $p_T$, of each of the tops, as well as the invariant mass of the top-quark pair, $t\bar{t}$, system. Try modifying the script to also produce the $p_T$ of the $t\bar{t}$ system. Have a look at the plots. Are these what you would expect? 

#### Extensions:

- Generate events for the production of $t\bar{t}$  with one additional parton.
  Make the same plots and compare them to the sample generated before.
  Which ones change and how? Can you explain the differences?

- In the above exercise we have produced stable tops. We know in reality tops are unstable and do decay into (mostly) a W-boson and a b-quark.
  Try to regenerate the events but now including both the top-quark and W-boson decays (we consider here semileptonic decays)
  ```
  generate p p > t t~, (t > W+ b, W+ > j j), (t~ > W- b~, W- > l- vl~)
  ```
  The above code will calculate the top production and decay process independently, in the so-called Narrow Width Approximation (NWA).
  Strictly speaking this is only exact in the limit of a vanishing top quark width,
  and the approximation will be worse and worse as one goes away from the resonance peak.



### 1b. Showering events using [Pythia8](https://www.pythia.org//latest-manual/Welcome.html)

Since QCD confines, quarks and gluons are not physically observable.
It is the job of Parton Shower programs to convert the Parton level events in to “particle-level” event samples
They will emit many soft and collinear QCD partons (which we can conveniently map into “jets”)
which will ultimately hadronise into hadrons and which after decay will produce the stable hadrons observable in our detector.
In addition, when two proton collides one can have multiple partons simultaneously producing a QCD interaction
(i.e. a g g -> j j collision overlapping with a q bar -> e+ e- collision where all partons are from the same protons.
The description of these Multiple Parton Interactions (MPI) is also performed by the parton showers.
The three main parton shower programs are Pythia8, Herwig and Sherpa, which differ in the details of the algorithms used both for the parton showering, hadronization and the MPI modeling. In this exercise we will explore the Pythia8 shower code.

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
cmsDriver.py Configuration/GenProduction/python/external_lhe_cff.py --python_filename external_lhe_cfg.py --eventcontent RAWSIM,NANOAODGEN --datatier GEN,NANOAOD --filein file:PATH/TO/YOUR/unweighted_events.lhe --fileout file:ttbar.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN,NANOGEN --geometry DB:Extended --era Run2_2018 --no_exec --mc --customise_commands process.MessageLogger.cerr.FwkReport.reportEvery="int(1000)" -n 10000
```

One can then run the config thus produced using the following command:

```
cmsRun external_lhe_cfg.py
```

By default, pythia produces events in the HEPMC format. We provide an example of 10 events in this format in [ttbar.hepmc](ttbar.hepmc). As you can see, this is not very readable, being a list of vertices (V) and particles coming from these (P). This is not outputted by CMSSW, but instead converted to a root file in the GEN format (`ttbar.root`). This is not very easy to analyse directly, and is intended for passing to further commands to run the detector simulation and reconstruction to provide the (mini/nano)AOD samples you use in your analysis.

The command you have just run further converts this to nanoGEN, a format similar to nanoAOD containing only generator information. You can try opening `ttbar_inNANOAODGEN.root` with either ROOT or uproot - you can find the pdgIds of the generated particles in the "GenPart_pdgId" branch of the "Events" tree, see what other properties you can find.

However for this exercise we will not attempt to perform an anlysis directly on this file, but instead look at the output of some analyses implemented in rivet which we included in the fragment.  We will cover how to make your own rivet analysis in section 3, but for now you can look at the output of the pre-defined ones, which include some unfolded data from previous anlyses. cmsRun will have produced a rivetfile called `ttbar_external_lhe.yoda` containing all of the output histograms from these analyses, which one can plot with the following command:

```
rivet-mkhtml --mc-errs ttbar_external_lhe.yoda
```

This will produce a directory called `rivet-plots`. If you managed to mount the file system, you can just open `rivet-plots/index.html` with a web browser, which will allow you to browse through the plots from the different analyses, along with their descriptions. If you didn't manage to mount the file system you can still open the individual pdf or png images inside these directories. have a look at the output distributions. Do these agree with the data? Is this what you would expect?

#### Extensions:

Pythia does a lot of steps to convert the hard process to a full event: a parton shower is run to simulate additional emissions (which can be separated into final state radiation (FSR), which leads to the formation of jets, and inital state radiation (ISR), which tends to produce additional jets), then the event is hadronised to turn the coloured particles into colourless hadrons, then the unstable hadrons are decayed. Additional interactions are also simulated due to the interaction of other partons in the colliding protons (multi-parton interactions, MPI). The best way to get a feel for these is to turn these off sequentially and look at the impact on the rivet analyses. In the `parameterSets` section of your `external_lhe_cfg.py` uncomment `processParameters` to allow additional options. You can then uncomment each of the lines in your `processParameters` block to turn each step off and rerun with `cmsRun` for each. You will also need to change the `OutputFile` argument of the `rivetAnalyzer` to save the histograms in a different file each time. To better compare, one can plot multiple rivet analyses on the same axes:

```
rivet-mkhtml --mc-errs ttbar_external_lhe.yoda MPI_off.yoda
```

Feel free to discuss your outputs with the Facilators to understand the impact of each step.

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
cp /PATH/TO/CMS_POSDAS_23_GEN/Fragments/gridpack_cff.py Configuration/GenProduction/python
scram b -j 4
cmsDriver.py Configuration/GenProduction/python/gridpack_cff.py --python_filename gridpack_cfg.py --eventcontent RAWSIM,LHE --datatier GEN,LHE --fileout file:ttbar_1j.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN --geometry DB:Extended --era Run2_2018 --no_exec --mc --customise_commands process.MessageLogger.cerr.FwkReport.reportEvery="int(1000)" -n 10000
cmsRun gridpack_cfg.py
```

You can then produce the rivet plots for this run, and compare it to what you produced for the external LHE. Do these agree? Would you expect them to?

```
rivet-mkhtml --mc-errs ttbar_gridpack.yoda ttbar_external_lhe.yoda
```

#### Extensions:

- To get a higher accuracy, one can simulate ttbar at next-to-leading order (NLO) with Madgraph. We provide the cards for this in `cards/examples/ttbar_NLO` have a look at these cards, produce a gridpack from them and shower this with pythia. How do the rivet plots compare to the LO ones?

- An alternative to producing full higher order predictions is to produce events at leading order with additional jets in madgraph, which can capture some of the higher order effect. Commonly this is done with up to four additional jets, however to have a reasonably quick example for this exercise we provide cards for ttbar with up to 1 additional jet in `cards/examples/tt1j_mlm`. This can lead to some double counting with the parton shower emmissions in Pythia, so we need to tell Pythia to remove this double counting. This can be done with the [Fragments/gridpack_mlm_cff.py](Fragments/gridpack_mlm_cff.py) fragment. How do these predictions compare to NLO and LO without additional emissions?

## Exercise 3: Modify rivet routines
Rivet is a system for validation of Monte Carlo event generators that provides a large set of experimental analysis. It contains most of the LHC and other high-energy colliders experiments code which is preserved for comparison and develompent of future therory models. In this exercise we will use CMS_2016_I1491950 and will modify to add the number of jets and jet pt doing:
```
vim CMSSW_12_5_0/src/Rivet/TOP/src/CMS_2016_I1491950.cc
```
and will book  the histograms inside `void init() {}` as:

```
    //book hists
    book(_h_pt1, "pt_jet1", logspace(50,1,500));
    book(_h_pt2, "pt_jet2", logspace(50,1,500));
    book(_h_pt3, "pt_jet3", logspace(50,1,500));
    book(_h_pt4, "pt_jet4", logspace(50,1,500));

```

Then inside the `void analyze ()` fill the histograms as:

```
      // fill histograms     
      _h_pt1->fill(allJets[0].pT());
      _h_pt2->fill(allJets[1].pT());
     
      if( allJets.size() > 2 ) _h_pt3->fill(allJets[2].pT());
      if( allJets.size() > 3 ) _h_pt4->fill(allJets[3].pT());
```


And finally in `void finalize(){}` normalize the histos as:

```
    void finalize()
    {
      //new histo normalize
      scale(_h_pt1, crossSection()/sumOfWeights());
      scale(_h_pt2, crossSection()/sumOfWeights());
      scale(_h_pt3, crossSection()/sumOfWeights());
      scale(_h_pt4, crossSection()/sumOfWeights());
```

Then at the very end one needs to declare the histograms as:

```
   Histo1DPtr _h_pt1;
   Histo1DPtr _h_pt2;
   Histo1DPtr _h_pt3;
   Histo1DPtr _h_pt4;

```

Then inside  `CMSSW_12_5_0/src/Rivet` do `scram b -j8` to compile the rivet routine. 

One then needs to rerun the CMSSW routine which generates events and runs the new analysis, then re-plot the outputs:

```
 cmsRun external_lhe_cfg.py
 rivet-mkhtml --mc-errs ttbar_external_lhe.yoda
```

