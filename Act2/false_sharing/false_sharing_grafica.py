import subprocess
import matplotlib.pyplot as plt
import os

# Ruta al ejecutable (en el mismo directorio que este script)
EXEC_PATH = os.path.join(os.path.dirname(__file__), 'false_sharing')

# Detectar el número de núcleos
try:
    max_cores = int(subprocess.check_output(['nproc']).decode().strip())
except Exception as e:
    print(f"Error detectando núcleos: {e}")
    max_cores = 4  # valor por defecto


ks = list(range(1, max_cores + 1))
compact_vals = []
padded_vals = []
private_vals = []

import re

for k in ks:
    try:
        output = subprocess.check_output([EXEC_PATH, str(k)])
        lines = output.decode().strip().split('\n')
        tiempo_compact = float('nan')
        tiempo_padded = float('nan')
        tiempo_private = float('nan')
        for line in lines:
            if 'compact' in line:
                match = re.search(r'compact\s+([\d\.eE+-]+)', line)
                if match:
                    tiempo_compact = float(match.group(1))
            if 'padded' in line:
                match = re.search(r'padded\s+([\d\.eE+-]+)', line)
                if match:
                    tiempo_padded = float(match.group(1))
            if 'private' in line:
                match = re.search(r'private\s+([\d\.eE+-]+)', line)
                if match:
                    tiempo_private = float(match.group(1))
        compact_vals.append(tiempo_compact)
        padded_vals.append(tiempo_padded)
        private_vals.append(tiempo_private)
        print(f"k={k}: compact={tiempo_compact}, padded={tiempo_padded}, private={tiempo_private}")
    except Exception as e:
        print(f"Error ejecutando k={k}: {e}")
        compact_vals.append(float('nan'))
        padded_vals.append(float('nan'))
        private_vals.append(float('nan'))

plt.figure(figsize=(8,5))
plt.plot(ks, compact_vals, marker='o', label='compact', color='blue')
plt.plot(ks, padded_vals, marker='s', label='padded', color='red')
plt.plot(ks, private_vals, marker='^', label='private', color='green')
plt.xlabel('k (núcleos)')
plt.ylabel('Tiempo (ms)')
plt.title('Resultados de false_sharing')
plt.legend()
plt.grid(True)
plt.savefig('false_sharing_resultados.png')
plt.show()
