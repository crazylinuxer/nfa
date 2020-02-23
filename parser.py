from typing import TextIO, Set, Dict
from mapper import State


class SimpleLineGenerator:
    def __init__(self, file: TextIO):
        self._stay = False
        self.file = file
        self._last_line = ''

    def __call__(self):
        while True:
            if self._stay:
                self._stay = False
            else:
                self._last_line = self.file.readline()
            if self._last_line:
                yield self._last_line
            else:
                return

    def hold_on(self):
        self._stay = True


class SmartRange:
    def __init__(self, start: int = 0):
        self.i = start
        self._count = 0

    def __call__(self, count: int):
        self._count = count
        while self.i < self._count:
            yield self.i
            self.i += 1

    def dec(self):
        self.i -= 1
        self._count -= 1


def transitions_filter(file: TextIO):
    file.seek(0)
    started = False
    line_reader = SimpleLineGenerator(file)
    try:
        for line in line_reader():
            line = line.strip()
            if line == '' or line[0] == "#":
                continue
            if line.lower() == "transitions":
                if started:
                    raise RuntimeError("Detected more than one 'TRANSITIONS' section. Aborting.")
                else:
                    started = True
                continue
            if line.lower() == "lambdas":
                for skipped_line in line_reader():
                    if skipped_line.strip().lower() == "transitions":
                        if started:
                            raise RuntimeError("Detected more than one 'TRANSITIONS' section. Aborting.")
                        else:
                            line_reader.hold_on()
                            break
            if started and line.lower() != "lambdas":
                yield line.replace(",", ' ').split()
    finally:
        if not started:
            raise RuntimeError("Can not find 'TRANSITIONS' section. Aborting.")


def lambdas_filter(file: TextIO):
    file.seek(0)
    started = False
    line_reader = SimpleLineGenerator(file)
    for line in line_reader():
        line = line.strip()
        if line == '' or line[0] == "#":
            continue
        if line.lower() == "lambdas":
            started = True
            continue
        if line.lower() == "transitions":
            started = False
            continue
        if started:
            yield line.replace(",", ' ').split()


class Parser:
    def __init__(self, alphabet_filename: str, input_filename: str):
        self.input_file = input_filename
        self.alphabet_file = alphabet_filename

    def _parse_transitions(self) -> Dict[str, State]:
        result = dict()
        counter = 0
        file = open(self.input_file, "r")
        try:
            alphabet = list(self.parse_alphabet())
            alphabet.sort()
            for line in transitions_filter(file):
                counter += 1
                line_counter = SmartRange()
                for i in line_counter(len(line)):
                    if line[i] == '':
                        del line[i]
                        line_counter.dec()
                if len(line) < 2:
                    raise RuntimeError("Syntax error while parsing line " + str(counter))
                transitions = dict()
                states = set()
                current_letter = 0
                for state in line[2:]:
                    if states:
                        if state.lower() == "null":
                            raise RuntimeError("Cannot understand null in state set")
                        if state[-1] == '}':
                            states.add(state.strip('}'))
                            try:
                                transitions[alphabet[current_letter]] = states
                            except IndexError:
                                raise RuntimeError("State " + line[0] + " has more state sets than letters in the alphabet")
                            states = set()
                            current_letter += 1
                        else:
                            states.add(state)
                    else:
                        if state.lower() == "null":
                            current_letter += 1
                            continue
                        if state[0] == '{':
                            states.add(state.strip('{'))
                        else:
                            try:
                                transitions[alphabet[current_letter]] = {state}
                            except IndexError:
                                raise RuntimeError("State " + line[0] + " has more state sets than letters in the alphabet")
                            current_letter += 1
                result[line[0]] = State(line[0], (line[1] == '1'), transitions)
            return result
        finally:
            file.close()

    def _add_lambdas(self, states: Dict[str, State]) -> None:
        file = open(self.input_file, "r")
        try:
            for line in lambdas_filter(file):
                if not states.get(line[0], False):
                    raise RuntimeError("Cannot find state " + line[0] + " in TRANSITIONS section")
                states[line[0]].add_lambdas(set(line[1:]))
        finally:
            file.close()

    def parse_states(self) -> Dict[str, State]:
        result = self._parse_transitions()
        self._add_lambdas(result)
        return result

    def parse_alphabet(self) -> Set[str]:
        parsed = set()
        with open(self.alphabet_file) as file:
            result = file.read().strip().replace(',', ' ').replace('.', ' ').strip().split()
            for letter in result:
                if len(letter) > 1:
                    raise RuntimeError("Error while parsing alphabet: letter must be a single char")
                if len(letter) == 1:
                    parsed.add(letter)
        return parsed
