def read_input() -> tuple[list, list]:
    """Reads input data."""
    with open("Day 8 - Seven Segment Search/input.txt", 'r') as f:
        signals = []
        digits = []
        for line in f:
            signals_line, digits_line = line.split('|')

            # Format
            signals.append(signals_line.strip().split())
            digits.append(digits_line.strip().split())

    return signals, digits


def count_easy_digits(digits):
    n_easy = 0
    for digits_line in digits:
        for d in digits_line:
            if len(d) in [2, 3, 4, 7]:
                n_easy += 1

    return n_easy


signals, digits = read_input()


# Part 1

n_easy_digits = count_easy_digits(digits)

print(f"The number of easy digits is equal to {n_easy_digits}")


# Part 2

class Display:

    def __init__(self, signals: list[str], digits: list [str]):
        self.signals = signals
        self.digits = digits

        # Keys represent the 7 possible segments of a seven-segment display
        # numbered from top to bottom and from left to right
        self.configuration = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None}

        # All signals corresponding to all possible digits. In a list for clarity
        self.signal_0 = None
        self.signal_1 = None
        self.signal_2 = None
        self.signal_3 = None
        self.signal_4 = None
        self.signal_5 = None
        self.signal_6 = None
        self.signal_7 = None
        self.signal_8 = None
        self.signal_9 = None

        # Set signals to corresponding numbers
        self.set_signal_1()
        self.set_signal_4()
        self.set_signal_7()
        self.set_signal_8()

        # Discover configurations and rest of signals. This needs to be in this order
        self.discover_segment_0()
        self.discover_segments_4_6()
        self.set_signal_9()
        self.discover_segments_2_3_5()
        self.discover_segments_1()
        self.set_signal_0()
        self.set_signal_2()
        self.set_signal_3()
        self.set_signal_5()
        self.set_signal_6()

        self.all_signals = [self.signal_0, self.signal_1, self.signal_2, self.signal_3, self.signal_4, self.signal_5,
                            self.signal_6, self.signal_7, self.signal_8, self.signal_9]

    def get_number(self):
        number = ""
        for digit in self.digits:
            for sig in self.all_signals:
                if sig == set(digit):
                    number += str(self.all_signals.index(sig))
                    continue

        return int(number)

    def get_signals_len_n(self, signal_len: int):
        return [set(x) for x in self.signals if len(x) == signal_len]

    def set_signal_1(self):
        self.signal_1 = self.get_signals_len_n(2)[0]

    def set_signal_4(self):
        self.signal_4 = self.get_signals_len_n(4)[0]

    def set_signal_7(self):
        self.signal_7 = self.get_signals_len_n(3)[0]

    def set_signal_8(self):
        self.signal_8 = self.get_signals_len_n(7)[0]

    def discover_segment_0(self):
        segment_0 = self.signal_7 - self.signal_1
        self.configuration[0] = list(segment_0)[0]

    def discover_segments_4_6(self):
        """
        If we add segments from 4 and 7 and we subtract this from all segments (the segments of 8), we have
        the two segments at the bottom left and at the bottom.

        If we intersect these two segments with digits 0, 6 and 9, we will obtain the segment at the bottom and bottom
        left positions.
        """
        # Find two possible letters
        sum_4_7 = self.signal_4 | self.signal_7
        missing_4_7 = self.signal_8 - sum_4_7

        # Intersect with signals corresponding to digits 0, 6 and 9
        signals_len_6 = self.get_signals_len_n(6)
        aux = [x & missing_4_7 for x in signals_len_6]
        segment_6 = [x for x in aux if len(x) == 1][0]
        segment_4 = [x for x in aux if len(x) == 2][0] - segment_6

        self.configuration[4] = list(segment_4)[0]
        self.configuration[6] = list(segment_6)[0]

    def set_signal_9(self):
        self.signal_9 = self.signal_8 - set(self.configuration[4])

    def discover_segments_2_3_5(self):
        """
        Knowing the signal for 9, looking at the signals of 0, 6 and 1, we can discover the top right segment and
        the central segment.
        """
        # Get only signals of 0 and 6
        signals_0_6 = []
        for sig in self.get_signals_len_n(6):
            if sig != self.signal_9:
                signals_0_6.append(sig)

        aux = [self.signal_8 - x for x in signals_0_6]
        set_aux = set([list(a)[0] for a in aux])

        segment_2 = set_aux & self.signal_1
        segment_3 = set_aux - segment_2
        segment_5 = self.signal_1 - segment_2

        self.configuration[2] = list(segment_2)[0]
        self.configuration[3] = list(segment_3)[0]
        self.configuration[5] = list(segment_5)[0]

    def discover_segments_1(self):
        """
        Knowing the rest of the segments, we can get the last one.
        """
        all_signals_minus_1 = set([x for x in self.configuration.values() if x is not None])
        segment_1 = self.signal_8 - all_signals_minus_1

        self.configuration[1] = list(segment_1)[0]

    def set_signal_0(self):
        self.signal_0 = set(self.configuration[0]) | set(self.configuration[1]) | set(self.configuration[2]) | \
                        set(self.configuration[4]) | set(self.configuration[5]) | set(self.configuration[6])

    def set_signal_2(self):
        self.signal_2 = set(self.configuration[0]) | set(self.configuration[2]) | set(self.configuration[3]) | \
                        set(self.configuration[4]) | set(self.configuration[6])

    def set_signal_3(self):
        self.signal_3 = set(self.configuration[0]) | set(self.configuration[2]) | set(self.configuration[3]) | \
                        set(self.configuration[5]) | set(self.configuration[6])

    def set_signal_5(self):
        self.signal_5 = set(self.configuration[0]) | set(self.configuration[1]) | set(self.configuration[3]) | \
                        set(self.configuration[5]) | set(self.configuration[6])

    def set_signal_6(self):
        self.signal_6 = set(self.configuration[0]) | set(self.configuration[1]) | set(self.configuration[3]) | \
                        set(self.configuration[4]) | set(self.configuration[5]) | set(self.configuration[6])


def add_all_numbers(signals, digits):
    total = 0
    for sig, dig in zip(signals, digits):
        total += Display(sig, dig).get_number()

    return total


total_amount = add_all_numbers(signals, digits)

print(f"The total amount is equal to {total_amount}")
