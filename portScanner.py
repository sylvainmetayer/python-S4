#!/usr/bin/python2

import socket
import sys
import time


def scanPort(address, port):
    s = socket.socket()
    s.connect((address, int(port)))


def main():
    if len(sys.argv) != 5:
        print "Syntaxe : portScanner.py <adresse> <portDebut> <portFin> <verbose (o/n)> "
        sys.exit(1)

    adresse = sys.argv[1]
    portDebut = sys.argv[2]
    portFin = sys.argv[3]
    verbose_s = sys.argv[4]
    verbose = True if verbose_s == "o" else False

    listePortsOuverts = []
    time_debut = time.time()
    for port in range(int(portDebut), int(portFin) + 1, 1):
        isConnect = 1

        try:
            scanPort(adresse, port)
        except Exception:
            if verbose:
                print "Le port " + str(port) + " est ferme"
        else:
            if verbose:
                print "Le port " + str(port) + " est ouvert"
            listePortsOuverts.append(port)

    time_end = time.time()
    temps = time_end - time_debut
    if len(listePortsOuverts) > 0:
        print "\n\nResume : Les ports suivants sont ouverts sur " + adresse + " : "
        for port in listePortsOuverts:
            print str(port) + ", "
    else:
        print "\n\nAucun ports n'est ouvert sur " + adresse + " : "
    print "Temps d'execution : " + str(temps) + " secondes"


main()
