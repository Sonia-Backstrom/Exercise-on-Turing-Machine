from __future__ import annotations

import sys
from collections.abc import Sequence
from enum import Enum, auto


class Symbol(Enum):
    """The complete finite tape alphabet."""

    BLANK = auto()
    ONE = auto()
    START = auto()
    MARK = auto()
    # fixed, finite number of marker symbols added here.


class Tape:
    """A one-sided, unbounded tape for the programming exercise.

    The dynamically growing list is part of the tape implementation. Your
    machine code must not use input-dependent containers of its own.
    """

    def __init__(self) -> None:
        self._cells: list[Symbol] = [Symbol.BLANK]
        self._position = 0

    @classmethod
    def from_arguments(cls, arguments: Sequence[str]) -> Tape:
        """Read the sole command-line argument, which must have form a^n."""
        if len(arguments) != 2:
            cls.reject("expected exactly one unary argument")

        tape = cls()
        first_cell = True

        for value in arguments[1]:
            if value != "a":
                cls.reject("the input must contain only the symbol 'a'")

            if first_cell:
                tape._cells[0] = Symbol.ONE
                first_cell = False
            else:
                tape._cells.append(Symbol.ONE)
        return tape

    def read(self) -> Symbol:
        return self._cells[self._position]

    def write(self, symbol: Symbol) -> None:
        """Write a nonblank symbol; the blank symbol is read-only."""
        if not isinstance(symbol, Symbol):
            raise TypeError("a tape cell must contain a member of Symbol")
        if symbol is Symbol.BLANK:
            self.reject("the blank symbol is read-only")
        self._cells[self._position] = symbol

    def move_left(self) -> None:
        if self._position == 0:
            self.reject("left move at the start of the tape")
        self._position -= 1

    def move_right(self) -> None:
        self._position += 1
        if self._position == len(self._cells):
            self._cells.append(Symbol.BLANK)

    def debug(self) -> None:
        """Optional debugging aid; it is not a Turing-machine operation."""
        print("---------------", file=sys.stderr)
        for index, symbol in enumerate(self._cells):
            head = "-> " if index == self._position else "   "
            print(f"{head}{symbol.name}", file=sys.stderr)
        print("---------------", file=sys.stderr)

    @staticmethod
    def accept() -> None:
        print("[accept]")
        raise SystemExit(0)

    @staticmethod
    def reject(reason: str | None = None) -> None:
        if reason is not None:
            print(f"reject: {reason}", file=sys.stderr)
        print("[reject]")
        raise SystemExit(0)
