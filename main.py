from tr_sys import TR_Bit_Extract_System

IP = "192.168.1.2" # <--- device's ip address goes here if host
SAMPLE_RATE = 44100
BIT_LENGTH = 64
VECTOR_LENGTH = 4096
IS_HOST = False

if __name__ == "__main__":
    tr = TR_Bit_Extract_System(IP, SAMPLE_RATE, BIT_LENGTH, VECTOR_LENGTH)
    if IS_HOST:
        tr.bit_agreement_exp_host()
    else:
        tr.bit_agreement_exp_dev()

        
