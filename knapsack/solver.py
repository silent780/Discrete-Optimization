#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple

Item = namedtuple("Item", ["index", "value", "weight"])


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

    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0] * len(items)

    # method 1 : greedy algorithm
    # sort items by value/weight ratio
    """
    items.sort(key=lambda item: item.value / item.weight, reverse=True)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    """

    # method 2 : dynamic programming

    dp = [[0 for _ in range(capacity + 1)] for _ in range(item_count + 1)]
    for i in range(1, item_count + 1):
        for j in range(1, capacity + 1):
            if items[i - 1].weight <= j:
                if (
                    dp[i - 1][j]
                    < dp[i - 1][j - items[i - 1].weight] + items[i - 1].value
                ):
                    taken[i - 1] = 1
                    dp[i][j] = dp[i - 1][j - items[i - 1].weight] + items[i - 1].value
                else:
                    dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = dp[i - 1][j]
    value = dp[item_count][capacity]
    # print the results
    print("value = ", value)
    print("weight = ", weight)
    print("taken = ", taken)

    # prepare the solution in the specified output format
    output_data = str(value) + " " + str(0) + "\n"
    output_data += " ".join(map(str, taken))
    return output_data


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, "r") as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            "This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)"
        )
