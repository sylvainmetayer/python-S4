#!/usr/bin/python2
# -*- coding : utf8 -*-
import socket
import sys

socket_l = socket.socket();
socket_l.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_l.bind((sys.argv[1], int(sys.argv[2])))

socket_l.listen(5)

while True:
    socket_c, address_c = socket_l.accept()
    socket_c.send("220 Bonjour\r\n")
    while True:
        message = socket_c.recv(1024)
        if len(message) == 0:
            socket_c.close()
            print("Client deconnecte !")
        else:
            print 'Message : ' + message + "||"
            commande = message[0:4]
            print commande
            if commande == "USER":
                socket_c.send("331\r\n")
            elif commande == "PASS":
                socket_c.send("230 Login OK.\r\n")
            elif commande == "SYST ":
                socket_c.send("215\r\n")
            elif commande == "QUIT":
                socket_c.send("221 Bye.\r\n")
            else:
                socket_c.send("500\r\n")
