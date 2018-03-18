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
        self.clients.append(EchoHandler(sock))

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(1024)
        if data:
            for x in Server.clients:
                x.send(data)

s = Server(host, port)
asyncore.loop()