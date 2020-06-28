#Makefile 

CC = gcc
CCOPTS = -Wall -Wextra -Wno-unused -Og -march=native -pipe

YAC8EOBS = yac8e.o cpu.o video.o memory.o

all: yac8e

yac8e: $(YAC8EOBS) 
	$(CC) $^ $(CCOPTS) -o $@ 

clean:
	rm -f yac8e *.o
