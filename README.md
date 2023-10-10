# CMS_POSDAS_23_GEN

##  Preliminaries

###  Setting up CMSSW 

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

## Exercise 1
### 1a.: Using madgraph5_aMC@NLO to generate parton-level events 

...Briefly descirbe ME generators...

The madgraph5_aMC@NLO (in short MG5_aMC) program is a flexible and powerful parton-level event generator.
It can perform the automatic computation of  parton-level events for arbitrary Standard Model processes
and for many theories Beyond the Standard Model at leading-order (LO) and next-to-leading-order (NLO) in the strong coupling.



MG5_aMC comes with an interactive shell, which is very helpful for learning the syntax of the commands. To start this, type:

```
./bin/mg5_aMC
```

This will show a splash screen, a few warnings related to additional packages not being installed (which you can ignore), and a list of predefined multiparticles such the proton. You will then see a command prompt. Two useful commands are `help`, to list all possible commands, or `tutorial`, which gives an interactive walk through of how to generate events. 

We will first need to specify the model we want to use. This specifies the particles considered and their interactions, and is implemented in UFO format. 
We can then display the particle content of the model with this command:
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

Look in lhe file

To add: script for looking at lhe events

Extensions:
- In the above exercise we have produced stable tops. We know in reality tops are unstable and do decay into (mostly) a W-boson and a b-quark.
  Try to regenerate the events but now including both the top-quark and W-boson decays (we consider here semileptonic decays)
  ```
  generate p p > t t~, (t > W+ b, W+ > j j), (t~ > W- b~, W- > l- vl~)
  ```
  The above code will calculate the top production and decay process independently, in the so-called Narrow Width Approximation (NWA).
  Strictly speaking this is only exact in the limit of a vanishing top quark width,
  and the approximation will be worse and worse as one goes away from the resonance peak.
  
- Redefine the proton to include b quarks (and set b mass to 0)
- Produce tt+1j mlm
- Uncertainty weights?

### 1b. Showering events using [Pythia8](https://www.pythia.org//latest-manual/Welcome.html)

...Briefly reiterate the concept of a PS, give introduction to pythia...

In CMSSW generation (and most other processes) is controlled by python configuration files, which typically end in `cfg.py`. These contain all of the options required to produce events, including generator information and information related to the specific year being produced. To ensure portability of processes between years, the generator information is factorised into a more light weight format called a "fragment", which typically end in `cff.py`. We have provided one such simple fragment designed to shower a LO MG5_aMC lhe file with pythia in `CMS_POSDAS_23_GEN/Fragments/external_lhe_cff.py`. This imports a set of common settings and the dedicated CMS UE Tune, CP5. To turn this fragment into a full configuration file that can produce events, one must first put it in a specific place within CMSSW, and recompile so CMSSW knows where to find it:

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

Then to run it and see the plots:

```
 cd RunRivetCMSSW/   
 cmsRun runRivetAnalyzer_13TeV_cfg.py 
```
For make and look at the plots just do: `rivet-mkhtml test.yoda ` and `evince rivet-plots/CMS_2016_I1491950/pt_jet1.pdf `

