#!/usr/bin/python2
# -*- coding: utf8 -*-

import socket
import sys

masocket = socket.socket()
adresse = sys.argv[1]
port = sys.argv[2]

masocket.connect((adresse, int(port)))

while True:
    message = masocket.recv(1024)
    print message
    input = raw_input("Texte : ")
    masocket.send(input)
