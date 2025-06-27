from PIL import Image

def encode_message(image_path, message, output_path):
    img = Image.open(image_path)
    bin_msg = ''.join([format(ord(c), '08b') for c in message]) + '00000000'
    pixels = img.load()

    idx = 0
    for y in range(img.height):
        for x in range(img.width):
            if idx < len(bin_msg):
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(bin_msg[idx])
                pixels[x, y] = (r, g, b)
                idx += 1
    img.save(output_path)
    print("✅ Message encoded.")

def decode_message(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    bits = ""
    for y in range(img.height):
        for x in range(img.width):
            bits += str(pixels[x, y][0] & 1)
            if bits[-8:] == '00000000':
                chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits)-8, 8)]
                return ''.join(chars)
    return ""

# Example
# encode_message("input.png", "HELLO WORLD", "encoded.png")
# print(decode_message("encoded.png"))
