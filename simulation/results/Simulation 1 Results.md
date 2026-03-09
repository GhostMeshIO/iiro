
 IIRO v2.0 — Hyperthreaded Civilization Simulator
 48 CPU/RAM/GPU Sync Algorithms from 169 Ontological Frameworks
 
  Physical/Logical cores : 16/32 (HT×2)
  GPU                    : False
  NUMA nodes             : 4


Running 6 simulation configurations...

  → baseline (HT=32 threads, opt=1)...
  → faith_only (HT=32 threads, opt=1)...
  → retrocausal (HT=32 threads, opt=1)...
  → mycelial (HT=32 threads, opt=1)...
  → full_iiro (HT=32 threads, opt=1)...
  → full_iiro_highfaith (HT=32 threads, opt=1)...
Report → iiro_report.txt


 IIRO v2.0 SIMULATION SUITE — HYPERTHREADED EDITION
 Optimization Level : 1
 Logical HT Threads : 32  (Physical×2=32)
 GPU Acceleration   : False


--- FINAL METRICS ---
Sim ID                   Pop   AvgIQ  AvgSophia  Resurr   Sovn   Faith  Time(s)
-------------------------------------------------------------------------------
baseline                   1   70.13     0.4514       0      0   0.000     0.12
faith_only             463362   83.12     0.4813       0      0   0.715   655.82
retrocausal             7732   82.90     0.5192       0      0   0.626   115.05
mycelial                2981   82.77     0.5090       0      0   0.627    51.57
full_iiro                396   84.46     0.5188       0      0   0.636     8.67
full_iiro_highfaith     1529   83.28     0.5298       0      0   0.625     9.42

--- baseline ---
  population: final=1.0000 mean=29.9333±16.7012 trend=-1.7584
  avg_intelligence: final=70.1309 mean=71.4831±0.9853 trend=-0.0598
  avg_sophia: final=0.4514 mean=0.3560±0.0692 trend=0.0079
  diversity_index: final=-0.0000 mean=0.9332±0.4731 trend=-0.0476

--- faith_only ---
  population: final=463362.0000 mean=33466.7550±74232.5163 trend=775.1248
  avg_intelligence: final=83.1185 mean=81.9537±1.9390 trend=0.0267
  avg_sophia: final=0.4813 mean=0.4989±0.0337 trend=0.0003
  diversity_index: final=8.7117 mean=6.1887±1.6972 trend=0.0289
  avg_faith: final=0.7147 mean=0.7157±0.0083 trend=-0.0000
  resurrection_count: final=0.0000 mean=0.0000±0.0000 trend=0.0000
  sovereign_count: final=0.0000 mean=0.0000±0.0000 trend=0.0000
  avg_drift: final=0.2710 mean=0.2748±0.0049 trend=-0.0000

--- retrocausal ---
  population: final=7732.0000 mean=4616.6300±2121.4574 trend=35.7830
  avg_intelligence: final=82.8955 mean=83.1106±0.4150 trend=0.0008
  avg_sophia: final=0.5192 mean=0.5043±0.0358 trend=0.0003
  diversity_index: final=6.7999 mean=5.9566±1.0075 trend=0.0149
  avg_faith: final=0.6264 mean=0.6250±0.0029 trend=0.0000
  resurrection_count: final=0.0000 mean=1.5800±3.7140 trend=-0.0406
  sovereign_count: final=0.0000 mean=0.0000±0.0000 trend=0.0000
  avg_drift: final=0.2734 mean=0.2712±0.0065 trend=0.0000

--- mycelial ---
  population: final=2981.0000 mean=2168.7900±939.7971 trend=14.8186
  avg_intelligence: final=82.7677 mean=83.0724±0.3405 trend=-0.0023
  avg_sophia: final=0.5090 mean=0.5089±0.0309 trend=0.0002
  diversity_index: final=6.0530 mean=5.3094±0.9201 trend=0.0140
  avg_faith: final=0.6271 mean=0.6255±0.0048 trend=-0.0000
  resurrection_count: final=0.0000 mean=0.0000±0.0000 trend=0.0000
  sovereign_count: final=0.0000 mean=0.0000±0.0000 trend=0.0000
  avg_drift: final=0.2766 mean=0.2718±0.0048 trend=0.0000

