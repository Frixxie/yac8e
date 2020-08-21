#ifndef CONFIG_H_
#define CONFIG_H_

#include<SDL2/SDL.h>

enum
{
   INPUT_FILELEN = 256,
   SCREEN_WIDTH = 640,
   SCREEN_LENGTH = 320,
};

#define ARGS "[--help] [--extended] [--test] [--inputfile] <inputfile>"

/* Global variables */

typedef struct options options_t;
struct options {
    int inputfile;
    int test;
    int extended;
    int help;
};

typedef struct color color_t;
struct color {
    int red, green, blue;
};

#endif
