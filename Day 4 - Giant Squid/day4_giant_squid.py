from copy import copy
import numpy as np


def read_input() -> tuple[list[int], list[np.ndarray]]:
    """Reads input data."""
    with open("Day 4 - Giant squid/input.txt", 'r') as f:
        boards = []
        board = None
        for i, line in enumerate(f):
            # First line contains drawn numbers
            if i == 0:
                drawn = [int(x) for x in line.strip().split(',')]
                continue

            # Define new board on every new line
            if line == '\n':
                if board is not None:
                    boards.append(board)

                # Restart board
                board = np.empty((0, 5), dtype=int)
                continue

            # Fill board
            row = [int(x) for x in line.strip().split()]
            board = np.vstack([board, row])

    return drawn, boards


def create_mask_boards(boards: list[np.ndarray]) -> list[np.ndarray]:
    """For every board in the list of boards, creates a mask that will be an boolean array of the same shape of the
    board.

    A value of zero will mean that the number at the same position in the corresponding board has not been drawn.
    A value of 1 will mean that the number has been drawn.

    Returns:
        List of arrays of same shape than the corresponding arrays in the input list of arrays.
        Arrays are initialized to all zero values, meaning that no numbers have been drawn yet.

    """
    return [np.zeros_like(board, dtype=bool) for board in boards]


def is_board_winner(mask: np.ndarray) -> bool:
    """Decides if a board has won by analyzing its corresponding boolean mask, where 1's correspond to drawn numbers at
    the same position and 0's to non drawn numbers.

    Args:
        mask: Boolean mask of a board. 1's correspond to drawn numbers at the same position and 0's to numbers not
              drawn.

    Returns:
        True if the corresponding board of the mask is a winner. False, otherwise.

    """
    # Check rows
    for i in range(mask.shape[0]):
        if (mask[i, :] == 1).all():
            return True

    # Check columns
    for j in range(mask.shape[1]):
        if (mask[:, j] == 1).all():
            return True

    # Board is not a winner
    return False


def calculate_score_board(board: np.ndarray, mask: np.ndarray, winner_number: int) -> int:
    """Calculates the score of a winner board.

    Args:
        board: Board in the shape of an array.
        mask: Corresponding mask of the board with the numbers that have been drawn (1's) and the ones that have
              not (0's).
        winner_number: Number that was just called when the board won.

    Returns:
        Score of a winner board.

    """
    # Sum of all unmarked numbers
    unmarked = board[mask == 0].sum()

    return unmarked * winner_number


def update_board_mask(number_drawn: int, board: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Updates a masks of the corresponding board given a drawn number.

    Args:
        number_drawn: Number that has been drawn in the bingo.
        board: Bingo board.
        mask: Corresponding mask of the board where 1's correspond to drawn numbers and 0's to not drawn numbers.

    Returns:
        The updated mask.

    """
    modified_mask = copy(mask)
    modified_mask[board == number_drawn] = 1

    return modified_mask


def calculate_first_winner_board(drawn: list[int], boards: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray, int]:
    """Calculates the board that will win first given a list of drawn numbers.

    Args:
        drawn: Numbers drawn in the bingo.
        boards: Boards that will play bingo.

    Returns:
        First winner board, it's corresponding mask and the last drawn number that made the board win.

    """
    # Create masks
    masks = create_mask_boards(boards)

    for number_drawn in drawn:
        # Update all mask boards
        for i, board in enumerate(boards):
            masks[i] = update_board_mask(number_drawn, board, masks[i])

        # Assume no ties
        for i, mask in enumerate(masks):
            if is_board_winner(mask):
                # Return corresponding board
                return boards[i], mask, number_drawn


def calculate_last_winner_board(drawn: list[int], boards: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray, int]:
    """Calculates the board that will win last given a list of drawn numbers.

    Args:
        drawn: Numbers drawn in the bingo.
        boards: Boards that will play bingo.

    Returns:
        Last winner board, it's corresponding mask and the last drawn number that made the board win.

    """
    # Create masks
    masks = create_mask_boards(boards)

    for number_drawn in drawn:
        # Update all mask boards
        for i, board in enumerate(boards):
            masks[i] = update_board_mask(number_drawn, board, masks[i])

        # Assume no ties
        for i, mask in enumerate(masks):
            if is_board_winner(mask):
                # Pop winner board and its corresponding mask
                popped_mask = masks.pop(i)
                popped_board = boards.pop(i)

        # Return last board after it has won
        if len(boards) == 0:
            return popped_board, popped_mask, number_drawn


drawn, boards = read_input()


# First part
first_winner_board, first_winner_mask, first_winner_number = calculate_first_winner_board(drawn, boards)
first_winner_score = calculate_score_board(first_winner_board, first_winner_mask, first_winner_number)

print(f"The score of the first winner board is equal to {first_winner_score}")


# Second part
last_winner_board, last_winner_mask, last_winner_number = calculate_last_winner_board(drawn, boards)
last_winner_score = calculate_score_board(last_winner_board, last_winner_mask, last_winner_number)

print(f"The score of the last winner board is equal to {last_winner_score}")
