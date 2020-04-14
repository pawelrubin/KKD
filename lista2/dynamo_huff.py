from typing import Dict

from node import Node


class Tree:
    def __init__(self):
        self.root = self.NYT = Node(index=256, weight=0)
        self.symbols: Dict[int, Node] = {}  # dict for seen symbols

    def _rebalance(self, node: Node):
        pass

    def _swap_nodes(self, node1: Node, node2: Node):
        assert node1.parent is not None and node2.parent is not None
        node1.parent, node2.parent = node2.parent, node1.parent

        if node1.parent.left is node2:
            node1.parent.left = node1
        else:
            node1.parent.right = node1

        if node2.parent.left is node1:
            node2.parent.left = node2
        else:
            node2.parent.right = node2

    def update(self, symbol: int):
        if symbol in self.symbols:
            node = self.symbols[symbol]
            self.symbols[symbol].frequency += 1
        else:
            node = self.NYT.insert(symbol)
            self.symbols[symbol] = node
        self._rebalance(node)

    def get_code(self, symbol: int):
        if symbol not in self.symbols:
            return self.NYT.code + "{:08b}".format(symbol)
        else:
            return self.symbols[symbol].code


class AdaptiveHuffman:
    def __init__(self):
        self.tree = Tree()

    def encode(self, data: str):
        result = ""
        for c in data:
            result += self.tree.get_code(c)
            self.tree.update(c)
