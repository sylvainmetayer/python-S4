#!/usr/bin/python2
# -*-coding:utf-8 -*
"""
Server FTP
"""
import socket
import subprocess
import sys

msgBienvenue = "220 Bienvenue sur le serveur FTP v0\r\n"
dictionnaireCmd = {'SYST': ['uname', '-a'], 'PWD': ['pwd'], 'LIST': ['ls', '-l']}
dictionnaireUser = {'anto': ['anto'], 'root': ['root'], 'remy': ['matasse']}


def retourneresultatcommande(cmd):
    p = subprocess.Popen(dictionnaireCmd[cmd], stdout=subprocess.PIPE)
    reponse = p.communicate()[0]
    print reponse + "|"  # Permet de vérifier le bon fonctionnement de la fonction, avec un '|' pour voir les eventuels \r\n présents en fin de chaine
    return reponse


socket_l = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
socket_l.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    socket_l.bind((sys.argv[1], int(sys.argv[2])))
except socket.error:
    print("Impossible de lier ce port.")
else:
    socket_l.listen(1)
    socket_c, adress_c = socket_l.accept()
    socket_l.close()

    socket_c.send(msgBienvenue)
    while True:
        print '----------'  # Affichage console
        commande = socket_c.recv(1024)
        commande = commande.replace('\n', '').replace('\r', '')

        code = commande[0:4]
        print code + "."  # Affiche le code reçu, avec un point pour savoir si un espace est présent ou non.

        print(commande)  # Affiche toute la demande du client.
        if (len(commande)) == 0:
            sys.exit(0)

        if 'USER' == code:
            user = ((commande.split(' '))[1])
            socket_c.send("331 Please specify the password.\r\n")

        elif 'PASS' in code:
            passwd = ((commande.split(' '))[1])

            if (user == "anto" and passwd == "anto"):
                socket_c.send("230 Login successful.\r\n")
            else:
                socket_c.send('530 Erreur login/pwd.\r\n')

            # TODO fix it.
            """
            if dictionnaireUser.has_key(user) == False:
                socket_c.send('530 Login incorrect.\r\n')
            elif dictionnaireUser.get(user) != passwd:
                socket_c.send('530 Login incorrect.\r\n')
            else:
                socket_c.send("230 Login successful.\r\n")
            """
        elif 'SYST' in code:
            socket_c.send('215 ' + retourneresultatcommande('SYST') + '\n')

        elif 'PWD' == code or 'XPWD' == code:
            socket_c.send('257 ' + retourneresultatcommande('PWD') + '\n')

        elif 'TYPE' in code:
            socket_c.send('220 OK.\r\n')

        elif 'PORT' in code:
            socket_t = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            socket_t.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            socket_t.bind((sys.argv[1], 2020))

            adressePort = commande.split(' ')
            argsAdressePort = adressePort[1].split(',')
            adresseClient = argsAdressePort[0] + '.' + argsAdressePort[1] + '.' + argsAdressePort[2] + '.' + \
                            argsAdressePort[3]
            portClient = 256 * int(argsAdressePort[4]) + int(argsAdressePort[5])
            socket_c.send('200 Port command successful. Consider using PASV.\r\n')
            # reponsePORT = socket_c.recv(1024)

        elif 'LIST' in code:
            socket_t.connect((adresseClient, portClient))
            socket_c.send('150 Here comes the directory listing.\r\n')
            socket_t.send(retourneresultatcommande('LIST') + '\n')
            socket_t.shutdown(0)
            socket_t.close()
            socket_c.send('226 Directory send OK.\r\n')

        elif 'QUIT' in code:
            socket_c.send('221 Goodbye.\r\n')
            socket_c.close()
            sys.exit(0)

        # commande inconnue
        else:
            socket_c.send("500 Unknown command.\r\n")

    socket_c.close()

    # Connexion non fonctionnelle
    # Pb LIST
