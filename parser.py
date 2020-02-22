from typing import TextIO, Set
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
                yield line.split()
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
            yield line.split()


class Parser:
    def __init__(self, alphabet_filename: str, input_filename: str):
        self.input_file = input_filename
        self.alphabet_file = alphabet_filename

    def _parse_transitions(self) -> Set[State]:
        pass

    def _parse_lambdas(self) -> Set[str]:
        pass

    def parse_states(self) -> Set[State]:
        pass

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
