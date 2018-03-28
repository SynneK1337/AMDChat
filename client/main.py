import asyncore
import socket

hostname = input("Server: ")
nickname = input("Nickname: ")

class Client(asyncore.dispatcher):
    def __init__(self, hostname, nickname):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.socket.setblocking(True)
        try:
            self.connect((hostname, 1337))
            self.send(nickname.encode('utf-8'))
        except:
            print("Connection failed.")
        else:
            print("Connected successful")

    def handle_read(self):
        data = self.recv(1024)
        if data:
            print(data.decode('utf-8'))
    
    def handle_write(self):
        msg = input("%s@%s$ " % (nickname, hostname))
        self.send(msg.encode('utf-8'))
c = Client(hostname, nickname)
asyncore.loop()