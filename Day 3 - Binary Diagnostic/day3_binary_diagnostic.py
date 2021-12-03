from collections import Counter


def read_input() -> list[str]:
    """Reads input data."""
    with open("Day 3 - Binary diagnostic/input.txt", 'r') as f:
        reps = []
        for line in f:
            # reports.append(bin(int(line, 2)))
            reps.append(line.strip())

    return reps


# Get gamma rate
def get_n_bit_positions(bin_nums: list[str]) -> list[list[str]]:
    """Given a list of binary numbers of length N, it creates a list of length N, where each element is a list of
    the corresponding bits in that position.

    Example:
        >>> get_n_bit_positions(['100', '001', '101'])
        [['1', '0', '1'], ['0', '0', '0'], ['0', '1', '1']]

    Args:
        bin_nums: List of binary numbers.

    Returns:
        List of bits in each position.

    """
    len_report = len(bin_nums[0])
    n_bits_pos = [[] for _ in range(len_report)]
    for byte in bin_nums:
        for pos, bit in enumerate(byte):
            n_bits_pos[pos].append(bit)

    return n_bits_pos


def _find_most_common_bit_position(n_bits_pos: list[list[str]]) -> str:
    """Finds the most common bit by position.

    Args:
        n_bits_pos: List where each element is a list of the bits of binary numbers in that position.

    Returns:
        String corresponding to a binary number where each bit is the most common bit in that position from a list of
        binary numbers.

    """
    gamma_rate_str = ""
    for pos in n_bits_pos:
        count = Counter(pos)
        if count['1'] >= count['0']:
            gamma_rate_str += '1'
        else:
            gamma_rate_str += '0'

    return gamma_rate_str


def find_most_common_bit_position(bin_nums: list[str]):
    """Wrapper of `_find_most_common_bit_position` that uses directly the binary numbers as input.

    Args:
        bin_nums: List of binary numbers.

    Returns:
        String corresponding to a binary number where each bit is the most common bit in that position from a list of
        binary numbers.

    """
    n_bits_pos = get_n_bit_positions(bin_nums)

    return _find_most_common_bit_position(n_bits_pos)


def _find_least_common_bit_position(n_bits_pos: list[list[str]]) -> str:
    """Finds the least common bit by position.

    Args:
        n_bits_pos: List where each element is a list of the bits of binary numbers in that position.

    Returns:
        String corresponding to a binary number where each bit is the least common bit in that position from a list of
        binary numbers.

    """
    epsilon_rate_str = ""
    for pos in n_bits_pos:
        count = Counter(pos)
        if count['0'] <= count['1']:
            epsilon_rate_str += '0'
        else:
            epsilon_rate_str += '1'

    return epsilon_rate_str


def find_least_common_bit_position(bin_nums: list[str]):
    """Wrapper of `_find_least_common_bit_position` that uses directly the binary numbers as input.

    Args:
        bin_nums: List of binary numbers.

    Returns:
        String corresponding to a binary number where each bit is the least common bit in that position from a list of
        binary numbers.

    """
    n_bits_pos = get_n_bit_positions(bin_nums)

    return _find_least_common_bit_position(n_bits_pos)


reports = read_input()

###############################################################################
# Part 1

# Get rates
gamma_rate = find_most_common_bit_position(reports)
epsilon_rate = find_least_common_bit_position(reports)

# Power consumption
power_consumption = int(gamma_rate, 2) * int(epsilon_rate, 2)

print(f"Power consumption is equal to {power_consumption}")


##################################################################################
# Part 2
# Get oxygen generator rating
bin_numbers = read_input()
for pos in range(len(bin_numbers)):
    gamma_rate = find_most_common_bit_position(bin_numbers)
    most_common_bit = gamma_rate[pos]
    bin_numbers = [x for x in bin_numbers if x[pos] == most_common_bit]

    if len(bin_numbers) == 1:
        break

oxygen = int(bin_numbers[0], 2)


# Get CO2 scrubber rating
bin_numbers = read_input()
for pos in range(len(bin_numbers)):
    epsilon_rate = find_least_common_bit_position(bin_numbers)
    least_common_bit = epsilon_rate[pos]
    bin_numbers = [x for x in bin_numbers if x[pos] == least_common_bit]

    if len(bin_numbers) == 1:
        break

co2 = int(bin_numbers[0], 2)

life_support = oxygen * co2
print(f"The life support rating is equal to: {life_support}")
