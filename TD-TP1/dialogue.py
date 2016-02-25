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

while 1:
    texte = raw_input("Saisissez du texte :");
    texte = texte + "\n";
    maSocket.send(texte);
    chaine = maSocket.recv(1024);
    print(chaine);

print(chaine);
maSocket.shutdown(0);
maSocket.close();
