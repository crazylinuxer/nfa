from typing import Dict, Set


class State:
    def __init__(self, name, is_err=False, is_end=False, local_map: Dict[str, str] = None, lambdas: Set[str] = None):
        """
        :param name: name of state
        :param local_map: dict in which keys are letters and values are state names to move automaton to
        """
        self.name = name
        self._is_err = is_err
        self._is_end = is_end
        self._local_map: Dict[str, str] = local_map if local_map and all(local_map.keys()) else dict()
        self._lambdas: Set[str] = lambdas or set()

    @property
    def is_error(self):
        return self._is_err

    @property
    def is_final(self):
        return self._is_end

    def add_jump(self, letter: str, state: str):
        if self._local_map.get(letter):
            raise ValueError("Letter " + letter + " already exists in " + self.name + " local map")
        self._local_map[letter] = state

    def next_state(self, letter: str) -> str:
        return self._local_map.get(letter) or self.name

    def is_present(self, letter: str) -> bool:
        return bool(self._local_map.get(letter))

    @property
    def used_alphabet(self) -> set:
        return set(self._local_map.keys())
