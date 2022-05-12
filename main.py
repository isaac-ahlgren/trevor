from tr_sys import TR_Bit_Extract_System

IP = "192.168.1.1" # <--- device's ip address goes here
SAMPLE_RATE = 44100
BIT_LENGTH = 64
VECTOR_LENGTH = 4096
IS_HOST = True
EXP_NAME = "test"

if __name__ == "__main__":
    tr = TR_Bit_Extract_System(IP, SAMPLE_RATE, BIT_LENGTH, VECTOR_LENGTH, EXP_NAME)
    if IS_HOST:
        tr.bit_agreement_exp_host()
    else:
        tr.bit_agreement_exp_dev()

        
