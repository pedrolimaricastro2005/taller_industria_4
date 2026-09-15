
from pathlib import Path
import pandas as pd
import pyomo.environ as pyo

# --------------------------------------------------
# 1. Lectura de datos
# --------------------------------------------------

BASE = Path(__file__).resolve().parent
CARPETA_DATOS = BASE / "datos"

tiempos = pd.read_csv(
    CARPETA_DATOS / "tiempos.csv",
    sep=";"
)

restriccion = pd.read_csv(
    CARPETA_DATOS / "restriccion_adicional.csv",
    sep=";"
)

# --------------------------------------------------
# 2. Conjuntos y parámetros
# --------------------------------------------------

ordenes = tiempos["orden"].tolist()
celdas = [col for col in tiempos.columns if col != "orden"]

A = {}

for _, fila in tiempos.iterrows():
    orden = fila["orden"]

    for celda in celdas:
        A[(orden, celda)] = fila[celda]

# Restricción adicional leída desde archivo
celdas_brazo = restriccion.loc[0, "celdas"].split("+")
tope = float(restriccion.loc[0, "tope_minutos"])

# --------------------------------------------------
# 3. Modelo
# --------------------------------------------------

m = pyo.ConcreteModel()

m.ORDENES = pyo.Set(initialize=ordenes)
m.CELDAS = pyo.Set(initialize=celdas)

m.x = pyo.Var(
    m.ORDENES,
    m.CELDAS,
    domain=pyo.Binary
)

# Función objetivo
m.obj = pyo.Objective(
    expr=sum(
        A[(o, c)] * m.x[o, c]
        for o in ordenes
        for c in celdas
    ),
    sense=pyo.minimize
)

# Cada orden se asigna a una celda
m.asignacion_orden = pyo.Constraint(
    m.ORDENES,
    rule=lambda m, o:
        sum(m.x[o, c] for c in celdas) == 1
)

# Cada celda recibe una orden
m.asignacion_celda = pyo.Constraint(
    m.CELDAS,
    rule=lambda m, c:
        sum(m.x[o, c] for o in ordenes) == 1
)

# Restricción del brazo compartido
m.restriccion_brazo = pyo.Constraint(
    expr=sum(
        A[(o, c)] * m.x[o, c]
        for o in ordenes
        for c in celdas_brazo
    ) <= tope
)

# --------------------------------------------------
# 4. Resolución
# --------------------------------------------------

resultado = pyo.SolverFactory("appsi_highs").solve(m)

print(
    "Condición de término:",
    resultado.solver.termination_condition
)

print(
    "Tiempo óptimo:",
    pyo.value(m.obj),
    "minutos"
)

print("\nAsignaciones:")

for o in ordenes:
    for c in celdas:
        if pyo.value(m.x[o, c]) > 0.5:
            print(
                f"{o} -> {c} | "
                f"{A[(o, c)]} minutos"
            )
