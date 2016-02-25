#!/usr/bin/python2
# -*- coding : utf8 -*-
import socket;
import sys;

socket_l = socket.socket();
socket_l.bind((sys.argv[1], int(sys.argv[2])))

socket_l.listen(5)
socket_c, address_c = socket_l.accept()
socket_l.close()
socket_c.send("Bonjour !")

while True:
    message = socket_c.recv(1024)
    if len(message) == 0:
        print("Fin du serveur")
        socket_c.close()
        sys.exit(0)
    else:
        socket_c.send("Vous avez tape " + message)
