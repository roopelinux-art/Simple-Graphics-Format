# Simple Graphics Format (SGF)

A lightweight, uncompressed high-performance graphics format designed specifically for custom operating system GUI environments operating under VESA VBE linear framebuffers.

## Specification Layer
- **Header Geometry:** 8 bytes total
- **Maximum Resolution Capping:** 640x480 pixels
- **Native Color Map Depth:** 16-bit RGB565 High-Color
- **Endianness:** Structural Little-Endian alignment targeting x86 CPU systems natively.

## Structural Map Layout
- `0x00 - 0x01`: Magic Identifier signature (`'S'`, `'G'`)
- `0x02`: Target format specification version
- `0x03`: Color bit-depth descriptor flag (`16`)
- `0x04 - 0x05`: Geometric pixel width size 
- `0x06 - 0x07`: Geometric pixel height size
- `0x08+`: Raw linear array byte stream of packed pixels