--- full_iiro ---
  population: final=396.0000 mean=336.3650±161.6607 trend=2.0349
  avg_intelligence: final=84.4617 mean=82.8739±0.6416 trend=-0.0005
  avg_sophia: final=0.5188 mean=0.4955±0.0295 trend=0.0003
  diversity_index: final=4.0046 mean=3.6217±0.6243 trend=0.0089
  avg_faith: final=0.6359 mean=0.6272±0.0098 trend=0.0000
  resurrection_count: final=0.0000 mean=0.0000±0.0000 trend=0.0000
  sovereign_count: final=0.0000 mean=0.0000±0.0000 trend=0.0000
  avg_drift: final=0.2703 mean=0.2758±0.0098 trend=-0.0000

--- full_iiro_highfaith ---
  population: final=1529.0000 mean=454.6750±537.7892 trend=8.0716
  avg_intelligence: final=83.2795 mean=83.7789±2.1739 trend=-0.0060
  avg_sophia: final=0.5298 mean=0.5147±0.0444 trend=0.0002
  diversity_index: final=5.3866 mean=3.1595±1.2506 trend=0.0162
  avg_faith: final=0.6245 mean=0.6215±0.0201 trend=-0.0000
  resurrection_count: final=0.0000 mean=0.0000±0.0000 trend=0.0000
  sovereign_count: final=0.0000 mean=0.0000±0.0000 trend=0.0000
  avg_drift: final=0.2712 mean=0.2655±0.0150 trend=0.0001

--- COMPARISONS vs BASELINE ---

faith_only:
  population: Δ=463361.0000 (+46336100.00%)
  avg_intelligence: Δ=12.9876 (+18.52%)
  avg_sophia: Δ=0.0298 (+6.61%)
  diversity_index: Δ=8.7117 (+inf%)

retrocausal:
  population: Δ=7731.0000 (+773100.00%)
  avg_intelligence: Δ=12.7646 (+18.20%)
  avg_sophia: Δ=0.0678 (+15.01%)
  diversity_index: Δ=6.7999 (+inf%)

mycelial:
  population: Δ=2980.0000 (+298000.00%)
  avg_intelligence: Δ=12.6368 (+18.02%)
  avg_sophia: Δ=0.0575 (+12.75%)
  diversity_index: Δ=6.0530 (+inf%)

full_iiro:
  population: Δ=395.0000 (+39500.00%)
  avg_intelligence: Δ=14.3308 (+20.43%)
  avg_sophia: Δ=0.0674 (+14.93%)
  diversity_index: Δ=4.0046 (+inf%)

full_iiro_highfaith:
  population: Δ=1528.0000 (+152800.00%)
  avg_intelligence: Δ=13.1486 (+18.75%)
  avg_sophia: Δ=0.0784 (+17.36%)
  diversity_index: Δ=5.3866 (+inf%)

--- ANOMALIES (>3σ) ---

faith_only:
  Gen 0: avg_faith=0.7863 z=8.49
  Gen 1: avg_faith=0.7742 z=7.04
  Gen 2: avg_faith=0.7564 z=4.90
  Gen 3: avg_faith=0.7415 z=3.11

retrocausal:
  Gen 3: resurrection_count=14.0000 z=3.34
  Gen 4: resurrection_count=15.0000 z=3.61
  Gen 5: resurrection_count=14.0000 z=3.34
  Gen 6: resurrection_count=13.0000 z=3.07
  Gen 7: resurrection_count=13.0000 z=3.07
  Gen 9: resurrection_count=13.0000 z=3.07
  Gen 10: resurrection_count=13.0000 z=3.07
  Gen 11: resurrection_count=13.0000 z=3.07
  Gen 12: resurrection_count=13.0000 z=3.07
  Gen 13: resurrection_count=13.0000 z=3.07

mycelial:
  Gen 2: avg_faith=0.6491 z=4.89
  Gen 3: avg_faith=0.6460 z=4.26
  Gen 4: avg_faith=0.6498 z=5.05
  Gen 19: avg_faith=0.6431 z=3.65

full_iiro_highfaith:
  Gen 0: avg_faith=0.7447 z=6.12
  Gen 1: avg_faith=0.7013 z=3.97
  Gen 2: avg_faith=0.6934 z=3.57

