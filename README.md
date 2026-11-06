# Miner-xmsrep — Samsung Galaxy A21s

Projet expérimental de minage CPU sur Samsung Galaxy A21s (Exynos 850 / ARM64), avec **VerusCoin (VRSC)** et Primo ARM Miner.

> Un smartphone n'est généralement pas rentable pour miner. Les performances et les récompenses dépendent du matériel, du pool, de la difficulté et du coût de l'électricité. Aucun gain n'est garanti.

## État du projet

- [x] Dépôt initialisé et diagnostic du Galaxy A21s
- [x] Architecture ARM64 (aarch64) et extensions CPU vérifiées
- [x] Primo ARM Miner Android ARM64 téléchargé et archive contrôlée par SHA-256
- [x] Connexion au pool Verus vérifiée
- [x] Partages acceptés observés lors d'un essai court
- [ ] Mesure longue de température, stabilité et consommation
- [ ] Mesure des paiements réellement reçus et calcul du rendement net

## Matériel testé

- Samsung Galaxy A21s, Exynos 850
- Android 12, ABI arm64-v8a
- 8 cœurs LITTLE Cortex-A55
- Test initial avec 2 threads
- Environ 0,86 à 0,96 MH/s observés sur un court essai (ce n'est pas une moyenne garantie)

## Mineur utilisé

[Primo ARM Miner](https://github.com/PrimoLab/primo-arm-miner) — logiciel tiers, indépendant de ce dépôt. Consulter son dépôt, sa licence GPL-3.0-or-later, ses avis de provenance et ses frais développeur avant utilisation. Pour Verus, le projet annonce des frais développeur de 2 %.

Le binaire, l'archive téléchargée et la configuration personnelle ne sont **pas** stockés dans ce dépôt.

## Installation et démarrage

Voir [docs/INSTALLATION.md](docs/INSTALLATION.md) et [docs/VERUS-MINING.md](docs/VERUS-MINING.md).

## Sécurité

- Ne publie jamais ton adresse privée (seed/phrase de récupération) ni ta clé privée.
- L'adresse publique de réception doit rester dans un fichier local ignoré par Git.
- N'envoie jamais `config.json`, le binaire du mineur ou les archives téléchargées sur GitHub.
- Ne désactive pas les protections thermiques Android et ne root pas le téléphone pour miner.
- Surveille la température et la batterie ; arrête si le téléphone chauffe anormalement, devient instable ou si la batterie gonfle.
- N'utilise pas une adresse de dépôt d'exchange directement pour miner : vérifie les règles de paiement du pool et du portefeuille.

## Limites

Les résultats obtenus sont des observations ponctuelles sur un seul appareil. Ils ne démontrent ni rentabilité, ni stabilité sur la durée. La conversion éventuelle de VRSC vers LTC puis vers Coinbase nécessite un service d'échange compatible et des vérifications séparées ; elle n'est pas automatique.
