import socket

class Network:
    def __init__(self, ip):
        self.ip = ip

        self.broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcast_sock.bind(("255.255.255.255", 5005))

        self.personal_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.personal_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.personal_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.personal_sock.bind((ip, 5005))
        
    # INITIALZER FUNCTIONS
    def send_start(self):
        print()
        print("Broadcasting Start")
        print()
        self.personal_sock.sendto("start".encode(), ('<broadcast>', 5005))


    # DEVICE FUNCTIONS
    def get_start(self):
        print()
        print("Polling For Start")
        print()
        while (1):
            message, address = self.broadcast_sock.recvfrom(8)
            if message is not None:
                break