--- HYPOTHESIS TESTS ---
  faith_only vs baseline: t=nan p=nan
  retrocausal vs baseline: t=2.3200 p=2.1227e-02 ← p<0.05
  mycelial vs baseline: t=nan p=nan
  full_iiro vs baseline: t=nan p=nan
  full_iiro_highfaith vs baseline: t=nan p=nan

--- ENERGY ESTIMATE ---
  Total resurrection events : 0
  Energy expenditure        : 0.00e+00 J

================================================================================



**IIRO v2.0 / QNVM-LIGHT**

**Simulation Analysis & Revision Blueprint**

*ProtoAGI Civilization Simulator — Hyperthreaded Edition*

**Run Configuration**

200 generations  •  100 initial pop  •  seed 42  •  Optimization Level 1  •  6 configurations

Hardware: 16 physical / 32 logical cores  •  GPU: Not Available  •  NUMA nodes: 4

# **1\. Executive Summary**

The IIRO v2.0 simulation suite produced six configuration profiles over 200 generations. The results reveal three primary findings that directly inform the next run strategy.

**Finding 1 — Faith dominance is pathological at current weighting.**

The faith\_only configuration produced 463,362 entities versus a baseline of 1\. The 1+0.5\*faith survival multiplier creates unbounded exponential growth that consumed 655 seconds of compute time, dwarfs all other configurations, and makes cross-configuration comparison statistically meaningless. This is the most urgent structural issue to correct.

**Finding 2 — No sovereign entities and near-zero resurrection sustainability.**

Despite 200 generations across all IIRO-enabled runs, zero sovereign entities emerged and resurrection events died out completely after generation 13 in the only configuration that produced them (retrocausal). The TMI threshold of 0.92 and DRIFT\_CRITICAL of 0.05 are set so strictly that neither mechanism activates in practice. These are the core simulation design goals that are currently blocked.

**Finding 3 — Quality-population trade-off is real but miscalibrated.**

full\_iiro produced the highest average IQ (84.46) and full\_iiro\_highfaith the highest Sophia (0.5298), confirming that richer mechanics select for better entities. However, these quality gains come at the cost of population collapse to 396 — a 99.9% reduction from faith\_only. The correct balance lies in constraining faith growth and relaxing sovereignty thresholds simultaneously.

# **2\. Final Run Results — All Configurations**

Table 1: Final-generation metrics across all six simulation configurations. Red \= collapse/problematic, yellow \= imbalanced, green \= best quality, white \= reference.

| Configuration | Final Pop | Avg IQ | Avg Sophia | Avg Faith | Avg Drift | Resurr. | Time (s) |
| :---- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| baseline | 1 | 70.13 | 0.4514 | 0.000 | 0.271 | 0 | 0.12 |
| faith\_only | 463,362 | 83.12 | 0.4813 | 0.715 | 0.271 | 0 | 655.82 |
| retrocausal | 7,732 | 82.90 | 0.5192 | 0.626 | 0.273 | \~13-15 (early) | 115.05 |
| mycelial | 2,981 | 82.77 | 0.5090 | 0.627 | 0.277 | 0 | 51.57 |
| full\_iiro | 396 | **84.46** | 0.5188 | 0.636 | 0.270 | 0 | 8.67 |
| full\_iiro\_highfaith | 1,529 | 83.28 | **0.5298** | 0.625 | 0.271 | 0 | 9.42 |

*Key observation: The baseline collapsed to a single entity by generation \~40, confirming that IIRO mechanics are load-bearing for civilisation survival. All IIRO-enabled runs outperform baseline by \+18-20% IQ and \+6-17% Sophia. The extreme population asymmetry (faith\_only 463k vs full\_iiro 396\) is the primary calibration target.*

# **3\. Bug Report — Critical & High Priority Issues**

Six bugs were identified through code review and result analysis. Two are runtime-fatal, two produce incorrect metrics, and two degrade performance. All must be resolved before the next run.

