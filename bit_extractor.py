from microphone import Microphone
import ctypes
import numpy as np

MAX_EIG_EXEC = 1000
EIG_ERR = 0.01

class Bit_Extractor:
    def __init__(self, sample_rate, bit_len, vec_len):
        self.sample_rate = sample_rate
        self.bit_len =  bit_len
        self.vec_len = vec_len
        self.microphone = Microphone(sample_rate, int(bit_len*vec_len))
        self.pca_samples = np.zeros(bit_len, dtype=np.float32)
        
        lib = ctypes.cdll.LoadLibrary("./tr_bit_extract.so")
        
        alloc_tr_bit_extract = lib.alloc_tr_bit_extract_args
        alloc_tr_bit_extract.restype = ctypes.c_voidp
        alloc_tr_bit_extract.argtypes = [ctypes.c_uint32,
                                         ctypes.c_uint32,
                                         ctypes.c_uint32,
                                         ctypes.c_float]
        
        self.args = alloc_tr_bit_extract(vec_len, bit_len, MAX_EIG_EXEC, EIG_ERR)
        
        # function for extracting pca samples
        self.bit_extract = lib.tr_bit_extract_get_samples
        self.bit_extract.restype = None
        self.bit_extract.argtypes = [np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"),
                                     np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"),
                                     ctypes.c_voidp]
                                  
    def gen_bits(self, proj_data):
        med = np.median(proj_data)
        bits = np.zeros(len(proj_data))
        for i in range(len(proj_data)):
           if proj_data[i] > med:
               bits[i] = 1;
           else:
               bits[i] = 0;
        return bits
        

    def extract_key(self):
        data = self.microphone.get_audio()
        self.bit_extract(data, self.pca_samples, self.args)
        return self.gen_bits(self.pca_samples)
