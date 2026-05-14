import sys
import time
import numpy as np
from mpi4py import MPI


def mpi_dot(x_local, y_local, comm):
    # Implementar usando operaciones colectivas
    pass


def mpi_matvec(A_local, x_local, comm):
    # Implementar usando operaciones colectivas
    pass


def cg_parallel(A_local, b_local, comm, tol=1e-6, max_iter=1000):
    x = np.zeros_like(b_local)
    r = b_local - mpi_matvec(A_local, x, comm)
    p = r.copy()
    rho = mpi_dot(r, r, comm)
    for k in range(max_iter):
        if np.sqrt(rho) < tol:
            break
        Ap      = mpi_matvec(A_local, p, comm)
        alpha   = rho / mpi_dot(p, Ap, comm)
        x       = x + alpha * p
        r       = r - alpha * Ap
        rho_new = mpi_dot(r, r, comm)
        p       = r + (rho_new / rho) * p
        rho     = rho_new
    return x, k + 1


if __name__ == "__main__":
    n = int(sys.argv[1])

    # Inicializar MPI: obtener comm, rank y size
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Asignar filas a cada proceso
    # El proceso rank maneja las filas [row_start, row_end) de la matriz A
    rows_per_proc = n // size
    remainder = n % size
    row_start = rank * rows_per_proc + min(rank, remainder)
    row_end = row_start + rows_per_proc + (1 if rank < remainder else 0)

    # Cada proceso genera solo sus filas de A
    i_idx = np.arange(row_start, row_end)[:, None]
    j_idx = np.arange(n)[None, :]
    A_local = 1.0 / (1 + np.abs(i_idx - j_idx))
    A_local[np.arange(row_end - row_start), np.arange(row_start, row_end)] += np.log(n)
    b_local = A_local @ np.ones(n)

    comm.Barrier()
    t0 = time.perf_counter()
    x_local, iters = cg_parallel(A_local, b_local, comm)
    comm.Barrier()
    elapsed = time.perf_counter() - t0

    # El proceso 0 reune x_local de todos los procesos y verifica que convergio a 1
    # Implementar usando operaciones colectivas
    if rank == 0:
        print(f"n={n}, p={size}, iteraciones={iters}, tiempo={elapsed:.4f}")
