#ifndef _TR_BIT_EXTRACT_H
#define _TR_BIT_EXTRACT_H

#include "fft.h"
#include "eig_vec_decomp.h"

struct tr_bit_extract_args {
    struct fft_args* f_args;
    struct eig_decomp_args* e_args;
    uint32_t vec_len;
    uint32_t vec_num;
    float* fft_buf;
    float* cov_mat;
    float* cov_mat_means;
    float* eig_vec;
};

void tr_bit_extract_get_samples(float* input_buffer, float* output_buffer, void* args);
void* alloc_tr_bit_extract_args(uint32_t vec_len, uint32_t vec_num, uint32_t eig_execs, float eig_error);
void free_tr_bit_extract_args(struct tr_bit_extract_args* args);

#endif
