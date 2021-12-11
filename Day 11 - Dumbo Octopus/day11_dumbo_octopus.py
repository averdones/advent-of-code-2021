from itertools import product
from collections import deque
import numpy as np


def read_input() -> np.ndarray:
    """Reads input data."""
    energies = None
    with open("Day 11 - Dumbo Octopus/input.txt", 'r') as f:
        for line in f:
            new_line = [int(x) for x in line.strip()]
            if energies is None:
                energies = np.array(new_line)
            else:
                energies = np.vstack([energies, new_line])

    return energies


def is_valid_idx(arr: np.ndarray, idxs: tuple[int, int]) -> bool:
    """Checks if an index is within the boundaries of an array-"""
    if (0 <= idxs[0] < arr.shape[0] and 0 <= idxs[1] < arr.shape[1]):
        return True

    return False


def get_neigh_idxs(idxs: tuple[int, int]):
    aux = list(product([-1, 0, 1], [-1, 0, 1]))
    aux.pop(aux.index((0, 0)))


    return [tuple(np.array(idxs) + np.array(x)) for x in aux]


def flash(arr: np.ndarray, idxs: tuple[int, int]) -> np.ndarray:
    """Given an array and a 2-dimensional index, adds 1 to all neighbors."""
    # Make the function idempotent
    new_arr = np.copy(arr)

    neigh_idxs = get_neigh_idxs(idxs)
    for neigh_idx in neigh_idxs:
        if is_valid_idx(new_arr, neigh_idx):
            new_arr[neigh_idx] += 1

    return new_arr


def model_energies_one_step(energies: np.ndarray) -> tuple:
    """Models one step of energy levels and flashes."""
    # Make the function idempotent
    new_energies = np.copy(energies)

    # Step 1: add 1 to each octopus
    new_energies = new_energies + 1

    # Flash
    seeds = deque([tuple(x) for x in np.argwhere(new_energies > 9)])
    flashed = []
    while len(seeds) > 0:
        idxs = seeds.popleft()

        # Add to visited list because one octopus flashes only once per step
        flashed.append(idxs)

        # Flash
        new_energies = flash(new_energies, idxs)

        # Add new seeds that have to flash too
        new_flashes = [tuple(x) for x in np.argwhere(new_energies > 9)]
        for new_flash in new_flashes:
            if new_flash not in seeds and new_flash not in flashed:
                seeds.append(new_flash)

    # Restart octopus greater than 9
    n_flashes = len(flashed)
    new_energies[new_energies > 9] = 0

    # Check if all octopus flash simultaneously
    if (new_energies == 0).all():
        sim_flash = True
    else:
        sim_flash = False

    return new_energies, n_flashes, sim_flash


def model_energies(energies: np.ndarray, n_steps: int) -> int:
    """Model energies for a number of steps."""
    total_n_flashes = 0
    for _ in range(n_steps):
        energies, n_flashes, _ = model_energies_one_step(energies)

        total_n_flashes += n_flashes

    return total_n_flashes


def find_first_simultaneous_flash(energies: np.ndarray) -> int:
    i = 0
    while True:
        i += 1
        energies, _, sim_flash = model_energies_one_step(energies)

        # We assume the loop won't be infinite
        if sim_flash:
            return i


energies = read_input()


# Part 1

n_steps = 10
n_flashes = model_energies(energies, 100)

print(f"The number of flashes after {n_steps} steps is equal to {n_flashes}")


# Part 2

step_first_sim_flash = find_first_simultaneous_flash(energies)
print(f"The first step in which all octopuses flash at the same time is step {step_first_sim_flash}")
