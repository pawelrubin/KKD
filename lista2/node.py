from __future__ import annotations


class Node:
    def __init__(
        self,
        weight: int = 0,
        symbol: int = None,
        parent: Node = None,
        left: Node = None,
        right: Node = None,
    ):
        self.weight = weight
        self.symbol = symbol
        self.parent = parent
        self.left = left
        self.right = right

    @property
    def code(self):
        if self.parent:
            if self is self.parent.left:
                return self.parent.code + b"0"
            else:
                return self.parent.code + b"1"
        else:
            return b""
