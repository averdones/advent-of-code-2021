import numpy as np
from collections import deque


def read_input() -> np.ndarray:
    """Reads input data."""
    heightmap = None
    with open("Day 9 - Smoke Basin/input.txt", 'r') as f:
        for line in f:
            new_line = [int(x) for x in line.strip()]
            if heightmap is None:
                heightmap = np.array(new_line)
            else:
                heightmap = np.vstack([heightmap, new_line])

    return heightmap


def find_low_points_idxs(arr: np.ndarray) -> list[tuple[int, int]]:
    """Given an array finds the indices of the elements surrounded by larger values."""
    # Pad array with zeros to not have boundary issues
    padded = np.pad(arr, 1, constant_values=10)

    low_idxs = []
    for i in range(1, padded.shape[0] - 1):
        for j in range(1, padded.shape[1] - 1):
            # Check 4 adjacent neighbors
            if (
                    padded[i + 1, j] > padded[i, j] and
                    padded[i - 1, j] > padded[i, j] and
                    padded[i, j + 1] > padded[i, j] and
                    padded[i, j - 1] > padded[i, j]
            ):
                # We want the indices in the original array not the padded one
                low_idxs.append((i - 1, j - 1))

    return low_idxs


def find_low_points_values(arr: np.ndarray, idxs: list[tuple[int, int]]) -> list[int]:
    """Given and array and a list of indices, find the values in the array corresponding to those indices."""
    lows = []
    for i, j in idxs:
        lows.append(arr[i, j])

    return lows


def sum_low_points(lows: list[int]) -> int:
    """Finds the sum of low point heights."""
    return sum([x + 1 for x in lows])


##################################################################################################

def is_valid(vis: np.ndarray, idxs: tuple) -> bool:
    """Checks if the index is valid.

    Checks for boundary conditions and whether the index has been visited or not.

    Args:
        vis: Boolean array. True elements indicate that the index has been visited.
        idxs: Index to check.

    Returns:
        True if the index is within the boundaries and if it has not been visited.

    """
    # If cell lies out of bounds
    if (idxs[0] < 0 or idxs[1] < 0 or idxs[0] >= vis.shape[0] or idxs[1] >= vis.shape[1]):
        return False

    # If cell is already visited
    if (vis[idxs]):
        return False

    return True


def bfs_basin(arr: np.ndarray, root: tuple):
    """Traverse a basin using breadth-first search.

    The search starts from a low point and it will traverse all the positions in the basin.

    Args:
        arr: Array to traverse.
        root: index from where to start traversing the basin.

    """
    # Neighbors vectors
    neighs = ((-1, 0), (0, -1), (1, 0), (0, 1))

    # Initialize visited array
    visited = np.zeros_like(arr, dtype=bool)

    # Stores indices to visit in a queue
    q = deque()

    # Mark the starting cell as visited and push it into the queue
    visited[root] = True
    q.append(root)

    # Iterate while the queue is not empty
    while (len(q) > 0):
        cell_idx = q.popleft()

        # Check 4 adjacent neighbors
        for neigh in neighs:
            neigh_idx = tuple([sum(x) for x in zip(neigh, cell_idx)])
            if is_valid(visited, neigh_idx):
                # Traverse only through basin
                if arr[cell_idx] < arr[neigh_idx] and arr[neigh_idx] < 9:
                    q.append(neigh_idx)
                    visited[neigh_idx] = True

    return visited


def find_largest_basins(arr: np.ndarray, low_idxs: tuple[int, int], n_largest: int):
    """Finds the largest basins of an array given a list of low points and returns the product of their sizes."""
    lengths_basins = []
    for low_idx in low_idxs:
        basin = bfs_basin(arr, low_idx)
        lengths_basins.append(basin.sum())

    largest_basins_lengths = np.array(sorted(lengths_basins)[-n_largest:])

    return np.prod(largest_basins_lengths)


heightmap = read_input()

# Part 1

low_idxs = find_low_points_idxs(heightmap)
low_points = find_low_points_values(heightmap, low_idxs)
lows_sum = sum_low_points(low_points)

print(f"The sum of low points is equal to {lows_sum}")


# Part 2
n_largest = 3
sum_largest_basins = find_largest_basins(heightmap, low_idxs, n_largest=n_largest)
print(f"The sum of the {n_largest} basins is equal to {sum_largest_basins}")
