
"""
Taller 1 - Equipo D. Industria 4.0: asignación de órdenes a celdas robotizadas.

Reproduce los tres escenarios reportados en el cuaderno con un solo script:

  1) python modelo.py                     -> LP continuo SIN restricción adicional (236 min)
  2) python modelo.py --con-tope           -> LP continuo CON restricción adicional (238 min)
  3) python modelo.py --con-tope --entero  -> binario CON restricción adicional (239 min)

Usa la misma convención de balance que el modelo principal del cuaderno
(m.bal: "sale - entra == q[n]"), para que los valores duales de
resultados/duales.csv coincidan con los ya interpretados en el cuaderno.
"""

import argparse
from pathlib import Path

import pandas as pd
import pyomo.environ as pyo

BASE = Path(__file__).resolve().parent
CARPETA_DATOS = BASE / "datos"

# --------------------------------------------------
# 1. Lectura de datos (sin cifras incrustadas en el modelo)
# --------------------------------------------------

tiempos = pd.read_csv(CARPETA_DATOS / "tiempos.csv", sep=";")
restriccion = pd.read_csv(CARPETA_DATOS / "restriccion_adicional.csv", sep=";")

ordenes = tiempos["orden"].tolist()
celdas = [col for col in tiempos.columns if col != "orden"]

A = {}
for _, fila in tiempos.iterrows():
    o = fila["orden"]
    for c in celdas:
        A[(o, c)] = float(fila[c])

N = ordenes + celdas
q = {o: 1 for o in ordenes}
q.update({c: -1 for c in celdas})

celdas_brazo = restriccion.loc[0, "celdas"].split("+")
tope = float(restriccion.loc[0, "tope_minutos"])


# --------------------------------------------------
# 2. Modelo (parametrizado: continuo/binario, con/sin tope)
# --------------------------------------------------

def construir_modelo(con_tope: bool, entero: bool) -> pyo.ConcreteModel:
    m = pyo.ConcreteModel()
    m.N = pyo.Set(initialize=N)
    m.A = pyo.Set(initialize=list(A.keys()), dimen=2)

    if entero:
        m.x = pyo.Var(m.A, domain=pyo.Binary)
    else:
        m.x = pyo.Var(m.A, domain=pyo.UnitInterval)

    m.obj = pyo.Objective(expr=sum(A[a] * m.x[a] for a in m.A), sense=pyo.minimize)

    def balance(m, n):
        sale = sum(m.x[i, j] for (i, j) in m.A if i == n)
        entra = sum(m.x[i, j] for (i, j) in m.A if j == n)
        return sale - entra == q[n]

    m.bal = pyo.Constraint(m.N, rule=balance)

    if con_tope:
        m.restriccion_brazo = pyo.Constraint(
            expr=sum(A[(o, c)] * m.x[o, c] for o in ordenes for c in celdas_brazo) <= tope
        )

    if not entero:
        m.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

    return m


# --------------------------------------------------
# 3. Resolución y reporte
# --------------------------------------------------

def resolver_y_reportar(con_tope: bool, entero: bool):
    m = construir_modelo(con_tope, entero)
    resultado = pyo.SolverFactory("appsi_highs").solve(m)

    print("Condición de término:", resultado.solver.termination_condition)
    print("Tiempo óptimo:", pyo.value(m.obj), "minutos")

    print("\nAsignaciones:")
    filas = []
    for (o, c) in sorted(m.A):
        v = pyo.value(m.x[o, c])
        if v > 1e-6:
            marca = "  <-- FRACCIONARIA" if 1e-6 < v < 1 - 1e-6 else ""
            print(f"{o} -> {c} | {A[(o, c)]:.0f} minutos  (x={v:.4f}){marca}")
            filas.append({"orden": o, "celda": c, "tiempo_min": A[(o, c)], "x": v})

    (BASE / "resultados").mkdir(exist_ok=True)
    sufijo = ("_con_tope" if con_tope else "") + ("_binario" if entero else "")
    pd.DataFrame(filas).to_csv(BASE / "resultados" / f"solucion{sufijo}.csv", index=False)

    if not entero:
        duales = [{"nodo": n, "q": q[n], "dual": m.dual[m.bal[n]],
                   "unidad": "min/unidad de orden"} for n in N]
        pd.DataFrame(duales).to_csv(BASE / "resultados" / f"duales{sufijo}.csv", index=False)

    return m, resultado


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--con-tope", action="store_true",
                         help="agrega la restricción del brazo compartido C1+C2 <= tope")
    parser.add_argument("--entero", action="store_true",
                         help="variables binarias en lugar de continuas")
    args = parser.parse_args()

    resolver_y_reportar(con_tope=args.con_tope, entero=args.entero)
