# Checkpoint Question Solutions
## Part 3 Detector-Level Analysis Tutorial (5-Day Bachelor Physics Module)

---

### Exercise 1 Checkpoint Question
**Question:**
*“What is the difference between a branch holding a reconstructed large-R jet mass and a branch holding a truth-matched origin label?”*

**Detailed Solution:**
- **Reconstructed Large-R Jet Mass (`largeRjet_m_NOSYS`)**:
  - This is a **reconstructed physical measurement** calculated from detector signals (energy deposits in calorimeter topo-clusters or track-calo UFO objects).
  - It is an observable that would also be measured in real LHC collision data.
  - It is subject to detector resolution, pileup contamination, and energy scale calibration uncertainties.
- **Truth-Matched Origin Label (`largeRjet_truth_label`)**:
  - This is an **unobservable Monte Carlo (MC) simulation annotation** produced by matching reconstructed jet axes to generator-level truth particles (e.g., $W$, $Z$, top quark, or parton shower decay products).
  - It represents ideal MC bookkeeping used exclusively to study detector performance, signal purity, and class composition in simulation.
- **Key Analysis Rule**: Truth labels exist **only in simulation** and must **never** be used as a selection cut when building a reconstructed data analysis strategy.

---

### Exercise 2 Checkpoint Question
**Question:**
*“Why should the y-axis label distinguish ‘events’, ‘weighted events’, and ‘normalized density’?”*

**Detailed Solution:**
- **Raw Event Counts (“Events”)**:
  - Represents unweighted raw entries ($N_{\rm raw}$) passing selection cuts in a given bin.
  - Useful for checking Poisson statistical sample size ($\sqrt{N_{\rm raw}}$), but does not represent real physical cross sections or expected collision yields.
- **Weighted Events (“Weighted Events / Bin Width”)**:
  - Represents physical yields scaled by generator and calibration scale factors: $Y = \sum_i w_{\rm norm, i}$.
  - Reflects the actual number of events expected in a specific integrated luminosity scenario (e.g., $44\text{ fb}^{-1}$).
- **Normalized Density (“Probability Density / Unit Width”)**:
  - Represents the unit-area normalized shape of a distribution ($\int \frac{dN}{dx} dx = 1$).
  - Allows direct shape comparisons between different sample sizes or physics processes independent of total cross section or sample statistics.
- **Key Analysis Rule**: Failing to specify the y-axis convention makes it impossible for readers to determine whether a plot shows raw simulation entries, expected physical collision rates, or pure shape comparisons.

---

### Exercise 3 Checkpoint Question
**Question:**
*“If mass and $p_T$ have a nonzero correlation, why does that not identify the physical mechanism causing it?”*

**Detailed Solution:**
- **Correlation vs. Causation**:
  - A non-zero Pearson correlation coefficient ($r_{XY} \neq 0$) or distance correlation statistic simply indicates that higher values of $p_T$ tend to co-occur with higher values of jet mass in the selected dataset.
  - It does not prove that $p_T$ directly causes mass, nor does it isolate the underlying physical mechanism.
- **Confounding Factors in QCD Jets**:
  - In QCD quark/gluon jets, soft gluon radiation scales with jet transverse momentum: $m_{\rm QCD}^2 \propto \alpha_s p_T^2 R^2$.
  - Kinematic phase-space acceptance (detector cuts, trigger thresholds, and jet cone size $R=1.0$) introduces artificial boundary correlations.
  - Sample composition shifts (e.g., changing fractions of quark vs. gluon jets at higher $p_T$) alter the observed joint distribution.
- **Key Analysis Rule**: Demonstrating statistical dependence between two variables is only the first exploratory step; isolating the physical origin requires controlling for phase-space boundaries, pileup dependence, and jet formation dynamics.

---

### Exercise 4 Checkpoint Question
**Question:**
*“Why does applying a higher binary tagger score threshold increase signal purity while reducing signal efficiency, and why must tagger working points be frozen prior to inspecting mass distributions?”*

**Detailed Solution:**
- **Signal Efficiency vs. Purity Trade-off**:
  - A binary tagger score ranks jets by classifier preference. Raising the threshold $y_{\rm cut}$ selects candidates in the extreme signal-like tail.
  - Because background score distributions fall off steeply, raising $y_{\rm cut}$ eliminates a much larger fraction of background events than signal events, thereby increasing signal purity ($N_{\rm sig} / [N_{\rm sig} + N_{\rm bkg}]$).
  - However, because some signal jets have intermediate scores, a higher threshold also rejects some true signal events, reducing overall signal efficiency ($\epsilon_{\rm sig} = N_{\rm pass}^{\rm sig} / N_{\rm total}^{\rm sig}$).
- **Freezing Working Points**:
  - Tagger working points must be frozen before inspecting invariant mass distributions to prevent **confirmation bias** and **data-driven tuning artifacts**.
  - Adjusting tagger thresholds dynamically while observing mass spectra leads to artificial selection tuning that can generate spurious mass bumps or obscure real resonance features.

---

### Exercise 5 Checkpoint Question
**Question:**
*“Why can a tagger-selected mass distribution differ significantly from the inclusive mass distribution in background events even when no physical resonance is present?”*

