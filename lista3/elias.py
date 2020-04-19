from typing import List


class Gamma:
    @staticmethod
    def encode(num: int) -> str:
        """Encodes given int."""
        bitstring = format(num, "b")
        return "0" * (len(bitstring) - 1) + bitstring

    @staticmethod
    def decode(bitstring: str) -> List[int]:
        """Decodes given bitstring."""
        codes = []
        padding_count = 0
        index = 0
        while index < len(bitstring):
            if bitstring[index] == "0":
                padding_count += 1
                index += 1
            else:
                codes.append(int(bitstring[index : index + padding_count + 1], 2))
                index += padding_count + 1
                padding_count = 0
        return codes


class Delta:
    @staticmethod
    def encode(num: int) -> str:
        """Encodes given int."""
        bitstring = format(num, "b")[1:]
        return Gamma.encode(len(bitstring) + 1) + bitstring

    @staticmethod
    def decode(bitstring: str) -> List[int]:
        pass


class Omega:
    @staticmethod
    def encode(number: int) -> str:
        """Encodes given int."""
        result = "0"
        while number > 1:
            bin_number = format(number, "b")
            result = bin_number + result
            number = len(bin_number) - 1
        return result

    @staticmethod
    def decode(bitstring: str) -> List[int]:
        pass
