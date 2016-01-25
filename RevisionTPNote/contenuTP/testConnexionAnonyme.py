#!/usr/bin/python2
# -*- coding: utf8 -*-

import socket
import sys

masocket = socket.socket()
masocket.connect((sys.argv[1], int(sys.argv[2])))
message = masocket.recv(1024)
masocket.send("USER anonymous\r\n""")
message = masocket.recv(1024)
code = message.split(" ")[0]
if int(code) == 530:
    print "Connexion anonyme interdite"
else:
    print "Connexion anonyme autorisee"

masocket.shutdown(0)
masocket.close()
sys.exit(0)
