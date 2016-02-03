#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
import time

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server


class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.username = "Anonyme"

    def Close(self):
        self._server.del_client(self)

    def Network(self, data):
        print('message de type %s recu' % data['action'])

    def Network_username(self, data):
        self.username = data['username']
        print "USERNAME :" + self.username
        self.Send({"action":"connexion_ok", "message":"Bienvenue !"})


class MyServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.clients = []
        print('Server launched')

    def Connected(self, channel, addr):
        print('New connection')
        self.clients.append(channel)

    def del_client(self, channel):
        print('client deconnecte')
        self.clients.remove(channel)


def main_prog():
    my_server = MyServer(localaddr=(sys.argv[1], int(sys.argv[2])))

    while True:
        my_server.Pump()
        time.sleep(0.01)


if __name__ == '__main__':
    main_prog()
    sys.exit(0)
