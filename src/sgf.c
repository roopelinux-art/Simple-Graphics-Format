#include "sgf.h"

/* Default address where VESA VBE maps the 16-bit Linear Frame Buffer */
#define VBE_CTRL_FRAMEBUFFER 0xE0000000

int draw_sgf_native(int screen_x, int screen_y, const uint8_t* file_data, uint32_t file_size) {
    sgf_header_t* header = (sgf_header_t*)file_data;

    /* 1. Complete Binary Structure Validation */
    if (header->magic[0] != 'S' || header->magic[1] != 'G') return SGF_ERROR_INVALID;
    if (header->version > 1) return SGF_ERROR_VERSION;
    if (header->color_depth != 16) return SGF_ERROR_DEPTH;
    if (header->width > 640 || header->height > 480) return SGF_ERROR_OVERSIZE;

    /* 2. Boundary Integrity Check */
    uint32_t expected_size = sizeof(sgf_header_t) + (header->width * header->height * 2);
    if (file_size != expected_size) return SGF_ERROR_INVALID;

    /* 3. Setup streaming pointers right past the 8-byte header offset */
    uint16_t* pixel_stream = (uint16_t*)(file_data + sizeof(sgf_header_t));
    uint16_t* vga_mem = (uint16_t*)VBE_CTRL_FRAMEBUFFER;

    /* 4. Draw loop with safe hardware-clipping boundaries */
    for (uint16_t y = 0; y < header->height; y++) {
        for (uint16_t x = 0; x < header->width; x++) {
            int dest_x = screen_x + x;
            int dest_y = screen_y + y;

            /* Clip everything cleanly to the active VBE 640x480 resolution */
            if (dest_x >= 0 && dest_x < 640 && dest_y >= 0 && dest_y < 480) {
                vga_mem[(dest_y * 640) + dest_x] = pixel_stream[(y * header->width) + x];
            }
        }
    }
    return SGF_SUCCESS;
}
