

#include <stdio.h>
#include <errno.h>
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
        for(int col = 0; col < n; col++) {
            S[n*row+col] = inner_product(&data[m*col], &data[m*row], m);
//            S[m*col+row] = S[m*row+col];
        }
    }
}

static void bin_fft(float *fft, uint32_t n, float *binned_fft, uint32_t nbins) {
    const unsigned int binsize = n / nbins; // Num samples per bin
    for(unsigned int k = 0; k < n; k++) {
        binned_fft[k] = 0.;
        for(unsigned int i = 0; i < n/nbins; i++) {
            binned_fft[k] += fft[i + k*binsize];
        }
    }
}

/*
 * Generates the transpose of m x n mtx, storing the output in out.
 *
 */
static void transpose(float *mtx, uint32_t m, uint32_t n, float *out) {
    for(unsigned int row = 0; row < m; row++) {
        for(unsigned int col = 0; col < n; col++) {
//            float tmp = mtx[row * m + col];
            out[row * n + col] = mtx[col * n + row];
//            out[col * m + row] = tmp;
        }
    }
}

int bit_extract(float *data, uint32_t n, uint32_t blocklen) {
    const unsigned int data_matrix_rows = n/blocklen;
    float *data_fft = malloc(sizeof(float) * n);
    float *cov_matrix = malloc(sizeof(float) * n);
    float *binned_fft = malloc(sizeof(float) * NUM_FFT_BINS * data_matrix_rows); // n/blocklen is number of rows in the data matrix
    float *binned_fft_transpose = malloc(sizeof(float) * NUM_FFT_BINS * data_matrix_rows); // n/blocklen is number of rows in the data matrix

    if(data_fft == NULL || cov_matrix == NULL || binned_fft == NULL) {
        errno = ENOMEM;
        return -ENOMEM;
    }

    // Blocklen cannot be greater than size of time series data
    if(blocklen > n) {
        errno = EINVAL;
        return -EINVAL;
    }

    // Compute the block-wise FFT of the time series data, dumping the values
    // into data_fft. Each "block" of the input data array will become a row in
    // the data matrix. This for loop iterates over rows of the data matrix.
    for(int k = 0; k < data_matrix_rows; k++) {

        complex *scratch =  malloc(sizeof(complex) * blocklen); // scratchpad for fft function
        complex *complex_fft =  malloc(sizeof(complex) * blocklen); // complex fft

        if(scratch == NULL || complex_fft == NULL) {
            errno = ENOMEM;
            return -ENOMEM;
        }

        // Copy a block of real-valued time series data into complex_fft array
        for(int m = 0; m < blocklen; m++) {
            complex_fft[m].Re = data[k*blocklen+m];
            complex_fft[m].Im = 0.;
        }

        // Compute FFT of a block of real-valued data
        fft( complex_fft, blocklen, scratch );

        // Find the absolute value of the FFT of the data computed above
        complex_abs(complex_fft, &data_fft[k*blocklen], blocklen);

        // TODO: Drop the first few samples of the FFT before binning. Also dump the top half of the array because it is a mirror image of the bottom half.

        // Bin the FFT block
        bin_fft( &data_fft[k*blocklen], blocklen, &binned_fft[k*NUM_FFT_BINS], NUM_FFT_BINS);
    }
//    printf("binned fft mtx\n----------------------\n");
//    print_matrix(binned_fft, NUM_FFT_BINS, data_matrix_rows);

    // Take the transpose of the binned FFT matrix
    transpose(binned_fft, data_matrix_rows, NUM_FFT_BINS, binned_fft_transpose);
    
//    printf("binned fft mtx TRANSPOSE\n----------------------\n");
//    print_matrix(binned_fft_transpose, data_matrix_rows, NUM_FFT_BINS);
    
    cov_mtx(binned_fft_transpose, NUM_FFT_BINS, data_matrix_rows, cov_matrix);
//    printf("covariance mtx\n----------------------\n");
//    print_matrix(cov_matrix, NUM_FFT_BINS, NUM_FFT_BINS);
   

    // Do the eigenvector decomposition of the covariance matrix
    uint32_t dim_size = NUM_FFT_BINS;
    uint32_t execs = 100000;
    float err_tol = 0.00001;
    int *convergence_iterations = malloc(NUM_FFT_BINS*sizeof(int));
    float *eig_vecs = malloc(sizeof(float) * NUM_FFT_BINS * NUM_FFT_BINS);

    struct eig_decomp_args* args = alloc_eig_args(dim_size, 6, execs, err_tol);


    eig_decomp(cov_matrix, eig_vecs, convergence_iterations , args);

    printf("eigenvectors mtx\n----------------------\n");
    print_matrix(eig_vecs, NUM_FFT_BINS, NUM_FFT_BINS);
    return 0;
}


extern float audiobuf[132300];

int main() {
    bit_extract(audiobuf, sizeof(audiobuf)/sizeof(float), 256);
}



