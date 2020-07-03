#ifndef SCREEN_H_
#define SCREEN_H_

#include <SDL2/SDL.h>
#include "config.h"

int screen_init(SDL_Window **window, SDL_Renderer **renderer);

int screen_clear(SDL_Renderer *renderer);

int screen_drawline(SDL_Renderer *renderer, color_t *color, int posx, int pos2x,int posy, int pos2y);

int screen_destroy(SDL_Window *window, SDL_Renderer *renderer);

int set_color(color_t *color, int red, int green, int blue);

#endif
