#Makefile 

CC = gcc
CFLAGS = -Wall -Wextra -Wno-unused -O2 -g -march=native -pipe 

YAC8EOBS = yac8e.o screen.o
		   # cpu.o video.o memory.o
		   #
all: yac8e

yac8e: $(YAC8EOBS) 
	$(CC) $^ $(CCOPTS) -lSDL2 -o $@ 

clean:
	rm -f yac8e *.o
