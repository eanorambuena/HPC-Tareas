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
valores = []


# Extraer el tiempo de la variante compact de la salida
import re

for k in ks:
    try:
        output = subprocess.check_output([EXEC_PATH, str(k)])
        lines = output.decode().strip().split('\n')
        # Buscar la línea que contiene 'compact'
        tiempo = float('nan')
        for line in lines:
            if 'compact' in line:
                match = re.search(r'compact\s+([\d\.eE+-]+)', line)
                if match:
                    tiempo = float(match.group(1))
                    break
        valores.append(tiempo)
        print(f"k={k}: {tiempo}")
    except Exception as e:
        print(f"Error ejecutando k={k}: {e}")
        valores.append(float('nan'))

plt.figure(figsize=(8,5))
plt.plot(ks, valores, marker='o')
plt.xlabel('k (núcleos)')
plt.ylabel('Valor de salida')
plt.title('Resultados de false_sharing')
plt.grid(True)
plt.savefig('false_sharing_resultados.png')
plt.show()
