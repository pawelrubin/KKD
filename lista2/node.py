from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class Node:
    index: int
    parent: Optional[Node] = None
    left: Optional[Node] = None
    right: Optional[Node] = None
    symbol: Optional[int] = None  # symbol as byte
    frequency: int = 1  # symbol frequency

    def insert(self, symbol: int):
        assert self.symbol is None and self.left is None  # assert it is NYT
        internal = Node(index=self.index, parent=self.parent)
        internal.right = symbol_node = Node(
            index=self.index - 1, symbol=symbol, parent=internal
        )
        internal.left = self
        self.parent = internal
        self.index -= 2
        return symbol_node

    @property
    def weight(self):
        if self.symbol is None:
            if self.left:  # internal node
                return self.left.weight + self.right.weight
            else:  # NYT node
                return 0
        else:  # leaf node with a symbol
            return self.frequency

    @property
    def code(self):
        if self.parent:
            if self is self.parent.left:
                return "0" + self.parent.code
            else:
                return "1" + self.parent.code
        else:
            return "0"