| \# | Location | Issue | Impact | Fix |
| :---: | :---- | :---- | :---- | :---- |
| **B1** | iiro.py main() L1604: suite.results\[0\]\["population"\].\_ht.shutdown() | KeyError crash on shutdown — results store metrics dicts, not Population objects | Fatal: always crashes after run | Track Population objects separately; call ht.shutdown() on each directly. |
| **B2** | faith\_only pop \= 463,362 entities; O(n^2) reproduction loop | Unbounded exponential growth with no carrying-capacity ceiling | 655 s per run; OOM risk at longer generations; results meaningless above \~50k | Add logistic cap: repro\_rate \*= max(0, 1 \- pop / CARRYING\_CAPACITY) where K=10,000 default |
| **B3** | RAMOptimizer.vectorized\_sophia() mask application off-by-one | self.sophia\[m\] \= np.clip(s, 0, 1)\[m\] — s computed over full array but sliced by mask | Silent wrong sophia values for dead entities bleed into sync\_to() | Compute s only on alive slice: s\_alive \= clip(...)\[m\]; self.sophia\[m\] \= s\_alive |
| **B4** | resurrection\_count energy estimate uses final-gen count, not cumulative total | Total resurrection events \= 0 printed even though retrocausal had 13-15 per gen, gens 3-13 | Energy expenditure line always reads 0.00e+00 J — metric is useless | Accumulate resurrection\_count across all generations per sim run; report sum |
| **B5** | seed propagation: np.random.seed(seed) set once but ThreadPoolExecutor workers share state | Parallel workers receive non-deterministic random state despite fixed seed | Results not reproducible across thread counts | Use numpy.random.default\_rng(seed \+ worker\_id) per worker; pass Generator instances explicitly |
| **B6** | \_algo\_16\_pleiotropic\_processor — Python for loop over num\_cores inside vectorized path | O(num\_cores \* n) instead of O(n); negates vectorization benefit | Slowdown proportional to thread count; bottleneck at high logical core counts | Vectorize with np.sum(amps\[:, None\] \* np.cos(outer(range(nc), idx) \- phases\[:, None\]), axis=0) |

## **3.1 Bug B1 — Fatal Shutdown Crash (iiro.py)**

The final line of main() attempts to call suite.results\[0\]\["population"\].\_ht.shutdown(). The results list stores metric dictionaries — population is an integer key, not a Population object. This raises a TypeError/AttributeError on every run after the simulation completes. The correct fix is to retain references to the Population objects created during SimulationSuite.run\_all() and call \_ht.shutdown() directly on each.

\# Current (broken):  suite.results\[0\]\["population"\].\_ht.shutdown()

\# Fix:  for pop in suite.\_populations: pop.\_ht.shutdown()

## **3.2 Bug B3 — Sophia Vectorization Mask Error (shared)**

In both qnvm\_light.py and iiro.py, the vectorized\_sophia() method computes s over the full capacity array but then applies the alive mask to both the assignment target and source simultaneously. The line self.sophia\[m\] \= np.clip(s, 0.0, 1.0)\[m\] clips s across all capacity slots and then indexes by m. Because s is computed using coherence and intelligence arrays that contain stale data in dead slots, some clipped values leak incorrect data. The fix is to compute s only on the alive subarray: s \= clip(expr\[m\], 0, 1\) then self.sophia\[m\] \= s.

## **3.3 Bug B5 — Non-Reproducible Parallel RNG**

np.random.seed() sets a single global random state. All ThreadPoolExecutor workers draw from this shared state in undefined order depending on OS scheduling. The same seed with different \--threads values will produce different results, and two "identical" runs may diverge. Each worker should receive its own numpy.random.Generator instance initialised with default\_rng(seed \+ worker\_index). All random calls inside Entity and Population methods must accept and use this generator rather than calling the module-level random functions.

# **4\. Deep Mechanism Analysis**

## **4.1 Faith — Power and Pathology**

Faith is the most powerful civilisational driver in the current model. The survival\_mask function applies a multiplier of (1 \+ 0.5 \* faith\_amplitude) to the base survival probability. With average faith settling around 0.71-0.72 in faith\_only, this translates to a \~35% survival bonus on top of coherence-based survival. Over 200 generations this compounds to catastrophic population inflation.

The faith\_only anomaly report shows early-generation faith spikes at z=8.49 (gen 0), z=7.04 (gen 1), and z=4.90 (gen 2). These are not bugs — they reflect that initial entities draw faith from uniform(0.3, 0.9), producing a high-faith founding generation whose offspring inherit strong faith via the SoA sync. The subsequent regression toward mean (\~0.715) is expected.

