# Banc de test émulateur (mGBA headless)

Outils dans `tools/topaze/emu/` (harnais C `harness.c` sur libmgba, pilote Python `drive.py`, patch de debug `debug.patch`) et `docs/topaze/route_test.py` / `route_shots.py`.

## Mise en place (environnement neuf)
1. `apt-get install -y libmgba-dev libmgba0.10` (le paquet `mgba-sdl` est inutile : pas de script).
2. `mkdir -p /tmp/gx && cp tools/topaze/emu/harness.c tools/topaze/emu/drive.py /tmp/gx/ && cd /tmp/gx && gcc -O1 -o harness harness.c -lmgba`
3. ROM de debug : `git apply tools/topaze/emu/debug.patch` (new_game.c : tableau `gTopazeDbg[8]` = [activer, groupe, numéro, x, y, pas-de-combats] lu à la fin de l'intro ; trainer_see.c / wild_encounter.c : plus de combats si `gTopazeDbg[5]`), `make -j8 firered`, copier `pokefirered.gba` en `/tmp/gx/dbg.gba`, puis `git apply -R tools/topaze/emu/debug.patch` et rebuilder la ROM normale. L'adresse de `gTopazeDbg` (0x03007480 le 12/10) est à relire dans `pokefirered.map` si le code change (`drive.py`, `route_test.py` et `route_shots.py` la codent en dur ; `gSaveBlock1Ptr` = 0x03005008 pareil).
4. Le jeu démarre en matraquant A / START (intro, noms par défaut) : `goto()` épingle `gTopazeDbg` à chaque image jusqu'à l'arrivée sur la carte voulue.

## Usage (depuis la racine du dépôt)
- Marche + sondes : `python3 docs/topaze/route_test.py /tmp/gx/dbg.gba Route14 1 51 23 17` (carte, départ, buts ; le dernier but est une case de warp). Le chemin vient de la collision de `map.bin` + attributs de métatuiles + cases d'objets ; à chaque case on essaie de traverser chaque voisin bloqué (arbre, eau, mur, cristal) : le joueur ne doit pas bouger. Sortie : pas, sondes, anomalies, carte d'arrivée.
- Captures en jeu : `python3 docs/topaze/route_shots.py /tmp/gx/dbg.gba out.png Route13:62:3 Route9:30:7 ...` (planche 2 colonnes).

## Résultats du 12/10 (tout passe)
- Routes 14, 13, 9, 11, 15 : trajet complet entrée -> sortie, 0 anomalie, warps vers les cartes voisines OK ; Route 11 : porte du poste de garde -> intérieur ; Routes 16 et 17 : trajet OK, connexions 16 -> 17 -> 18 OK. Neige, lilas, Spinellia, Apatia, escaliers, pont, embarcadère : rendu en jeu conforme aux rendus mapkit.
- Bordure (`border.bin`) : une seule pour toute la carte, donc teinte de l'étage 0 (Route 11 : pins dorés d'Apatia visibles au-delà de la sortie est teal ; Route 16 : motif d'arbres enneigés au-delà de l'est). Cosmétique, signalé.
- **Hematown : palette 13 jamais chargée** (rendu en jeu : cristaux et panneaux arc-en-ciel). Corrigé : cristaux sur la palette primaire 4 (`CRY_PAL = 4` dans `hematown_town.py`), rendu mapkit identique, en jeu rouge hématite comme prévu. Pallet Town (Grenalux) a 2 cases en palette 14 sous la cheminée (calque bas masqué) : visuellement correct.

## Scénarios scriptés (13/10)
Bibliothèque `tz.py` (classe `T` : boot via la ROM de debug avec équipe forte, drapeaux/variables préchargés via `gTopazeFlags` / `gTopazeVars` / `gTopazeGod`, marche BFS avec dresseurs, `spin_bfs` pour les cases-flèches) : non versionnée pour l'instant ; résultats dans TEST_PASSE_13_10.md. Piège : `pos()` reste figée pendant un combat ; la boîte de dialogue d'un dresseur déjà battu se rouvre si on matraque A à côté de lui.
