import numpy as np
import ctypes

def init_lib():
    lib = ctypes.cdll.LoadLibrary("../tr_bit_extract.so")
    alloc_args = lib.alloc_eig_args
    alloc_args.restype = ctypes.c_voidp
    alloc_args.argtypes = [ctypes.c_uint32,
                           ctypes.c_uint32,
                           ctypes.c_uint32,
                           ctypes.c_float]

    args = alloc_args(10, 4, 10000, 0.001)

    eig_decomp = lib.eig_decomp
    eig_decomp.restype = None
    eig_decomp.argtypes = [np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"),
                           np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"),
                           np.ctypeslib.ndpointer(ctypes.c_int32, flags="C_CONTIGUOUS"),
                           ctypes.c_voidp]
    return eig_decomp, args

def test():
    x = np.random.randint(100, size=(100))
    data_matrix = np.array(np.split(x, 10), dtype=np.float32)

    cov_matrix = np.cov(data_matrix.T)

    w, v = np.linalg.eigh(cov_matrix)

    eig_vecs = np.zeros((4, 10))

    for i in range(4):
        eig_vecs[i,:] = v[:,len(v) - 1 - i]

    eig_decomp, args = init_lib()

    eig_vecs2 = np.zeros(40, dtype=np.float32)
    flat_cov = np.array(cov_matrix.flatten(), dtype=np.float32)
    conv = np.zeros(4, dtype=np.int32)
    eig_decomp(flat_cov, eig_vecs2, conv, args)

    split_eigs = np.split(eig_vecs2, 4)

    for i in range(4):
        print(eig_vecs[i,:])
        print(split_eigs[i])
        
if __name__ == "__main__":
    test()

