import numpy as np
from numpy.linalg import norm

EIG_ERROR_TOL = 0.01
MAX_ITERATIONS = 1000

def eig_decomp(X, vec_len, c, tol):

    r = np.ones(vec_len)
    r = r / norm(r, 2)

    for i in range(c):
        s = X.dot(r)
        s = s / norm(s, 2)
        error = norm(s - r, 1)
        r = s
        if error < tol:
            break
    return r

def gen_bits(proj_data):
    med = np.median(proj_data)
    bits = np.zeros(len(proj_data), np.bool)
    for i in range(len(proj_data)):
        if proj_data[i] > med:
            bits[i] = True
        else:
            bits[i] = False
    return bits

def tr_bit_extract(data, vec_num):
    data_matrix = np.array(np.split(data, vec_num), dtype=np.float32)
    vec_len = len(data) // vec_num

    fft_data_matrix = np.abs(np.fft.fft(data_matrix))

    cov_mat = np.cov(fft_data_matrix.T)

    eig_vec = eig_decomp(cov_mat, vec_len, MAX_ITERATIONS, EIG_ERROR_TOL)

    eig_vec = np.abs(eig_vec)

    proj_data = (eig_vec.T).dot(fft_data_matrix.T)

    bits = gen_bits(proj_data)

    return bits
