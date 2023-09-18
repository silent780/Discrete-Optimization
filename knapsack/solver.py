"""
@File    :   solver.py
@Time    :   2023/09/18 14:08:32
@Author  :   glx 
@Version :   1.0
@Contact :   18095542g@connect.polyu.hk
@Desc    :   this is a script for solving knapsack problem, I used three methods to solve it,
            1. greedy algorithm
            2. A* algorithm
            3. dynamic programming
"""

# here put the import lib
from collections import namedtuple
from typing import List
from ortools_solver import ortools_solver

Item = namedtuple("Item", ["index", "value", "weight"])


def greedy_solver(items: List[Item], capacity: int) -> [int, int, List]:
    value = 0
    weight = 0
    taken = [0] * len(items)
    items.sort(key=lambda item: item.value / item.weight, reverse=True)
    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    return value, weight, taken


def dp_solver(items: List[Item], capacity: int) -> [int, int, List]:
    """
    this is a function for solving knapsack problem using dynamic programming
    """
    weights = []
    values = []
    for i in items:
        weights.append(i.weight)
        values.append(i.value)
    taken = [0 for _ in range(len(items))]

    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, capacity + 1):
            if weights[i - 1] > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(
                    dp[i - 1][j], dp[i - 1][j - weights[i - 1]] + values[i - 1]
                )

    # 回溯求解最优解
    i, j = n, capacity
    weight = 0
    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            taken[i - 1] = 1
            j -= weights[i - 1]
            weight += weights[i - 1]
        i -= 1
    value = dp[n][capacity]
    return value, weight, taken


def bb_solver(items: List[Item], capacity: int) -> [int, int, List]:
    """branch and bound algorithm to solve knapsack problem"""
    import branch_and_bound

    items = [(i.weight, i.value) for i in items]

    value, weight, taken = branch_and_bound.solve_it(items, capacity)

    return value, weight, taken


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split("\n")

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    # method 1 : greedy algorithm
    # sort items by value/weight ratio
    items.sort(key=lambda item: item.value / item.weight, reverse=True)
    if 200 < len(items) < 999:
        value, weight, taken = greedy_solver(items, capacity)

    # method 2: A_star algorithm for huge amount problem
    elif len(items) > 1000:
        import A_star

        value, weight, taken = A_star.knapsack_a_star(items=items, capacity=capacity)

    # method 3 : dynamic programming
    else:
        value, weight, taken = dp_solver(items, capacity)
    # return dp[n][capacity], selected_items

    # value, weight, taken = bb_solver(items, capacity)
    # value, weight, taken = ortools_solver(items, capacity)

    print("value = ", value)
    print("weight = ", weight)
    print("taken = ", taken)

    # prepare the solution in the specified output format
    output_data = str(value) + " " + str(0) + "\n"
    output_data += " ".join(map(str, taken))
    return output_data


if __name__ == "__main__":
    import sys
    import os

    # if len(sys.argv) > 1:
    #     file_location = sys.argv[1].strip()
    #     with open(file_location, "r") as input_data_file:
    #         input_data = input_data_file.read()
    #         print(solve_it(input_data))
    # else:
    #     print(
    #         "This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)"
    #     )

    # list_dir = os.listdir("data")
    # for file in list_dir:
    #     # file_location = r"./data/ks_4_0"
    #     file_location = os.path.join("./data", file)
    #     with open(file_location, "r") as input_data_file:
    #         input_data = input_data_file.read()
    #         print(solve_it(input_data))

    file_location = r"data\ks_4_0"
    # file_location = os.path.join("./data", file)
    with open(file_location, "r") as input_data_file:
        input_data = input_data_file.read()
        print(solve_it(input_data))