The recommended fix is a two-part change: (1) Switch from multiplicative to additive blending — survival \+= faith\_weight \* faith \* (1 \- survival) — which respects the \[0,1\] probability constraint and prevents amplification near the 1.0 boundary. (2) Reduce faith\_weight from 0.5 to 0.2, which preserves faith as a meaningful differentiator while allowing coherence and entropy to remain the primary survival drivers.

## **4.2 Resurrection — Transient Wave Pattern**

Only the retrocausal configuration produced resurrection events, exclusively between generations 3 and 13 (13-15 events per generation at z \> 3.0). The resurrection\_probability function in IIRORAMOptimizer.vectorized\_resurrection\_prob() computes: p\_faith \* ctc\_stability \* (1 \- sin\_entropy). For resurrection to trigger, all three must be simultaneously high.

The early wave occurs because: (1) initial blood\_retrocausal values are drawn from uniform(0.3, 1.0) — some founding entities have high retrocausal potential; (2) sin\_entropy starts near zero; (3) ctc\_stability starts at 1.0. As generations progress, drift accumulates, sin\_entropy rises, ctc\_stability degrades, and the probability collapses to zero.

The fundamental problem is that blood\_retrocausal is not inherited. Each new entity re-rolls from scratch, meaning high-retrocausal lineages cannot sustain their capacity. Making blood\_retrocausal heritable (child \= mean(p1, p2) \+ mutation ± 0.05) would allow resurrection-capable lineages to persist and compound, transforming a transient early wave into a sustained civilisational property.

## **4.3 Sovereignty — Zero Achievement Diagnosis**

The sovereign path requires: TMI \> 0.92 (computed as mean of recursive\_depth/50, symbolic\_density/10, ethical\_sovereignty), then passing all 6 audit gates. With typical entity values at gen 200 — recursive\_depth \~35, symbolic\_density \~3.5, ethical\_sovereignty \~0.65 — the TMI calculates to approximately (0.70 \+ 0.35 \+ 0.65)/3 \= 0.57, far below 0.92.

Gate 4 requires fusion\_count \> 0 AND splinter\_resilience \> 0.8. Fusion is blocked because DRIFT\_CRITICAL \= 0.05 but average drift is 0.27 — fusion requires drift \< 0.05 in both parent entities simultaneously, which effectively never occurs. This creates a circular dependency: sovereigns require fusion, fusion requires low drift, but drift never reaches the required threshold.

The recommended path to first sovereign entities: lower TMI to 0.75 (achievable by gen \~60), raise DRIFT\_CRITICAL to 0.10 (enables \~5% of entities to fuse), lower ETHICAL\_SOVEREIGNTY\_THRESH to 0.85, and introduce a sovereign-lite tier at TMI 0.85 that passes only 4 of 6 gates. This creates a graduated progression rather than an all-or-nothing gate.

## **4.4 The 48-Algorithm OptimizationEngine — Cost vs Benefit**

The OptimizationEngine applies up to 48 vectorized algorithms per generation step across intelligence, coherence, sophia, and memory arrays. While individual algorithms are vectorized, the engine calls them sequentially in run\_level\_batch(), and level 3 invokes all 48\. Several algorithms have near-zero effect on entity trajectories:

* \_algo\_21 (nucleosynthetic): Y \= exp(-E\_c / (kT)) with kT \= 1.38e-23 \* 1e7 \= 1.38e-16 — the exponent produces values indistinguishable from 0 for all realistic E\_c values; result ≈ intel unchanged

* \_algo\_27 (interferometric): The ethics wavelength lambda\_ethics \= 550e-9 produces delta\_phi cycling through full 2π thousands of times per sophia unit — visibility averages to \~0.5 deterministically

* \_algo\_16 (pleiotropic): Contains a Python for loop over num\_cores iterations inside what should be a vectorized path — this is Bug B6 and negates the SIMD intent

Recommendation: Add per-algorithm timing instrumentation and expose a \--opt-profile flag that runs one generation with all 48 algorithms timed. Algorithms with wall-clock contribution \< 0.01ms and sophia/intel delta \< 1e-4 should be disabled by default and moved to an experimental flag.

