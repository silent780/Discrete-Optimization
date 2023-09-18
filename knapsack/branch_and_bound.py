"""
@File    :   branch_and_bound.py
@Time    :   2023/09/18 16:07:15
@Author  :   glx 
@Version :   1.0
@Contact :   18095542g@connect.polyu.hk
@Desc    :   None
"""


# here put the import lib
import heapq


class Node:
    def __init__(self, level, weight, value, bound):
        self.level = level
        self.weight = weight
        self.value = value
        self.bound = bound

    def __lt__(self, other):
        return self.bound > other.bound


def bound(u, max_weight, items):
    if u.weight >= max_weight:
        return 0

    total_value = u.value
    j = u.level + 1
    total_weight = u.weight

    while j < len(items) and total_weight + items[j][1] <= max_weight:
        total_weight += items[j][1]
        total_value += items[j][0]
        j += 1

    if j < len(items):
        total_value += (max_weight - total_weight) * items[j][0] / items[j][1]

    return total_value


def knapsack(items, max_weight):
    items.sort(key=lambda x: x[0] / x[1], reverse=True)

    queue = []
    root_node = Node(-1, 0, 0, 0)
    root_node.bound = bound(root_node, max_weight, items)
    heapq.heappush(queue, root_node)

    max_value = 0
    while queue:
        current_node = heapq.heappop(queue)

        if current_node.bound > max_value:
            i = current_node.level + 1

            next_node = Node(
                i,
                current_node.weight + items[i][1],
                current_node.value + items[i][0],
                0,
            )
            if next_node.weight <= max_weight and next_node.value > max_value:
                max_value = next_node.value

            next_node.bound = bound(next_node, max_weight, items)
            if next_node.bound > max_value:
                heapq.heappush(queue, next_node)

            next_node = Node(i, current_node.weight, current_node.value, 0)
            next_node.bound = bound(next_node, max_weight, items)
            if next_node.bound > max_value:
                heapq.heappush(queue, next_node)
    value, weight, taken = (
        max_value,
        max_weight,
    )

    return value, weight, taken


items = [(60, 10), (100, 20), (120, 30)]
max_weight = 50
print("The maximum value is ", knapsack(items, max_weight))
