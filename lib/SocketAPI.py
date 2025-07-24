import socket

class Server():
    def __init__(self, ip, port):
        self.IP = ip
        self.PORT = port
        self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # whatever the arguments in this variables are, idk
        self.SERVER.bind((self.IP, self.PORT))
        self.client_socket = None
    
    def acceptConection(self):
        self.SERVER.listen(0)
        client_SOCKET, client_ADDRESS = self.SERVER.accept()
        self.client_socket = client_SOCKET
        return (client_SOCKET, client_ADDRESS)
    
    def receiveMSG(self):
        req = self.client_socket.recv(1024)
        if not req:
            return "No user here."
        else:
            req = req.decode("utf-8")
            return req

    def sendMSG(self, message: str):
        message = message.encode("utf-8")
        self.client_socket.send(message)
    
    def close(self):
        self.SERVER.close()

class Client():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        self.client.connect((self.ip, self.port))
    
    def sendMSG(self, msg):
        self.client.send(msg.encode("utf-8")[:1024])
    
    def receiveMSG(self):
        response = self.client.recv(1024)
        response = response.decode("utf-8")
        return response
    
    def close(self):
        self.client.close()