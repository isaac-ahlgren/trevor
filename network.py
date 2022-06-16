import socket

class Network:
    def __init__(self, ip, other_ip):
        self.ip = ip
        self.other_ip = other_ip

        #self.broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #self.broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.broadcast_sock.bind(("255.255.255.255", 5005)

        self.personal_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.personal_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.personal_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.personal_sock.bind((ip, 5005))
        
    # INITIALZER FUNCTIONS
    def send_start(self):
        print()
        print("Sending Start")
        print()
        self.personal_sock.sendto("start".encode(), (self.other_ip, 5005))

    def get_bits(self, bit_len):
        print()
        print("Waiting For Bits")
        print()
        while (1):
            message, address = self.personal_sock.recvfrom(bit_len)
            if message is not None:
                break
        print()
        print("Bits Recieved")
        print()
        bits = message.decode()
        print(bits)
        return bits

    # DEVICE FUNCTIONS
    def get_start(self):
        print()
        print("Polling For Start")
        print()
        while (1):
            message, address = self.personal_sock_sock.recvfrom(8)
            if message is not None:
                break
    
    def send_bits(self, bits):
        print()
        print("Sending Bits")
        print()
        self.personal_sock.sendto(bits.encode(), (self.other_ip, 5005))
