import numpy as np


def read_input():
    """Reads input data."""
    with open("Day 7 - The Treachery of Wales/input.txt", 'r') as f:
        pos = f.readline()

    # Format positions
    return np.array([int(x) for x in pos.split(',')])


def find_min_cost(positions: np.ndarray) -> int:
    min_pos = np.min(positions)
    max_pos = np.max(positions)

    min_cost = np.Inf
    for i in range(min_pos, max_pos + 1):
        cost = abs(positions - i).sum()
        if cost < min_cost:
            min_cost = cost

    return min_cost


def calculate_crab_fuel_cost(distance):
    return sum([x for x in range(1, distance + 1)])


def find_min_cost_crab_strategy(positions: np.ndarray) -> int:
    min_pos = np.min(positions)
    max_pos = np.max(positions)

    min_cost = np.Inf
    for i in range(min_pos, max_pos + 1):
        all_cost = []
        # This could be vectorized to speed it up
        for pos in positions:
            cost_move = calculate_crab_fuel_cost(abs(pos - i))
            all_cost.append(cost_move)

        cost = sum(all_cost)
        if cost < min_cost:
            min_cost = cost

    return min_cost


positions = read_input()

# Part 1
min_cost = find_min_cost(positions)

print(f"The minimum amount of fuel is equal to: {min_cost}")


# Part 2
min_cost = find_min_cost_crab_strategy(positions)

print(f"The minimum amount of fuel using the crab strategy is equal to: {min_cost}")
