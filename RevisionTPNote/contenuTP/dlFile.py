#!/usr/bin/python2
# -*- coding: utf8 -*-

import socket
import sys


def getPort():
    ports = []
    ports.append(9)
    ports.append(32)
    return ports


def getPortCalc(port):
    return int(port[0]) * 256 + int(port[1])


if len(sys.argv) != 4:
    print "Syntaxe : " + sys.argv[0] + " <adresse> <port> <fichier a recuperer>"
    sys.exit(1)

fichier = sys.argv[3]
adresse = sys.argv[1]
port = sys.argv[2]

socket_c = socket.socket()
socket_c.connect((adresse, int(port)))

portRandom = getPort()
socket_c.send("PORT 127,0,0,1," + str(portRandom[0]) + "," + str(portRandom[1]) + "\r\n")
portData = getPortCalc(portRandom)
print socket_c.recv(1024)
socket_c.send("RETR " + fichier)  # Je dis quel fichier recuperer sur le serveur

socketData = socket.socket()
socketData.bind(("127.0.0.1", int(portData)))
socketData.listen(2)
socketData, addressTmp = socketData.accept()
print socket_c.recv(1024)  # Je t'envoie des donnees
dataFile = ""
tmp = socketData.recv(4096)  # Je recois les data
while len(tmp) > 0:
    print "Passage dans la recuperation de data"
    dataFile += tmp
    tmp = socketData.recv(4096)  # Je recois les data
socketData.shutdown(0)
socketData.close()
print socket_c.recv(2014)  # Fin du transfert

try:
    handle = open("download", "w+")
    handle.write(dataFile)
    handle.close()
except Exception:
    pass

socketData.close()
socket_c.close()
print "Termine !"
