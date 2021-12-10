from statistics import median


def read_input() -> list[str]:
    """Reads input data."""
    parens = []
    with open("Day 10 - Syntax Scoring/input.txt", 'r') as f:
        for line in f:
            parens.append(line.strip())

    return parens


def create_balance_stack(chunk: str, verbose: bool = False) -> list | str:
    """Creates a stack of parens.

    If the chunk is correctly balanced, the return will be an empty string.

    Args:
        chunk: string of parentheses.
        verbose: Whether to print information messages or not.

    Returns:
        Empty string if chunk is balanced. Otherwise, it returns the remaining parentheses.

    """
    # Helper lists to know right pairs
    open_parens = ['(', '[', '{', '<']
    close_parens = [')', ']', '}', '>']

    stack = []
    for i, s in enumerate(chunk):
        if s in open_parens:
            stack.append(s)
        elif s in close_parens:
            if len(stack) > 0:
                # The closing and opening parens match
                if open_parens.index(stack[-1]) == close_parens.index(s):
                    stack.pop()
                else:
                    if verbose:
                        print("The chunk is corrupted, i.e. a chunk closes with the wrong character")
                    return s

    if verbose:
        if len(stack) > 0:
            print("The chunk is incomplete, i.e. some parens are not closed")

    return stack


def get_score_corrupted_chunks(chunks: list[str]) -> int:
    """Get the score of corrupted chunks only.

    Args:
        chunks: list of strings of parens.

    Returns:
        Score.

    """
    table_scores = {')': 3, ']': 57, '}': 1197, '>': 25137}

    score = 0
    for chunk in chunks:
        stack = create_balance_stack(chunk)

        if isinstance(stack, str):
            score += table_scores[stack]

    return score


def get_missing_closing_parens(chunk: str) -> list:
    """If the chunk is incomplete, it returns the parens necessary so that it would be complete.

    Args:
        chunk: string of parentheses.

    Returns:
        List of parens to make the chunk complete. List will be empty if chunk is complete.

    """
    # Helper lists to know right pairs
    open_parens = ['(', '[', '{', '<']
    close_parens = [')', ']', '}', '>']

    stack = create_balance_stack(chunk)

    missing_parens = []
    if isinstance(stack, list):
        for s in stack:
            missing_parens.append(close_parens[open_parens.index(s)])

    # Reverse because the last parens should be the first added to make the chunk complete
    return missing_parens[::-1]


def get_score_missing_parens(missing_parens: list) -> int:
    """Given a list of missing parens, calculate the final score.

    Args:
        missing_parens: list of string parens.

    Returns:
        Final score.

    """
    table_scores = {')': 1, ']': 2, '}': 3, '>': 4}

    score = 0
    for s in missing_parens:
        score *= 5
        score += table_scores[s]

    return score


def get_score_incomplete_chunks(chunks: list[str]) -> int:
    """Get the score of incomplete chunks only.

    Args:
        chunks: list of strings of parens.

    Returns:
        Score.

    """
    scores = []
    for chunk in chunks:
        missing_parens = get_missing_closing_parens(chunk)

        # Don't consider complete chunks
        if len(missing_parens) > 0:
            scores.append(get_score_missing_parens(missing_parens))

    return median(scores)


chunks = read_input()


# Part 1
corrupted_score = get_score_corrupted_chunks(chunks)

print(f"The final score of corrupted chunks is equal to {corrupted_score}")


# Part 2
incomplete_score = get_score_incomplete_chunks(chunks)
print(f"The final score of incomplete chunks is equal to {incomplete_score}")
