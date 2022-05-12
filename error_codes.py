
MAX_HAMMING_DISTANCE = 8

class Error_Corrector:
    def __init__(self):
        # Hamming 8-4 error codes
        #self.hamming_error_code_strings = [bitarray("00000000"), bitarray("00011110"), bitarray("00110011"), bitarray("00101101"),
        #                                   bitarray("01010101"), bitarray("01001011"), bitarray("01100110"), bitarray("01111000"),
        #                                   bitarray("10000111"), bitarray("10011001"), bitarray("10110100"), bitarray("10101010"),
        #                                   bitarray("11010010"), bitarray("11001100"), bitarray("11100001"), bitarray("11111111")]

    def get_nearest_hamming_code(self, bits):
        best_hamming_dist = MAX_HAMMING_DISTANCE
        best_hamming_code = None
        for i in range(16):
            hamming_dist = 0
            for j in range(8):
                if bits[j] is not self.hamming_error_code_string[i][j]:
                    hamming_dist += 1
            if hamming_dist < best_hamming_dist:
                best_hamming_dist = hamming_dist
                best_hamming_code = self.hamming_error_codes_strings[i]
        return best_hamming_code

    '''
        Get error code difference of a byte of the key
    '''
    def get_error_diff(self, bits):
        nearest_code = self.get_nearest_hamming_code(bits)
        return nearest_code ^ bits

    '''
        Get error code difference of every byte of the key
    '''
    def get_key_error_diff(self, key):
        byte_len = int(len(key) / 8)
        key_diff = bitarray()
        for i in range(byte_len):
            byte = key[i*8:(i+1)*8]
            byte_diff = self.get_error_diff(byte)
            key_diff.extend(byte_diff)
        return key_diff


        

                    
