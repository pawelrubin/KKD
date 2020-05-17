from sys import argv


from quantization import quantify, MSE, SNR
from tga import TGAParser


def main() -> None:
    in_file, out_file, colors = argv[1:]
    in_tga = TGAParser(in_file)
    in_bitmap = in_tga.get_bitmap()

    new_bitmap = quantify(in_bitmap, 2 ** int(colors))

    mse = MSE(in_bitmap, new_bitmap)
    snr = SNR(in_bitmap, mse)
    print("MSE:", mse)
    print("SNR:", snr)

    in_tga.new_tga(new_bitmap, out_file)


if __name__ == "__main__":
    main()
