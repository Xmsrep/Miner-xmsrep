# Installation sur Galaxy A21s

## 1. Ne rien effacer pour le moment

Une réinitialisation ou une ROM alternative n'améliore pas les capacités de calcul. Garder Android permet de contrôler la température et l'état de la batterie.

## 2. Installer Termux

Installe Termux uniquement depuis une source officielle :
- F-Droid : https://f-droid.org/packages/com.termux/
- GitHub officiel : https://github.com/termux/termux-app/releases

Évite les APK provenant de sites tiers.

## 3. Préparer l'environnement

Ouvre Termux et exécute :

```sh
pkg update && pkg upgrade
pkg install git python
```

## 4. Récupérer le projet

```sh
git clone https://github.com/Xmsrep/Miner-xmsrep.git
cd Miner-xmsrep
chmod +x scripts/*.sh
```

## 5. Faire un diagnostic sans minage

```sh
./scripts/device-info.sh
```

Envoie le résultat (masque toute information personnelle). Ce diagnostic ne lance aucun mineur et ne modifie pas le système.

## 6. Avant de choisir une crypto

Nous vérifierons d'abord l'architecture ABI, la RAM disponible, la version Android et les limites thermiques. Ensuite seulement, nous comparerons les logiciels de minage ARM64 réellement maintenus, leurs licences, leurs sommes de contrôle et les pools disponibles.

**Ne saisis jamais de phrase de récupération ou de clé privée dans Termux, dans un script ou dans GitHub.**
