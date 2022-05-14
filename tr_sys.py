from bit_extractor import Bit_Extractor
from network import Network
import time
import numpy as np

pickle_folder = "./pickled/"

class TR_Bit_Extract_System():
    def __init__(self, ip, sample_rate, bit_length, vector_length, exp_name):
        self.ip = ip
        self.sample_rate = sample_rate
        self.bit_length = bit_length
        self.vector_length = vector_length
        self.net = Network(ip)
        self.be = Bit_Extractor(sample_rate, bit_length, vector_length)
        self.exp_name = exp_name
        self.count = 0

    def extract_context(self):
        print()
        print("Extracting Audio")
        key = self.be.extract_key()
        print("Generated key: " + str(key))
        print()
        return key

    def bit_agreement_exp_dev(self):
        while (1):
            self.net.get_start()
            key = self.extract_context()
            np.save(pickle_folder + self.exp_name + "_mykey_" + str(self.count) + "_pickled.npy", key)
            self.count += 1

    def bit_agreement_exp_host(self):
        while (1):
            time.sleep(15)
            self.net.send_start()
            key = self.extract_context()
            np.save(pickle_folder + self.exp_name + "_mykey_" + str(self.count) + "_pickled.npy", key)
            self.count += 1
