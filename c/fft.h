
#ifndef __FFT_H
#define __FFT_H

typedef float real;
typedef struct{real Re; real Im;} complex;

#ifndef PI
# define PI	3.14159265358979323846264338327950288
#endif

void fft( complex *v, int n, complex *tmp );
void complex_abs(complex *vec, real *out, uint32_t n);
#endif
