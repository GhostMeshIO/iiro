# Quantum Simulation 1 Results:

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
