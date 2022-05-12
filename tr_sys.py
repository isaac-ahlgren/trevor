from bit_extractor import Bit_Extractor
from network import Network
from error_codes import Error_Corrector
import time
import numpy as np

class TR_Bit_Extract_System():
    def __init__(self, ip, sample_rate, bit_length, vector_length):
        self.ip = ip
        self.sample_rate = sample_rate
        self.bit_length = bit_length
        self.vector_length = vector_length
        self.net = Network(ip)
        self.be = Bit_Extractor(sample_rate, bit_length, vector_length)
        self.corrector = Error_Corrector()

    def extract_context(self):
        print()
        print("Extracting Audio")
        key = self.be.extract_key()
        print("Generated key: " + str(key))
        print()
        return key

    def attempt_auth_host(self):
        self.net.send_start()
        key = self.extract_context()
        time.sleep(1)
        self.net.send_auth_token(auth_token)
        time.sleep(3)


    def bit_agreement_exp_dev(self):
        while (1):
            self.get_start()
            key = self.extract_context()
            other_key = self.recieve_auth_token(auth_token)

    def bit_agreement_exp_host(self):
        while (1):
            time.sleep(3)
            self.net.send_start()
            key = self.extract_context()
            time.sleep(1)
            self.net.send_auth_token(auth_token)

