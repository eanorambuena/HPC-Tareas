"""
kmeans.py — K-means serial para distintos k.

Uso:
    python kmeans.py
"""

import time
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=100_000, centers=16, cluster_std=1.5, random_state=42)

K_VALUES = list(range(1, 17))

t0 = time.perf_counter()
results = []
for k in K_VALUES:
    print(f"  k={k} iniciando...", flush=True)
    km = KMeans(n_clusters=k, n_init=10, random_state=0)
    km.fit(X)
    results.append((k, km.inertia_))
    print(f"  k={k} listo", flush=True)
t_total = time.perf_counter() - t0

print(f"Tiempo total: {t_total:.2f} s")
print()
print(f"{'k':>3} | {'inertia':>12}")
print("-" * 18)
for k, inertia in results:
    print(f"{k:>3} | {inertia:>12.1f}")
