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
        self.broadcast_sock.sendto("start".encode(), ('<broadcast>', 5005))

    def send_auth_token(self, auth_token):
        print()
        print("Sending Authentication Token")
        print()
        self.broadcast_sock.sendto(auth_token, ('<broadcast>', 5005))

    # DEVICE FUNCTIONS
    def get_start(self):
        print()
        print("Polling For Start")
        print()
        while (1):
            message, address = self.personal_sock.recvfrom(8)
            if message is not None:
                break

    def receive_auth_key(self):
        print()
        print("Polling For Authentication Token")
        print()
        while (1):
            message, address = self.personal_sock.recvfrom(8)
            if message is not None:
                return message


