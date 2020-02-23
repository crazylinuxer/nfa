from mapper import Map, Set
from parser import Parser


def green(inp: str) -> str:
    """Returns string in green color to print"""
    return "\033[92m" + inp + "\033[0m"


def red(inp: str) -> str:
    """Returns string in red color to print"""
    return "\033[91m" + inp + "\033[0m"


def yellow(inp: str) -> str:
    """Returns string in yellow color to print"""
    return "\033[93m" + inp + "\033[0m"


def underline(inp: str) -> str:
    """Returns underlined string to print"""
    return "\033[4m" + inp + "\033[0m"


def blue(inp: str) -> str:
    """Returns string in blue color to print"""
    return "\033[94m" + inp + "\033[0m"


class Runner:
    def __init__(self):
        parser = Parser("./data/alphabet.txt", "./data/input.txt")
        self.map = Map(parser.parse_alphabet(), parser.parse_states())

    def __call__(self, string_to_check: str, explain: bool = False) -> bool:
        current_states: Set[str] = self.map.initial_states
        if explain:
            states = list(current_states)
            states.sort()
            print("Beginning with states: " + (str().join(
                (green(state) + ' ' if self.map[state].is_final else yellow(state) + ' ') for state in states) or red("none")))
        for symbol in string_to_check:
            if symbol not in self.map.alphabet:
                if explain:
                    print("Symbol " + underline(red(symbol)) + " not found in the alphabet")
                return False
            next_states = self.map.step(current_states, symbol)
            if explain:
                print("Detected symbol " + underline(blue(symbol)))
                states = list(next_states)
                states.sort()
                print("Obtaining states: " + (str().join(
                    (green(state) + ' ' if self.map[state].is_final else yellow(state) + ' ') for state in states) or red("none")))
            current_states = next_states
        result_states = list(current_states)
        result_states.sort()
        finals = ''
        for state in result_states:
            if self.map[state].is_final:
                finals += state + ' '
        if explain:
            if finals:
                print("Ended with final states: " + green(finals.strip()))
            else:
                print("Ended without any final state")
        return bool(finals)
