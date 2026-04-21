## Grafique los resultados de tiempo versus número de threads para las tres variantes.
<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/0326f41e-2205-4051-bb2e-44b7f317db25" />

> **Nota:** Solo se muestran resultados para hasta 2 threads porque el entorno de Codespaces utilizado para esta actividad solo dispone de 2 núcleos de CPU. Si se ejecuta en una máquina con más núcleos, se podrán observar resultados para más valores de threads.

## ¿Qué diferencia estructuralmente a compact y padded? ¿Cuántos contadores de cada tipo caben en una línea de caché?
La diferencia entre compact y padded es que en padded cada contador está almacenado de forma aislada en una estructura cuyo tamaño es el de la línea de caché, por lo que cada dato será enviado en su propia línea de caché. En cambio, en compact, por localidad espacial, todos los datos serán enviados en una misma línea de caché. 

En una línea de caché de 64 bytes y considerando que un long ocupa 8 bytes, caben 8 contadores tipo long en una línea de caché (compact). En padded, solo cabe un contador por línea de caché, ya que cada uno está alineado y ocupa toda la línea.

## ¿Cómo afecta la coherencia de caché al rendimiento de cada variante al aumentar el número de threads? Justifique con los resultados obtenidos.
"Cuando un núcleo escribe en una línea, el protocolo de coherencia (MESI) invalida las copias de esa misma línea en los demás núcleos. Ellos deben recargarla antes de su próximo acceso."
Por este mismo motivo, a mayor número de threads habrá más accesos simultáneos y, por tanto, más invalidaciones, haciendo que empeore el rendimiento de todas las variantes.

Sin embargo, el impacto es mayor en la variante compact, ya que varios contadores comparten la misma línea de caché y cualquier modificación provoca invalidaciones para todos los threads que usan esa línea. En padded, cada contador está en su propia línea de caché, por lo que las invalidaciones afectan solo al thread correspondiente, reduciendo el false sharing. En private, cada thread trabaja con su variable local y solo al final copia el resultado, minimizando la contención y las invalidaciones.

## Comente lo que está ocurriendo en este código a nivel de coherencia de caché. Este es el fenómeno de false sharing.
Cuando se modifica un dato, toda la línea de caché es invalidada por el protocolo de coherencia de caché. "Cuando un núcleo escribe en una línea, el protocolo de coherencia (MESI) invalida las copias de esa misma línea en los demás núcleos. Ellos deben recargarla antes de su próximo acceso."

Esto genera el fenómeno conocido como false sharing: la modificación de datos lógicamente independientes (por ejemplo, contadores de distintos threads que comparten línea de caché en compact) provoca igualmente un decremento en el rendimiento, debido a que los mecanismos de coherencia invalidan la línea de caché completa. Así, aunque los datos sean independientes a nivel lógico, la unidad mínima de transferencia e invalidación es la línea de caché, generando interferencia entre threads.

## La variante private es más rápida que padded incluso con 1 thread, donde no hay contención. ¿Por qué?
Private es más rápida porque solo tiene un punto de contacto con los datos reales: cada thread acumula en una variable local y solo al final copia el resultado al arreglo compartido. Esto implica menos modificaciones a los datos compartidos y, por tanto, menos invalidaciones por la coherencia de caché. Incluso con un solo thread, se reduce la sobrecarga de acceso a memoria compartida respecto a padded, donde cada acceso implica trabajar con una estructura alineada a caché.
