# Installation sur Samsung Galaxy A21s

## 1. Environnement

Le test a été réalisé sur un Samsung Galaxy A21s (Exynos 850), Android 12, ABI `arm64-v8a` (`aarch64`), avec Termux.

Installer Termux depuis une source officielle :
- [F-Droid](https://f-droid.org/packages/com.termux/)
- [GitHub officiel](https://github.com/termux/termux-app/releases)

Mettre à jour les paquets :

```sh
pkg update && pkg upgrade
pkg install -y git python curl
```

## 2. Récupérer le projet

```sh
git clone https://github.com/Xmsrep/Miner-xmsrep.git
cd Miner-xmsrep
chmod +x scripts/*.sh
./scripts/device-info.sh
```

Le diagnostic ne lance aucun mineur.

## 3. Installer le mineur tiers

Le mineur utilisé est [Primo ARM Miner](https://github.com/PrimoLab/primo-arm-miner). Il ne fait pas partie du code de ce dépôt.

Consulter les instructions et les versions publiées par son éditeur. Télécharger uniquement l'archive Android ARM64 depuis la source officielle indiquée par le projet. Vérifier son empreinte avec le fichier SHA256SUMS publié par le même éditeur avant extraction. Une somme de contrôle confirme l'intégrité par rapport au fichier de sommes publié ; elle ne constitue pas une garantie indépendante d'absence de logiciel malveillant.

Ne pas exécuter aveuglément un script d'installation distant et ne pas télécharger de binaire depuis un dépôt inconnu.

## 4. Configuration locale

Créer la configuration sur le téléphone, dans le dossier local du mineur, sous le nom `config.json`. Exemple de structure :

```json
{
  "algo": "verus",
  "url": "stratum+tcp://pool.verus.io:9998",
  "user": "VOTRE_ADRESSE_VRSC.worker",
  "pass": "x",
  "threads": 2
}
```

Remplacer `VOTRE_ADRESSE_VRSC` localement par une adresse publique de réception Verus que tu contrôles. Ne jamais mettre cette adresse dans un fichier suivi par Git si tu ne souhaites pas la rendre publique. Ne jamais saisir une phrase de récupération ou une clé privée.

## 5. Vérifier la configuration

Depuis le dossier du mineur :

```sh
python -m json.tool config.json
```

Si le JSON est valide, Python affiche le contenu formaté. Cette commande ne valide pas l'adresse auprès du pool.

## 6. Démarrer et arrêter

Lancer le mineur depuis son dossier, avec sa configuration locale selon les options documentées par Primo ARM Miner. Pour arrêter proprement, utiliser `CTRL+C` dans Termux.

Commencer avec 1 ou 2 threads, surveiller le téléphone et augmenter uniquement si la température reste raisonnable. Ne pas laisser le téléphone miner sans surveillance au début.

## 7. Notes

- Le pool utilisé pendant l'essai était `pool.verus.io:9998`.
- La connexion et l'autorisation Stratum ont réussi lors de l'essai.
- Des partages acceptés ont été observés ; cela confirme une activité de minage, pas un paiement garanti.
- Le mineur annonce des frais développeur de 2 % sur Verus (60 secondes par tranche de 50 minutes), à vérifier dans la documentation de la version utilisée.
- Le rendement net doit tenir compte de la consommation électrique, de la difficulté, des frais et du seuil de paiement du pool.
