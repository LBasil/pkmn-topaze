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
