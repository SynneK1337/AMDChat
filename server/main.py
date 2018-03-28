#! /usr/bin/env python
import asyncore
import socket
host = ''
port = 1337

class Server(asyncore.dispatcher):
    clients = []
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        print("[+] Server listening on port %s" % port)

    def handle_accept(self):
        sock, addr = self.accept()
        print("%s connected" % addr[0])
        sock.setblocking(True)
        nickname = sock.recv(64)
        while not nickname:
            nickname = sock.recv(64)
        self.clients.append((EchoHandler(sock), nickname))

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(1024)
        if data:
            print(data)
            for x in Server.clients:
                try:
                    x.send(data)
                except:
                    Server.clients.remove(x)
s = Server(host, port)
asyncore.loop()