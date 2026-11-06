# Minage Verus sur Galaxy A21s

## Résultat de l'essai

Le 6 novembre 2026, Primo ARM Miner v1.1.0 a été lancé sur un Galaxy A21s avec l'algorithme Verus, le pool `stratum+tcp://pool.verus.io:9998` et 2 threads.

Les journaux ont montré :
- authentification Stratum réussie ;
- 2 threads actifs sur les cœurs LITTLE ;
- environ 0,86 à 0,96 MH/s lors de cet essai court ;
- 19 partages acceptés et 0 rejeté sur une capture de session.

Ces valeurs sont ponctuelles et ne représentent pas une moyenne sur 24 h. Elles ne garantissent aucun paiement.

## Paramètres de départ

- Algorithme : `verus`
- Pool : `pool.verus.io:9998`
- Threads : commencer à 1 ou 2
- Worker : suffixe libre, par exemple `.A21s`
- Mot de passe du pool : `x` dans la configuration testée

L'adresse de réception VRSC doit être saisie uniquement dans la configuration locale du téléphone. Ne pas la publier sur GitHub avec d'autres informations personnelles.

## Frais du logiciel

Le projet Primo ARM Miner annonce un frais développeur de 2 % pour Verus, soit 60 secondes par tranche de 50 minutes. Vérifier les informations de la version effectivement installée.

## Sécurité et rendement

Un Exynos 850 est un processeur mobile d'entrée de gamme. Surveiller la température, la batterie, la fréquence CPU et la stabilité. Arrêter le minage en cas de chauffe anormale ou de comportement inhabituel. Ne pas désactiver les protections thermiques Android.

Pour calculer un rendement réel, relever les paiements du pool sur plusieurs jours et comparer leur valeur au coût de l'électricité. La conversion VRSC vers LTC puis vers Coinbase n'est pas intégrée au mineur et dépend d'un service d'échange externe.
