from __future__ import annotations

from typing import Optional


class Node:
    def __init__(
        self,
        weight: int = 0,
        symbol: Optional[int] = None,
        parent: Optional[Node] = None,
        left: Optional[Node] = None,
        right: Optional[Node] = None,
    ):
        self.weight = weight
        self.symbol = symbol
        self.parent = parent
        self.left = left
        self.right = right

    @property
    def code(self) -> bytes:
        if self.parent:
            if self is self.parent.left:
                return self.parent.code + b"0"
            else:
                return self.parent.code + b"1"
        else:
            return b""
