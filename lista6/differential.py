from tga import BitMap


def encode(bitmap: BitMap) -> BitMap:
    prev = bitmap.pixels[0][0]
    pixels = []
    for i, row in enumerate(bitmap.pixels):
        encoded_row = []
        for j, pixel in enumerate(row):
            if i == 0 and j == 0:
                encoded_row.append(prev)
                continue
            prev = pixel - prev
            encoded_row.append(prev)
            prev = pixel
        pixels.append(encoded_row)
    return BitMap(pixels, bitmap.width, bitmap.height)


def decode(bitmap: BitMap) -> BitMap:
    prev = bitmap.pixels[0][0]
    pixels = []
    for i, row in enumerate(bitmap.pixels):
        decoded_row = []
        for j, pixel in enumerate(row):
            if i == 0 and j == 0:
                decoded_row.append(prev)
                continue
            prev = prev + pixel
            decoded_row.append(prev)
        pixels.append(decoded_row)
    return BitMap(pixels, bitmap.width, bitmap.height)