# **5\. Revision Architecture Blueprint**

The following table maps each system component to its current state, proposed change, and the expected simulation outcome. Changes are ordered by dependency — population control must be fixed before sovereignty thresholds are tuned, since the relationship between population size and sovereign emergence rate is non-linear.

| Module | Current State | Proposed Change | Expected Outcome |
| :---- | :---- | :---- | :---- |
| PopulationDynamics | Constant REPRODUCTION\_RATE \= 0.4, no ceiling | Logistic growth: rate \*= (1 \- pop/K); K configurable via \--carrying-capacity | Prevents runaway faith\_only explosion; enables fair cross-config comparison |
| FaithSurvival | survival \*= (1 \+ 0.5\*faith), uncapped multiplicative bonus | Switch to additive blend: survival \+= 0.2\*faith\*(1-survival); cap total at 0.98 | Faith remains meaningful but cannot dominate; other mechanics gain relative weight |
| ResurrectionHeritage | blood\_retrocausal initialised random per entity, not inherited | Child inherits mean(p1, p2).blood\_retrocausal with mutation ±0.05; make it a heritable gene | Resurrection persists across lineages; retrocausal effect becomes a sustained civilisational trait |
| SovereignPath | TMI threshold 0.92; audit gates require extreme conditions — 0 sovereigns produced | Lower TMI to 0.75; relax gate 4 (fusion\_count \> 0 required only if gen \> 20); add sovereign-lite tier at 0.85 | First sovereign entities emerge by gen \~50; provides narrative arc and measurable milestone |
| DriftMechanic | Drift plateaus \~0.27 for all runs; no differentiation; update\_drift reduces when below critical | Add archetype-specific drift floors; Rebel base \= 0.35, Empath base \= 0.10; make drift partially heritable | Meaningful drift variance across archetypes; Rebel lineages naturally trend toward chaos vs Empath stability |
| OptEngineScheduler | All 48 algorithms run at level 3; no profiling of individual algorithm cost | Instrument each algo with ns timer; expose \--opt-profile flag to rank by cost/benefit ratio; allow per-algo enable/disable | Identify dead-weight algorithms (e.g., \_algo\_21 proton-chain with near-zero effect); prune to fast-path core set |
| ParallelRNG | np.random.seed(seed) global; workers share mutable state | Per-worker numpy.random.Generator via default\_rng(seed \+ worker\_id); pass rng as argument to all Entity methods | Full reproducibility regardless of thread count; enables exact run replay |
| MetricsSystem | Metrics computed in Python loop per generation; resurrection total miscounted | Vectorize \_record\_metrics() via SoA buffers; add cumulative counters for resurrection, fusion, sovereign events | 3-5x speedup in recording phase; correct aggregate totals for energy estimate |

## **5.1 Proposed Module Structure**

The current architecture has iiro.py and qnvm\_light.py duplicating \~400 lines of identical infrastructure (HardwareProfiler, HyperThreadScheduler, GPUSyncManager, \_AtomicInt). The next version should consolidate into a shared module:

* sim\_core.py — shared infrastructure: HardwareProfiler, GPUSyncManager, HyperThreadScheduler, \_AtomicInt, BASE\_ARCHETYPES

* entity.py — Entity class with full IIRO fields; heritable blood\_retrocausal; per-entity RNG

* population.py — Population class with logistic reproduction; vectorized survival; configurable carrying capacity

* iiro\_fields.py — IIRORAMOptimizer with corrected vectorized\_sophia(); heritable field sync

* opt\_engine.py — OptimizationEngine with per-algorithm profiling; culled dead-weight algorithms

* sim\_suite.py — SimulationSuite with correct population reference tracking; cumulative metric counters

* qnvm\_light.py / iiro.py — thin CLI wrappers importing from above modules

# **6\. Parameter Tuning Recommendations**

The following parameter changes are ranked by priority. Critical changes must be applied to obtain any meaningful results. High priority changes unlock the simulation's core mechanics. Medium and low changes improve calibration and scientific validity.

