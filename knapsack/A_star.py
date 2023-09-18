from queue import PriorityQueue


# Define the item class
class Item:
    def __init__(self, index, weight, value):
        self.index = index
        self.weight = weight
        self.value = value


# Define the state class
class State:
    def __init__(self, index, capacity, value, path):
        self.index = index
        self.capacity = capacity
        self.value = value
        self.path = path

    def __lt__(self, other):
        # Comparison function for priority queue
        return self.value > other.value


# A* algorithm for 0/1 Knapsack problem
def knapsack_a_star(items, capacity):
    n = len(items)
    best_solution = None

    # Heuristic function: value per unit weight
    def heuristic(index, capacity, value):
        remaining_items = items[index:]
        remaining_items.sort(key=lambda x: x.value / x.weight, reverse=True)
        estimate = value
        total_weight = 0

        for item in remaining_items:
            if total_weight + item.weight <= capacity:
                total_weight += item.weight
                estimate += item.value
            else:
                fraction = (capacity - total_weight) / item.weight
                estimate += item.value * fraction
                break

        return estimate

    # Initialize priority queue
    open_set = PriorityQueue()
    open_set.put(State(0, capacity, 0, []))

    while not open_set.empty():
        current_state = open_set.get()

        # Check if current state is a valid solution
        if current_state.index == n:
            best_solution = current_state
            break

        # Generate successor states (include or exclude next item)
        include_item = current_state.index + 1
        exclude_item = current_state.index + 1

        # Include next item
        if current_state.capacity >= items[current_state.index].weight:
            include_state = State(
                include_item,
                current_state.capacity - items[current_state.index].weight,
                current_state.value + items[current_state.index].value,
                current_state.path + [current_state.index],
            )
            include_cost = include_state.value + heuristic(
                include_item, include_state.capacity, include_state.value
            )
            open_set.put(include_state, include_cost)

        # Exclude next item
        exclude_state = State(
            exclude_item,
            current_state.capacity,
            current_state.value,
            current_state.path,
        )
        exclude_cost = exclude_state.value + heuristic(
            exclude_item, exclude_state.capacity, exclude_state.value
        )
        open_set.put(exclude_state, exclude_cost)

    # Retrieve selected items from the best solution
    selected_items_index = [items[i] for i in best_solution.path]
    token = [0 for _ in range(n)]  # n = len(items)
    weight = 0
    for item in selected_items_index:
        token[item.index] = 1
        weight += item.weight
    return best_solution.value, weight, token


if __name__ == "__main__":
    # Example usage
    items = [Item(1, 2, 3), Item(2, 3, 4), Item(3, 4, 5), Item(4, 5, 6)]
    capacity = 8
    max_value, selected_items = knapsack_a_star(items, capacity)
    print("Maximum value:", max_value)
    print("Selected items:")
    for item in selected_items:
        print("Weight:", item.weight, "Value:", item.value)
