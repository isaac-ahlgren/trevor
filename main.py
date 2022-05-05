from bit_extractor import Bit_Extractor
from network import Network
import numpy as np
import time

IP = "192.168.2.1"
SAMPLE_RATE = 44100
BIT_LENGTH = 64
VECTOR_LENGTH = 4096
IS_HOST = False

if __name__ == "__main__":
    net = Network(IS_HOST, IP)
    be = Bit_Extractor(SAMPLE_RATE, BIT_LENGTH, VECTOR_LENGTH)
    
    while(1):
        if IS_HOST:
            time.sleep(3)
            net.send_start()
        else:
            net.get_start()
        print()
        print("Extracting Audio")
        print()
        key = be.extract_key()
        print(key)
        
