#include <SDL2/SDL.h>
#include "config.h"

int screen_init(SDL_Window **window, SDL_Renderer **renderer) {
    if(SDL_Init(SDL_INIT_VIDEO) < 0) {
            printf( "SDL could not initialize! SDL_Error: %s\n", SDL_GetError() );
            return -1;
    }

    SDL_CreateWindowAndRenderer(SCREEN_WIDTH, SCREEN_LENGTH, 0, &(*window), &(*renderer));

    if( window == NULL ) {
            printf( "Window could not be created! SDL_Error: %s\n", SDL_GetError() );
            return -1;
        }
    return 1;
}

int screen_clear(SDL_Renderer *renderer) {
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, SDL_ALPHA_OPAQUE);
    SDL_RenderClear(renderer);
    SDL_RenderPresent(renderer);
    return 1;
}

int screen_drawline(SDL_Renderer *renderer, color_t *color, int posx, int pos2x,int posy, int pos2y){
    //TODO: Check integrety of color
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, SDL_ALPHA_OPAQUE);
    SDL_RenderClear(renderer);
    //SDL_SetRenderDrawColor(renderer, color->red, color->green, color->blue, SDL_ALPHA_OPAQUE);
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, SDL_ALPHA_OPAQUE);
    SDL_RenderDrawLine(renderer, posx, pos2x, posy, pos2y);
    SDL_RenderPresent(renderer);
    return 1;
}

int screen_destroy(SDL_Window *window, SDL_Renderer *renderer) {
    SDL_DestroyWindow(window);
    SDL_DestroyRenderer(renderer);
    SDL_Quit();
    return 1;
}

int set_color(color_t *color, int red, int green, int blue) {
    color->red = red;
    color->green = green;
    color->blue = blue;
    return 1;
}
