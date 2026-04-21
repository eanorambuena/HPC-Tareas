"""
kmeans_demo0.py — K-means para distintos k, sin threadpool limits.

Uso:
    python kmeans_demo0.py [N_WORKERS]
"""

import sys, time, pprint
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from multiprocessing import Pool
from threadpoolctl import threadpool_info

X, _ = make_blobs(n_samples=100_000, centers=16, cluster_std=1.5, random_state=42)

K_VALUES = list(range(1, 17))

def run_kmeans(k):
    print(f"  k={k} iniciando...", flush=True)
    km = KMeans(n_clusters=k, n_init=10, random_state=0)
    km.fit(X)
    print(f"  k={k} listo", flush=True)
    return k, km.inertia_

pprint.pprint(threadpool_info())

if __name__ == '__main__':
    n_workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    t0 = time.perf_counter()
    with Pool(processes=n_workers) as pool:
        results_parallel = pool.map(run_kmeans, K_VALUES)
    t_parallel = time.perf_counter() - t0

    print(f"Paralelo: {t_parallel:.2f} s  ({n_workers} workers)")
    print()
    print(f"{'k':>3} | {'inertia':>12}")
    print("-" * 18)
    for k, inertia in sorted(results_parallel):
        print(f"{k:>3} | {inertia:>12.1f}")
