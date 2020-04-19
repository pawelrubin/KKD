import elias
import fib

def handle_padding(bitstring, mode="encode"):
    if mode == "encode":
        bitstring = "000" + bitstring
        if len(bitstring) % 8 != 0:
            padding = "0" * abs(len(bitstring) % -8)
            bitstring += padding
            bitstring = format(len(padding), "03b") + bitstring[3:]
    elif mode == "decode":
        padding = int(bitstring[:3], 2)
        bitstring = bitstring[3:-padding] if padding > 0 else bitstring[3:]
    return bitstring


def to_bitstring(data: bytes) -> str:
    return "".join(format(byte, "08b") for byte in data)


def lzw_compress(in_file_name, out_file_name, coding):
    # read bytes from file
    with open(in_file_name, "rb") as in_file:
        in_bytes = in_file.read()

    dictionary = {chr(i): i for i in range(256)}
    result = []
    c = chr(in_bytes[0])

    for byte in in_bytes[1:]:
        s = chr(byte)
        cs = c + s
        if cs in dictionary:
            c += s
        else:
            result.append(dictionary[c])
            dictionary[cs] = len(dictionary)
            c = s

    result.append(dictionary[c])

    code = "".join(map(coding.encode, result))

    # add padding
    code = handle_padding(code, mode="encode")

    # write bytes to file
    with open(out_file_name, "wb") as out_file:
        out_file.write(
            bytes(int(code[i : i + 8].encode(), 2) for i in range(0, len(code), 8))
        )


def lzw_decompress(in_file_name, out_file_name, coding):
    from io import StringIO
    
    # read bytes from file
    with open(in_file_name, "rb") as in_file:
        in_bitstring = handle_padding(to_bitstring(in_file.read()), mode="decode")

    dictionary = {i: format(i, "08b") for i in range(256)}

    codes = coding.decode(in_bitstring)
    prev_code = codes[0]
    curr_char = ""
    result = StringIO()
    result.write(dictionary[prev_code])

    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        else:
            entry = dictionary[prev_code] + curr_char

        result.write(entry)
        curr_char = entry[:8]
        dictionary[len(dictionary)] = dictionary[prev_code] + curr_char
        prev_code = code

    result = result.getvalue()

    # write bytes to file
    with open(out_file_name, "wb") as out_file:
        out_file.write(
            bytes(int(result[i : i + 8], 2) for i in range(0, len(result), 8))
        )


def main():
    import argparse

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--compress", action="store_true")
    group.add_argument("--decompress", action="store_true")
    parser.add_argument("inputfile")
    parser.add_argument("outputfile")
    parser.add_argument("coding", choices=["gamma", "delta", "omega", "fib"])

    args = parser.parse_args()

    if args.coding == "gamma":
        coding = elias.Gamma
    elif args.coding == "delta":
        coding = elias.Delta
    elif args.coding == "omega":
        coding = elias.Omega
    else:
        coding = fib.Fib

    if args.compress:
        lzw_compress(args.inputfile, args.outputfile, coding)
    else:
        lzw_decompress(args.inputfile, args.outputfile, coding)


if __name__ == "__main__":
    main()
