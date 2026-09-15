
# Taller 1 - Formulación y resolución de un modelo en red

## Integrantes
- Pedro Limarí
- Diego Baltazar

## Instancia asignada
Instancia D - Industria 4.0

## Objetivo

Este repositorio contiene el desarrollo del Taller 1 de Investigación de Operaciones.

El problema corresponde a una asignación entre órdenes y celdas robotizadas, formulada inicialmente como una red bipartita de flujo a costo mínimo.

Posteriormente se incorpora una restricción operacional adicional asociada a un brazo de carga compartido por las celdas C1 y C2, analizando su efecto sobre la integralidad de la solución.

## Estructura del repositorio

- datos/
  - tiempos.csv
  - restriccion_adicional.csv

- resultados/
  - solucion.csv
  - duales.csv

- modelo.py
  - Modelo final reproducible desarrollado en Python y Pyomo.

- cuaderno.ipynb
  - Desarrollo completo del taller, incluyendo formulación, resolución, verificación, integralidad, duales y análisis de sensibilidad.

## Metodología

1. Formulación del problema como red de flujo a costo mínimo.
2. Resolución del modelo lineal con variables continuas.
3. Verificación de la integralidad de la solución base.
4. Análisis de la matriz de incidencia y total unimodularidad.
5. Incorporación de la restricción adicional del brazo compartido.
6. Comparación entre relajación lineal y modelo binario.
7. Verificación independiente mediante enumeración exhaustiva.
8. Análisis de valores duales y sensibilidad.

## Resultado principal

El modelo binario con la restricción adicional obtiene un tiempo óptimo total de 239 minutos.

## Ejecución

Desde la carpeta principal del proyecto ejecutar:

python modelo.py

## Software utilizado

- Python
- Pyomo
- HiGHS
- pandas
- Google Colab

## Reproducibilidad

Los parámetros numéricos del problema se leen desde los archivos CSV contenidos en la carpeta datos/. De esta forma, los datos se mantienen separados del código del modelo.
