with open("Day 1 - Sonar Sweep/input.txt", 'r') as f:
    depths = []
    for line in f:
        depths.append(int(line))


#######################################################
# Part 1

def calculate_increases(arr: list[int]):
    """Calculate how many times in an array an element increases with respect to the previous element.

    Args:
        arr: Array of numbers.

    Returns:
        Number of increases.

    """
    n_larger = 0
    for i, depth in enumerate(arr):
        if i > 0:
            if depth > prev:
                n_larger += 1

        # Save to compare next
        prev = depth

    return n_larger


print(f"Number of measurements larger than the previous measurement: {calculate_increases(depths)}")


#######################################################
# Part 2

def create_sliding_windows(arr, size_window):
    arr_windowed = []
    for i in range(len(arr) - size_window + 1):
        arr_windowed.append(sum(arr[i:i + size_window]))

    return arr_windowed


depths_windows = create_sliding_windows(depths, 3)
print(f"Number of measurements larger than the previous measurement in windowed array: "
      f"{calculate_increases(depths_windows)}")
