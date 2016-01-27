#!/usr/bin/python2
# -*- coding: utf8 -*-

import socket
import sys

masocket = socket.socket()
masocket.bind((sys.argv[1], int(sys.argv[2])))
masocket.listen(5)
socket_c, adresse_c = masocket.accept()
masocket.close()

while True:
    message = socket_c.recv(1024)
    retour = hex(int(message))
    retour = retour.split("x")[1]
    socket_c.send(retour + "\r\n")
