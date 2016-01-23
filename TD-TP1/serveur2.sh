#!/bin/bash
echo "Bienvenue sur mon serveur !!!"
while [ 1 = 1 ]
do
    read choice
    if [ "$choice" = "TIME" ]
    then
        date
    elif [[ "$choice" = "SYS" ]]
    then
        uname -a
    elif [[ "$choice" = "QUIT" ]]
    then
        echo "quitting ..." 
        exit 0
    elif [[ "$choice" = "DISK" ]]
    then
        df
    else
        echo "Commande erronée !"
    fi
done

