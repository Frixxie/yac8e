#include <stdlib.h>
#include <stdarg.h>
#include <stdio.h>
#include <assert.h>
#include <getopt.h>
#include <string.h>
#include "screen.h"
#include "config.h"

char *progname;

/* prototypes of local functions */
static int init_opts(options_t *opts);
static void print_help(void);

int main(int argc, char **argv) {
    /* Option handling */
    progname = argv[0];
    options_t opts;
    int ret = init_opts(&opts);
    assert(ret);

    char input[INPUT_FILELEN];
    memset(input, 0, INPUT_FILELEN);

    /* Using getopts for better options implementations */
    int c;
    int num_options = 0;
    static struct option long_options[] = {
        {"inputfile", 1, NULL, (int)'i'},
        {"extended",  0, NULL, (int)'e'},
        {"test",      0, NULL, (int)'t'},
        {"help",      0, NULL, (int)'h'},
        {NULL,        0, NULL, 0},
    };
    while((c = getopt_long(argc, argv, "i:eth", long_options, NULL)) != -1) {
        switch(c) {
            case 'i':
                memcpy(input, optarg, strlen(optarg));
                opts.inputfile = 1;
                ++num_options;
                break;
            case 'e':
                opts.extended = 1;
                ++num_options;
                break;
            case 't':
                opts.test = 1;
                ++num_options;
                break;
            case 'h':
                opts.help = 1;
                ++num_options;
                break;
            default:
                break;
        }
    }

    if(opts.help) {
        printf("helpflag is set printing help\n");
        print_help();
    }

    /* if(!opts.inputfile) { */
    /*     print_help(); */
    /*     return -1; */
    /* } */

    printf("Input file: %d, %s, Extended: %d, Test: %d, Help: %d\n", opts.inputfile, input, opts.extended, opts.test, opts.help);


    SDL_Window *window = NULL;
    SDL_Renderer *renderer = NULL;

    if(screen_init(&window, &renderer) < 1) {
        exit(-1);
    }

    screen_clear(renderer);

    color_t color;

    set_color(&color, 255, 255, 255);

    screen_drawline(renderer, &color, 0, 320, 160, 160);

    SDL_Delay(2000);

    screen_destroy(window, renderer);
    return 0;
}

static int init_opts(options_t *opts) {
    opts->inputfile = 0;
    opts->test = 0;
    opts->extended = 0;
    opts->help = 0;
    return 1;
}

static void print_help(void) {
    printf("This is %s, usage: %s\n", progname, ARGS);
}
