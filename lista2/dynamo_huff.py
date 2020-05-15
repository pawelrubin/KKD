import math
from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional

from node import Node


class Tree:
    def __init__(self) -> None:
        self.root = self.NYT = Node()
        self.nodes: List[Node] = []
        self.seen: List[Optional[Node]] = [None] * 256

    def _get_largest(self, weight: int) -> Optional[Node]:
        for node in self.nodes:
            if node.weight == weight:
                return node
        return None

    def _rebalance(self, node: Node) -> None:
        while node is not None:
            largest = self._get_largest(node.weight)

            if (
                node is not largest
                and node is not largest.parent
                and largest is not node.parent
            ):
                self._swap_nodes(node, largest)

            node.weight += 1
            node = node.parent

    def _swap_nodes(self, node1: Node, node2: Node) -> None:
        i1, i2 = self.nodes.index(node1), self.nodes.index(node2)
        self.nodes[i1], self.nodes[i2] = self.nodes[i2], self.nodes[i1]

        node1.parent, node2.parent = node2.parent, node1.parent

        if node1.parent.left is node2:
            node1.parent.left = node1
        else:
            node1.parent.right = node1

        if node2.parent.left is node1:
            node2.parent.left = node2
        else:
            node2.parent.right = node2

    def update(self, symbol: int) -> None:
        node = self.seen[symbol]

        if node is None:
            symbol_node = Node(symbol=symbol, weight=1)
            internal_node = Node(
                weight=1, parent=self.NYT.parent, left=self.NYT, right=symbol_node
            )

            symbol_node.parent = internal_node
            self.NYT.parent = internal_node

            if internal_node.parent is not None:
                internal_node.parent.left = internal_node
            else:
                self.root = internal_node

            self.nodes.append(internal_node)
            self.nodes.append(symbol_node)

            self.seen[symbol] = symbol_node
            node = internal_node.parent

        self._rebalance(node)

    def get_code(self, symbol: int) -> bytes:
        if (node := self.seen[symbol]) is None:
            return self.NYT.code + "{:08b}".format(symbol).encode()
        else:
            return node.code


def bitstring(data: bytes) -> str:
    return "".join(format(byte, "08b") for byte in data)


def entropy(text) -> float:
    stats = defaultdict(int)

    for c in text:
        stats[c] += 1

    result = sum(stat * math.log2(stat) for stat in stats.values())

    return math.log2(len(text)) - (result / len(text))


class AdaptiveHuffman:
    def __init__(self) -> None:
        self.tree = Tree()

    def encode(self, data: bytes) -> bytes:
        result = b"000"
        for c in data:
            code = self.tree.get_code(c)
            result += code
            self.tree.update(c)

        if len(result) % 8 != 0:
            padding = b"0" * abs(len(result) % -8)
            result += padding
            result = format(len(padding), "03b").encode() + result[3:]
        return result

    def decode(self, data: bytes) -> str:
        bits = bitstring(data)
        padding = int(bits[:3], 2)

        bits = bits[3 : -int(bits[:3], 2)] if padding != 0 else bits[3:]

        result = ""
        symbol = int(bits[:8], 2)
        result += chr(symbol)
        self.tree.update(symbol)

        node = self.tree.root

        i = 8
        while i < len(bits):
            node = node.left if bits[i] == "0" else node.right
            symbol = node.symbol

            if symbol:
                if node is self.tree.NYT:
                    symbol = int(bits[i + 1 : i + 9], 2)
                    i += 8

                result += chr(symbol)
                self.tree.update(symbol)
                node = self.tree.root

            i += 1

        return result


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--encode", action="store_true")
    group.add_argument("--decode", action="store_true")
    parser.add_argument("inputfile")
    parser.add_argument("outputfile")

    args = parser.parse_args()

    if args.encode:
        with open(args.inputfile, "rb") as inputf, open(
            args.outputfile, "wb"
        ) as outputf:
            text = inputf.read()
            result = AdaptiveHuffman().encode(inputf.read())
            as_bytes = bytes(
                int(result[i : i + 8], 2) for i in range(0, len(result), 8)
            )
            outputf.write(as_bytes)
            print(f"Entropy:    {entropy(text)}")
            print(f"Avg len:    {len(result) / len(text)}")
            print(f"Compresion: {len(text) / len(result) / 8}")

    else:
        with open(args.inputfile, "rb") as inputf, open(
            args.outputfile, "w"
        ) as outputf:
            result = AdaptiveHuffman().decode(inputf.read())
            outputf.write(result)


if __name__ == "__main__":
    main()
