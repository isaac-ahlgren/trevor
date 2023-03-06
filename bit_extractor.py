from microphone import Microphone
import numpy as np
import ctypes

class Bit_Extractor:
    def __init__(self, sample_rate, vector_num, eig_num, bins, seconds, audio_source_name):
        self.sample_rate = sample_rate
        self.vector_num = vector_num
        self.eig_num = eig_num
        self.bins = bins
        self.microphone = Microphone(sample_rate, int(seconds*sample_rate), audio_source_name)
        
        self.eig_vecs = np.zeros(bins*eig_num, dtype=np.float32)
        
        # Custom Eigenvector decomposition algorithm
        lib = ctypes.cdll.LoadLibrary("./tr_bit_extract.so")
        alloc_args = lib.alloc_eig_args
        alloc_args.restype = ctypes.c_voidp
        alloc_args.argtypes = [ctypes.c_uint32,
                               ctypes.c_uint32,
                               ctypes.c_uint32,
                               ctypes.c_float]

        self.args = alloc_args(bins, eig_num, 10000, 0.001)

        eig_decomp = lib.eig_decomp
        eig_decomp.restype = None
        eig_decomp.argtypes = [np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"),
                               np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"),
                               np.ctypeslib.ndpointer(ctypes.c_int32, flags="C_CONTIGUOUS"),
                               ctypes.c_voidp]
        self.eig_decomp = eig_decomp            
    
    def tr_bit_extract(self, data, vector_num, eig_num, bins, throw_samples):

        vector_len = int(len(data) / vector_num)
        difference = len(data) % vector_num
        end = len(data) - difference
 
        data_matrix = np.array(np.split(data[:end], vector_num))

        print("vector_num is " + str(vector_num))
        print("shape of data is " + str(data.shape))
        print("Shape of data_matrix is " + str(data_matrix.shape))

        fft_data_matrix = np.abs(np.fft.rfft(data_matrix))[:,throw_samples:]

        fft_data_matrix  = self.bin_fft(fft_data_matrix, bins)

        cov_matrix = np.cov(fft_data_matrix.T)

        conv = np.zeros(self.eig_num, dtype=np.int32)
        flat_cov = np.array(cov_matrix.flatten(), dtype=np.float32)
        self.eig_decomp(flat_cov, self.eig_vecs, conv, self.args)

        #w, v = np.linalg.eigh(cov_matrix)

        #for i in range(eig_num):
        #    eig_vecs[i,:] = v[:,len(v) - 1 - i]

        eig_vecs = np.array(np.split(self.eig_vecs, self.eig_num))

        fixed_eig_vecs = self.fix_direction(eig_vecs)

        bits = self.gen_bits(fixed_eig_vecs)

        return bits, conv

    def bin_fft(self, fft_data_matrix, bins):
        vec_len = len(fft_data_matrix[0,:])
        vec_num = len(fft_data_matrix[:,0])
        block_sz = int(np.floor(vec_len / bins))
        ret = np.zeros((vec_num, bins))
    
        for i in range(vec_num):
            for j in range(bins):
                ret[i,j] = np.sum(fft_data_matrix[i,j*block_sz:(j+1)*block_sz])
        return ret

    def fix_direction(self, eig_vecs):
        vec_num = len(eig_vecs[:,0])
    
        for i in range(vec_num):
            eig_vec = eig_vecs[i,:]
            max_ind = np.argmax(np.abs(eig_vec))
            if eig_vec[max_ind] < 0:
                eig_vecs[i,:] *= -1
        return eig_vecs

    def gen_bits(self, eig_vecs):
        flat_vecs = eig_vecs.flatten()
        bits = ""

        max_comp = np.max(flat_vecs)
        min_comp = np.min(flat_vecs)
        mean = np.mean(flat_vecs)

        for i in range(len(flat_vecs)):
            if flat_vecs[i] > mean:
                bits += "1"
                if flat_vecs[i] > (max_comp + mean) / 2:
                    bits += "0"
                else:
                    bits += "1"
            else:
                bits += "0"
                if flat_vecs[i] > (min_comp + mean) / 2:
                    bits += "1"
                else:
                    bits += "0"
        return bits

    def extract_key(self):
        data = self.microphone.get_audio()
        #print(data) # check if the mic is actually on
        bits, conv = self.tr_bit_extract(data, self.vector_num, self.eig_num, self.bins, 10)
        return bits, conv
