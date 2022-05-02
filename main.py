from bit_extractor import Bit_Extractor
import numpy as np

if __name__ == "__main__":
    be = Bit_Extractor(44100, 64, 4096)
    
    key = be.extract_key()
    print(len(key))
    np.set_printoptions(threshold=np.inf)
    print(key)
