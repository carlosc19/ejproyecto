from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')

    # VARIABLES BINARIAS x_ij
    x12 = solver.BoolVar('x12')
    x13 = solver.BoolVar('x13')
    x15 = solver.BoolVar('x15')
    x24 = solver.BoolVar('x24')
    x25 = solver.BoolVar('x25')
    x27 = solver.BoolVar('x27')
    x34 = solver.BoolVar('x34')
    x35 = solver.BoolVar('x35')
    x45 = solver.BoolVar('x45')
    x47 = solver.BoolVar('x47')
    x56 = solver.BoolVar('x56')
    x67 = solver.BoolVar('x67')

    # FUNCIÓN OBJETIVO (minimizar costo total)
    solver.Minimize(
        1100*x12 + 1300*x13 + 2000*x15 +
        1400*x24 + 2000*x25 + 2600*x27 +
        780*x34 + 1000*x35 + 900*x45 +
        1300*x47 + 800*x56 + 200*x67
    )

    # --- RESTRICCIONES ---

    # 1. El árbol debe tener |N|-1 = 6 aristas
    solver.Add(
        x12 + x13 + x15 + x24 + x25 + x27 +
        x34 + x35 + x45 + x47 + x56 + x67 == 6
    )

    # 2. Cada nodo debe estar conectado (al menos una arista incidente)
    solver.Add(x12 + x13 + x15 >= 1)                   # Nodo 1 (SE)
    solver.Add(x12 + x24 + x25 + x27 >= 1)             # Nodo 2 (LA)
    solver.Add(x13 + x34 + x35 >= 1)                   # Nodo 3 (DE)
    solver.Add(x24 + x34 + x45 + x47 >= 1)             # Nodo 4 (DA)
    solver.Add(x15 + x25 + x35 + x45 + x56 >= 1)       # Nodo 5 (CH)
    solver.Add(x56 + x67 >= 1)                         # Nodo 6 (NY)
    solver.Add(x27 + x47 + x67 >= 1)                   # Nodo 7 (DC)

    # 3. Evitar ciclos (restricciones de subconjunto)
    # (en un modelo completamente expandido habría 2^7 - 2 = 126 subconjuntos posibles)
   
    #Hubo subciclos, por lo que se incluyen algunas restricciones de subconjunto:
    solver.Add(x34 + x35 + x45 + x56 + x67 <= 4)  # Subconjunto {3, 4, 5, 6, 7}
    #Sigue habiendo subciclos, por lo que se incluye otra restricción de subconjunto:
    solver.Add(x34 + x47 + x45 + x56 + x67 <= 4)  # Subconjunto {4, 5, 6, 7}
    
   # Como no hubo más subciclos en la solución, no fue necesario incluir más restricciones de subconjunto.

    # --- RESOLVER ---
    status = solver.Solve()

    # --- RESULTADOS ---
    if status == pywraplp.Solver.OPTIMAL:
        print("✅ Solución óptima encontrada")
        print("Costo mínimo total =", solver.Objective().Value())
        print("\nAristas seleccionadas:")
        for var in [x12, x13, x15, x24, x25, x27, x34, x35, x45, x47, x56, x67]:
            if var.solution_value() > 0.5:
                print(f"{var.name()} = 1")

        print("\nNombres de nodos conectados:")
        nombres = {1: "SE", 2: "LA", 3: "DE", 4: "DA", 5: "CH", 6: "NY", 7: "DC"}
        conexiones = {
            'x12': (1, 2), 'x13': (1, 3), 'x15': (1, 5),
            'x24': (2, 4), 'x25': (2, 5), 'x27': (2, 7),
            'x34': (3, 4), 'x35': (3, 5),
            'x45': (4, 5), 'x47': (4, 7),
            'x56': (5, 6), 'x67': (6, 7)
        }
        for var in [x12, x13, x15, x24, x25, x27, x34, x35, x45, x47, x56, x67]:
            if var.solution_value() > 0.5:
                i, j = conexiones[var.name()]
                print(f"({nombres[i]}, {nombres[j]})")
    else:
        print("No se encontró solución óptima.")


if __name__ == "__main__":
    main()
