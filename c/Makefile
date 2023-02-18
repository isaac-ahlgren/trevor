

CC = gcc

CFLAGS = -g -fPIC -shared -Wall -lm

TARGET = tr_bit_extract.so

CFILES = \
	eig_vec_decomp.c \
    portaudio.c

all: $(CFILES)
	$(CC) $(CFLAGS) -o $(TARGET) $(CFILES)
	mv $(TARGET) ..

clean:
	rm ../$(TARGET)
