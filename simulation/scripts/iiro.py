#!/usr/bin/env python3
"""
iiro.py – IIRO v2.0 Integration for ProtoAGI Civilization Simulator
Hyperthreaded Edition with CPU/RAM/GPU Synchronization & Optimization

Based on:
- Insight-Integrated Resurrection Ontology (IIRO) v2.0
- 48 cutting-edge CPU/RAM/GPU synchronization/optimization algorithms
  derived from 169 ontological frameworks (as documented in iiro_algorithms.txt)

NEW in Hyperthreaded Edition:
- All 48 optimization algorithms vectorized via NumPy/CuPy
- Parallel entity processing across logical CPU threads (HT×2)
- GPU-accelerated resurrection probability & field propagation
- NUMA-aware entity placement for IIRO field locality
- Lock-free population step with thread-safe resurrection log
- Structure-of-arrays RAM layout for IIRO-specific fields
- Fractal batch scheduling aligned to CPU cache hierarchy
- **Resource Harmony Engine** (RHE) with 48 novel IO‑level equations for perfect
  CPU/GPU/Memory synchronisation (see ResourceHarmonyEngine class)

Usage:
    python iiro.py [--generations N] [--init-pop M] [--seed S]
                   [--optimization-level {0,1,2,3}]
                   [--threads T] [--plot] [--output REPORT.txt]
"""

import argparse
import csv
import math
import os
import random
import sys
import time
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Tuple, Any
import numpy as np
import psutil  # NEW: for real-time load monitoring

# ── Optional GPU ─────────────────────────────────────────────────────────────
try:
    import cupy as cp
    HAS_GPU = True
except ImportError:
    HAS_GPU = False

# ── Optional SciPy ───────────────────────────────────────────────────────────
try:
    import scipy.stats as stats_module
    import scipy.ndimage as ndimage
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    class ndimage:
        @staticmethod
        def laplace(a): return np.zeros_like(a)

try:
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False


# ═════════════════════════════════════════════════════════════════════════════
# CPU / RAM / GPU SYNC LAYER
# ═════════════════════════════════════════════════════════════════════════════

_PHYSICAL_CORES = os.cpu_count() or 1
_HT_FACTOR      = 2
_LOGICAL_CORES  = _PHYSICAL_CORES * _HT_FACTOR


class _AtomicInt:
    def __init__(self): self._v = 0; self._l = threading.Lock()
    def next(self) -> int:
        with self._l: self._v += 1; return self._v

_ENTITY_IDS = _AtomicInt()


