# Final Year Project - Complete Summary
## AI-Powered Parameter Optimization for Graphene Metamaterial THz Devices

**Student:** Linah Salem Alrejaee  
**Student ID:** 231001766  
**Programme:** BSc Computer Science  
**Supervisor:** Dr. Riccardo Degl'Innocenti  
**Institution:** Queen Mary University of London  
**Date:** March 2026

---

## Table of Contents

1. [What This Project Is About](#what-this-project-is-about)
2. [The Problem We're Solving](#the-problem-were-solving)
3. [Project Objectives](#project-objectives)
4. [What We Discussed With Professor](#what-we-discussed-with-professor)
5. [Original Proposal vs Current Project](#original-proposal-vs-current-project)
6. [Technical Background](#technical-background)
7. [What Data We Need](#what-data-we-need)
8. [What We Will Build](#what-we-will-build)
9. [Success Criteria](#success-criteria)
10. [Current Project Status](#current-project-status)
11. [Important Clarifications](#important-clarifications)

---

## What This Project Is About

### Simple Explanation

Professor Degl'Innocenti designs tiny electronic devices (terahertz metamaterial modulators) using computer simulation software called COMSOL. Each simulation takes **24 hours** to complete. He needs to test many different design combinations to find the best one, but testing 50 designs would take **50 days** of continuous computation.

**Our Solution:** Build an AI system that learns from 20-30 existing simulations and can predict the performance of **any** design combination instantly, without running expensive 24-hour simulations.

### Academic Context

This is a **Machine Learning Applied Research Project** that:
- Solves a real bottleneck in photonics/metamaterials research
- Applies AI/ML techniques to electromagnetic device optimization
- Bridges Computer Science and Electronic Engineering
- Has practical impact on research lab workflow
- Could lead to academic publication

---

## The Problem We're Solving

### Current Research Challenge

**What Professor Does:**
- Designs graphene-based devices that control terahertz waves
- Uses COMSOL software to simulate how designs perform
- Changes 7 different parameters (dimensions and properties)
- Each simulation requires 24 hours + 32GB RAM computer
- Often computer crashes, needs to restart

**Why This is Difficult:**
1. **Time Constraint:** 100 designs = 100 days of computation
2. **Resource Constraint:** Computer runs out of memory
3. **No Systematic Method:** Trial-and-error based on intuition
4. **7-Dimensional Space:** Impossible to visualize all parameter interactions
5. **Multiple Goals:** Need to optimize TWO things at once (depth + frequency shift)

**Real-World Impact:**
- Slows down research progress significantly
- Cannot explore innovative design ideas
- Limits ability to find truly optimal solutions
- Wastes expensive computational resources

---

## Project Objectives

### Primary Goal

**Build a Machine Learning tool that predicts device performance from design parameters**

Instead of:
```
Design → COMSOL (24 hrs) → Results
```

We want:
```
Design → ML Model (1 second) → Predicted Results
```

### Specific Technical Objectives

#### Objective 1: Maximize S21 Dip Depth

**What is S21?**
- Measure of how much signal passes through the device
- Measured in decibels (dB), negative numbers
- "Dip" = resonance where signal is absorbed

**Target:**
- Current: -13 dB (moderate performance)
- Goal: -20 dB or deeper (excellent performance)
- Why: Deeper dip = better modulation

#### Objective 2: Maximize Frequency Shift

**What is Frequency Shift?**
- Device has ON and OFF states
- Each state resonates at different frequency
- Shift = difference between ON and OFF frequencies

**Target:**
- Current: 0.5-1.0 GHz (small shift)
- Goal: >1.5 GHz (large shift)
- Why: Larger shift = more tunable device

### The Challenge: Multi-Objective Optimization

These two goals can conflict:
- Parameters that give deep S21 dip might give small frequency shift
- Parameters that give large frequency shift might give shallow S21 dip
- Need to find **optimal balance** between both

### What Success Looks Like

**Minimum Success (Pass):**
- ML model can predict S21 with reasonable accuracy (R² > 0.6)
- Model suggests parameter combinations better than random guessing
- Working prediction tool delivered

**Good Success (Merit/Distinction):**
- ML predictions achieve >80% accuracy (R² > 0.8)
- Find parameter combinations that outperform professor's current best results
- Professional tool with good user interface
- Professor validates predictions with real simulations

**Outstanding Success:**
- Discover parameters achieving S21 < -18 dB (breakthrough performance)
- Tool adopted for regular use in research lab
- Results worthy of academic publication

---

## What We Discussed With Professor

### Email Exchange Summary

#### First Contact (Weekend)
**Professor said:**
- "What size database do you need?"
- "Would 20-30 different simulations be ok?"
- "We could vary parameters a,b,c,d,e (geometrical + conductivity)"
- "Two outputs we want to optimize: S-parameters"

**What we understood:**
- Dataset size: 20-30 simulations (acceptable for FYP)
- Parameters: Mix of geometrical dimensions + electrical properties
- Goals: Optimize S-parameter performance

#### Detailed Information Received

**Professor provided:**
1. **COMSOL .mph file** - The simulation setup file
2. **README document** explaining:
   - Which parameters to vary (g_w, c_w, w_au, ALD_s, w_au_top, w_graph, h_graph)
   - Which parameters NOT to touch
   - How simulations work
   - What results look like
   - What optimization goals are

**Key insights from README:**
- Each simulation takes ~24 hours (originally said 8-10, actually longer)
- Currently using "brute force" approach manually
- Computer crashes frequently due to memory limits
- Goal 1: Maximize S21 dip depth (target -20 dB)
- Goal 2: Maximize frequency shift between ON/OFF states
- **Critical statement:** "Hence the need to use a ML approach" - confirms ML is essential, not optional

#### Follow-up Clarification

**Student (Linah) asked:**
1. "Are these electromagnetic simulations or experimental measurements?"
2. "Would ML model predict optimal S-parameters or analyze existing ones?"
3. "What format is the data?"

**Professor answered:**
- "Yes: attached screenshot of typical sims geometry in COMSOL"
- "Yes: see second screenshot, typical S parameter image"
- "Clearly we do have data in .csv format"
- "At this moment I am changing parameters manually, brutal force way"
- "Each sim takes roughly 24 hr"
- Explained the geometry and what each parameter does

### Critical Understanding from Discussions

**What Professor NEEDS:**
- Tool to suggest optimal parameters WITHOUT running 100+ simulations
- Faster way to explore design space
- Systematic optimization instead of trial-and-error

**What Professor PROVIDES:**
- 20-30 CSV files with simulation results
- Domain expertise to validate predictions
- Will run 2-3 new simulations to test ML suggestions

**What Student DOES:**
- Build ML models on provided data
- Create optimization algorithms
- Develop user-friendly prediction tool
- Does NOT need to run COMSOL or understand quantum physics

---

## Original Proposal vs Current Project

### What Changed

#### Original Proposal (Week 1)

**Project Title:** "AI-Powered Terahertz Image Classification for Automated Material Defect Detection"

**Original Idea:**
- Computer vision project
- Classify THz images as defective/non-defective
- Binary image classification using CNNs
- Transfer learning with ResNet18
- Dataset: 200-500 THz images

**Why We Proposed This:**
- Aligned with professor's THz research area
- Fit student's AI/ML background
- Standard supervised learning problem
- Used Image Processing module (ECS605U)

#### Actual Project (After Professor Clarification)

**Actual Title:** "Machine Learning-Based Parameter Optimization for Graphene Metamaterial THz Devices"

**Actual Project:**
- NOT image classification
- NOT computer vision
- IS regression/optimization problem
- Dataset: 20-30 simulation CSV files (tabular data, not images)
- Predict numerical values (S-parameters) from design parameters

**Why It Changed:**
- Professor's actual need is parameter optimization, not image analysis
- He has simulation data (CSV files), not image datasets
- His bottleneck is running simulations, not analyzing images
- ML needed to replace expensive simulations, not classify images

### Evolution of Understanding

**Week 1: Assumed Project**
- "THz image classification"
- "Defect detection"
- "Computer vision with CNNs"

**Week 2: Actual Project**
- "Parameter prediction from simulations"
- "Multi-objective optimization"
- "Regression with small dataset"

**Week 3: Refined Understanding**
- "Surrogate model for COMSOL"
- "Bayesian optimization"
- "7-input, 2-output regression problem"

### What Stayed the Same

✅ **Still AI/ML project** - Just different ML technique (regression vs classification)  
✅ **Still THz devices** - Same research domain  
✅ **Still helps professor** - Solves real research problem  
✅ **Still 3-month scope** - Feasible for bachelor's FYP  
✅ **Still uses your modules** - ML, optimization, data analysis  

### What's Better About Current Project

**Advantages over original proposal:**
1. **Smaller dataset needed** (20-30 samples vs 200-500 images)
2. **More manageable** (tabular data easier than images)
3. **Clearer success metric** (prediction accuracy vs subjective defect classification)
4. **Higher impact** (directly speeds up professor's research)
5. **Better for CV** (optimization problem more impressive than image classification)
6. **Publication potential** (ML for metamaterial design is cutting-edge)

---

## Technical Background

### The Device: Graphene Metamaterial THz Modulator

**What It Does:**
- Controls terahertz electromagnetic waves (frequency between microwave and infrared)
- Acts as electrically-controlled switch for THz signals
- Can turn ON/OFF or modulate THz transmission

**Applications:**
- 6G wireless communications (future technology)
- Medical imaging (safe, non-invasive)
- Security screening (see through clothing/packages)
- Materials characterization (quality control)

**Physical Structure:**
- Size: ~100 micrometers (about width of human hair)
- Made of: Gold electrodes + graphene layer + metamaterial pattern
- Key feature: Split-ring resonators creating LC resonance

### The 7 Design Parameters

**Parameters We Can Change:**

| Parameter | Full Name | Range | What It Does |
|-----------|-----------|-------|--------------|
| **g_w** | Capacitor gap width | 3-7 μm | **Most important** - defines resonance frequency |
| **c_w** | Capacitor width | 20-35 μm | **Most important** - defines resonance frequency |
| **w_au** | Gold line width | 2-5 μm | Affects capacitance and resistance |
| **ALD_s** | Center square size | 30-40 μm | Must be larger than capacitor |
| **w_au_top** | Top gate thickness | 1-3 μm | Controls field coupling to graphene |
| **w_graph** | Graphene width | 0.5-2 μm | Tunes graphene conductivity effect |
| **h_graph** | Graphene height | 1-3 μm | Tunes graphene conductivity effect |

**Physical Constraints:**
- All dimensions must be positive
- ALD_s must be larger than c_w (geometric requirement)
- Top gate must align with graphene layer
- Values limited by manufacturing capabilities

### Understanding S-Parameters

**What are S-Parameters?**
- **S = Scattering parameters**
- Describe how electromagnetic waves interact with device
- In decibels (dB) - negative numbers indicate attenuation

**Key S-Parameters for This Project:**

**S21 - Transmission:**
- Measures signal passing from input (port 1) to output (port 2)
- S21 = 0 dB means 100% transmission (perfect pass-through)
- S21 = -10 dB means 10% transmission (90% absorbed/reflected)
- S21 = -20 dB means 1% transmission (99% absorbed/reflected)

**What We Want:**
- Deep "dip" in S21 curve = strong resonance
- Dip occurs at resonance frequency
- Target: S21 dip at -20 dB or deeper

**ON vs OFF States:**

**ON State (Graphene Conductive):**
- Graphene acts like metal
- Resonance occurs at frequency f₁
- Example: S21 dip at f₁ = 4.2 GHz

**OFF State (Graphene Resistive):**
- Graphene blocks current
- Resonance shifts to frequency f₂
- Example: S21 dip at f₂ = 5.1 GHz

**Frequency Shift:**
- Δf = |f₂ - f₁|
- Example: Δf = |5.1 - 4.2| = 0.9 GHz
- Larger shift = better modulation capability

### Why This is a Machine Learning Problem

**Traditional Approach Problems:**
- 7 parameters = 7-dimensional space
- Cannot visualize all parameter interactions
- No analytical formula relating parameters to performance
- Electromagnetic equations too complex to solve analytically

**ML Approach Advantages:**
- Learn patterns from data without knowing underlying physics equations
- Handle complex non-linear relationships
- Explore millions of combinations quickly
- Provide predictions with uncertainty estimates

---

## What Data We Need

### Data Format

**Input: CSV Files from COMSOL Simulations**

Each CSV file contains:
- **Header section:** Input parameter values (7 numbers)
- **Data section:** Frequency sweep results

**Example Structure:**
- Row 1: Parameter names and values
- Rows 2-N: Frequency (GHz) | S21_ON (dB) | S21_OFF (dB) | S12_ON (dB) | S12_OFF (dB)
- Typically 200-300 rows (frequency from 2-7 GHz with small steps)

### What We Extract From Each CSV

**Input Features (X):**
- 7 parameter values: [g_w, c_w, w_au, ALD_s, w_au_top, w_graph, h_graph]

**Output Targets (Y):**
- S21_dip_ON: Minimum S21 value in ON state
- S21_dip_OFF: Minimum S21 value in OFF state  
- Freq_ON: Frequency where ON state dip occurs
- Freq_OFF: Frequency where OFF state dip occurs
- Freq_shift: |Freq_ON - Freq_OFF|

### Dataset Size

**Provided by Professor:**
- 20-30 CSV files
- Each represents one complete simulation run
- Dataset rows: 20-30 (one row per simulation)
- Dataset columns: 7 inputs + 5 outputs = 12 total

**Challenge:**
- Small dataset for machine learning
- Risk of overfitting
- Need techniques for small-data ML

**Mitigation:**
- Use Gaussian Process Regression (excellent for small data)
- Cross-validation to maximize training data use
- Regularization to prevent overfitting
- Feature engineering for better patterns

### Data Source Clarification

**IMPORTANT: Student Does NOT Run COMSOL**

**Who provides data:**
- Professor runs COMSOL simulations
- Professor exports results to CSV
- Professor shares CSV files with student

**Why student doesn't run COMSOL:**
- Requires expensive license (~$5000/year)
- Needs powerful computer (32GB RAM minimum)
- Takes 24 hours per simulation
- Requires domain expertise in electromagnetic simulation
- Student's role is ML/AI, not physics simulation

---

## What We Will Build

### Main Deliverable: ML-Powered Parameter Optimization Tool

**Core Functionality:**

1. **Data Processing Module**
   - Load and parse COMSOL CSV files
   - Extract parameters and S-parameter metrics
   - Clean and validate data
   - Create train/test splits

2. **Machine Learning Models**
   - Regression models predicting S-parameters from design parameters
   - Multiple algorithms: Random Forest, XGBoost, Gaussian Process
   - Model comparison and selection
   - Cross-validation for robust evaluation

3. **Optimization Engine**
   - Multi-objective optimization balancing two goals
   - Bayesian Optimization for intelligent search
   - Generates ranked list of promising parameter combinations
   - Pareto frontier showing trade-offs

4. **User Interface (Streamlit Web App)**
   - Input: Manual parameter entry or CSV upload
   - Output: Predicted S21 dip depth and frequency shift
   - Visualization: Predicted S-parameter curves
   - Optimization: "Suggest best parameters" button
   - Results export to CSV

5. **Validation Reports**
   - Model performance metrics (R², RMSE, MAE)
   - Feature importance analysis
   - Uncertainty quantification
   - Comparison with professor's actual validation simulations

### User Workflow

**For Researcher (Professor):**

**Step 1:** Upload 20-30 existing simulation CSV files  
**Step 2:** Tool trains ML model automatically  
**Step 3:** Click "Optimize Parameters"  
**Step 4:** Receive top 5 recommended parameter combinations  
**Step 5:** (Optional) Run 2-3 COMSOL simulations to validate best predictions  
**Step 6:** Use validated optimal design in actual device fabrication  

**For New Design Exploration:**

**Step 1:** Enter hypothetical parameter values  
**Step 2:** Get instant prediction of performance  
**Step 3:** Explore "what-if" scenarios quickly  
**Step 4:** Understand which parameters matter most  

### Technical Components

**Machine Learning:**
- Supervised learning (regression)
- Small-data techniques (Gaussian Process, regularization)
- Hyperparameter tuning (Grid Search, Random Search)
- Ensemble methods (model averaging)

**Optimization:**
- Multi-objective optimization (NSGA-II, weighted sum)
- Bayesian Optimization (intelligent sequential search)
- Constraint handling (parameter bounds, geometric constraints)
- Pareto frontier analysis (visualize trade-offs)

**Software Engineering:**
- Clean, modular Python code
- Version control (Git/GitHub)
- Documentation (docstrings, user manual)
- Testing (unit tests for key functions)
- Reproducibility (random seeds, saved models)

---

## Success Criteria

### Academic Success (Grade-Related)

**Pass (60-69%):**
- ✅ Successfully process 20-30 CSV files into clean dataset
- ✅ Build at least one working regression model
- ✅ Achieve R² > 0.6 on test data
- ✅ Generate parameter recommendations
- ✅ Complete technical report (30+ pages)
- ✅ Deliver working Python scripts

**Merit (70-79%):**
- ✅ All Pass criteria PLUS:
- ✅ Compare 3+ different ML algorithms
- ✅ Achieve R² > 0.75 on test data
- ✅ Implement optimization algorithm
- ✅ Build basic web interface (Streamlit)
- ✅ Comprehensive evaluation metrics

**Distinction (80-100%):**
- ✅ All Merit criteria PLUS:
- ✅ Achieve R² > 0.85 on test data
- ✅ Multi-objective optimization with Pareto analysis
- ✅ Professor validates predictions with real simulations
- ✅ ML suggestions outperform professor's best manual results
- ✅ Professional-quality tool with documentation
- ✅ Publication-worthy analysis and results

### Research Impact Success

**Minimum Impact:**
- Tool provides reasonable predictions
- Helps professor understand parameter sensitivities
- Saves some simulation time

**Significant Impact:**
- Predictions accurate enough to trust without validation
- Discovers parameter combinations professor hadn't tried
- Tool adopted for regular lab use
- Saves weeks of simulation time

**Outstanding Impact:**
- Finds parameters achieving breakthrough performance (S21 < -18 dB)
- Results publishable in academic journal
- Methodology applicable to other metamaterial designs
- Tool becomes standard in research group

### Technical Success Metrics

**Model Performance:**
- R² Score > 0.80 (explains 80%+ of variance)
- RMSE < 1.0 dB for S21 predictions
- RMSE < 0.3 GHz for frequency predictions
- Cross-validation stable across folds

**Optimization Quality:**
- Suggested parameters better than random search
- At least 1 in top 5 suggestions outperforms current best
- Pareto frontier shows clear trade-offs
- Confidence intervals help assess risk

**Software Quality:**
- No crashes or errors in normal use
- Intuitive interface requiring minimal training
- Results reproducible (same inputs → same outputs)
- Code documented and maintainable

---

## Current Project Status

### Where We Are Now

**Completed:**
- ✅ Initial project meetings with professor
- ✅ Received project requirements and scope
- ✅ Understood the optimization problem
- ✅ Clarified data format and availability
- ✅ Confirmed project is NOT image classification
- ✅ Identified it's a regression/optimization problem
- ✅ Received COMSOL .mph file and README documentation
- ✅ Understood professor will provide CSV data

**In Progress:**
- 🔄 Waiting for 20-30 CSV files from professor
- 🔄 Preparing project proposal document
- 🔄 Setting up Python development environment
- 🔄 Reviewing ML techniques for small datasets

**Next Steps:**
- 📅 Meeting with professor to:
  - Receive sample CSV files
  - Confirm data format
  - Agree on validation approach
  - Set communication schedule
- 📅 Begin data exploration once CSVs received
- 📅 Finalize project proposal and submit

### Key Understandings Achieved

**About the Project:**
- NOT image classification → IS parameter optimization
- NOT running COMSOL → USING existing simulation data
- NOT large dataset → SMALL data ML techniques needed
- NOT single objective → MULTI-objective optimization

**About the Data:**
- Format: CSV files (20-30 total)
- Source: Professor's COMSOL simulations
- Content: 7 input parameters, S-parameter curves
- Challenge: Small sample size requires careful ML approach

**About Our Role:**
- Build ML models (NOT run physics simulations)
- Develop optimization algorithms
- Create user-friendly tool
- Validate with professor's help

**About Success:**
- Minimum: Working predictor with >60% accuracy
- Target: >80% accuracy + tool adoption
- Stretch: Breakthrough performance discoveries

### Open Questions to Resolve

**Data Questions:**
1. Exact CSV format (will know when we receive files)
2. Current best performance achieved (baseline for comparison)
3. Acceptable parameter ranges and constraints
4. How many validation simulations professor willing to run

**Technical Questions:**
1. How to handle cases where COMSOL crashed/failed?
2. Are there parameter combinations known to fail?
3. What error tolerance is acceptable for predictions?
4. Preferred output format for recommendations?

**Project Management:**
1. Frequency of meetings with professor
2. Deadline for intermediate deliverables
3. Access to lab computer if needed for tool testing
4. Format for final presentation

---

## Important Clarifications

### What Student (Linah) Needs to Understand

**About Terahertz Physics:**
- ❌ Don't need: Quantum mechanics, Maxwell's equations, semiconductor physics
- ✅ Do need: Basic understanding that S21 measures transmission, resonance = dip in curve, ON/OFF states exist

**About COMSOL Software:**
- ❌ Don't need: How to use COMSOL, electromagnetic simulation theory
- ✅ Do need: Understand it's simulation software that takes parameters as input, produces S-parameter curves as output

**About the Device:**
- ❌ Don't need: How to fabricate graphene, detailed metamaterial physics
- ✅ Do need: Know it's a tiny device with 7 adjustable parameters, used for THz modulation

**About Machine Learning:**
- ✅ Do need: Regression, optimization, cross-validation, overfitting prevention
- ✅ Do need: How to handle small datasets effectively
- ✅ Do need: Multi-objective optimization concepts
- ✅ Do need: Model evaluation and validation

### What Professor Needs to Provide

**Essential:**
- 20-30 CSV files with simulation results
- Parameter bounds (min/max values)
- Current best-performing parameter combination
- 2-3 validation simulation runs after ML suggests parameters

**Helpful:**
- Sample CSV file early for format checking
- Domain expertise for interpreting unexpected results
- Guidance on physical constraints between parameters
- Feedback on tool usability

### What Makes This Project Feasible

**Why This Works for Bachelor's FYP:**

✅ **Clear scope:** 3-month timeline realistic  
✅ **Defined dataset:** 20-30 samples manageable  
✅ **Available tools:** Python, scikit-learn, free libraries  
✅ **No special hardware:** Student laptop sufficient for ML  
✅ **Practical validation:** Professor runs real simulations  
✅ **Measurable success:** Clear metrics (R², prediction error)  
✅ **Real impact:** Solves actual research bottleneck  
✅ **Module alignment:** Uses ML, optimization, data analysis courses  

**Red Flags Avoided:**
❌ Not requiring expensive software licenses  
❌ Not needing specialized hardware  
❌ Not depending on large dataset collection  
❌ Not requiring physics PhD knowledge  
❌ Not involving hardware experiments  
❌ Not open-ended research with unclear outcomes  

### Contingency Plans

**If dataset is smaller than expected (<15 simulations):**
- Focus on parameter sensitivity analysis
- Use heavy data augmentation techniques
- Build theoretical model using electromagnetic principles
- Reduce scope to single-objective optimization

**If predictions are inaccurate (<60% R²):**
- Analyze which parameters predictions fail on
- Focus on subset of parameter space where model works
- Provide wider confidence intervals
- Recommend experimental validation for all suggestions

**If COMSOL access becomes available:**
- Could run 5-10 additional simulations strategically
- Use active learning to select most informative parameters
- Validate model on newly generated data
- Expand dataset for better predictions

**If professor cannot validate predictions:**
- Use cross-validation as primary validation method
- Compare predictions to published literature values
- Theoretical analysis using electromagnetic equations
- Clearly document limitation in report

---

## Course Module Integration

### How This FYP Uses Your Degree Modules

**ECS663U - Principles of Machine Learning:**
- Supervised learning (regression)
- Model selection and evaluation
- Overfitting and regularization
- Cross-validation techniques
- Performance metrics (R², RMSE, MAE)

**ECS647U - Bayesian Decision and Risk Analysis:**
- Bayesian Optimization for parameter search
- Gaussian Process Regression
- Uncertainty quantification
- Decision-making under uncertainty
- Prior knowledge incorporation

**ECS659U - Neural Networks and Deep Learning:**
- Multi-layer perceptrons for regression
- Training on small datasets
- Regularization techniques
- Comparison with traditional ML

**ECS529U - Algorithms and Data Structures:**
- Efficient data processing pipelines
- Optimization algorithms
- Computational complexity analysis
- Search space exploration

**ECS509U - Probability and Matrices:**
- Statistical analysis of results
- Matrix operations in ML models
- Probability distributions for uncertainty
- Correlation and covariance analysis

**ECS607U - Data Mining (Optional Module):**
- Extracting patterns from simulation data
- Feature importance analysis
- Dimensionality considerations
- Outlier detection

**ECS640U - Big Data Processing (If Taken):**
- Batch processing of simulation files
- Parallel model training
- Efficient data pipelines

---

## Meeting Questions & Checklist

### Questions for Next Meeting With Professor

**Critical Questions:**

1. **Data Availability**
   - "Can you provide 2-3 sample CSV files now so I can check the format?"
   - "Do you have 20-30 simulations ready, or will you run new ones?"
   - "What is the current best performance you've achieved?"

2. **Validation Approach**
   - "After my model suggests parameters, will you run 2-3 validation simulations?"
   - "How many validation runs are you willing to do?"
   - "What prediction accuracy would you consider useful?"

3. **Parameter Constraints**
   - "Are there parameter combinations known to fail or crash?"
   - "Besides the ranges mentioned, are there other constraints?"
   - "Must ALD_s always be larger than c_w by a minimum amount?"

4. **Tool Requirements**
   - "Do you prefer a web interface, desktop app, or Jupyter notebook?"
   - "Should it handle batch processing of multiple designs?"
   - "What output format works best for your workflow?"

5. **Timeline**
   - "When can I expect the CSV files?"
   - "How often should we meet to discuss progress?"
   - "When do you need the final tool delivered?"

### Pre-Meeting Checklist

**Before meeting, student should:**
- ✅ Read this entire document
- ✅ Prepare specific questions about CSV format
- ✅ Install Python, Jupyter, pandas, scikit-learn
- ✅ Review Gaussian Process Regression basics
- ✅ Understand S-parameters at basic level
- ✅ Bring notebook for taking notes

**To bring/send to professor:**
- ✅ This summary document
- ✅ List of clarification questions
- ✅ Proposed meeting schedule
- ✅ Draft project proposal (if ready)

### Post-Meeting Action Items

**Immediately after meeting:**
- ✅ Send thank-you email summarizing discussion
- ✅ Confirm next meeting date/time
- ✅ Request sample CSV files if not received
- ✅ Clarify any ambiguous points

**Within 48 hours:**
- ✅ Process sample CSV files (if received)
- ✅ Set up project repository
- ✅ Begin literature review on ML for electromagnetic optimization
- ✅ Draft detailed project timeline

---

## References & Resources

### Academic Papers (To Review)

**ML for Electromagnetic Design:**
- Search: "machine learning electromagnetic optimization"
- Search: "surrogate modeling COMSOL"
- Search: "Bayesian optimization metamaterial design"

**Small Dataset ML:**
- "Gaussian Processes for Machine Learning" (Rasmussen & Williams)
- Papers on active learning and data-efficient ML

**Multi-Objective Optimization:**
- NSGA-II algorithm papers
- Pareto optimization in engineering design

### Technical Resources

**Python Libraries:**
- scikit-learn (ML models)
- GPy or scikit-learn GP (Gaussian Process)
- XGBoost / LightGBM (Gradient Boosting)
- Bayesian Optimization library
- Streamlit (web interface)
- Plotly / Matplotlib (visualization)

**Learning Resources:**
- Scikit-learn documentation
- "Hands-On Machine Learning" by Aurélien Géron
- Streamlit tutorials
- Bayesian Optimization guides

### Professor's Research

**Lab Publications:**
- Check Dr. Degl'Innocenti's Google Scholar
- Focus on recent papers about graphene metamaterials
- Note: S-parameter optimization methods used
- Understand: Current state-of-the-art performance

### University Resources

**QMUL Support:**
- Library access to papers
- Potential COMSOL lab for demonstrations
- Computing resources if needed
- Thesis writing workshops

---

## Final Summary

### One-Paragraph Project Description

This Final Year Project develops a machine learning tool to optimize the design of graphene-based terahertz metamaterial modulators. Currently, finding optimal device parameters requires running electromagnetic simulations in COMSOL Multiphysics, with each simulation taking 24 hours. By training regression models on 20-30 existing simulation results, we build a surrogate model that predicts device performance instantly for any parameter combination. The tool uses multi-objective Bayesian optimization to suggest parameter sets that maximize both S21 resonance dip depth (target: -20 dB) and frequency shift between ON/OFF states (target: >1.5 GHz), enabling researchers to explore millions of design variations in seconds rather than months, ultimately accelerating the development of next-generation terahertz devices for 6G communications and imaging applications.

### Key Takeaways

**What This Project IS:**
- ✅ Machine learning regression and optimization
- ✅ Real research problem with practical impact
- ✅ Tabular data analysis (not image classification)
- ✅ Small-data ML techniques
- ✅ Software tool development
- ✅ Interdisciplinary (CS + Engineering)

**What This Project is NOT:**
- ❌ Running COMSOL simulations
- ❌ Image classification or computer vision
- ❌ Large dataset deep learning
- ❌ Pure theoretical research
- ❌ Hardware experiments
- ❌ Novel algorithm invention

**Why This Project is Good for FYP:**
- Real-world problem solving
- Measurable success criteria
- Appropriate 3-month scope
- Uses degree module knowledge
- Publication potential
- Portfolio-worthy for CV

### Student's Role Summary

**Your job:** Build AI system that learns from 20-30 examples and predicts performance of millions of untested designs

**Not your job:** Understanding quantum mechanics, running simulations, fabricating devices

**Success = Tool that saves professor weeks of simulation time + Grade 70-90%**

---

**Document Version:** 1.0  
**Last Updated:** March 2026  
**Status:** Pre-Project (Awaiting CSV Data)  
**Next Milestone:** Receive sample CSV files from professor