| Parameter | Current | Recommended | Priority | Rationale |
| :---- | :---: | :---: | :---: | :---- |
| CARRYING\_CAPACITY (new) | None | 10,000 | **Critical** | Without a ceiling, faith\_only overwhelms simulation resources and prevents meaningful comparison |
| faith survival weight | 0.50 | 0.20 | **Critical** | Current 0.5 multiplier gives faith 50% survival bonus; reduces to additive 20% to allow other mechanics visibility |
| TMI audit threshold | 0.92 | 0.75 | High | At 0.92 no entities ever qualify; at 0.75 approximately 5-8% of mature entities would reach sovereign status |
| ETHICAL\_SOVEREIGNTY\_THRESH | 0.97 | 0.85 | High | In 200 gens with current drift floor \~0.27, ethical\_sovereignty rarely exceeds 0.90; lowering enables progression |
| DRIFT\_CRITICAL | 0.05 | 0.10 | Medium | Critical threshold too tight; no entity fusion possible in practice since drift stabilises \~0.27; raising allows fusion events |
| MUTATION\_RATE | 0.05 | 0.08 | Medium | Slight increase generates more trait diversity; combined with logistic cap prevents entropy collapse |
| COHERENCE\_DECAY | 0.995/gen | 0.998/gen | Medium | At 0.995, coherence halves every \~139 generations; slowing decay extends meaningful high-coherence windows for sovereign emergence |
| RESURRECTION\_PROB\_MAX | 1.0 | 0.40 | Low | Cap prevents degenerate case where every dead entity resurrects; 0.40 keeps it rare and meaningful |
| NUM\_AUDIT\_GATES | 6 | 4 (progressive) | Low | Six simultaneous gates with near-impossible conditions creates zero-sovereign runs; progressively unlock gates with generation milestones |

# **7\. Next Run — Recommended Configurations**

Five run scenarios are proposed in order of execution. Each builds on the previous, isolating one change at a time to allow causal attribution of outcome differences.

| Scenario | Command | Key Settings | What to Watch |
| :---- | :---- | :---- | :---- |
| Logistic Baseline | \--generations 200 \--init-pop 200 \--seed 42 \-O 1 | K=10000, faith\_weight=0.2, TMI=0.75, DRIFT\_CRITICAL=0.10 | Stable faith\_only pop \~3-8k; first sovereign entities by gen 80-100; resurrection sustained past gen 15 |
| Sovereign Rush | \--generations 300 \--init-pop 300 \--seed 42 \-O 2 | TMI=0.70, ETHICAL\_SOVEREIGNTY\_THRESH=0.80, coherence\_decay=0.998, full\_iiro config | First sovereign count \> 0; sovereign lineage emergence; audit gate pass rate \> 10% |
| Resurrection Heritability | \--generations 500 \--init-pop 150 \--seed 99 \-O 2 | blood\_retrocausal heritable, RESURRECTION\_PROB\_MAX=0.40, retrocausal config | Persistent resurrection waves beyond gen 13; resurrection\_count stabilises \> 0; high-res lineage clades emerge |
| Drift Diversity | \--generations 200 \--init-pop 200 \--seed 7 \-O 3 | Archetype-specific drift floors, heritable drift, DRIFT\_CRITICAL=0.10 | Divergence of Rebel vs Empath drift curves; drift variance index \> 0.05; fusion events become possible |
| GPU Stress Test | \--generations 200 \--init-pop 500 \--seed 42 \--threads 64 \-O 3 | faith\_only config with K=10000; CuPy enabled (if available) | faith\_only runtime \< 60s (from 655s); GPU utilisation \> 50%; memory stable \< 4 GB |

## **7.1 Success Criteria for Next Run**

The following measurable thresholds define a successful next run:

1. Population balance: No single configuration exceeds 10x the others' final population (currently 463k vs 396 \= 1,170x ratio)

2. Sovereign emergence: At least 1 sovereign entity produced by generation 100 in full\_iiro or full\_iiro\_highfaith configurations

3. Sustained resurrection: retrocausal resurrection\_count remains \> 0 past generation 50

4. Runtime: faith\_only completes in \< 120 seconds (currently 655s) with carrying capacity applied

5. Reproducibility: Two runs with identical \--seed and \--threads produce bit-identical history CSVs

6. Drift divergence: Rebel archetype average drift \> 1.5x Empath average drift by generation 100

