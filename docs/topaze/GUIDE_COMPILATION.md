# Compiler Pokémon Topaze chez soi (Windows + WSL, ou Linux/macOS)

## 1. Prérequis (Windows : installer WSL2 + Ubuntu d'abord, puis tout dans le terminal Ubuntu)
sudo apt update
sudo apt install build-essential binutils-arm-none-eabi gcc-arm-none-eabi libnewlib-arm-none-eabi libpng-dev git

## 2. Récupérer le projet
git clone <URL du dépôt Topaze> topaze
cd topaze

## 3. Installer agbcc (compilateur historique du jeu), à côté du projet
cd ..
git clone https://github.com/pret/agbcc.git
cd agbcc && sh build.sh && sh install.sh ../topaze && cd ../topaze

## 4. Compiler
make -j$(nproc) firered
# -> produit pokefirered.gba, à ouvrir dans mGBA (https://mgba.io)

## 5. Éditer les cartes
Porymap (https://github.com/huderlod/porymap) : ouvrir le dossier du projet.
