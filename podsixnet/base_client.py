#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
import time

from PodSixNet.Connection import connection, ConnectionListener


class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))

    def Loop(self):
        connection.Pump()
        self.Pump()

    def Network(self, data):
        print('message de type %s recu' % data['action'])

    ### Network event/message callbacks ###
    def Network_connected(self, data):
        print('connecte au serveur !')
        user = raw_input("Votre user : ")
        connection.Send({"action":"username", "username":user})

    def Network_connexion_ok(self, data):
        print data["message"]

    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()

    def Network_disconnected(self, data):
        print 'Server disconnected'
        sys.exit()


if len(sys.argv) != 3:
    print "Usage:", sys.argv[0], "host port"
else:
    c = Client(sys.argv[1], int(sys.argv[2]))
    while True:
        c.Loop()
        time.sleep(0.001)
