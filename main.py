from bit_extractor import Bit_Extractor

if __name__ == "__main__":
    be = Bit_Extractor(44100, 64, 4096)
    
    key = be.extract_key()
    print(key)