# import numpy as np
from copy import copy


# ####################################################################################
# # Unoptimized version treating lanternfishes individually
# def read_input():
#     """Reads input data."""
#     with open("Day 6 - Lanternfish/input.txt", 'r') as f:
#         timers = f.readline()
#
#     # Format timers
#     timers = [int(x) for x in timers.split(',')]
#
#     fishes = []
#     for t in timers:
#         fishes.append(Lanternfish(t))
#
#     return fishes
#
#
# class Lanternfish:
#
#     cycle_start = 6
#
#     def __init__(self, timer: int, days_until_fertile: int = 0) -> None:
#         self.timer = timer
#         self.days_until_fertile = days_until_fertile
#
#         # Whether this lanternfish spawns a new fish today
#         self.new_fish_today = False
#
#     def __iter__(self) -> object:
#         return self
#
#     def __next__(self) -> int:
#         self.timer -= 1
#         if self.days_until_fertile > 0:
#             self.days_until_fertile -= 1
#         self.new_fish_today = False
#
#         # Reset timer and spawn new lanternfish
#         if self.timer == -1:
#             self.timer = self.cycle_start
#             self.new_fish_today = True
#
#         return self.timer
#
#     def __repr__(self) -> str:
#         return f"Lanternfish(timer={self.timer}, days_until_fertile={self.days_until_fertile})"
#
#     def is_fertile(self) -> bool:
#         return self.days_until_fertile == 0
#
#
# def create_new_lanternfish() -> Lanternfish:
#     """Creates a newborn lanternfish."""
#     return Lanternfish(timer=8, days_until_fertile=8)
#
#
# def simulate_days(days: int, fishes: list[Lanternfish]) -> int:
#     """Simulate `days` days given a list of lanternfish.
#
#     Args:
#         days: Number of days to simulate.
#         fishes: list of Lanternfish.
#
#     Returns:
#         Number of lanternfish at the end of the last simulated day.
#
#     """
#     for day in range(days):
#         new_fishes = []
#         for fish in fishes:
#             next(fish)
#             if fish.new_fish_today:
#                 new_fishes.append(create_new_lanternfish())
#
#         print(f"Day: {day}. Fish: {len(fishes)}. New fishes: {len(new_fishes)}")
#         fishes.extend(new_fishes)
#
#     return len(fishes)

# ####################################################################################
# Optimized numpy version treating lanternfishes individually
# def simulate_days_brute_force(days: int, fishes: np.ndarray) -> int:
#     """Simulate `days` days given a list of lanternfish timers.
#
#     Args:
#         days: Number of days to simulate.
#         fishes: list of Lanternfish timers.
#
#     Returns:
#         Number of lanternfish at the end of the last simulated day.
#
#     """
#     for day in range(days):
#         if day == 0:
#             n_newborns = 0
#         else:
#             n_newborns = (fishes_yesterday == 7).sum()
#
#         # Update fish timers
#         fishes = fishes - 1
#         fishes[fishes <= 6] = fishes[fishes <= 6] % 7
#
#         # Add new fishes
#         n_new_fishes = (fishes == 6).sum() - n_newborns
#         new_fishes = np.repeat(8, n_new_fishes)
#
#         print(f"Day: {day}. Fish: {len(fishes)}. New fishes: {len(new_fishes)}")
#
#         fishes = np.concatenate([fishes, new_fishes])
#
#         fishes_yesterday = np.copy(fishes)
#
#     return len(fishes)

def read_input():
    """Reads input data."""
    with open("Day 6 - Lanternfish/input.txt", 'r') as f:
        timers = f.readline()

    # Format timers
    return [int(x) for x in timers.split(',')]


def simulate_days(days: int, fishes: list[int]) -> int:
    """Simulate `days` days given a list of lanternfish timers.

    We treat lanternfishes as a group instead of individually, which allows us to use a dictionary.

    Args:
        days: Number of days to simulate.
        fishes: list of Lanternfish timers.

    Returns:
        Number of lanternfish at the end of the last simulated day.

    """
    counter_fish = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    for fish in fishes:
        counter_fish[fish] += 1

    for day in range(days):
        new_counter_fish = copy(counter_fish)

        # Pass of the day. Without a loop so to easier to understand
        new_counter_fish[0] = counter_fish[1]
        new_counter_fish[1] = counter_fish[2]
        new_counter_fish[2] = counter_fish[3]
        new_counter_fish[3] = counter_fish[4]
        new_counter_fish[4] = counter_fish[5]
        new_counter_fish[5] = counter_fish[6]
        new_counter_fish[6] = counter_fish[7] + counter_fish[0]
        new_counter_fish[7] = counter_fish[8]
        new_counter_fish[8] = 0

        # Number of new fishes
        n_new_fish = new_counter_fish[6] - counter_fish[7]
        new_counter_fish[8] += n_new_fish

        counter_fish = new_counter_fish

    return sum(counter_fish.values())

lanternfishes = read_input()


# Part 1
day_to_simulate = 80
n_fishes = simulate_days(day_to_simulate, lanternfishes)

print(f"The number of lanternfish after {day_to_simulate} days is equal to: {n_fishes}")


# Part 2
day_to_simulate = 256
n_fishes = simulate_days(256, lanternfishes)

print(f"The number of lanternfish after {day_to_simulate} days is equal to: {n_fishes}")
