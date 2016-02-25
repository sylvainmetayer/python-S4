#!/usr/bin/python2
# -r -coding : utf8
import socket;
import sys;

maSocket = socket.socket();

adresse = sys.argv[1];
port = int(sys.argv[2]);

maSocket.connect((adresse, port));
chaine = maSocket.recv(1024);
print(chaine);
maSocket.shutdown(0);
maSocket.close();
