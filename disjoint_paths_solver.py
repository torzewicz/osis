import sys
from ortools.linear_solver import pywraplp
from util import load_graph


if __name__ == '__main__':

    solver = pywraplp.Solver.CreateSolver('SCIP')

    number_of_nodes, from_edges, to_edges, weights_list, defined_k, beginning, end = load_graph(sys.argv[1])

    xs = [[[None for x in range(number_of_nodes)] for y in range(number_of_nodes)] for k in range(defined_k)]
    weights = [[None for x in range(number_of_nodes)] for y in range(number_of_nodes)]

    objective = solver.Objective()

    for k in range(defined_k):

        for i in range(len(from_edges)):
            edge_start = from_edges[i]
            edge_end = to_edges[i]
            weight = weights_list[i]

            x1 = solver.IntVar(0.0, 1.0, f'x^{k}_{edge_start}-{edge_end}')
            x2 = solver.IntVar(0.0, 1.0, f'x^{k}_{edge_end}-{edge_start}')
            xs[k][edge_start][edge_end] = x1
            xs[k][edge_end][edge_start] = x2
            weights[edge_start][edge_end] = weight
            weights[edge_end][edge_start] = weight
            objective.SetCoefficient(x1, weight)
            objective.SetCoefficient(x2, weight)

    objective.SetMinimization()

    for k in range(defined_k):

        for i in range(number_of_nodes):

            if i == beginning:
                end_count = 1
            elif i == end:
                end_count = -1
            else:
                end_count = 0

            constraint = solver.Constraint(end_count, end_count)

            for j in range(number_of_nodes):
                if xs[k][j][i]:
                    constraint.SetCoefficient(xs[k][i][j], 1.0)
                    constraint.SetCoefficient(xs[k][j][i], -1.0)

    for i in range(0, number_of_nodes, 1):
        for j in range(i + 1, number_of_nodes, 1):
            constraint_created = False
            one_time_used_constraint = None
            for k in range(defined_k):
                if xs[k][i][j]:
                    if not constraint_created:
                        one_time_used_constraint = solver.Constraint(0.0, 1.0)
                        constraint_created = True
                    one_time_used_constraint.SetCoefficient(xs[k][i][j], 1.0)
                    one_time_used_constraint.SetCoefficient(xs[k][j][i], 1.0)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        for s in range(defined_k):
            print(f"Ścieżka {s}: {beginning} -> {end}")

        print("\n")
        print(f"Łączna waga ścieżek: {solver.Objective().Value()}")

        for k in range(defined_k):
            print(f"Krawędzie wchodzące w skład ścieżki {k}:")
            for i in range(number_of_nodes):
                for j in range(number_of_nodes):
                    if xs[k][i][j] and xs[k][i][j].solution_value() == 1:
                        print(f"{i} -> {j}, waga: {weights[i][j]}")
            print("\n")
    else:
        print("Brak rozwiązań")
