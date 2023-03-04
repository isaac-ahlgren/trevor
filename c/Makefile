

CC = gcc

CFLAGS = -g -fPIC -shared -Wall -lm

TARGET = tr_bit_extract.so

ODIR = obj
SDIR = src

OFILES = \
	eig_vec_decomp.o \
    fft.o \
    bitextract.o \
	audio.o

OBJ = $(patsubst %,$(ODIR)/%,$(OFILES))

$(ODIR)/%.o: $(SDIR)/%.c
	$(CC) $(CFLAGS) -c -g -o $@ $^


all: $(OBJ)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJ)
	cp $(TARGET) ..

test: $(OBJ)
	$(CC) -g -Wall -lm obj/* -o test

clean:
	rm ../$(TARGET) ./$(TARGET)
	rm obj/*.o
