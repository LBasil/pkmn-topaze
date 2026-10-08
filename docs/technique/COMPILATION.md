# Compiler Pokémon Topaze

Le projet est un fork de [pret/pokefirered](https://github.com/pret/pokefirered) (commit `037335f4`). **Aucune ROM d'origine n'est nécessaire** : tout est compilé depuis le code source avec `agbcc`, le compilateur historique du jeu.

> La branche de travail est **`topaze`** (la branche `main` ne contient que « Initial commit »).

## 1. Prérequis

### Windows : WSL2 + Ubuntu
1. PowerShell (administrateur) : `wsl --install -d Ubuntu`, redémarrer, créer un utilisateur.
2. Travailler **dans le système de fichiers Linux** (`~/`), pas dans `/mnt/c/...` (très lent, et problèmes de permissions).

### Linux (Debian/Ubuntu) / macOS
```bash
sudo apt update
sudo apt install build-essential binutils-arm-none-eabi gcc-arm-none-eabi libnewlib-arm-none-eabi libpng-dev git
```
macOS : `brew install libpng git` + la toolchain `arm-none-eabi` (`brew install --cask gcc-arm-embedded` ou équivalent).

## 2. Récupérer le projet et agbcc
```bash
git clone -b topaze https://github.com/LBasil/pkmn-topaze.git topaze
git clone https://github.com/pret/agbcc.git
cd agbcc && sh build.sh && sh install.sh ../topaze && cd ../topaze
```
`install.sh` copie le compilateur dans `topaze/tools/agbcc/` (ce dossier n'est pas versionné : à refaire sur chaque nouvelle machine).

## 3. Compiler
```bash
make -j$(nproc) firered
```
Produit **`pokefirered.gba`** (≈16 Mo) à la racine. Première compilation : 2 à 5 minutes ; les suivantes sont incrémentales.

## 4. Lancer
Ouvrir `pokefirered.gba` dans [mGBA](https://mgba.io). Commencer avec une **nouvelle sauvegarde** (une sauvegarde d'un autre build peut être incompatible).
Sous WSL le fichier est accessible depuis Windows via `\\wsl$\Ubuntu\home\<utilisateur>\topaze\`.

## 5. Éditer les cartes
[Porymap](https://github.com/huderlod/porymap) : ouvrir le dossier du projet (`topaze/`). Après modification, recompiler.

## 6. Régénérer le site joueur
```bash
python3 tools/topaze/build_site.py   # écrit docs/data/*.js
```

## Dépannage
| Symptôme | Cause / solution |
|---|---|
| `fatal error: string.h` ou `agbcc: not found` | agbcc non installé : refaire l'étape 2 (`install.sh ../topaze`). |
| `arm-none-eabi-gcc: command not found` | Toolchain absente : refaire l'étape 1. |
| `png.h: No such file` | `sudo apt install libpng-dev`. |
| Erreurs de permissions / lenteur extrême | Projet dans `/mnt/c/...` : le déplacer dans `~/`. |
| Modification d'un `.json` de carte sans effet | Relancer `make` (les `.h`/`.inc` sont régénérés). |
| `excess elements in array initializer` | Une table a une taille fixe (ex. `gTypeEffectiveness[372]`) : l'agrandir. |
| Vérifier l'état d'origine | `make compare_firered` ne passe **plus** (le jeu est modifié) : normal. |
