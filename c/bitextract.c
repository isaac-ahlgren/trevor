
#include <stdlib.h>
#include <stdint.h>
#include "fft.h"
#include "eig_vec_decomp.h"

#define NUM_FFT_BINS 16

/*
 * cov_mtx
 *
 * Computes the n x n covariance matrix S from n x m data matrix. 
 *
 */
static void cov_mtx(float *data, uint32_t n, uint32_t m, float *S) {

    for(int row = 0; row < n; row++) {
        for(int col = row; col < m; col++) {
            S[m*row+n] = inner_product(&data[m*col], &data[m*row], m);
            S[n*row+m] = S[m*row+n];
        }
    }
}

static void bin_fft(float *fft, uint32_t n, float *binned_fft, uint32_t nbins) {
    unsigned int i = 0;
    unsigned int binsize = n / nbins; // Num samples per bin
    for(unsigned int k = 0; k < n; k += binsize) {
        binned_fft[k] += fft[i++];
    }
}

int bit_extract(float *data, uint32_t n, uint32_t blocklen) {
    float *data_fft = malloc(sizeof(float) * n);
    float *cov_matrix = malloc(sizeof(float) * n);
    float *binned_fft = malloc(sizeof(float) * NUM_FFT_BINS * (n/blocklen)); // n/blocklen is number of rows in the data matrix
    
    // Blocklen cannot be greater than size of time series data
    if(blocklen > n) {
        return -1;
    }

    // Compute the block-wise FFT of the time series data, dumping the values
    // into data_fft. Each "block" of the input data array will become a row in
    // the data matrix. This for loop iterates over rows of the data matrix.
    for(int k = 0; k < n / blocklen; k++) {

        complex *scratch =  malloc(sizeof(complex) * blocklen); // scratchpad for fft function
        complex *complex_fft =  malloc(sizeof(complex) * blocklen); // complex fft

        // Copy a block of real-valued time series data into complex_fft array
        for(int m = 0; m < blocklen; m++) {
            complex_fft[m].Re = data[k*blocklen+m];
            complex_fft[m].Im = 0.;
        }

        // Compute FFT of a block of real-valued data
        fft( complex_fft, blocklen, scratch );

        // Find the absolute value of the FFT of the data computed above
        complex_abs(complex_fft, &data_fft[k*blocklen], blocklen);

        // Bin the FFT block
        bin_fft( &data_fft[k*blocklen], blocklen, &binned_fft[k*NUM_FFT_BINS], NUM_FFT_BINS);
    }
    cov_mtx(data_fft, n/blocklen, blocklen, cov_matrix);
    return 0;
}


extern float audiobuf[132300];

int main() {
    bit_extract(audiobuf, sizeof(audiobuf)/sizeof(float), 256);
}



