import argparse
from argparse import Namespace


def parse_arguments() -> Namespace:
    parser = argparse.ArgumentParser(
        description="Quantization, differential encoding and low/high-pass filters."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--encode",
        action="store_true",
        help=(
            """
        Encode given tga file. It will create 4 files:
            1) low.tga - low-pass filter applied
            2) low_encoded - low.tga encoded with differential encoding and Elias gamma encoding
            3) high.tga - high-pass filter applied
            4) high_quantified.tga - high-pass filter with quantization 
        """
        ),
    )
    group.add_argument(
        "--decode",
        action="store_true",
        help=(
            """
        Decode given file that was previously encoded with differential and 
        elias gamma encodings (low_encoded).
        """
        ),
    )
    parser.add_argument("inputfile", help="Path to the tga file.")
    parser.add_argument(
        "-k",
        default=2,
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7],
        help="Number of bits for color in quantization.",
    )
    parser.add_argument(
        "--silent", action="store_true", help="Silent mode. Won't print statistics.",
    )

    return parser.parse_args()
