from microphone import Microphone
from tr_bit_extract import tr_bit_extract

class Bit_Extractor:
    def __init__(self, sample_rate, bit_len, vec_len):
        self.sample_rate = sample_rate
        self.bit_len =  bit_len
        self.vec_len = vec_len
        self.microphone = Microphone(sample_rate, int(bit_len*vec_len))

    def extract_key(self):
        data = self.microphone.get_audio()
        return tr_bit_extract(data, self.bit_len)
