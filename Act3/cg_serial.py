import sys
import time
import numpy as np


def cg_serial(A, b, tol=1e-6, max_iter=1000):
    x = np.zeros_like(b)
    r = b - A @ x
    p = r.copy()
    rho = np.dot(r, r)
    for k in range(max_iter):
        if np.sqrt(rho) < tol:
            break
        Ap      = A @ p
        alpha   = rho / np.dot(p, Ap)
        x       = x + alpha * p
        r       = r - alpha * Ap
        rho_new = np.dot(r, r)
        p       = r + (rho_new / rho) * p
        rho     = rho_new
    return x, k + 1


if __name__ == "__main__":
    n = int(sys.argv[1])

    # Generar matriz simetrica definida positiva con solucion exacta = vector de unos
    i_idx = np.arange(n)[:, None]
    j_idx = np.arange(n)[None, :]
    A = 1.0 / (1 + np.abs(i_idx - j_idx))
    A += np.log(n) * np.eye(n)
    b = A @ np.ones(n)

    t0 = time.perf_counter()
    x, iters = cg_serial(A, b)
    elapsed = time.perf_counter() - t0

    # Verificar que la solucion convergio a 1
    error = np.linalg.norm(x - np.ones(n))
    print(f"n={n}, iteraciones={iters}, error={error:.2e}, tiempo={elapsed:.4f}")
