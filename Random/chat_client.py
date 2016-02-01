#!/usr/bin/python2
# -*- coding: utf8 -*-

import select
import socket
import sys

if len(sys.argv) != 3:
    print "Syntaxe : " + sys.argv[0] + " <adresse> <port>"
    sys.exit(1)

adresse = sys.argv[1]
port = sys.argv[2]

socket_c = socket.socket()
socket_c.connect((adresse, int(port)))
socket_list = []
socket_list.append(sys.stdin)
socket_list.append(socket_c)
username_set = False

while True:
    read_s, write_s, err_s = select.select(socket_list, [], [])
    for s in read_s:
        if s == socket_c:
            message = socket_c.recv(1024);
            code = message.split(" ")[0]
            if code == "331":  # Ask username
                username = raw_input(message[4:])
                socket_c.send("USER " + username + "\n")
            elif code == "221":  # OK USER
                print message[4:]
                socket_c.shutdown(0)
                socket_c.close()
                sys.exit(0)
            elif code == "403":
                print "TODO, un doublon d'username !"
                print message[4:]

                pass
            elif code == "200":
                print message[4:]
                username_set = True
            else:
                print message
        elif s == sys.stdin:
            message = sys.stdin.readline()
            if message == "quit":
                socket_c.send("QUIT\n")
            elif message[0:4] == "USER":
                username = message[4:]
                socket_c.send("USER " + username)
            else:
                socket_c.send(message + "\n")