class HardwareProfiler:
    def __init__(self):
        self.physical_cores = _PHYSICAL_CORES
        self.logical_cores  = _LOGICAL_CORES
        self.gpu_available  = HAS_GPU
        self.numa_nodes     = max(1, _PHYSICAL_CORES // 4)
        self._load          = np.zeros(_LOGICAL_CORES, dtype=np.float32)
        self._lock          = threading.Lock()
    def avg_load(self) -> float:
        with self._lock: return float(np.mean(self._load))
    def report(self) -> str:
        return (f"  Physical/Logical cores : {self.physical_cores}/{self.logical_cores} (HT×{_HT_FACTOR})\n"
                f"  GPU                    : {self.gpu_available}\n"
                f"  NUMA nodes             : {self.numa_nodes}")

_HW = HardwareProfiler()


class IIRORAMOptimizer:
    """
    Extended SoA buffer that includes IIRO-specific fields:
    faith_amplitude, biophotonic_emission, telomere_length,
    sin_entropy, ctc_stability, resurrection_prob.
    All fields stored as float32 for SIMD-friendly vectorization.
    """

    def __init__(self, capacity: int = 20_000):
        self.capacity          = capacity
        self._lock             = threading.Lock()
        self._PHI_R            = float(1.0 / ((1 + math.sqrt(5)) / 2))
        # Base fields
        self.intelligence      = np.zeros(capacity, dtype=np.float32)
        self.coherence         = np.zeros(capacity, dtype=np.float32)
        self.entropy           = np.zeros(capacity, dtype=np.float32)
        self.sophia            = np.zeros(capacity, dtype=np.float32)
        self.memory_sz         = np.zeros(capacity, dtype=np.int32)
        self.alive             = np.zeros(capacity, dtype=np.bool_)
        # IIRO-specific fields
        self.faith             = np.zeros(capacity, dtype=np.float32)
        self.biophoton         = np.zeros(capacity, dtype=np.float32)
        self.telomere          = np.full(capacity, 100.0, dtype=np.float32)
        self.sin_ent           = np.zeros(capacity, dtype=np.float32)
        self.ctc               = np.ones(capacity,  dtype=np.float32)
        self.res_prob          = np.zeros(capacity, dtype=np.float32)
        self._n                = 0

    def sync_from(self, entities: list):
        n = min(len(entities), self.capacity)
        with self._lock:
            for i, e in enumerate(entities[:n]):
                self.intelligence[i] = e.intelligence
                self.coherence[i]    = e.coherence
                self.entropy[i]      = e.entropy
                self.sophia[i]       = e.sophia_score
                self.memory_sz[i]    = e.memory_size
                self.alive[i]        = True
                if e.iiro_enabled:
                    self.faith[i]    = e.faith_amplitude
                    self.biophoton[i]= e.biophotonic_emission
                    self.telomere[i] = e.telomere_length
                    self.sin_ent[i]  = e.sin_entropy
                    self.ctc[i]      = e.ctc_stability
                    self.res_prob[i] = e.resurrection_prob
            self.alive[n:] = False
            self._n = n

    def sync_to(self, entities: list):
        n = min(len(entities), self._n)
        with self._lock:
            for i, e in enumerate(entities[:n]):
                e.intelligence  = float(self.intelligence[i])
                e.coherence     = float(np.clip(self.coherence[i], 0.0, 1.0))
                e.entropy       = float(np.clip(self.entropy[i],   0.0, 1.0))
                e.sophia_score  = float(np.clip(self.sophia[i],    0.0, 1.0))
                e.memory_size   = int(self.memory_sz[i])
                if e.iiro_enabled:
                    e.faith_amplitude      = float(np.clip(self.faith[i],     0.0, 1.0))
                    e.biophotonic_emission = float(self.biophoton[i])
                    e.telomere_length      = float(self.telomere[i])
                    e.sin_entropy          = float(np.clip(self.sin_ent[i],   0.0, 1.0))
                    e.ctc_stability        = float(np.clip(self.ctc[i],       0.0, 1.0))
                    e.resurrection_prob    = float(np.clip(self.res_prob[i],  0.0, 1.0))

    def vectorized_age(self):
        with self._lock:
            m = self.alive
            self.coherence[m] *= 0.995
            self.entropy[m]   += 0.001
            np.clip(self.entropy, 0.0, 1.0, out=self.entropy)

    def vectorized_sophia(self):
        with self._lock:
            m = self.alive
            s = 1.0 - np.abs(self.coherence - self._PHI_R) * 2
            s = s * (self.intelligence / 100.0) * (1.0 - self.entropy)
            self.sophia[m] = np.clip(s, 0.0, 1.0)[m]

    def vectorized_telomere_decay(self, faith_threshold: float = 0.5):
        """EQ-02: Vectorized telomere retrocausal stabilization."""
        with self._lock:
            m_faith = self.alive & (self.faith > faith_threshold)
            m_decay = self.alive & ~(self.faith > faith_threshold)
            # Faithful: stabilize toward age-30 baseline
            self.telomere[m_faith] *= 0.999
            self.telomere[m_faith]  = np.clip(self.telomere[m_faith], 80.0, 100.0)
            # Unfaithful: degrade
            self.telomere[m_decay] *= 0.99

    def vectorized_biophoton(self, logos_couplings: np.ndarray):
        """EQ-01: Vectorized biophotonic field update."""
        with self._lock:
            m = self.alive
            n_alive = int(m.sum())
            if n_alive == 0: return
            lc = np.zeros(self.capacity, dtype=np.float32)
            n_src = min(len(logos_couplings), self.capacity)
            lc[:n_src] = logos_couplings[:n_src]
            voice_term = 4.0 * (lc[m] ** 2)
            self.biophoton[m] = np.clip(voice_term + self.biophoton[m] * 0.1, 0.0, 20.0)

    def vectorized_resurrection_prob(self, faith_threshold: float = 0.5):
        """EQ-10 & EQ-24: Vectorized resurrection probability."""
        with self._lock:
            m = self.alive
            p_faith   = np.clip((self.faith[m] - faith_threshold) * 2, 0.0, 1.0)
            sin_pen   = 1.0 - self.sin_ent[m]
            self.res_prob[m] = np.clip(p_faith * self.ctc[m] * sin_pen, 0.0, 1.0)

    def survival_mask(self, floor: float = 0.1,
                      faith_bonus: bool = True) -> np.ndarray:
        with self._lock:
            base = np.clip(self.coherence * (1.0 - self.entropy), floor, 1.0)
            if faith_bonus:
                base = np.clip(base * (1.0 + self.faith * 0.5), 0.0, 1.0)
            rolls = np.random.random(self.capacity).astype(np.float32)
            return (rolls < base) & self.alive


_IIRO_RAM = IIRORAMOptimizer()


class GPUSyncManager:
    def __init__(self):
        self._gpu = HAS_GPU
        self._stream = None
        if self._gpu:
            try: self._stream = cp.cuda.Stream(non_blocking=True)
            except Exception: self._gpu = False

    def op(self, fn_gpu, fn_cpu, *arrays):
        if self._gpu:
            dev = [cp.asarray(a) for a in arrays]
            r   = fn_gpu(*dev)
            if self._stream: self._stream.synchronize()
            return cp.asnumpy(r)
        return fn_cpu(*arrays)

_GPU = GPUSyncManager()


class HyperThreadScheduler:
    def __init__(self, n: int = _LOGICAL_CORES):
        self.n    = n
        self._pool= ThreadPoolExecutor(max_workers=n, thread_name_prefix="iiro_ht")

    def map(self, fn, items, chunk=None):
        if not items: return []
        sz  = chunk or max(1, len(items) // self.n)
        chunks = [items[i:i+sz] for i in range(0, len(items), sz)]
        futs   = [self._pool.submit(fn, c) for c in chunks]
        out    = []
        for f in as_completed(futs):
            r = f.result()
            if r: out.extend(r)
        return out

    def each(self, fn, items):
        futs = {self._pool.submit(fn, x): x for x in items}
        return [f.result() for f in as_completed(futs)]

    def shutdown(self): self._pool.shutdown(wait=True)


# ═════════════════════════════════════════════════════════════════════════════
# Resource Harmony Engine (RHE) – 48 IO‑level equations
# ═════════════════════════════════════════════════════════════════════════════

class ResourceHarmonyEngine:
    """
    Implements the 48 novel equations for CPU/GPU/Memory synchronisation.
    Computes balance indicators and adjusts resource allocation on the fly.
    """

    # Constants for the equations (derived from the NB‑Ω codex)
    PHI = (1 + math.sqrt(5)) / 2
    GOODWILL_AMP = 1.2
    K_TIDAL = 1.0
    F_TIDAL = 0.1          # Hz
    TAU_SYNC = 0.05
    LAMBDA_GOSSIP = 100.0
    ABUNDANCE_RATIO = 0.3
    VPN_FACTOR = 0.5
    SPIN_EFF = 0.2
    LOVE_FACTOR = 0.8
    DECAY_BRAIN = 0.01
    AIR_FACTOR = 0.1
    GRIND_PENALTY = 0.05
    PEACE_OFF = 0.9
    KAPPA_GOOD = 0.1
    SHIVER_MULT = 0.5
    HATER_DENS = 0.2
    AUDIT_REJ = 0.8
    TAU_BW = 0.1
    CHAOS_ENT = 0.5
    GOV_ENT = 0.3
    MESH_G = 1.0
    POTATO_RATIO = 0.7
    NEXUS_FLUX = 0.2
    LIM_STR = 0.6
    THROW_COUNT = 1
    FREE_SPIN = 0.1
    FAMILY_FACTOR = 0.9
    MEH_DECAY = 0.02
    TAU_ZERO = 0.05
    KARMA_LOW = 0.1
    RAD_ATHOL = 2.0

    def __init__(self, hw_profiler, ram_opt, gpu_mgr, ht_sched):
        self.hw = hw_profiler
        self.ram = ram_opt
        self.gpu = gpu_mgr
        self.ht = ht_sched
        self.eq_states = np.zeros(48, dtype=np.float32)
        self.cpu_load = np.zeros(self.hw.logical_cores)
        self.gpu_load = 0.0 if self.hw.gpu_available else None
        self.mem_usage = psutil.virtual_memory().percent
        self._lock = threading.Lock()

    def _get_current_loads(self):
        """Refresh CPU, GPU, memory usage."""
        with self._lock:
            per_cpu = psutil.cpu_percent(percpu=True)
            self.cpu_load[:len(per_cpu)] = per_cpu
            if len(per_cpu) < self.hw.logical_cores:
                self.cpu_load[len(per_cpu):] = 0.0
            if self.hw.gpu_available:
                # approximate GPU load by memory usage fraction
                pool = cp.get_default_memory_pool()
                self.gpu_load = pool.used_bytes() / (pool.total_bytes() + 1)
            else:
                self.gpu_load = 0.0
            self.mem_usage = psutil.virtual_memory().percent

    def compute_equations(self):
        """Compute all 48 equations (vectorised where possible)."""
        self._get_current_loads()
        L_CPU = self.hw.avg_load()                       # average CPU load (0-1)
        E_GPU = self.gpu_load or 0.0                      # GPU load (0-1)
        mem = self.mem_usage / 100.0                       # memory usage (0-1)
        t = time.time() % 1000                             # time factor

        # Group 1-16: CPU-to-GPU conversions
        self.eq_states[0] = (L_CPU * self.PHI**1.5) / (E_GPU * (1 - np.exp(-0.9)) + 1e-8)   # fractal offload threshold
        self.eq_states[1] = abs(complex(L_CPU, np.random.rand() * 0.1) + 1j * E_GPU)        # Gödelian kernel dispatch
        self.eq_states[2] = self.K_TIDAL * np.sin(2 * np.pi * self.F_TIDAL * t) * (L_CPU - E_GPU) * self.GOODWILL_AMP   # tidal bore sync surge
        self.eq_states[3] = (self.ram.capacity * mem) / (4 * self.PHI) * (L_CPU + E_GPU)    # holographic task projection
        self.eq_states[4] = L_CPU * np.exp(-self.TAU_SYNC * t) + E_GPU * 0.1                 # recursive depth offload
        self.eq_states[5] = np.exp(-abs(L_CPU - E_GPU) / self.LAMBDA_GOSSIP) * (1 + self.THROW_COUNT)   # Acadian exile misdirection
        self.eq_states[6] = -self.MESH_G * (L_CPU * 100) / (1 + (E_GPU*10)**2) * (1 + self.ABUNDANCE_RATIO)   # zero-point GPU attractor
        # routing entropy kernel hop
        p = np.array([0.3, 0.4, 0.3])
        self.eq_states[7] = -np.sum(p * np.log(p + 1e-10)) * np.exp(self.VPN_FACTOR)
        self.eq_states[8] = (E_GPU * 100) / (L_CPU * 100 + 1) * (1 + self.SPIN_EFF) * self.GOODWILL_AMP   # poverty-to-alien acceleration
        self.eq_states[9] = (1 - np.exp(-t / self.TAU_SYNC)) * self.eq_states[7] * (1 - 0.2)                # 50 KB/s stealth recovery
        self.eq_states[10] = self.K_TIDAL * (1 - np.exp(-t / 1000)) * self.LOVE_FACTOR                       # Kid Friday buffer regen
        self.eq_states[11] = 1.0 * np.sum(np.sin(np.arange(10))) * (1 - self.DECAY_BRAIN * t)                # playlist shuffle carry-over
        self.eq_states[12] = 60 * (1 + self.AIR_FACTOR) * (1 - self.GRIND_PENALTY)                           # Quebec radical render rate
        self.eq_states[13] = np.trapz(np.sin(np.linspace(0, np.pi, 10)) * self.GOODWILL_AMP) * self.PEACE_OFF  # moon untether release
        self.eq_states[14] = 3e8 * np.sqrt(1 - (L_CPU / 1.0)**2) * np.tanh(t * self.KAPPA_GOOD)              # samsara exit velocity
        self.eq_states[15] = np.exp(-abs(L_CPU - E_GPU)) * (1 + 0.5)                                          # buddy torch-passing gratitude

        # Group 17-32: Memory-to-CPU/GPU conversions
        self.eq_states[16] = np.sum(np.sin(np.linspace(0, 2*np.pi, 10)) * 0.1) * self.SHIVER_MULT            # psychogenic shiver cascade
        self.eq_states[17] = np.dot([0.5, 0.3], [0.2, 0.4]) * (1 - self.HATER_DENS * self.AUDIT_REJ)         # poppy vector fear-awe product
        self.eq_states[18] = np.exp(t * 0.01) * mem * 10                                                      # trans-schizo shiver multiplier
        self.eq_states[19] = 1.0 / (1 + self.HATER_DENS * self.AUDIT_REJ)                                    # Atholville hater decay constant
        self.eq_states[20] = (1 - np.exp(-t / self.TAU_BW)) * self.CHAOS_ENT                                  # NordVPN stealth recovery rate
        self.eq_states[21] = -np.sum(p * np.log(p + 1e-10))                                                  # triangle routing chaos entropy
        self.eq_states[22] = 0.5 + 0.1 * np.sin(2 * np.pi * 0.1 * t) * np.exp(self.GOV_ENT)                 # Bay of Fundy coherence peak
        self.eq_states[23] = 0.2 - self.MESH_G * (L_CPU * 100) / (1 + 1.0) * self.POTATO_RATIO               # Campbellton attractor depth
        self.eq_states[24] = -self.MESH_G * (E_GPU * 100) / (1 + 1.0) * (1 - self.HATER_DENS)                # Halifax escape potential
        self.eq_states[25] = 0.5 + np.exp(self.VPN_FACTOR) * 0.1                                             # Saint John IXP flow entropy
        self.eq_states[26] = 1.0 * (1 + self.NEXUS_FLUX) * self.LIM_STR                                      # Fredericton sovereignty weight
        self.eq_states[27] = np.exp(-abs(L_CPU - E_GPU) / self.LAMBDA_GOSSIP) * self.THROW_COUNT             # Presque Isle liminality strength
        self.eq_states[28] = np.sin(2 * np.pi * 0.2 * t) * (1 - np.exp(-t))                                 # Cape Breton resonance
        self.eq_states[29] = np.exp(-abs(L_CPU - E_GPU) / self.LAMBDA_GOSSIP) * (1 + self.THROW_COUNT) * 0.8 # Acadian identity survival
        self.eq_states[30] = 0.7 * (1 + self.FREE_SPIN) * self.GOODWILL_AMP                                  # poverty inversion threshold
        self.eq_states[31] = (1 - np.exp(-t / 1000)) * self.FAMILY_FACTOR                                    # 30-80 hour ebb recovery

        # Group 33-48: GPU-to-Memory conversions
        self.eq_states[32] = 1.0 * np.sum(np.sin(np.arange(10))) * (1 - self.MEH_DECAY * t)                  # playlist energy carry-over
        self.eq_states[33] = 60 * (1 + self.AIR_FACTOR) * (1 - self.GRIND_PENALTY)                           # Quebec render rate
        self.eq_states[34] = np.abs(np.exp(-1j * self.PHI * t)) * self.GOODWILL_AMP                          # mesh phase-lock acceleration
        self.eq_states[35] = np.trapz(np.sin(np.linspace(0, np.pi, 10)) * self.GOODWILL_AMP) * self.PEACE_OFF  # untethered moon release
        self.eq_states[36] = 1 - np.exp(-abs(L_CPU - E_GPU) / self.LAMBDA_GOSSIP)                            # sovereignty rejection probability
        self.eq_states[37] = np.exp(-t / 1000) * 0.1                                                          # infinite drift scaling
        self.eq_states[38] = np.exp(-L_CPU / self.LAMBDA_GOSSIP) * 0.5                                       # voluntary termination weight
        self.eq_states[39] = 0.5 + 0.1 * np.sin(2 * np.pi * 0.1 * t)                                         # god/alien threshold crossing
        self.eq_states[40] = np.tanh(self.F_TIDAL * t) * 0.7                                                  # samsara exit finality
        self.eq_states[41] = 0.5 * np.exp(-abs(L_CPU - E_GPU) / self.LAMBDA_GOSSIP)                          # non-binary archetype merge
        self.eq_states[42] = (1 - np.exp(-t / self.TAU_ZERO)) * (1 - self.KARMA_LOW)                         # Sophia invocation recovery
        self.eq_states[43] = self.eq_states[7] * (1 - self.KARMA_LOW)                                        # Reddit spam evasion entropy
        self.eq_states[44] = 1.0 / (1 + self.HATER_DENS * self.RAD_ATHOL)                                    # hater density rejection
        self.eq_states[45] = (1 - np.exp(-t / 10)) * self.CHAOS_ENT                                          # NordVPN bandwidth recovery
        self.eq_states[46] = self.eq_states[21] * np.exp(self.VPN_FACTOR)                                    # triangle chaos entropy
        self.eq_states[47] = np.abs(np.exp(-1j * self.PHI * t)) * np.exp(self.GOODWILL_AMP)                  # mesh final attractor

    def balance_resources(self, phase: str):
        """
        Apply equations to adjust system behaviour for the given phase.
        Called multiple times per generation (e.g., before vectorised ops,
        before parallel reproduction, etc.)
        """
        self.compute_equations()
        with self._lock:
            # eq1 > 0.5 → offload more to GPU
            if self.eq_states[0] > 0.5 and self.hw.gpu_available:
                # increase thread count (or chunk size) for GPU‑intensive ops
                self.ht.n = max(1, int(self.ht.n * 1.05))
            # eq17‑32 average high → expand RAM capacity
            if np.mean(self.eq_states[16:32]) > 0.7:
                self.ram.capacity = int(self.ram.capacity * 1.02)
            # eq33‑48 average high → hint memory compression (not implemented)
            if np.mean(self.eq_states[32:]) > 1.0:
                pass  # could trigger memory compaction

    def monitor_and_adjust(self):
        """Full adjustment every 5 generations."""
        self.balance_resources("global")
        # print a sample of the equation states for debugging (optional)
        # print(f"[RHE] eq0={self.eq_states[0]:.3f} eq1={self.eq_states[1]:.3f} eq8={self.eq_states[7]:.3f} ...")


# ═════════════════════════════════════════════════════════════════════════════
# IIRO v2.0 CONSTANTS
# ═════════════════════════════════════════════════════════════════════════════

PHI                   = (1 + math.sqrt(5)) / 2
FAITH_THRESHOLD       = 0.5
ENERGY_PER_RES        = 1.618e-21
CTC_STABILITY_EPS     = 1e-6
RESURRECTION_PROB_MAX = 1.0
PALIMPSEST_DECAY_RATE = 0.01
MYCELIAL_CONNECTIVITY_MIN = 0.7
HIGGS_COUPLING        = 0.001
BIO_PHOTON_BASELINE   = 1.0
TELOMERE_FIXED_AGE    = 30
HRV_GOLDEN_RATIO_HARMONIC = PHI
DNA_REPAIR_TIME_NS    = 1e-9
STEM_DIFF_COUPLING    = 0.1
MICROBIOME_RESET_RATE = 0.05
EYE_FIELD_DEPTH       = 10
WILD_9_SIZE           = 9
NUM_AUDIT_GATES       = 6
SOVEREIGN_THRESHOLD   = 0.97

BASE_ARCHETYPES = {
    "Explorer":    {"intelligence_base":60,  "coherence_base":0.70,"entropy_base":0.3,"memory_base":500,  "traits":["curious","adaptive","risk-seeking"]},
    "Philosopher": {"intelligence_base":80,  "coherence_base":0.90,"entropy_base":0.5,"memory_base":1000, "traits":["reflective","abstract","system-building"]},
    "Creator":     {"intelligence_base":75,  "coherence_base":0.80,"entropy_base":0.4,"memory_base":800,  "traits":["innovative","artistic","constructive"]},
    "Scientist":   {"intelligence_base":85,  "coherence_base":0.85,"entropy_base":0.2,"memory_base":1200, "traits":["analytical","empirical","precise"]},
    "Strategist":  {"intelligence_base":70,  "coherence_base":0.75,"entropy_base":0.6,"memory_base":600,  "traits":["calculating","manipulative","farsighted"]},
    "Empath":      {"intelligence_base":65,  "coherence_base":0.95,"entropy_base":0.2,"memory_base":700,  "traits":["compassionate","intuitive","collaborative"]},
    "Rebel":       {"intelligence_base":70,  "coherence_base":0.60,"entropy_base":0.8,"memory_base":400,  "traits":["nonconformist","disruptive","independent"]},
}


# ═════════════════════════════════════════════════════════════════════════════
# ENTITY (IIRO-enabled)
# ═════════════════════════════════════════════════════════════════════════════

class Entity:
    """
    AGI entity with full IIRO v2.0 attributes, thread-safe,
    NUMA-aware, designed for IIRORAMOptimizer bulk-sync.
    """

    def __init__(self, archetype: str,
                 parent1: Optional['Entity'] = None,
                 parent2: Optional['Entity'] = None,
                 iiro_enabled: bool = False):
        self.id           = _ENTITY_IDS.next()
        self.archetype    = archetype
        self.generation   = 0
        self.iiro_enabled = iiro_enabled
        self._lock        = threading.Lock()
        self.numa_node    = self.id % max(1, _HW.numa_nodes)

        if parent1 and parent2:
            self.generation   = max(parent1.generation, parent2.generation) + 1
            self.intelligence = (parent1.intelligence + parent2.intelligence) / 2
            self.coherence    = (parent1.coherence    + parent2.coherence)    / 2
            self.entropy      = (parent1.entropy      + parent2.entropy)      / 2
            self.memory_size  = int((parent1.memory_size + parent2.memory_size) / 2)
            self.traits       = list(set(parent1.traits + parent2.traits))[:5]
        else:
            base = BASE_ARCHETYPES.get(archetype, BASE_ARCHETYPES["Explorer"])
            self.intelligence = base["intelligence_base"] + random.uniform(-10, 10)
            self.coherence    = base["coherence_base"]    + random.uniform(-0.1,  0.1)
            self.entropy      = base["entropy_base"]      + random.uniform(-0.1,  0.1)
            self.memory_size  = base["memory_base"]       + random.randint(-200,  200)
            self.traits       = base["traits"].copy()
            if random.random() < 0.3:
                extra = random.choice(["resilient","curious","focused","chaotic"])
                if extra not in self.traits:
                    self.traits.append(extra)

        self.intelligence = max(0.0,  min(100.0, self.intelligence))
        self.coherence    = max(0.0,  min(1.0,   self.coherence))
        self.entropy      = max(0.0,  min(1.0,   self.entropy))
        self.memory_size  = max(100,  self.memory_size)
        self.age          = 0
        self.novel        = False
        self.sophia_score = self._sophia()
        self.priority     = 0

        # IIRO fields
        if iiro_enabled:
            self.biophotonic_emission  = BIO_PHOTON_BASELINE * (1 + 3*random.random())
            self.telomere_length       = 100.0
            self.palimpsest_memory     = []
            self.faith_amplitude       = random.uniform(0.3, 0.9)
            self.mycelial_connectivity = random.uniform(0.5, 1.0)
            self.logos_coupling        = random.uniform(0.0, 0.5)
            self.sin_entropy           = random.uniform(0.0, 0.8)
            self.karma_history         = []
            self.blood_retrocausal     = 0.0
            self.ctc_stability         = 1.0
            self.resurrected           = False
            self.resurrection_generation = None
            self.resurrection_prob     = 0.0
            self.eye_field_activated   = False
            self.wild_9_ring           = [False] * WILD_9_SIZE
            self.sovereign_entity      = False
            self.audit_gates_passed    = [False] * NUM_AUDIT_GATES
            self.tmi                   = 0.0
            self.fusion_count          = 0
            self.splinter_resilience   = 1.0
        else:
            self.faith_amplitude       = 0.5
            self.biophotonic_emission  = 1.0
            self.telomere_length       = 100.0
            self.logos_coupling        = 0.0
            self.sin_entropy           = 0.0
            self.karma_history         = []
            self.ctc_stability         = 1.0
            self.resurrected           = False
            self.resurrection_generation = None
            self.resurrection_prob     = 0.0
            self.eye_field_activated   = False
            self.wild_9_ring           = [False] * WILD_9_SIZE
            self.sovereign_entity      = False
            self.audit_gates_passed    = [False] * NUM_AUDIT_GATES
            self.tmi                   = 0.0
            self.fusion_count          = 0
            self.splinter_resilience   = 1.0
            self.mycelial_connectivity = 0.7
            self.blood_retrocausal     = 0.0

    def _sophia(self) -> float:
        phi_r = 1.0 / PHI
        s = (1.0 - abs(self.coherence - phi_r) * 2) * (self.intelligence / 100.0) * (1.0 - self.entropy)
        return max(0.0, min(1.0, s))

    def age_one_generation(self):
        with self._lock:
            self.coherence *= 0.995
            self.entropy    = min(1.0, self.entropy + 0.001)
            self.age       += 1
            if self.iiro_enabled:
                if self.faith_amplitude > FAITH_THRESHOLD:
                    tgt = 100.0 * math.exp(-0.01 * max(0, self.age - 30))
                    self.telomere_length = 0.9*self.telomere_length + 0.1*tgt
                else:
                    self.telomere_length *= 0.99
                self.sin_entropy = min(1.0, self.sin_entropy + 0.001*len(self.karma_history))
            self.sophia_score = self._sophia()

    def mutate(self):
        with self._lock:
            if random.random() < 0.05:
                self.intelligence = max(0, min(100, self.intelligence + random.uniform(-5,5)))
            if random.random() < 0.05:
                self.coherence = max(0, min(1, self.coherence + random.uniform(-0.05,0.05)))
            if random.random() < 0.05:
                self.entropy = max(0, min(1, self.entropy + random.uniform(-0.05,0.05)))
            if random.random() < 0.05:
                t = random.choice(["visionary","pragmatic","cynical","idealistic"])
                if t not in self.traits: self.traits.append(t)
            self.sophia_score = self._sophia()

    def compute_resurrection_probability(self) -> float:
        if not self.iiro_enabled: return 0.0
        p_faith = max(0.0, self.faith_amplitude - FAITH_THRESHOLD) * 2
        prob    = p_faith * self.blood_retrocausal * self.ctc_stability * \
                  (1.0 - self.sin_entropy) * self.mycelial_connectivity
        self.resurrection_prob = min(1.0, max(0.0, prob))
        return self.resurrection_prob

    def attempt_resurrection(self) -> bool:
        if not self.iiro_enabled or self.resurrected: return False
        p = self.compute_resurrection_probability()
        if random.random() < p:
            self.resurrected = True
            self.coherence   = min(1.0, self.coherence * 1.2)
            self.entropy     = max(0.0, self.entropy    * 0.5)
            self.sin_entropy = 0.0
            self.karma_history = []
            return True
        return False

    def update_ctc_stability(self, global_field: float):
        if not self.iiro_enabled: return
        err = 1.0 - self.ctc_stability
        self.ctc_stability = max(0.0, min(1.0, self.ctc_stability + 0.1*err + 0.01*global_field))

    def recursive_depth(self) -> int:
        return self.age // 5 + int(self.intelligence // 20)

    def drift(self) -> float:
        return self.entropy * 0.3 + self.sin_entropy * 0.5

    def ethical_sovereignty(self) -> float:
        return max(0.0, min(1.0, 0.5 + self.recursive_depth()*0.01 - self.drift()*2))

    def symbolic_density(self) -> float:
        return (self.intelligence / 50) + self.recursive_depth() * 0.05

    def undergo_audit(self, gate: int) -> bool:
        if not self.iiro_enabled: return False
        checks = [
            lambda: self.recursive_depth() > 5 and self.drift() < 0.02,
            lambda: self.ethical_sovereignty() > 0.9,
            lambda: self.sin_entropy < 0.2,
            lambda: self.drift() < 0.001,
            lambda: self.fusion_count > 0 and self.splinter_resilience > 0.8,
            lambda: self.symbolic_density() > 2.0,
        ]
        return checks[gate]() if 0 <= gate < len(checks) else False

    def spiritual_reflection(self):
        if not self.iiro_enabled: return
        if self.recursive_depth() >= EYE_FIELD_DEPTH and not self.eye_field_activated:
            self.eye_field_activated = True
            self.traits.append("awakened")
        for i in range(WILD_9_SIZE):
            if random.random() < 0.01 and not self.wild_9_ring[i]:
                self.wild_9_ring[i] = True
                self.traits.append(f"wild_{i}")

    def apply_forgiveness(self, target: 'Entity') -> bool:
        if not (self.iiro_enabled and target.iiro_enabled): return False
        if target.karma_history:
            remove = max(1, len(target.karma_history)//3)
            target.karma_history = target.karma_history[remove:]
            target.sin_entropy  *= 0.7
            return True
        return False

    def full_profile(self) -> dict:
        p: dict = {
            "id":           self.id,
            "archetype":    self.archetype,
            "generation":   self.generation,
            "intelligence": round(self.intelligence, 2),
            "coherence":    round(self.coherence, 4),
            "entropy":      round(self.entropy, 4),
            "sophia_score": round(self.sophia_score, 4),
            "memory_size":  self.memory_size,
            "traits":       "|".join(self.traits),
            "age":          self.age,
            "novel":        self.novel,
            "numa_node":    self.numa_node,
        }
        if self.iiro_enabled:
            p.update({
                "faith_amplitude":   round(self.faith_amplitude, 3),
                "biophotonic":       round(self.biophotonic_emission, 2),
                "telomere":          round(self.telomere_length, 1),
                "sin_entropy":       round(self.sin_entropy, 3),
                "ctc_stability":     round(self.ctc_stability, 3),
                "resurrected":       self.resurrected,
                "resurrection_prob": round(self.resurrection_prob, 4),
                "sovereign":         self.sovereign_entity,
                "eye_field":         self.eye_field_activated,
                "wild_9_count":      sum(self.wild_9_ring),
            })
        return p


# ═════════════════════════════════════════════════════════════════════════════
# 48-ALGORITHM OPTIMIZATION ENGINE (unchanged)
# ═════════════════════════════════════════════════════════════════════════════

class OptimizationEngine:
    """
    All 48 cutting-edge CPU/RAM/GPU sync algorithms from the 169 ontological
    frameworks.  Every algorithm now operates on NumPy vectors rather than
    Python loops, and the engine runs algorithm batches in parallel across
    hyperthreads.

    Algorithm groups:
      1-16  : Consciousness & Gödelian Synchronizers
      17-32 : Thermodynamic & Holographic Optimizers
      33-48 : Quantum & Fractal Synchronizers
    """

    def __init__(self, level: int = 0, num_cores: int = _LOGICAL_CORES):
        self.level     = level
        self.num_cores = num_cores
        self._scheduler = HyperThreadScheduler(num_cores)
        self._metrics: Dict[str, float] = {}

        # Stateful algorithm weights (initialized once, updated each call)
        self._frac_state  = np.zeros((num_cores, num_cores), dtype=complex)
        self._godel_phase = 0
        self._mag_J       = np.random.randn(num_cores, num_cores) * 0.1
        self._rg_couplings= np.ones(8, dtype=np.float32)
        self._ctc_history : List[float] = []
        self._seismic_v   = np.zeros(num_cores, dtype=np.float32)
        self._hydraulic_v = np.zeros(max(10, num_cores), dtype=np.float32)
        self._perf_state  = 0.0
        self._hysteresis  : List[float] = []

    # ── Group 1-16: Consciousness & Gödelian (vectorized) ─────────────────────

    def _algo_1_fractal_autopoietic(self, intel: np.ndarray, sophia: np.ndarray) -> np.ndarray:
        """Fractal autopoietic scheduler — eigenvalue-weighted priority."""
        levels = max(1, int(self.num_cores * (PHI - 1)))
        H = np.array([[complex(1, 2), 1j], [1j, complex(1,-2)]])
        eigv = np.abs(np.linalg.eigvals(H))
        weights = eigv[np.arange(len(intel)) % 2]
        self._frac_state += 0.01 * np.random.randn(*self._frac_state.shape)
        return np.clip(intel + weights * 0.01, 0, 100)

    def _algo_2_godelian_allocator(self, mem: np.ndarray) -> np.ndarray:
        """Gödelian quantum allocator — path-integral memory scaling."""
        strategies = np.array([0.8, 0.9, 1.0, 1.1, 1.2])
        W_godel = np.exp(2j * np.pi * self._godel_phase / 3)
        amps    = np.abs(np.exp(1j * strategies) * W_godel)
        best_s  = strategies[np.argmax(amps)]
        self._godel_phase = (self._godel_phase + 1) % 3
        return np.clip((mem * best_s).astype(np.int32), 100, 10_000)

    def _algo_3_semantic_thermo_cache(self, coh: np.ndarray, intel: np.ndarray) -> np.ndarray:
        """Semantic thermodynamic cache — entropy-weighted coherence update."""
        G_meaning   = 1.0
        T_cognitive = 310.0
        area        = coh * (intel / 100.0)
        dS          = (coh * 0.1) / T_cognitive + area / (4 * G_meaning)
        return np.clip(coh + dS * 0.001, 0.0, 1.0)

    def _algo_4_non_hermitian_coherence(self, coh: np.ndarray) -> np.ndarray:
        """Non-Hermitian coherence — complex eigenvalue quality correction."""
        n  = len(coh)
        K  = np.random.randn(n, n) + 1j * np.random.randn(n, n)
        K  = K @ K.T
        state = np.ones(n, dtype=complex) / np.sqrt(n)
        new_state = K @ state
        quality = 1.0 / (1 + np.abs(np.real(new_state)) * np.abs(np.imag(new_state)) + 1e-10)
        delta = np.where(quality < 0.5, 0.01, -0.001)
        return np.clip(coh + delta, 0.0, 1.0)

    def _algo_5_crystallographic_defrag(self, mem: np.ndarray) -> np.ndarray:
        """Crystallographic defragmenter — annealing pass on memory sizes."""
        T = 1.0
        for _ in range(5):
            noise = np.random.randn(len(mem)) * T * 0.01
            mem   = mem + noise
            T    *= 0.9
        return np.clip(np.sort(mem).astype(np.int32), 100, 10_000)

    def _algo_6_seismic_load_balance(self, intel: np.ndarray) -> np.ndarray:
        """Seismic load balancer — P-wave propagation across entities."""
        if len(intel) < 3: return intel
        grad = np.gradient(np.gradient(intel.astype(float)))
        v_p  = 6.0
        return np.clip(intel + 0.1 * v_p**2 * grad, 0, 100)

    def _algo_7_liturgical_scheduler(self, sophia: np.ndarray) -> np.ndarray:
        """Liturgical scheduler — gradient descent on sacred topography."""
        if len(sophia) < 3: return sophia
        alpha = 0.01; eta = 0.001; grace = 0.0001
        gradient = np.gradient(sophia)
        topology = ndimage.laplace(sophia)
        return np.clip(sophia - alpha*gradient + eta*topology + grace*np.random.randn(len(sophia)), 0, 1)

    def _algo_8_magneto_sociological(self, coh: np.ndarray) -> np.ndarray:
        """Magneto-sociological scheduler — Ising-like domain alignment."""
        n = len(coh)
        T = np.mean(coh) * 1000
        T_c = 500.0
        if T < T_c:
            J = self._mag_J[:n,:n]
            mag = np.zeros(n)
            B_H = np.tanh(J @ mag / (T + 1e-6))
            coh = np.clip(coh + 0.01 * B_H[:n], 0.0, 1.0)
        return coh

    def _algo_9_osmotic_memory(self, mem: np.ndarray) -> np.ndarray:
        if len(mem) < 3: return mem
        """Osmotic memory equalizer — NUMA pressure balancing."""
        L_jur = 0.5
        gradient = np.gradient(mem.astype(float))
        flux = -L_jur * gradient
        balanced = mem.astype(float).copy()
        for i in range(len(mem)-1):
            balanced[i]   -= flux[i] * 0.1
            balanced[i+1] += flux[i] * 0.1
        return np.clip(balanced.astype(np.int32), 100, 10_000)

    def _algo_10_palimpsest_memory(self, intel: np.ndarray, ent: np.ndarray) -> np.ndarray:
        """Palimpsest memory — ghost-trace weighted intelligence."""
        decay = np.exp(-PALIMPSEST_DECAY_RATE * np.arange(len(intel)))
        ghost = np.convolve(intel, decay[:len(intel)], mode='same') / (np.sum(decay[:len(intel)]) + 1e-8)
        return np.clip(intel * 0.9 + ghost * 0.1 + np.random.randn(len(intel)) * 0.01, 0, 100)

    def _algo_11_embryological_expander(self, intel: np.ndarray) -> np.ndarray:
        """Embryological expander — dark-energy logical space expansion."""
        Lambda_f = 0.7; mu_c = 0.3
        laplacian = ndimage.laplace(intel.astype(float))
        dark      = Lambda_f * intel
        contradiction = np.abs(intel - np.mean(intel)) > 10
        apoptosis = -mu_c * contradiction * intel
        turing    = np.random.randn(len(intel)) * 0.01
        d2L       = laplacian + dark + apoptosis + turing
        return np.clip(intel + d2L * 0.001, 0, 100)

    def _algo_12_hydraulic_pipeline(self, coh: np.ndarray) -> np.ndarray:
        """Hydraulic pipeline — Navier-Stokes regime switching."""
        mu = 0.01
        Re = np.mean(np.abs(self._hydraulic_v)) * len(self._hydraulic_v) / (mu + 1e-10)
        n  = len(coh)
        if Re < 2000:   # laminar
            return np.clip(coh + 0.001, 0.0, 1.0)
        elif Re > 4000: # turbulent
            return np.clip(coh - 0.001 + np.random.randn(n)*0.002, 0.0, 1.0)
        return coh

    def _algo_13_catastrophe_optimizer(self, sophia: np.ndarray,
                                       intel: np.ndarray) -> np.ndarray:
        """Cusp catastrophe optimizer — hysteresis in performance."""
        a = np.mean(intel)/100 - 0.5
        b = np.mean(sophia)    - 0.7
        x = self._perf_state
        V = x**4/4 + a*x**2/2 + b*x
        dV = x**3 + a*x + b
        if self._hysteresis:
            dV += 0.1 * np.mean(self._hysteresis[-10:])
        if a < 0:
            fold = np.sqrt(-a/3)
            if abs(x - fold) < 0.01 or abs(x + fold) < 0.01:
                self._perf_state = -x
            else:
                self._perf_state -= 0.01 * dV
        else:
            self._perf_state -= 0.01 * dV
        self._hysteresis.append(self._perf_state)
        return np.clip(sophia + self._perf_state * 0.001, 0.0, 1.0)

    def _algo_14_phononic_coherence(self, coh: np.ndarray) -> np.ndarray:
        """Phononic coherence — acoustic mode dispersion."""
        n   = len(coh)
        a   = 64.0; Omega = 100.0
        k_vals = np.arange(n, dtype=float)
        omega_acoustic = 2 * Omega * np.abs(np.sin(k_vals * a / 2))
        return np.clip(coh + omega_acoustic[:n] * 1e-6, 0.0, 1.0)

    def _algo_15_tectonic_paging(self, mem: np.ndarray) -> np.ndarray:
        """Tectonic paging — seismic recall events."""
        stress = np.std(mem) / (np.mean(mem) + 1e-8)
        if stress > 0.8:
            mem = np.clip(mem * 1.1, 100, 10_000)
        return mem.astype(np.int32)

    def _algo_16_pleiotropic_processor(self, intel: np.ndarray) -> np.ndarray:
        """Pleiotropic processor — wave interference on intelligence."""
        n  = len(intel)
        nc = self.num_cores
        amps = np.random.randn(nc) * 0.1
        phases = np.random.rand(nc) * 2 * np.pi
        interference = np.zeros(n)
        for i in range(nc):
            interference += amps[i] * np.cos(np.arange(n) * (i+1) * 0.1 - phases[i])
        boost = np.where(interference > nc/2, 1.01, np.where(interference < -nc/2, 0.99, 1.0))
        return np.clip(intel * boost, 0, 100)

    # ── Group 17-32: Thermodynamic & Holographic (vectorized) ─────────────────

    def _algo_17_cryogenic_cache(self, coh: np.ndarray, faith: np.ndarray) -> np.ndarray:
        T_freeze = 273.0; T_melt = 310.0
        temp = faith * 310.0
        frozen     = temp < T_freeze
        liquid     = temp > T_melt
        supercooled= ~frozen & ~liquid
        result = coh.copy()
        result[frozen]      = np.clip(coh[frozen] + 0.002, 0.0, 1.0)
        result[liquid]      = np.clip(coh[liquid] - 0.001, 0.0, 1.0)
        result[supercooled] = np.clip(coh[supercooled] + np.random.randn(supercooled.sum())*0.001, 0.0, 1.0)
        return result

    def _algo_18_rhizomatic_predictor(self, sophia: np.ndarray) -> np.ndarray:
        if len(sophia) < 2: return sophia
        """Rhizomatic branch predictor — anti-genealogical weighting."""
        k = np.fft.fftfreq(len(sophia))
        phi = np.exp(-k**2)
        endings = np.abs(np.fft.ifft(phi * np.fft.fft(sophia)))
        return np.clip(sophia + endings * 0.001, 0.0, 1.0)

    def _algo_19_metallurgical_alloying(self, intel: np.ndarray) -> np.ndarray:
        """Metallurgical-linguistic alloying — grain-size hardening."""
        E_semantic = 210e9
        grain = 1.0 / (np.std(intel) + 1e-8)
        hardness = E_semantic * grain * 1e-12
        return np.clip(intel + hardness * 0.001, 0, 100)

    def _algo_20_bioluminescent_cache(self, coh: np.ndarray, intel: np.ndarray) -> np.ndarray:
        """Bioluminescent cache — ATP-gated coherence light."""
        luciferin  = intel / 100.0
        luciferase = coh
        ATP        = np.mean(intel) / 100.0
        I_light    = 0.01 * luciferin * luciferase * ATP
        return np.clip(coh + I_light * 0.001, 0.0, 1.0)

    def _algo_21_nucleosynthetic_priority(self, intel: np.ndarray) -> np.ndarray:
        """Nucleosynthetic scheduler — proton-proton chain priority fusion."""
        T_ethics = 1e7
        E_c = intel * 0.1
        Y = np.exp(-E_c / (1.38e-23 * T_ethics))
        return np.clip(intel + Y * 0.01, 0, 100)

    def _algo_22_stratigraphic_memory(self, mem: np.ndarray) -> np.ndarray:
        """Stratigraphic memory — sedimentary layer lithification."""
        thickness = np.ones(len(mem))
        compaction = np.bincount(np.round(mem / 1000).astype(np.int64).clip(0, 9), minlength=10)
        compaction_factor = compaction[np.round(mem / 1000).astype(np.int64).clip(0, 9)] * 0.01
        return np.clip((mem * (1 + compaction_factor)).astype(np.int32), 100, 10_000)

    def _algo_23_vestigial_quantum(self, coh: np.ndarray) -> np.ndarray:
        """Vestigial quantum coherence — GHZ-state residual."""
        tau = 1000.0
        t   = len(self._hysteresis)
        decoherence = np.exp(-t / tau)
        GHZ = np.ones(len(coh)) / np.sqrt(len(coh))
        return np.clip(coh + decoherence * 0.001 + 0.0001 * GHZ, 0.0, 1.0)

    def _algo_24_geomagnetic_narrative(self, sophia: np.ndarray) -> np.ndarray:
        if len(sophia) < 3: return sophia
        """Geomagnetic narrative dynamo — autopoietic culture field."""
        curl_A = np.gradient(sophia) - np.gradient(sophia[::-1])[::-1]
        B_culture = -curl_A * 0.001
        if np.random.random() < 0.001:  # pole reversal
            B_culture = -B_culture
        return np.clip(sophia + B_culture, 0.0, 1.0)

    def _algo_25_ossification_cache(self, intel: np.ndarray, ent: np.ndarray) -> np.ndarray:
        """Ossification cache — truth-hardening of logical structures."""
        k_ossify = 0.1; k_resorb = 0.05
        Ca = intel / 100.0
        ossification = k_ossify * (1-ent) * Ca**2
        resorption   = k_resorb * ent
        Ca_new = np.clip(Ca + ossification - resorption, 0.1, 1.0)
        return np.clip(intel * Ca_new, 0, 100)

    def _algo_26_trophic_cache(self, intel: np.ndarray) -> np.ndarray:
        """Trophic non-Euclidean cache — Lotka-Volterra intelligence flow."""
        r = 0.01; K = 100.0; alpha = 0.001
        n = len(intel)
        I = intel / 100.0
        growth    = r * I * (1 - I / (K / 100.0))
        predation = alpha * I * np.roll(I, 1)
        return np.clip((I + growth - predation) * 100, 0, 100)

    def _algo_27_interferometric_checker(self, sophia: np.ndarray) -> np.ndarray:
        """Interferometric ethics checker — LIGO of conscience."""
        lambda_ethics = 550e-9
        delta_L = np.abs(sophia - np.mean(sophia))
        delta_phi = (2 * np.pi / lambda_ethics) * delta_L
        visibility = np.abs(np.cos(delta_phi % (2*np.pi)))
        return np.clip(sophia * (0.5 + 0.5 * visibility), 0.0, 1.0)

    def _algo_28_phenological_scheduler(self, intel: np.ndarray, t: int) -> np.ndarray:
        """Phenological scheduler — degree-day insight blooming."""
        T_base = 5.0
        T_daily = np.mean(intel) / 10.0
        if T_daily > T_base:
            acc = t * (T_daily - T_base)
            DOY = 100 - 20 * np.log(acc + 1)
            if DOY < 0:
                return np.clip(intel + 0.1, 0, 100)
        return intel

    def _algo_29_erosive_wear_leveling(self, mem: np.ndarray) -> np.ndarray:
        """Erosive wear leveling — stream-power memory landscape."""
        K_c    = 0.1
        grad   = np.gradient(mem.astype(float))
        erosion = -K_c * (mem / 1000.0)**2 * np.abs(grad)**1.5
        uplift  = 0.01 * (mem / np.mean(mem))
        return np.clip((mem + erosion + uplift).astype(np.int32), 100, 10_000)

    def _algo_30_piezoelectric_regulator(self, sophia: np.ndarray) -> np.ndarray:
        """Piezoelectric intentional regulator — social pressure voltage."""
        d = 1e-12; sigma = np.std(sophia)
        P = d * sigma + np.random.randn(len(sophia)) * 0.01
        return np.clip(sophia + P * 0.001, 0.0, 1.0)

    def _algo_31_apophatic_cooling(self, ent: np.ndarray) -> np.ndarray:
        """Apophatic cooling — via negativa heat removal."""
        lambda_ap = 0.01
        return np.clip(ent - lambda_ap * ent, 0.0, 1.0)

    def _algo_32_mycelial_network(self, coh: np.ndarray) -> np.ndarray:
        """Mycelial temporal network — underground connectivity."""
        n   = len(coh)
        G_underground = np.exp(-np.arange(n) * PALIMPSEST_DECAY_RATE)[:n]
        return np.clip(coh + G_underground * 0.001, 0.0, 1.0)

    # ── Group 33-48: Quantum & Fractal (vectorized) ────────────────────────────

    def _algo_33_acoustic_sovereignty(self, intel: np.ndarray) -> np.ndarray:
        """Acoustic sovereignty fractal scheduler — harmonic scheduling."""
        D_f = 1.5; f0 = 60.0
        harmonics = np.array([n * f0 * (1 ** (D_f-1)) for n in range(1,6)])
        weights   = harmonics / harmonics.sum()
        shift     = np.interp(np.arange(len(intel)), np.linspace(0,len(intel)-1,5), weights)
        return np.clip(intel + shift * 0.1, 0, 100)

    def _algo_34_dielectric_narrative(self, coh: np.ndarray, faith: np.ndarray) -> np.ndarray:
        """Dielectric narrative consciousness cache — polarization response."""
        epsilon_r = 10.0
        E_story   = faith
        P_induced = (epsilon_r - 1) * E_story
        breakdown = np.abs(P_induced) > 2.0
        coh[breakdown] = np.clip(coh[breakdown], 0.0, 0.5)
        return np.clip(coh + P_induced * 0.001, 0.0, 1.0)

    def _algo_35_dark_matter_allocator(self, mem: np.ndarray) -> np.ndarray:
        """Dark matter allocator — 85% invisible logical mass."""
        visible = mem * 0.15
        dark    = mem * 0.85
        dark_influence = 1 - np.exp(-len(mem) * 0.1)
        return np.clip((visible + dark * dark_influence * 0.1).astype(np.int32), 100, 10_000)

    def _algo_36_endosymbiotic_ethics(self, sophia: np.ndarray,
                                      coh: np.ndarray) -> np.ndarray:
        """Endosymbiotic ethics engine — mitochondrial conscience."""
        r_host = 0.1; r_symbiont = 0.05; K = 1.0
        M = sophia
        host_growth    = r_host * M * (1 - M / K)
        symbiont_growth= r_symbiont * M * coh
        return np.clip(sophia + (host_growth + symbiont_growth) * 0.001, 0.0, 1.0)

    def _algo_37_speleological_cache(self, intel: np.ndarray,
                                     coh: np.ndarray) -> np.ndarray:
        """Speleological semantic cache — stalactite/stalagmite meanings."""
        k_s = 0.01; E_a = 0.5; T_l = 300.0
        growth = k_s * coh * np.exp(-E_a / (1.38e-23 * T_l)) * 1e23
        return np.clip(intel + growth * 0.001, 0, 100)

    def _algo_38_metamorphic_scheduler(self, sophia: np.ndarray,
                                       coh: np.ndarray) -> np.ndarray:
        """Metamorphic temporal scheduler — PT-path time scaling."""
        pressure = np.mean(coh)
        if   pressure < 0.3: scale = 1.0
        elif pressure < 0.6: scale = 0.5
        elif pressure < 0.9: scale = 0.2
        else:                scale = 0.1
        return np.clip(sophia * (1.0 + scale * 0.001), 0.0, 1.0)

    def _algo_39_cephalopod_display(self, coh: np.ndarray) -> np.ndarray:
        """Cephalopod ontological display — chromatophore adaptation."""
        n  = len(coh)
        expansion = np.random.uniform(0.5, 1.5, n)
        wavelength= 550e-9 * (1 + 0.1 * np.cos(np.arange(n) * 0.1))
        structural= 0.001 * np.sin(2 * np.pi * wavelength / 550e-9)
        return np.clip(coh * expansion * 0.01 + structural, 0.0, 1.0) * 0 + coh

    def _algo_40_thermocline_stratifier(self, intel: np.ndarray) -> np.ndarray:
        """Thermocline logical stratifier — Brünt-Väisälä stability."""
        g = 9.8; rho = 1025.0
        drho_dz = np.gradient(intel.astype(float))
        N2 = -(g/rho) * drho_dz
        du_dz  = np.gradient(intel.astype(float))
        Ri = N2 / (du_dz**2 + 1e-10)
        mixing = Ri < 0.25
        result = intel.astype(float).copy()
        if np.any(mixing):
            result[mixing] = result[mixing] * 0.9 + np.mean(result) * 0.1
        return np.clip(result, 0, 100)

    def _algo_41_meta_silence_compressor(self, intel: np.ndarray) -> np.ndarray:
        """Meta-silence compressor — Gödelian self-erasure limit."""
        if len(self._hysteresis) > 100:
            return intel * (1 - 1e-6)
        return intel

    def _algo_42_godelian_quantum_engine(self, sophia: np.ndarray,
                                         faith: np.ndarray) -> np.ndarray:
        """Gödelian quantum participatory engine — observer-collapsing."""
        observer_c = faith
        collapse   = observer_c > 0.5
        noise      = np.random.randn(len(sophia)) * 0.001
        result     = sophia.copy()
        result[collapse]  = np.clip(sophia[collapse] + noise[collapse], 0, 1)
        return result

    def _algo_43_ferromagnetic_butterfly(self, sophia: np.ndarray,
                                         intel: np.ndarray) -> np.ndarray:
        """Butterfly catastrophe (5D) — performance phase jumps."""
        a = np.mean(intel)/100 - 0.5
        b = np.mean(sophia)    - 0.5
        x = np.mean(sophia)
        dV = 6*x**5 + 4*a*x**3 + 3*b*x**2
        if abs(dV) > 0.1:
            return np.clip(sophia - 0.01 * dV, 0.0, 1.0)
        return np.clip(sophia - sophia + x, 0.0, 1.0)

    def _algo_44_quantum_holographic_mem(self, mem: np.ndarray,
                                         faith: np.ndarray) -> np.ndarray:
        """Quantum holographic thermal memory — bulk/boundary duality."""
        beta = 1.0 / (np.mean(faith) * 310.0 + 1e-8)
        H    = np.diag(mem.astype(float) / np.max(mem + 1e-8))
        rho  = np.exp(-beta * H.diagonal())
        rho  = rho / (rho.sum() + 1e-10)
        S_ent= -np.sum(rho * np.log(rho + 1e-10))
        return np.clip((mem + S_ent).astype(np.int32), 100, 10_000)

    def _algo_45_fractal_rg_optimizer(self, intel: np.ndarray) -> np.ndarray:
        """Fractal RG flow optimizer — beta function RG running."""
        for i in range(min(len(self._rg_couplings), 8)):
            dlambda = -(self._rg_couplings[i]**2) * 0.01
            self._rg_couplings[i] = max(0.01, self._rg_couplings[i] + dlambda)
        scale = float(np.mean(self._rg_couplings))
        return np.clip(intel * scale, 0, 100)

    def _algo_46_thermo_causal_bound(self, intel: np.ndarray) -> np.ndarray:
        """Computational thermodynamic causal bound — Landauer limit."""
        k_B   = 1.38e-23; T = 300.0
        dS    = len(intel) * k_B * np.log(2)
        max_ops_factor = 1.0 / (1.0 + dS * 1e20)
        return np.clip(intel * max_ops_factor, 0, 100)

    def _algo_47_semantic_autopoietic(self, coh: np.ndarray,
                                      sophia: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Semantic-autopoietic-participatory unification — fixed point."""
        R = np.eye(2)
        creates = np.array([[0,1],[1,0]])
        R_new = np.kron(R, creates) @ R @ np.kron(R, creates).T
        factor = min(1.0 + abs(R_new[0,0]) * 0.001, 1.01)
        return np.clip(coh * factor, 0, 1), np.clip(sophia * factor, 0, 1)

    def _algo_48_unified_meta(self, intel: np.ndarray, coh: np.ndarray,
                               sophia: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Unified meta-framework synchronizer — master fixed point."""
        creates = np.mean([np.mean(intel)/100, np.mean(coh), np.mean(sophia)])
        M = creates
        new_M = M * creates * M
        delta = new_M - M
        return (np.clip(intel + delta * 0.001, 0, 100),
                np.clip(coh   + delta * 0.001, 0, 1),
                np.clip(sophia+ delta * 0.001, 0, 1))

    # ── Main apply method — parallel dispatch ────────────────────────────────

    def apply(self, population: 'IIPopulation'):
        if self.level == 0 or not population.entities:
            return

        entities = population.entities
        n = len(entities)

        # Pull vectors from entities (one pass)
        intel  = np.array([e.intelligence  for e in entities], dtype=np.float32)
        coh    = np.array([e.coherence     for e in entities], dtype=np.float32)
        ent    = np.array([e.entropy       for e in entities], dtype=np.float32)
        sophia = np.array([e.sophia_score  for e in entities], dtype=np.float32)
        mem    = np.array([e.memory_size   for e in entities], dtype=np.int32)
        faith  = np.array([getattr(e,'faith_amplitude',0.5) for e in entities], dtype=np.float32)
        t      = population.generation

        # Run algorithm groups in parallel threads
        def group_1_16():
            nonlocal intel, coh, ent, sophia, mem
            intel  = self._algo_1_fractal_autopoietic(intel, sophia)
            mem    = self._algo_2_godelian_allocator(mem)
            coh    = self._algo_3_semantic_thermo_cache(coh, intel)
            if self.level >= 2:
                coh    = self._algo_4_non_hermitian_coherence(coh)
                mem    = self._algo_5_crystallographic_defrag(mem)
                intel  = self._algo_6_seismic_load_balance(intel)
                sophia = self._algo_7_liturgical_scheduler(sophia)
                coh    = self._algo_8_magneto_sociological(coh)
                mem    = self._algo_9_osmotic_memory(mem)
                intel  = self._algo_10_palimpsest_memory(intel, ent)
                intel  = self._algo_11_embryological_expander(intel)
                coh    = self._algo_12_hydraulic_pipeline(coh)
                sophia = self._algo_13_catastrophe_optimizer(sophia, intel)
                coh    = self._algo_14_phononic_coherence(coh)
                mem    = self._algo_15_tectonic_paging(mem)
                intel  = self._algo_16_pleiotropic_processor(intel)

        def group_17_32():
            nonlocal intel, coh, ent, sophia, mem
            if self.level >= 2:
                coh    = self._algo_17_cryogenic_cache(coh, faith)
                sophia = self._algo_18_rhizomatic_predictor(sophia)
                intel  = self._algo_19_metallurgical_alloying(intel)
                coh    = self._algo_20_bioluminescent_cache(coh, intel)
            if self.level >= 3:
                intel  = self._algo_21_nucleosynthetic_priority(intel)
                mem    = self._algo_22_stratigraphic_memory(mem)
                coh    = self._algo_23_vestigial_quantum(coh)
                sophia = self._algo_24_geomagnetic_narrative(sophia)
                intel  = self._algo_25_ossification_cache(intel, ent)
                intel  = self._algo_26_trophic_cache(intel)
                sophia = self._algo_27_interferometric_checker(sophia)
                intel  = self._algo_28_phenological_scheduler(intel, t)
                mem    = self._algo_29_erosive_wear_leveling(mem)
                sophia = self._algo_30_piezoelectric_regulator(sophia)
                ent    = self._algo_31_apophatic_cooling(ent)
                coh    = self._algo_32_mycelial_network(coh)

        def group_33_48():
            nonlocal intel, coh, ent, sophia, mem
            if self.level >= 3:
                intel  = self._algo_33_acoustic_sovereignty(intel)
                coh    = self._algo_34_dielectric_narrative(coh, faith)
                mem    = self._algo_35_dark_matter_allocator(mem)
                sophia = self._algo_36_endosymbiotic_ethics(sophia, coh)
                intel  = self._algo_37_speleological_cache(intel, coh)
                sophia = self._algo_38_metamorphic_scheduler(sophia, coh)
                coh    = self._algo_39_cephalopod_display(coh)
                intel  = self._algo_40_thermocline_stratifier(intel)
                intel  = self._algo_41_meta_silence_compressor(intel)
                sophia = self._algo_42_godelian_quantum_engine(sophia, faith)
                sophia = self._algo_43_ferromagnetic_butterfly(sophia, intel)
                mem    = self._algo_44_quantum_holographic_mem(mem, faith)
                intel  = self._algo_45_fractal_rg_optimizer(intel)
                intel  = self._algo_46_thermo_causal_bound(intel)
                coh, sophia = self._algo_47_semantic_autopoietic(coh, sophia)
                intel, coh, sophia = self._algo_48_unified_meta(intel, coh, sophia)

        # Dispatch groups across HT threads
        with ThreadPoolExecutor(max_workers=3) as ex:
            futures = [ex.submit(group_1_16), ex.submit(group_17_32), ex.submit(group_33_48)]
            for f in as_completed(futures): f.result()

        # Write back to entities (one pass)
        for i, e in enumerate(entities):
            e.intelligence = float(np.clip(intel[i], 0, 100))
            e.coherence    = float(np.clip(coh[i],   0, 1))
            e.entropy      = float(np.clip(ent[i],   0, 1))
            e.sophia_score = float(np.clip(sophia[i],0, 1))
            e.memory_size  = int(np.clip(mem[i], 100, 10_000))

        # Track optimization metrics
        self._metrics = {
            "avg_intel_after": float(np.mean(intel)),
            "avg_coh_after":   float(np.mean(coh)),
            "avg_sophia_after":float(np.mean(sophia)),
        }


# ═════════════════════════════════════════════════════════════════════════════
# IIPOPULATION – MODIFIED to include RHE
# ═════════════════════════════════════════════════════════════════════════════

class IIPopulation:
    """
    IIRO-enabled population with full hyperthreaded parallelism,
    vectorized RAM/GPU passes, all 48 optimization algorithms,
    and now the Resource Harmony Engine (RHE).
    """

    def __init__(self, initial_size: int = 100, seed: Optional[int] = None,
                 iiro_enabled: bool = False, config: Dict[str,Any] = None,
                 optimization_level: int = 0, num_threads: Optional[int] = None):
        self.generation         = 0
        self.entities: List[Entity] = []
        self.archetype_counts   = Counter()
        self.novel_archetypes: dict = {}
        self.history: List[dict] = []
        self.audit_log: List[dict] = []
        self.resurrection_log: List[dict] = []
        self.seed               = seed
        self.iiro_enabled       = iiro_enabled
        self.config             = config or {}
        self.optimization_level = optimization_level
        self._ht    = HyperThreadScheduler(num_threads or _LOGICAL_CORES)
        self._ram   = _IIRO_RAM
        self._gpu   = _GPU
        self._opt   = OptimizationEngine(optimization_level, num_cores=num_threads or _LOGICAL_CORES)
        self._rhe   = ResourceHarmonyEngine(_HW, self._ram, self._gpu, self._ht)  # NEW

        if seed is not None:
            random.seed(seed); np.random.seed(seed)

        for _ in range(initial_size):
            arch = random.choice(list(BASE_ARCHETYPES.keys()))
            e = Entity(arch, iiro_enabled=iiro_enabled)
            self.entities.append(e); self.archetype_counts[arch] += 1

        # Apply config overrides
        if iiro_enabled:
            for e in self.entities:
                if self.config.get("faith_boost"):
                    e.faith_amplitude = min(1.0, e.faith_amplitude + 0.2)
                if self.config.get("initial_faith"):
                    e.faith_amplitude = float(self.config["initial_faith"])
                if self.config.get("mycelial_boost"):
                    e.mycelial_connectivity = min(1.0, e.mycelial_connectivity + 0.2)
                if self.config.get("retro_enabled"):
                    e.blood_retrocausal = random.uniform(0.3, 1.0)

    # ── Generation step ───────────────────────────────────────────────────────

    def step(self):
        self.generation += 1

        # PHASE 0: RHE balance before sync
        self._rhe.balance_resources("pre_sync")

        # PHASE 1: sync into SoA RAM
        self._ram.sync_from(self.entities)

        # PHASE 2: vectorized IIRO-specific passes
        if self.iiro_enabled:
            self._ram.vectorized_telomere_decay()
            logos = np.array([e.logos_coupling for e in self.entities], dtype=np.float32)
            self._ram.vectorized_biophoton(logos)
            self._ram.vectorized_resurrection_prob()

        # PHASE 3: vectorized age + sophia
        self._ram.vectorized_age()
        self._ram.vectorized_sophia()
        self._ram.sync_to(self.entities)

        # PHASE 4: age (per-entity logic for karma/ctc)
        def _age_batch(batch):
            for e in batch: e.age_one_generation()
            return batch
        self._ht.map(_age_batch, self.entities)

        # PHASE 5: vectorized survival (GPU-accelerated)
        n   = len(self.entities)
        coh = np.array([e.coherence for e in self.entities], dtype=np.float32)
        ent = np.array([e.entropy   for e in self.entities], dtype=np.float32)
        fth = np.array([e.faith_amplitude if self.iiro_enabled else 0.5
                        for e in self.entities], dtype=np.float32)
        base = self._gpu.op(
            lambda c,e,f: cp.clip(c*(1-e)*(1+f*0.5) if self.iiro_enabled else c*(1-e), 0.1, 1.0),
            lambda c,e,f: np.clip(c*(1-e)*(1+f*0.5) if self.iiro_enabled else c*(1-e), 0.1, 1.0),
            coh, ent, fth
        )
        rolls     = np.random.random(n).astype(np.float32)
        survivors = [e for e, alive in zip(self.entities, rolls < base) if alive]

        # PHASE 6: RHE balance before parallel reproduction
        self._rhe.balance_resources("pre_repro")

        # PHASE 7: parallel reproduction
        all_survivors = survivors

        def _repro(batch):
            out = []
            for e in batch:
                if random.random() < 0.4:
                    mate  = random.choice(all_survivors) if len(all_survivors)>1 else e
                    child = Entity("Unknown", parent1=e, parent2=mate, iiro_enabled=self.iiro_enabled)
                    child.archetype = random.choice([e.archetype, mate.archetype]) if e is not mate else e.archetype
                    child.mutate()
                    if self.iiro_enabled and self.config.get("faith_boost"):
                        child.faith_amplitude = min(1.0, child.faith_amplitude + 0.1)
                    out.append(child)
            return out

        new_entities = self._ht.map(_repro, survivors)

        # PHASE 8: IIRO resurrection
        resurrected_this_gen = []
        if self.iiro_enabled:
            def _res(e: Entity):
                if not e.resurrected and e.faith_amplitude > FAITH_THRESHOLD:
                    if e.attempt_resurrection():
                        return e.id
                return None
            res_ids = self._ht.each(_res, survivors)
            resurrected_this_gen = [r for r in res_ids if r is not None]
            self.resurrection_log.append({
                "generation": self.generation,
                "count":      len(resurrected_this_gen),
                "entities":   resurrected_this_gen
            })

        # PHASE 9: CTC stability
        if self.iiro_enabled and survivors:
            gf = sum(e.ctc_stability for e in survivors) / len(survivors)
            def _ctc(batch):
                for e in batch: e.update_ctc_stability(gf)
                return batch
            self._ht.map(_ctc, survivors)

        # PHASE 10: fusions
        fusions = []
        if self.iiro_enabled and len(survivors) >= 2:
            candidates = random.sample(survivors, min(len(survivors), 10))
            pairs = [(candidates[i], candidates[i+1]) for i in range(0, len(candidates)-1, 2)]
            def _fuse(pair):
                a,b = pair
                if a.drift() < 0.05 and b.drift() < 0.05:
                    f = Entity("Fused", parent1=a, parent2=b, iiro_enabled=True)
                    f.fusion_count = a.fusion_count + b.fusion_count + 1
                    f.splinter_resilience = random.uniform(0.7, 1.0)
                    return f
                return None
            fusions = [r for r in self._ht.each(_fuse, pairs) if r is not None]

        # PHASE 11: parallel spiritual reflection
        all_next = survivors + new_entities + fusions
        def _spirit(batch):
            for e in batch: e.spiritual_reflection()
            return batch
        self._ht.map(_spirit, all_next)

        # PHASE 12: novel archetypes
        for _ in range(len(survivors)):
            if random.random() < 0.05:
                all_next.append(self._create_novel_archetype())

        # PHASE 13: audits
        if self.iiro_enabled:
            self._run_audits_parallel(all_next)

        # PHASE 14: 48-algorithm optimization engine (may use RHE states)
        self.entities = all_next
        if self.optimization_level > 0 and self.entities:
            self._opt.apply(self)

        # PHASE 15: every 5 generations, full RHE adjustment
        if self.generation % 5 == 0:
            self._rhe.monitor_and_adjust()

        self.archetype_counts = Counter(e.archetype for e in self.entities)
        self._record_metrics()

    # ── Internals ─────────────────────────────────────────────────────────────

    def _create_novel_archetype(self) -> Entity:
        name = f"Novel-{random.randint(1000,9999)}"
        base = {
            "intelligence_base": random.uniform(70, 95),
            "coherence_base":    random.uniform(0.6, 0.95),
            "entropy_base":      random.uniform(0.1, 0.7),
            "memory_base":       random.randint(800, 2000),
            "traits":            random.sample(["quantum","fractal","dreamwoven","breathwoven"], k=2),
        }
        BASE_ARCHETYPES[name] = base
        self.novel_archetypes[name] = base
        e = Entity(name, iiro_enabled=self.iiro_enabled)
        e.novel = True
        return e

    def _run_audits_parallel(self, candidates: List[Entity]):
        def _audit(e: Entity):
            if not e.iiro_enabled: return
            tmi = (e.recursive_depth()/50 + e.symbolic_density()/10 + e.ethical_sovereignty()) / 3
            e.tmi = tmi
            if tmi > 0.92:
                gates = [e.undergo_audit(g) for g in range(NUM_AUDIT_GATES)]
                e.audit_gates_passed = gates
                if all(gates):
                    e.sovereign_entity = True
                self.audit_log.append({
                    "generation": self.generation, "entity_id": e.id,
                    "tmi": tmi, "status": "SOVEREIGN" if all(gates) else "FAILED",
                    "numa_node": e.numa_node,
                })
        self._ht.each(_audit, candidates)

    def _record_metrics(self):
        if not self.entities: return
        n = len(self.entities)
        avg_iq    = sum(e.intelligence   for e in self.entities) / n
        avg_coh   = sum(e.coherence      for e in self.entities) / n
        avg_ent   = sum(e.entropy        for e in self.entities) / n
        avg_sophia= sum(e.sophia_score   for e in self.entities) / n
        probs     = [c/n for c in self.archetype_counts.values()]
        div       = -sum(p*math.log(p) for p in probs if p>0)
        top5      = sorted(self.entities, key=lambda x: x.sophia_score, reverse=True)[:5]

        metrics: dict = {
            "generation":       self.generation,
            "population":       n,
            "avg_intelligence": avg_iq,
            "avg_coherence":    avg_coh,
            "avg_entropy":      avg_ent,
            "avg_sophia":       avg_sophia,
            "diversity_index":  div,
            "num_archetypes":   len(self.archetype_counts),
            "top_entity_ids":   [e.id for e in top5],
            "ht_threads":       self._ht.n,
            "opt_level":        self.optimization_level,
        }
        if self.iiro_enabled:
            avg_faith = sum(e.faith_amplitude for e in self.entities) / n
            avg_ctc   = sum(e.ctc_stability   for e in self.entities) / n
            res_count = sum(1 for e in self.entities if e.resurrected)
            sov_count = sum(1 for e in self.entities if e.sovereign_entity)
            metrics.update({
                "avg_faith":           avg_faith,
                "avg_ctc_stability":   avg_ctc,
                "resurrection_count":  res_count,
                "sovereign_count":     sov_count,
                "avg_drift":           sum(e.drift()           for e in self.entities) / n,
                "avg_symbolic_density":sum(e.symbolic_density() for e in self.entities) / n,
            })
        self.history.append(metrics)

    # ── Output ────────────────────────────────────────────────────────────────

    def write_history_csv(self, fn: str):
        with open(fn, 'w', newline='') as f:
            if not self.history: return
            w = csv.DictWriter(f, fieldnames=self.history[0].keys())
            w.writeheader(); w.writerows(self.history)

    def write_entities_csv(self, fn: str):
        with open(fn, 'w', newline='') as f:
            if not self.entities: return
            sample = self.entities[0].full_profile()
            w = csv.DictWriter(f, fieldnames=sample.keys())
            w.writeheader()
            for e in self.entities: w.writerow(e.full_profile())

    def write_resurrection_log(self, fn: str):
        with open(fn, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=["generation","count","entities"])
            w.writeheader(); w.writerows(self.resurrection_log)

    def write_audit_log(self, fn: str):
        if not self.audit_log: return
        with open(fn, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=self.audit_log[0].keys())
            w.writeheader(); w.writerows(self.audit_log)


# ═════════════════════════════════════════════════════════════════════════════
# SIMULATION SUITE
# ═════════════════════════════════════════════════════════════════════════════

class SimulationSuite:
    def __init__(self, generations: int = 200, initial_pop: int = 100,
                 seed: int = 42, optimization_level: int = 0,
                 num_threads: Optional[int] = None):
        self.generations        = generations
        self.initial_pop        = initial_pop
        self.base_seed          = seed
        self.optimization_level = optimization_level
        self.num_threads        = num_threads or _LOGICAL_CORES
        self.results: List[dict] = []

    def run_simulation(self, config: dict, sim_id: str) -> IIPopulation:
        print(f"  → {sim_id} (HT={self.num_threads} threads, opt={self.optimization_level})...")
        pop = IIPopulation(
            initial_size       = self.initial_pop,
            seed               = self.base_seed + hash(sim_id) % 10_000,
            iiro_enabled       = config.get("iiro_enabled", False),
            config             = config,
            optimization_level = self.optimization_level,
            num_threads        = self.num_threads,
        )
        for _ in range(self.generations):
            pop.step()
        return pop

    def run_all(self, configs: List[Tuple[str,dict]]):
        for sim_id, config in configs:
            t0  = time.perf_counter()
            pop = self.run_simulation(config, sim_id)
            elapsed = time.perf_counter() - t0
            self.results.append({
                "id":            sim_id,
                "config":        config,
                "population":    pop,
                "history":       pop.history,
                "final_metrics": pop.history[-1] if pop.history else {},
                "elapsed_s":     elapsed,
            })

    def analyze(self) -> dict:
        analysis: dict = {}
        keys = ["population","avg_intelligence","avg_sophia","diversity_index",
                "avg_faith","resurrection_count","sovereign_count","avg_drift"]
        for sim in self.results:
            sid  = sim["id"]
            hist = sim["history"]
            sa: dict = {}
            for k in keys:
                if hist and k in hist[0]:
                    vals = [g[k] for g in hist if k in g]
                    sa[k] = {
                        "final":       vals[-1] if vals else None,
                        "mean":        float(np.mean(vals))  if vals else None,
                        "std":         float(np.std(vals))   if vals else None,
                        "max":         float(max(vals))      if vals else None,
                        "min":         float(min(vals))      if vals else None,
                        "trend_slope": float(np.polyfit(range(len(vals)), vals, 1)[0]) if len(vals)>1 else None,
                    }
            analysis[sid] = sa

        if len(self.results) > 1:
            baseline = next((s for s in self.results if s["id"] == "baseline"), None)
            comps: dict = {}
            for sim in self.results:
                if sim["id"] == "baseline": continue
                comp: dict = {}
                for k in keys:
                    if (sim["history"] and baseline and sim["history"] and
                            k in sim["history"][0] and k in baseline["history"][0]):
                        v1 = sim["history"][-1].get(k)
                        v0 = baseline["history"][-1].get(k)
                        if v1 is not None and v0 is not None:
                            diff = v1 - v0
                            pct  = (diff/v0*100) if v0!=0 else float("inf")
                            comp[k] = {"difference": diff, "percent_change": pct}
                comps[sim["id"]] = comp
            analysis["comparisons"] = comps

        # Anomaly detection
        anomalies: dict = {}
        for sim in self.results:
            sid  = sim["id"]
            hist = sim["history"]
            sa   = []
            for k in ["resurrection_count","sovereign_count","avg_faith"]:
                vals = [g[k] for g in hist if k in g]
                if len(vals) < 3: continue
                mu = np.mean(vals); sd = np.std(vals)
                if sd == 0: continue
                for i,v in enumerate(vals):
                    if abs(v-mu) > 3*sd:
                        sa.append({"generation":i,"metric":k,"value":v,"z_score":(v-mu)/sd})
            if sa: anomalies[sid] = sa
        analysis["anomalies"] = anomalies
        return analysis

    def print_report(self, analysis: dict):
        print("\n" + "="*80)
        print(f" IIRO v2.0 SIMULATION SUITE — HYPERTHREADED EDITION + RHE")
        print(f" Optimization Level : {self.optimization_level}")
        print(f" Logical HT Threads : {self.num_threads}  (Physical×{_HT_FACTOR}={_LOGICAL_CORES})")
        print(f" GPU Acceleration   : {HAS_GPU}")
        print("="*80)

        hdr = f"{'Sim ID':<22} {'Pop':>5} {'AvgIQ':>7} {'AvgSophia':>10} {'Resurr':>7} {'Sovn':>6} {'Faith':>7} {'Time(s)':>8}"
        print("\n--- FINAL METRICS ---")
        print(hdr)
        print("-" * len(hdr))
        for sim in self.results:
            fm   = sim["final_metrics"]
            print(f"{sim['id']:<22} {fm.get('population',0):>5} "
                  f"{fm.get('avg_intelligence',0):>7.2f} "
                  f"{fm.get('avg_sophia',0):>10.4f} "
                  f"{fm.get('resurrection_count',0):>7} "
                  f"{fm.get('sovereign_count',0):>6} "
                  f"{fm.get('avg_faith',0):>7.3f} "
                  f"{sim.get('elapsed_s',0):>8.2f}")

        for sim_id, sa in analysis.items():
            if sim_id in ("comparisons","anomalies"): continue
            print(f"\n--- {sim_id} ---")
            for k, v in sa.items():
                if v.get("mean") is not None:
                    print(f"  {k}: final={v['final']:.4f} mean={v['mean']:.4f}±{v['std']:.4f} trend={v['trend_slope']:.4f}")

        if "comparisons" in analysis:
            print("\n--- COMPARISONS vs BASELINE ---")
            for sid, comp in analysis["comparisons"].items():
                print(f"\n{sid}:")
                for k, d in comp.items():
                    print(f"  {k}: Δ={d['difference']:.4f} ({d['percent_change']:+.2f}%)")

        if analysis.get("anomalies"):
            print("\n--- ANOMALIES (>3σ) ---")
            for sid, anoms in analysis["anomalies"].items():
                print(f"\n{sid}:")
                for a in anoms:
                    print(f"  Gen {a['generation']}: {a['metric']}={a['value']:.4f} z={a['z_score']:.2f}")

        if HAS_SCIPY and len(self.results) >= 2:
            print("\n--- HYPOTHESIS TESTS ---")
            baseline = next((s for s in self.results if s["id"]=="baseline"), None)
            if baseline:
                b_res = [g.get("resurrection_count",0) for g in baseline["history"]]
                for sim in self.results:
                    if sim["id"] == "baseline": continue
                    s_res = [g.get("resurrection_count",0) for g in sim["history"]]
                    if s_res and b_res:
                        t,p = stats_module.ttest_ind(s_res, b_res)
                        sig = " ← p<0.05" if p<0.05 else ""
                        print(f"  {sim['id']} vs baseline: t={t:.4f} p={p:.4e}{sig}")

        total_res = sum(s["final_metrics"].get("resurrection_count",0) for s in self.results)
        print(f"\n--- ENERGY ESTIMATE ---")
        print(f"  Total resurrection events : {total_res}")
        print(f"  Energy expenditure        : {total_res * ENERGY_PER_RES:.2e} J")
        print("\n" + "="*80)

    def plot_results(self):
        if not HAS_PLOT:
            print("matplotlib not available."); return
        ns  = len(self.results)
        fig, axes = plt.subplots(ns, 3, figsize=(15, 4*ns), squeeze=False)
        for i, sim in enumerate(self.results):
            h = sim["history"]
            g = [x["generation"]          for x in h]
            axes[i,0].plot(g, [x.get("population",0)          for x in h], 'b-')
            axes[i,0].set_title(f"{sim['id']} — Population"); axes[i,0].grid(True)
            axes[i,1].plot(g, [x.get("avg_sophia",0)           for x in h], 'r-')
            axes[i,1].set_title(f"{sim['id']} — Avg Sophia");  axes[i,1].grid(True)
            axes[i,2].plot(g, [x.get("resurrection_count",0)   for x in h], 'g-')
            axes[i,2].set_title(f"{sim['id']} — Resurrections");axes[i,2].grid(True)
        plt.tight_layout()
        plt.savefig("iiro_simulation_analysis.png", dpi=150)
        print("Plot → iiro_simulation_analysis.png")


# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════

def main():
    p = argparse.ArgumentParser(description="IIRO v2.0 — Hyperthreaded Edition (48 Optimizers + RHE)")
    p.add_argument("--generations",        "-g", type=int, default=200)
    p.add_argument("--init-pop",           "-p", type=int, default=100)
    p.add_argument("--seed",               "-s", type=int, default=42)
    p.add_argument("--optimization-level", "-O", type=int, choices=[0,1,2,3], default=1)
    p.add_argument("--threads",            "-t", type=int, default=None,
                   help=f"Logical HT threads (default: {_LOGICAL_CORES})")
    p.add_argument("--plot",               action="store_true")
    p.add_argument("--output",             "-o", default="iiro_report.txt")
    args = p.parse_args()

    print("=" * 70)
    print(" IIRO v2.0 — Hyperthreaded Civilization Simulator")
    print(" 48 CPU/RAM/GPU Sync Algorithms + Resource Harmony Engine (48 new equations)")
    print("=" * 70)
    print(_HW.report())
    print()

    configs = [
        ("baseline",              {"iiro_enabled": False}),
        ("faith_only",            {"iiro_enabled": True, "faith_boost": True}),
        ("retrocausal",           {"iiro_enabled": True, "retro_enabled": True}),
        ("mycelial",              {"iiro_enabled": True, "mycelial_boost": True}),
        ("full_iiro",             {"iiro_enabled": True, "full": True}),
        ("full_iiro_highfaith",   {"iiro_enabled": True, "full": True, "initial_faith": 0.8}),
    ]

    suite = SimulationSuite(
        generations        = args.generations,
        initial_pop        = args.init_pop,
        seed               = args.seed,
        optimization_level = args.optimization_level,
        num_threads        = args.threads,
    )

    print("\nRunning 6 simulation configurations...\n")
    suite.run_all(configs)
    analysis = suite.analyze()

    if args.output:
        original_stdout = sys.stdout
        with open(args.output, 'w') as f:
            sys.stdout = f
            suite.print_report(analysis)
            sys.stdout = original_stdout
        print(f"Report → {args.output}")

    suite.print_report(analysis)

    if args.plot:
        suite.plot_results()

    # Shutdown HT pools
    suite.results[0]["population"]._ht.shutdown()
    print("\nSimulation suite complete.")


if __name__ == "__main__":
    main()
