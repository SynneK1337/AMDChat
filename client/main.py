import asyncore
import socket

hostname = input("Server: ")
nickname = input("Nickname: ")

class Client(asyncore.dispatcher):
    def __init__(self, hostname, nickname):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        try:
            self.connect((hostname, 1337))
            self.send(nickname.encode('utf-8'))
        except:
            print("Connection failed.")
        else:
            print("Connected successful")

c = Client(hostname, nickname)
asyncore.loop()