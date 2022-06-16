from microphone import Microphone
import numpy as np

class Bit_Extractor:
    def __init__(self, sample_rate, vector_num, eig_num, bins, seconds):
        self.sample_rate = sample_rate
        self.vector_num = vector_num
        self.eig_num = eig_num
        self.bins = bins
        self.microphone = Microphone(sample_rate, int(seconds*sample_rate))
    
    def tr_bit_extract(self, data, vector_num, eig_num, bins):
        eig_vecs = np.zeros((eig_num, bins))

        vector_len = int(len(data) / vector_num)
        difference = len(data) % vector_num
        end = len(data) - difference

        data_matrix = np.array(np.split(data[:end], vector_num))

        fft_data_matrix = np.abs(np.fft.rfft(data_matrix))

        fft_data_matrix  = self.bin_fft(fft_data_matrix, bins)

        cov_matrix = np.cov(fft_data_matrix.T)

        w, v = np.linalg.eigh(cov_matrix)

        for i in range(eig_num):
            eig_vecs[i,:] = v[:,len(v) - 1 - i]

        fixed_eig_vecs = self.fix_direction(eig_vecs)

        bits = self.gen_bits(fixed_eig_vecs)

        return bits

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
                    bits += "1"
                else:
                    bits += "0"
            else:
                bits += "0"
                if flat_vecs[i] > (min_comp + mean) / 2:
                    bits += "1"
                else:
                    bits += "0"
        return bits

    def extract_key(self):
        data = self.microphone.get_audio()
        print(data) # check if the mic is actually on
        bits = self.tr_bit_extract(data, self.vector_num, self.eig_num, self.bins)
        return bits
