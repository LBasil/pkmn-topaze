# Banc de test sans écran (mGBA)

`h.c` est un petit lanceur qui charge `pokefirered.gba` dans la bibliothèque mGBA, envoie des touches, prend des captures (PPM) et lit/écrit la mémoire. `play.py` / `pl.py` sont les aides Python (conversion en PNG, états sauvegardés, lecture de la position du joueur).

## Construire
```bash
git clone --depth 1 https://github.com/mgba-emu/mgba.git && cd mgba && mkdir build && cd build
cmake .. -DBUILD_QT=OFF -DBUILD_SDL=OFF -DBUILD_GL=OFF -DBUILD_GLES2=OFF -DBUILD_GLES3=OFF -DBUILD_EXAMPLE=OFF \
  -DBUILD_HEADLESS=OFF -DBUILD_SHARED=OFF -DBUILD_STATIC=ON -DUSE_FFMPEG=OFF -DUSE_EPOXY=OFF -DUSE_LIBZIP=OFF \
  -DUSE_MINIZIP=OFF -DUSE_SQLITE3=OFF -DUSE_LUA=OFF -DUSE_EDITLINE=OFF -DUSE_DISCORD_RPC=OFF -DCMAKE_BUILD_TYPE=Release
make -j8
D=$(grep C_DEFINES CMakeFiles/mgba.dir/flags.make | cut -d= -f2-)
gcc -O1 $D -o h /chemin/tools/topaze/emu/h.c -I ../include -I include libmgba.a -lm -lz -lpng -lpthread
```
## Utiliser
Script texte : `run N` (N images), `key A|B|START|UP|... N`, `shot f.ppm`, `readp 03005008 0 6` (position : x, y, groupe, n° de carte via `gSaveBlock1Ptr`), `read ADDR N`, `write ADDR V`, `ss f` / `ls f` (états sauvegardés).
Exemples d'usage : voir `base.py` (nouvelle partie jusqu'à Grenalux) et `pl.py`.

Commandes ajoutées : `keys B+DOWN N` (touches combinées), `writepb PTRADDR OFF HEX` (écriture d'octets via pointeur, ex. badges : `writepb 03005008 fe4 ff`). `states.py <Starter>` régénère les états de départ ; `fight.py` joue le premier combat. Variable `TOPAZE_STATES` = dossier des états.

## ROM de debug
Pour tester un endroit lointain : modifier temporairement `WarpToPlayersRoom()` (destination) et ajouter un `CreateMon` dans `NewGameInitData()` (`src/new_game.c`), compiler, copier la ROM sous un autre nom, **annuler la modification** et recompiler. Lancer ensuite avec `TOPAZE_ROM=chemin/debug.gba`. (Écrire la position dans la sauvegarde ne marche pas : la disposition de carte reste celle de l'ancienne carte.)

**Piège de build** : `make` ne détecte pas toujours les changements de `data/layouts/*/map.bin` (objet `build/firered/data/maps.o` non reconstruit). Après avoir modifié une carte, supprimer `build/firered/data/maps.o` (et `build/firered/src/graphics.o` pour un tileset) avant de compiler, sinon les tests montrent l'ancienne carte.
