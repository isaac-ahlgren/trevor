

CC = gcc

CFLAGS = -g -fPIC -shared -Wall -lm -Xlinker --verbose

LIBS = libkissfft-float.a

TARGET = tr_bit_extract.so

CFILES = \
	fft.c \
	eig_vec_decomp.c \
	tr_bit_extract.c \

all: $(CFILES)
	$(CC) $(CFLAGS) -o $(TARGET) $(CFILES) $(LIBS)
	mv $(TARGET) ..

clean:
	rm ../$(TARGET)
