from typing import List


class Fib:
    @staticmethod
    def _encode_sequence(number: int) -> List[int]:
        sequence = []
        a, b = 0, 1

        while a <= number:
            sequence.append(a)
            a, b = b, a + b

        return sequence[2:]

    @staticmethod
    def _decode_sequence(number: int) -> List[int]:
        sequence = []
        a, b = 0, 1

        for _ in range(number + 2):
            sequence.append(a)
            a, b = b, a + b

        return sequence[2:]

    @staticmethod
    def encode(number: int) -> str:
        """Encodes given int."""
        sequence = Fib._encode_sequence(number)
        result = ["0" for _ in sequence]

        while number > 0:
            i, x = [(i, x) for i, x in enumerate(sequence) if x <= number][-1]
            result[i] = "1"
            number %= x
        result.append("1")
        return "".join(result)

    @staticmethod
    def decode(bitstring: str) -> List[int]:
        codes = [x + "1" for x in bitstring.split("11")][0:-1]
        sequence = Fib._decode_sequence(max([len(x) for x in codes]))
        return [
            sum([sequence[i] if x == "1" else 0 for i, x in enumerate(code)])
            for code in codes
        ]