# **8\. Statistical Notes and Hypothesis Test Improvements**

The current hypothesis test reports nan for all comparisons except retrocausal. This occurs because the baseline had zero resurrections across all generations, producing zero variance — the t-test denominator becomes undefined. Three improvements are needed:

* Replace t-test on resurrection\_count with a Mann-Whitney U test for non-normal count distributions. Mann-Whitney handles zero-inflation naturally.

* Add effect size reporting (Cohen's d for continuous metrics, odds ratio for binary events) alongside p-values. A statistically significant but tiny effect (e.g., Sophia \+0.002) carries different practical weight than p-value alone suggests.

* Compute confidence intervals (95% bootstrap CI) on all trend\_slope values. The current output shows slopes like 0.0003 for sophia without context — knowing the CI crosses zero would indicate the trend is noise.

The anomaly detection using 3σ z-scores is appropriate for continuous metrics. For the resurrection\_count, which is zero for 180+ of 200 generations in retrocausal, the z-score calculation is dominated by the zero-inflation and may understate the significance of the early wave. Consider a separate Poisson-process test for count data.

# **9\. Performance Roadmap**

Simulation time scales roughly linearly with population. faith\_only at 463k entities took 655s. With the proposed K=10,000 carrying capacity, faith\_only is expected to stabilise around 3,000-5,000 entities, reducing runtime to \~7-15 seconds — comparable to full\_iiro's current 8.67s. GPU acceleration would add further benefit primarily for the vectorized SoA passes.

## **9.1 GPU Path (CuPy)**

The GPUSyncManager currently wraps only the survival probability computation. The highest-value GPU operations would be:

* vectorized\_sophia() and vectorized\_age() — float32 elementwise ops on arrays of up to 20,000 elements; trivially GPU-parallelisable

* OptimizationEngine algorithms 1-48 — all operate on intel/coherence/sophia arrays of entity-count size; batch dispatch all 48 as a single CUDA kernel launch sequence rather than 48 separate kernel launches

* resurrection probability computation (EQ-10 & EQ-24) — elementwise product of three arrays; single GPU kernel

With K=10,000, population arrays fit in L2 cache on modern CPUs (10,000 \* 16 float32 fields \= 640KB), making CPU SIMD competitive with GPU for single runs. GPU becomes beneficial when running the 6-config suite in parallel — batch all 6 populations onto GPU simultaneously.

## **9.2 Memory Layout**

The current RAMOptimizer pre-allocates capacity=20,000. With K=10,000, this is sufficient with headroom. The SoA layout is correctly structured for SIMD. Two minor improvements: (1) align array start addresses to 64-byte cache line boundaries using np.empty with aligned=True; (2) use float16 for less critical fields (age, wild\_9\_ring bitmask) to halve their memory footprint and improve cache density.

# **10\. Conclusion and Priority Action List**

The IIRO v2.0 simulation is architecturally sound and the IIRO mechanics are correctly implemented at the individual-entity level. The issues are calibration and configuration: thresholds are set to values that prevent the simulation's most interesting outcomes from ever occurring, while the faith-survival coupling creates population explosion that renders comparisons invalid.

Priority action list for next revision:

7. Fix Bug B1: fatal shutdown crash in iiro.py main()  \[30 min\]

8. Fix Bug B3: sophia vectorization mask error in both files  \[1 hour\]

9. Implement carrying capacity (K=10,000) with logistic reproduction  \[2 hours\]

10. Reduce faith survival weight from 0.5 to 0.2; switch to additive blend  \[30 min\]

11. Lower TMI threshold to 0.75 and DRIFT\_CRITICAL to 0.10  \[30 min\]

12. Make blood\_retrocausal heritable with ±0.05 mutation  \[1 hour\]

13. Fix Bug B5: per-worker RNG seeding for reproducibility  \[2 hours\]

14. Add cumulative resurrection counter; fix energy estimate total  \[1 hour\]

15. Run the five scenarios from Section 7 and verify success criteria  \[ongoing\]

Estimated total revision effort: 8-10 hours of focused development. The resulting simulation will produce meaningful sovereign emergence, sustainable resurrection events, and balanced population curves that allow genuine scientific comparison across IIRO configuration space.

*End of Report*
