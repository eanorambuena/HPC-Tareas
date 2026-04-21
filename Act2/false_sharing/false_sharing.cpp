#include <iostream>
#include <limits>
#include <cstdlib>
#include <omp.h>

static const long ITERS   = 100'000'000;  // 100M incrementos por thread
static const int  REPS    = 3;
static const int  MAX_THR = 16;

// Una cache line mide 64 bytes en x86-64.
// sizeof(long) == 8 bytes, por lo tanto 64/8 = 8 longs por cache line.
static const int LONGS_PER_LINE = 64 / sizeof(long);  // == 8

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Uso: " << argv[0] << " <num_threads>\n";
        return 1;
    }
    int nt = std::atoi(argv[1]);
    if (nt < 1 || nt > MAX_THR) {
        std::cerr << "num_threads debe estar entre 1 y " << MAX_THR << "\n";
        return 1;
    }

    // compact: los MAX_THR contadores quedan contiguos en memoria.
    // Con 8 threads, los 8 longs (8*8 = 64 bytes) comparten una cache line.
    volatile long compact[MAX_THR] = {};

    // padded: cada fila ocupa exactamente una cache line (64 bytes).
    // alignas(64) garantiza que padded[0] empiece en un borde de cache line;
    // como cada fila mide 64 bytes, padded[tid] siempre está en su propia línea.
    // Solo usamos la primera columna ([tid][0]) como contador.
    alignas(64) volatile long padded[MAX_THR][LONGS_PER_LINE] = {};

    // private: cada thread acumula en una variable local (stack) y copia al final.
    volatile long priv[MAX_THR] = {};

    // compact: primeras nt entradas contiguas en memoria
    {
        double best = std::numeric_limits<double>::max();
        for (int r = 0; r < REPS; r++) {
            for (int i = 0; i < nt; i++) compact[i] = 0;
            double t0 = omp_get_wtime();

            #pragma omp parallel num_threads(nt)
            {
                int tid = omp_get_thread_num();
                for (long i = 0; i < ITERS; i++)
                    compact[tid]++;
            }

            double elapsed = omp_get_wtime() - t0;
            if (elapsed < best) best = elapsed;
        }
        std::cout << "threads=" << nt << "  compact  " << best * 1000.0 << " ms\n";
    }

    // padded: cada thread escribe en su propia cache line
    {
        double best = std::numeric_limits<double>::max();
        for (int r = 0; r < REPS; r++) {
            for (int i = 0; i < nt; i++) padded[i][0] = 0;
            double t0 = omp_get_wtime();

            #pragma omp parallel num_threads(nt)
            {
                int tid = omp_get_thread_num();
                for (long i = 0; i < ITERS; i++)
                    padded[tid][0]++;
            }

            double elapsed = omp_get_wtime() - t0;
            if (elapsed < best) best = elapsed;
        }
        std::cout << "threads=" << nt << "  padded   " << best * 1000.0 << " ms\n";
    }

    // private: variable local por thread, copia al arreglo compartido al final
    {
        double best = std::numeric_limits<double>::max();
        for (int r = 0; r < REPS; r++) {
            for (int i = 0; i < nt; i++) priv[i] = 0;
            double t0 = omp_get_wtime();

            #pragma omp parallel num_threads(nt)
            {
                int tid = omp_get_thread_num();
                volatile long local = 0;
                for (long i = 0; i < ITERS; i++)
                    local++;
                priv[tid] = local;
            }

            double elapsed = omp_get_wtime() - t0;
            if (elapsed < best) best = elapsed;
        }
        std::cout << "threads=" << nt << "  private  " << best * 1000.0 << " ms\n";
    }

    return 0;
}
