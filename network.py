import socket

class Network:
    def __init__(self, is_host, ip):
        self.is_host = is_host
        self.ip = ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if is_host:
            self.sock.bind((ip, 5005))
        else:
            self.sock.bind(("255.255.255.255", 5005))
        
    def send_start(self):
        if self.is_host is True:
            print()
            print("Broadcasting Start")
            print()
            self.sock.sendto("start".encode(), ('<broadcast>', 5005))

    def get_start(self):
        print()
        print("Polling for start")
        print()
        while (1):
            message, address = self.sock.recvfrom(10)
            if message is not None:
                break

