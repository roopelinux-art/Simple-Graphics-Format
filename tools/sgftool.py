#!/usr/bin/env python3
import sys
import os
import struct
from PIL import Image

def encode_sgf(input_path, output_path):
    try:
        img = Image.open(input_path)
    except Exception as e:
        print(f"Error: Could not open image {input_path}. {e}")
        return

    width, height = img.size
    if width > 640 or height > 480:
        print(f"[*] Image is {width}x{height}. Resizing to fit 640x480 max canvas...")
        img.thumbnail((640, 480))
        width, height = img.size

    img = img.convert("RGB")
    print(f"[+] Encoding '{input_path}' to SGF Specification v1 ({width}x{height} @ 16-bit)...")

    with open(output_path, "wb") as f:
        f.write(struct.pack("<2sBBHH", b"SG", 1, 16, width, height))

        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                r_5 = (r >> 3) & 0x1F
                g_6 = (g >> 2) & 0x3F
                b_5 = (b >> 3) & 0x1F
                rgb565 = (r_5 << 11) | (g_6 << 5) | b_5
                f.write(struct.pack("<H", rgb565))

    print(f"[+] Saved SGF asset: '{output_path}' ({os.path.getsize(output_path)} bytes)")

def decode_sgf(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: SGF file '{input_path}' does not exist.")
        return

    with open(input_path, "rb") as f:
        header_data = f.read(8)
        if len(header_data) < 8:
            return
            
        magic, version, color_depth, width, height = struct.unpack("<2sBBHH", header_data)
        
        if magic != b"SG" or color_depth != 16:
            print("Error: Invalid or unsupported SGF file.")
            return

        img = Image.new("RGB", (width, height))
        for y in range(height):
            for x in range(width):
                pixel_data = f.read(2)
                if len(pixel_data) < 2: break
                rgb565 = struct.unpack("<H", pixel_data)[0]
                
                r = (((rgb565 >> 11) & 0x1F) * 255) // 31
                g = (((rgb565 >> 5) & 0x3F) * 255) // 63
                b = ((rgb565 & 0x1F) * 255) // 31
                img.putpixel((x, y), (r, g, b))

    img.save(output_path)
    print(f"[+] Decoded viewing copy saved to: '{output_path}'")

if __name__ == "__main__":
    if len(sys.argv) < 4 or sys.argv[1] not in ["-e", "-d"]:
        print("Usage:\n  Encode: python sgftool.py -e <input.png> <output.sgf>\n  Decode: python sgftool.py -d <input.sgf> <output.png>")
        sys.exit(1)
    mode, infile, outfile = sys.argv[1], sys.argv[2], sys.argv[3]
    if mode == "-e": encode_sgf(infile, outfile)
    elif mode == "-d": decode_sgf(infile, outfile)
