from bit_extractor import Bit_Extractor
from network import Network
import time
import numpy as np

pickle_folder = "./pickled/"

class TR_Bit_Extract_System():
    def __init__(self, ip, other_ip, sample_rate, vector_num, eig_num, bins, seconds, exp_name):
        self.ip = ip
        self.other_ip = other_ip
        self.sample_rate = sample_rate
        self.vector_num = vector_num
        self.eig_num = eig_num
        self.bins = bins
        self.seconds = seconds
        self.net = Network(ip, other_ip)
        self.be = Bit_Extractor(sample_rate, vector_num, eig_num, bins, seconds)
        self.exp_name = exp_name
        self.count = 0

    def compare_bits(self, bits1, bits2):
        tot = 0
        for i in range(len(bits1)):
            if bits1[i] == bits2[i]:
                tot += 1
        return tot / len(bits1)

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
            np.save(pickle_folder + self.exp_name + "_other_mykey_" + str(self.count) + "_pickled.npy", key)
            time.sleep(15)
            self.net.send_bits(key)
            self.count += 1

    def bit_agreement_exp_host(self):
        while (1):
            time.sleep(15)
            self.net.send_start()
            key = self.extract_context()
            np.save(pickle_folder + self.exp_name + "_host_mykey_" + str(self.count) + "_pickled.npy", key)
            other_bits = self.net.get_bits(len(key))
            agreement = self.compare_bits(key, other_bits)
            print("Agreement Rate: " + str(agreement))
            self.count += 1
