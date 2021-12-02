def read_input() -> list[tuple[str, int]]:
    """Reads input data."""
    with open("Day 2 - Dive!/input.txt", 'r') as f:
        commands = []
        for line in f:
            direction, amount = line.split()
            amount = int(amount)

            commands.append((direction, amount))

    return commands


def calculate_position(commands: list[tuple[str, int]]) -> tuple:
    """Calculates the final horizontal and vertical position of the submarine.

    Args:
        commands: List of commands. Possible commands are 'forward', 'down' and 'up'.

    Returns:
        Horizontal and vertical position.

    """
    hor = 0
    ver = 0
    for direction, amount in commands:
        if direction == 'forward':
            hor += amount
        elif direction == 'down':
            ver += amount
        elif direction == 'up':
            ver -= amount

    return hor, ver


def calculate_position_new_instructions(commands: list[tuple[str, int]]) -> tuple:
    """Calculates the final horizontal and vertical position of the submarine using the new instructions.

    Args:
        commands: List of commands. Possible commands are 'forward', 'down' and 'up'.

    Returns:
        Horizontal and vertical position.

    """
    hor = 0
    ver = 0
    aim = 0
    for direction, amount in commands:
        if direction == 'forward':
            hor += amount
            ver += aim * amount
        elif direction == 'down':
            aim += amount
        elif direction == 'up':
            aim -= amount

    return hor, ver


# Part 1
commands = read_input()
hor_pos, ver_pos = calculate_position(commands)
print(f"Multiplication of the horizontal and vertical position is equal to: {hor_pos * ver_pos}")


# Part 2
hor_pos, ver_pos = calculate_position_new_instructions(commands)
print(f"Multiplication of the horizontal and vertical position with the new instructions is equal "
      f"to: {hor_pos * ver_pos}")
