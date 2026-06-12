#ifndef SGF_H
#define SGF_H

#include <stdint.h>

/* Force compiler layout to pack variables tightly with zero structural padding bytes */
#pragma pack(push, 1)
typedef struct {
    char magic[2];        /* Identification signature: 'S', 'G' */
    uint8_t version;      /* Layout version number (0x01) */
    uint8_t color_depth;  /* Target bit depth: 8, 16, or 32 bits */
    uint16_t width;       /* Canvas physical pixel width (Max 640) */
    uint16_t height;      /* Canvas physical pixel height (Max 480) */
} sgf_header_t;
#pragma pack(pop)

/* Architectural Status Return Codes */
#define SGF_SUCCESS          0
#define SGF_ERROR_INVALID    1
#define SGF_ERROR_VERSION    2
#define SGF_ERROR_DEPTH      3
#define SGF_ERROR_OVERSIZE   4

#endif /* SGF_H */
