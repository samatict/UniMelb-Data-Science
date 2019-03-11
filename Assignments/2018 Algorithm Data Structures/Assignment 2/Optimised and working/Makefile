CC=gcc
CPPFLAGS=-Wall  -Werror  -O3

# Uncomment below if you want to use debug flags
#
#CPPFLAGS=-g

SRC=puzzle.o  
TARGET=15puzzle

all: $(SRC)
	$(CC) -o $(TARGET) $(SRC) $(CPPFLAGS)

clean:
	rm -f $(TARGET) *.o
