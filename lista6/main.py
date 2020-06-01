#!/usr/bin/env python3
import differential
import gamma
from config import parse_arguments
from pass_filters import filter_bitmap
from stats import print_stats
from tga import BitMap, TGAParser


def quantify(bitmap: BitMap, k: int) -> BitMap:
    step = 256 // (2 ** k)
    pixels = []
    for row in bitmap.pixels:
        new_row = []
        for pixel in row:
            new_row.append(pixel.quantify(step))
        pixels.append(new_row)
    return BitMap(pixels, bitmap.width, bitmap.height)


def encode_bitmap_elias(bitmap: BitMap) -> bytes:
    byte_array = TGAParser.bitmap_to_array(bitmap)
    byte_array = [2 * x if x > 0 else abs(x) * 2 + 1 for x in byte_array]
    bitstring = "".join([gamma.encode(x) for x in byte_array])
    if len(bitstring) % 8 != 0:
        bitstring += "0" * (8 - (len(bitstring) % 8))
    return bytes(int(bitstring[i : i + 8], 2) for i in range(0, len(bitstring), 8))


def encode(bitmap: BitMap, k: int = 2):
    low = filter_bitmap(bitmap)
    high = filter_bitmap(bitmap, high=True)

    low_differential = differential.encode(low)
    low_encoded = encode_bitmap_elias(low_differential)
    high_quantified = quantify(high, k)

    return low, low_encoded, high, high_quantified


def to_bitstring(data: bytes) -> str:
    return "".join(format(byte, "08b") for byte in data)


def decode(encoded: bytes, width: int, height: int) -> BitMap:
    bitstring = to_bitstring(encoded)

    codes = gamma.decode(bitstring)
    bitmap_bytes_encoded = [x // 2 if x % 2 == 0 else -(x // 2) for x in codes]

    bitmap_encoded = TGAParser.sequence_to_bitmap(bitmap_bytes_encoded, width, height)
    bitmap_decoded = differential.decode(bitmap_encoded)

    return bitmap_decoded


def main():
    args = parse_arguments()

    tga = TGAParser(args.inputfile)

    if args.encode:
        bitmap = tga.get_bitmap()

        low, low_encoded, high, high_quantified = encode(bitmap, args.k)

        tga.new_tga(low, "low.tga")
        tga.new_tga_from_bytes(low_encoded, "low_encoded")
        tga.new_tga(high, "high.tga")
        tga.new_tga(high_quantified, "high_quantified.tga")

        if not args.silent:
            print("\033[4m", "LOW PASS FILTER", "\033[0m")
            print_stats(bitmap, low)
            print("\n\033[4m" "HIGH PASS FILTER, QUANTIFIED", "\033[0m")
            print_stats(bitmap, high_quantified)

    else:
        tga.new_tga(decode(tga.bitmap, tga.width, tga.height), "low_decoded.tga")


if __name__ == "__main__":
    main()
