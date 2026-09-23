
# Taller 1 - Formulación y resolución de un modelo en red

## Integrantes
- Pedro Limarí
- Diego Baltazar

## Instancia asignada
Instancia D - Industria 4.0

## Objetivo

Este repositorio contiene el desarrollo del Taller 1 de Investigación de Operaciones.

El problema corresponde a una asignación entre órdenes y celdas robotizadas, formulada
inicialmente como una red bipartita de flujo a costo mínimo.

Posteriormente se incorpora una restricción operacional adicional asociada a un brazo de carga
compartido por las celdas C1 y C2, analizando su efecto sobre la integralidad de la solución.

## Estructura del repositorio

- datos/
  - tiempos.csv
  - restriccion_adicional.csv

- resultados/
  - solucion.csv / duales.csv — caso base (LP continuo, sin restricción adicional)
  - solucion_con_tope.csv / duales_con_tope.csv — LP continuo con la restricción del brazo
  - solucion_con_tope_binario.csv — modelo binario con la restricción del brazo (resultado final)

- modelo.py
  - Modelo reproducible en Pyomo. Un mismo script resuelve los tres escenarios del taller
    según los parámetros con que se ejecute (ver sección Ejecución).

- cuaderno.ipynb
  - Desarrollo completo del taller: formulación, resolución de los tres escenarios,
    verificación de conservación de flujo, integralidad (submatrices de la matriz de
    incidencia), valores duales, análisis de sensibilidad y verificación independiente por
    enumeración exhaustiva.

## Metodología

1. Formulación del problema como red de flujo a costo mínimo.
2. Resolución del modelo lineal con variables continuas (caso base).
3. Verificación de la integralidad de la solución base.
4. Análisis de la matriz de incidencia y total unimodularidad.
5. Incorporación de la restricción adicional del brazo compartido (LP continuo).
6. Comparación entre relajación lineal y modelo binario.
7. Verificación independiente mediante enumeración exhaustiva (720 asignaciones).
8. Análisis de valores duales y sensibilidad.

## Resultados

| Escenario | Óptimo | Notas |
|---|---|---|
| Base (sin restricción adicional) | 236 min | Sale 0-1 sin imponer integralidad |
| Con restricción del brazo (LP continuo) | 238 min | 6 variables fraccionarias |
| Con restricción del brazo (binario) | 239 min | Resultado operacionalmente válido; brecha de 1 min (0.42%) respecto del LP |

## Ejecución

Desde la carpeta principal del proyecto:

```
python modelo.py                     # caso base: 236 min
python modelo.py --con-tope          # LP con restricción adicional: 238 min
python modelo.py --con-tope --entero # binario con restricción adicional: 239 min
```

Cada ejecución imprime la condición de término, el valor óptimo y la asignación, y escribe los
archivos correspondientes en resultados/.

## Software utilizado

- Python
- Pyomo
- HiGHS
- pandas
- Google Colab (desarrollo) / entorno local (verificación de modelo.py)

## Reproducibilidad

Los parámetros numéricos del problema se leen desde los archivos CSV contenidos en la carpeta
datos/. Ningún valor está escrito dentro de modelo.py.
