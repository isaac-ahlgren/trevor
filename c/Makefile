

CC = gcc

CFLAGS = -g -fPIC -shared -Wall -lm

TARGET = tr_bit_extract.so

CFILES = \
	eig_vec_decomp.c \
    fft.c \
    bitextract.c

all: $(CFILES)
	$(CC) $(CFLAGS) -o $(TARGET) $(CFILES)
	cp $(TARGET) ..

clean:
	rm ../$(TARGET) ./$(TARGET)
