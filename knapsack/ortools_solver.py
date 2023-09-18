"""
@File    :   ortools_solver.py
@Time    :   2023/09/18 17:09:29
@Author  :   glx 
@Version :   1.0
@Contact :   18095542g@connect.polyu.hk
@Desc    :   None
"""

from ortools.algorithms.python import knapsack_solver
from typing import List


def ortools_solver(items, capacity):
    solver = knapsack_solver.KnapsackSolver(
        knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
        "KnapsackExample",
    )

    values = [i.value for i in items]
    weights = [i.weight for i in items]
    capacity = [capacity]
    solver.init(values, [weights], capacity)

    computed_value = solver.solve()
    total_weight = 0

    taken = [0 for _ in range(len(items))]
    print("Total value =", computed_value)
    for i in range(len(values)):
        if solver.best_solution_contains(i):
            total_weight += weights[i]
            taken[i] = 1

    return computed_value, total_weight, taken


if __name__ == "__main__":
    ## example by google
    from ortools.algorithms.python import knapsack_solver

    def main():
        # Create the solver.
        solver = knapsack_solver.KnapsackSolver(
            knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
            "KnapsackExample",
        )

        values = [
            # fmt:off
        360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
        78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
        87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
        312
            # fmt:on
        ]
        weights = [
            # fmt: off
        [7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
        42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
        3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13],
            # fmt: on
        ]
        capacities = [850]

        solver.init(values, weights, capacities)
        computed_value = solver.solve()

        packed_items = []
        packed_weights = []
        total_weight = 0
        print("Total value =", computed_value)
        for i in range(len(values)):
            if solver.best_solution_contains(i):
                packed_items.append(i)
                packed_weights.append(weights[0][i])
                total_weight += weights[0][i]
        print("Total weight:", total_weight)
        print("Packed items:", packed_items)
        print("Packed_weights:", packed_weights)

    main()
