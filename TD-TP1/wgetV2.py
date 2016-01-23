#!/usr/bin/python2
# -r -coding : utf8
import socket;
import sys;

maSocket = socket.socket();

adresse = sys.argv[1];

message = "GET / HTTP/1.0\nHost:" + adresse + "\n\r\n"

maSocket.connect((adresse, 80));
maSocket.send(message);
texte = ""

chaine = maSocket.recv(1024);
texte += chaine

while texte.__contains__("\n\r\n") == False:
    texte += chaine
    chaine = maSocket.recv(1024);

tab = texte.split("\r\n\n")
numToDelete = len(tab[1])

numDebut = tab[0].find("Content-Length:")
numFin = tab[0].find("Vary")
headerSpecialLigne = tab[0][numDebut:numFin];
longueurMessage = headerSpecialLigne.split(":")[1].split(" ")[1]

longueurMessage = int(longueurMessage)

"A RETENIR : numDebut:numFin : on recupere de numDebut a numFin"

"""print("Longueur du header : " + longueurMessage)"""

toRecup = longueurMessage - numToDelete
chaine = maSocket.recv(toRecup);
print(tab[1] + chaine)

maSocket.shutdown(0);
maSocket.close();
