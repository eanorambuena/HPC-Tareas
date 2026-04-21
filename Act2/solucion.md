## Grafique los resultados de tiempo versus número de threads para las tres variantes.
[Grafica](./false_sharing/false_sharing_resultados.png)

## ¿Qué diferencia estructuralmente a compact y padded? ¿Cuántos contadores de cada tipo caben en una línea de caché?
La diferencia entre compact y padded es que en padded cada contador está almacenado de forma aislada en una estructura cuyo tamaño es el de la línea de caché, por lo que cada dato será enviado en su propia línea de caché. En cambio, en compact, por localidad espacial, todos los datos serán enviados en una misma línea de caché.

## ¿Cómo afecta la coherencia de caché al rendimiento de cada variante al aumentar el número de threads? Justifique con los resultados obtenidos.
"Cuando un núcleo escribe en una línea, el protocolo de coherencia (MESI) invalida las copias de esa misma línea en los demás núcleos. Ellos deben recargarla antes de su próximo acceso."
Por este mismo motivo, a mayor número de threads habrá más accesos simultáneos y, por tanto, más invalidaciones, haciendo que empeore el rendimiento de todas las variantes, pero empeorando más en compact que en padded y private.

## Comente lo que está ocurriendo en este código a nivel de coherencia de caché. Este es el fenómeno de false sharing.
Cuando se modifica un dato, toda la línea de caché es invalidada por el protocolo de coherencia de caché. "Cuando un núcleo escribe en una línea, el protocolo de coherencia (MESI) invalida las copias de esa misma línea en los demás núcleos. Ellos deben recargarla antes de su próximo acceso."
Por tanto, false sharing consiste en que la modificación de datos lógicamente independientes genera igualmente un decremento en el rendimiento debido a que hay efectos colaterales en la práctica por los mecanismos de coherencia de caché que invalidan la línea de caché completa, ya que la unidad mínima de caché es la línea de caché.

## La variante private es más rápida que padded incluso con 1 thread, donde no hay contención. ¿Por qué?
Porque private solo tiene un punto de contacto con los datos reales, lo que implica menos modificaciones a estos y, por tanto, menos invalidaciones por la coherencia de caché.