**Detailed Solution:**
- **Mass Sculpting Mechanism**:
  - Standard ML taggers use substructure inputs (such as energy correlation functions $ECF$, $N$-subjettiness $\tau_{21}$, and splitting scales) that naturally scale with jet mass ($m \propto p_T \sqrt{\tau_{21}}$).
  - When a binary classifier selects jets passing a high tagger score, it implicitly selects a non-uniform region of substructure phase space that corresponds to a specific mass window.
- **Fake Peaking Artifacts**:
  - In a smooth background process like QCD dijets, cutting on a non-mass-decorrelated tagger shapes the broad, falling QCD mass spectrum into a localized peak or bump that mimics a physical particle resonance (such as a $W$ or $Z$ boson peak).
- **Key Analysis Solution**:
  - Mass decorrelation techniques (such as DDT - Designed Decorrelated Taggers or mass-decorrelated ML architectures like `ParT_W_massDec_score`) must be used when jet mass is subsequently analyzed as a signal observable.

---

### Exercise 6 Checkpoint Question
**Question:**
*“Why can a large `bb` classifier output enrich a Z→bb MC sample without proving that every selected reconstructed jet originated from a b-quark pair?”*

**Detailed Solution:**
- **Probabilistic Enrichment vs. Deterministic Proof**:
  - High multiclass score (e.g., $D_{bb} > 0.8$ or `GN3X_phbb` > 0.8) indicates that the jet exhibits radiation patterns, track displacement, or sub-jet kinematics strongly characteristic of a $b\bar{b}$ topology.
  - Applying this cut increases the overall fraction of true $Z\to b\bar{b}$ jets in the sample (class enrichment).
- **Mistag Background Contamination**:
  - Hadronic jets from $c\bar{c}$ decays, gluon splitting to $b\bar{b}$ in QCD, or overlap pileup tracks can occasionally produce high tagger scores (mistags).
  - Therefore, individual jets in real collision data passing the tagger score cut cannot be individually guaranteed to originate from $b\bar{b}$ without statistical background subtraction and efficiency/mistag calibration.

**Question 2:**
*“How can selection boundaries be drawn on the 2D $D_{bb}$ vs. $D_{qq}$ plane to simultaneously isolate $Z\to b\bar{b}$ signal, $W/Z\to q\bar{q}$ hadronic decays, and QCD background jets?”*

**Detailed Solution:**
- **Topological Phase Space Separation**:
  - $D_{bb} = \frac{P_{hbb}}{P_{hbb} + P_{Wqq} + P_{\text{QCD\_all}}}$ measures 2-prong $b\bar{b}$ topology strength.
  - $D_{qq} = \frac{P_{Wqq}}{P_{Wqq} + P_{\text{QCD\_all}}}$ measures 2-prong light-quark $q\bar{q}$ topology strength vs. QCD.
- **Selection Corner Boundaries**:
  - **$Z\to b\bar{b}$ Enriched Region**: High $D_{bb}$ and low $D_{qq}$ ($D_{bb} > 0.60, D_{qq} < 0.20$), isolating bottom-quark pair decays.
  - **$W/Z\to q\bar{q}$ Enriched Region**: Low $D_{bb}$ and high $D_{qq}$ ($D_{bb} < 0.20, D_{qq} > 0.60$), isolating light-quark 2-prong decays while suppressing $b\bar{b}$.
  - **QCD Dijet Background Region**: Low $D_{bb}$ and low $D_{qq}$ ($D_{bb} < 0.20, D_{qq} < 0.20$), where background dijets cluster near the origin $(0,0)$.
- **Multi-Region Selection Benefit**:
  - Orthogonal rectangular cuts on the $(D_{bb}, D_{qq})$ plane allow simultaneous isolation of orthogonal signal categories into distinct analysis channels while cleanly rejecting non-resonant QCD dijet background.

---

### Exercise 7 Checkpoint Question
**Question:**
*“Why is taking the sum of squared weights $\sum w^2$ necessary for calculating the statistical uncertainty on a weighted histogram bin, especially when generator weights can be negative?”*

**Detailed Solution:**
- **Variance Propagation for Weighted Yields**:
  - For a histogram bin with content $Y = \sum_{i \in \text{bin}} w_i$, each event contribution $w_i$ is an independent random variable.
  - According to error propagation for independent variables:
    $$\operatorname{Var}(Y) = \sum_{i \in \text{bin}} \operatorname{Var}(w_i) = \sum_{i \in \text{bin}} w_i^2$$
  - The statistical standard error is therefore $\sigma_Y = \sqrt{\sum_{i \in \text{bin}} w_i^2}$.
- **Negative Generator Weights**:
  - In NLO Monte Carlo generators (e.g., Sherpa or MadGraph@NLO), negative weights ($w_i < 0$) occur due to interference terms and real emission subtractions.
  - Squaring the weight ($w_i^2 > 0$) ensures that every event—whether positive or negative—correctly adds positive variance to the total MC statistical uncertainty band.
  - Using $\sqrt{N_{\rm raw}}$ or $\sqrt{|Y|}$ severely misestimates the true statistical uncertainty in weighted MC distributions.
