# Banc de scénarios (copie de travail du 13/10)
Copiés tels quels depuis /tmp/gx (chemins en dur : `/tmp/gx`, `/home/claude/pkmn-topaze` ; à adapter).
- `mkdbg2.py` : construit la ROM de debug (équipe forte, drapeaux/variables préchargés, mode « dieu », pas de combat) et la remet à zéro ; sauvegarde aussi `.map` et `.elf`.
- `drive.py` : pilote mGBA (harnais `harness.c`) ; `tz.py` : classe `T` (boot sur une carte, marche BFS, `scene()` qui joue dialogues/combats jusqu'au retour du contrôle, `chain` de warps, portes à collision, escaliers).
- `spin.py` : BFS avec cases-flèches (le joueur continue tout droit sur sol normal après une flèche, jusqu'à une case d'arrêt 0x58 ou un obstacle). `xreach.py` : atteignabilité statique à travers les warps.
- Audit statique des dresseurs dans les couloirs : `docs/topaze/audit_couloirs.py`.
Adresses utiles (ROM de debug) : gMain 0x030030f0 (callback2 +4, inBattle +0x439 bit0), sLockFieldControls 0x03000f9c, gObjectEvents 0x02036e38 (0x24 par objet, coordonnées +7 à +0x10).

## Mise à jour du 15/10
- Les adresses mémoire en dur (tz.py, drive.py) ont été recalculées pour la build du 15/10 (`arm-none-eabi-nm dbg2.elf | grep -E ' (gMain|gSaveBlock1Ptr|gObjectEvents|gTopazeDbg|CB2_Overworld)$'`). Elles bougent à chaque build qui change la taille des variables : si les tests ne trouvent plus la position du joueur (`pos()` renvoie None, ou le jeu reste dans la chambre), recalculer avec `nm`.
- `harness.c` : `desiredVideoDimensions` remplacé par `baseVideoSize` (mGBA récent). Compiler vers `/tmp/gx/harness` (voir `../README.md`).
- Nouveaux scénarios : `volcan_scene_test.py` (B4F : Kronos, la pierre était déjà partie), `lair_finale_scene_test.py` (le pendentif attire l'ombre vers Red), `league_rival_name_test.py` (rival renommé affiché dans le combat de Ligue).


## Autopilote `run_full.py` (15/10) : une vraie partie, du début aux crédits
`python3 run_full.py [etape ...]` (cwd = racine du dépôt, `PYTHONDONTWRITEBYTECODE=1`, copier `run_full.py tz.py spin.py` dans /tmp/gx). Boot sur la chambre (ROM `/tmp/gx/dbg2.gba`, mode dieu), puis enchaîne les étapes `STAGES` (ranch, école, labo, quête Route 1, Opanihrum, arènes 1-8, cottage, S.S. Anne, tour, Bourg Quartz, Amethiolite, Hematown, Chrondrolia + raid, volcan Écume, repaire de la Route Victoire, Ligue : tournoi, Champion, 3 fins, générique). Chaque étape part de l'état sauvegardé de la précédente (`/tmp/gx/st/<etape>.ss`) : `python3 run_full.py gym8` reprend après `seafoam`.
- Graphe statique carte/composante accessible + warps ; `go(carte)` marche jusqu'à la carte voulue (portes, flèches, téléporteurs internes, Surf, arbres à couper, rochers Force non gérés), lit la grille VIVANTE (RAM) à chaque carte, laisse jouer les scènes et les combats (`scene()`), et sauvegarde `hopfail_*` / `noroute_*` quand un passage échoue (à rejouer avec `Auto.resume`).
- Règles moteur modélisées : altitude (0 et 15 libres), corniches, case-flèche + arrêt 0x58, portes à tapis, ligne de vue des dresseurs, Surf (embarquement libre, **débarquement seulement sur altitude 3** = `CanStopSurfing`), arènes à quiz (`quiz_signs`), ferry (`sail`).
- Piège : les objets hors de portée de la caméra ne sont pas dans `live_objs()` ; `plan_objs()` ajoute les objets immobiles du JSON, sinon le plan change selon la position et le joueur oscille (arène de la Fonderie).
- Ne jamais lancer `pkill -f run_full` dans la même commande shell (le motif tue le shell) ; lancer avec `setsid nohup … &` et lire `run.out` (sortie bufferisée : `python3 -u`).
- Soins : `heal()` (équipe, entre les pas) et `heal_battle()` (combattant actif, à chaque appui en combat) ; le bot n'a qu'un Pokémon, donc Destin Lié / Chant Canon le tuent quand même (limite connue ; Vesper sauté par drapeau, tournoi rejoué).
- Menu de combat : la variation de `scene()` revient au menu d'actions (B,B,B,HAUT,GAUCHE,A) avant de changer de capacité ; sinon le curseur reste sur SAC et la boucle ouvre le Sac sans fin. Les scènes de plus de 150 appuis sauvegardent `scenelong_<carte>.ss`.
- La case d'arrivée de la salle de Lorelei est une porte à collision : le graphe statique n'y trouve pas de composante, `league_enter()` franchit la porte à la main.

## Post-game (16/10)
Étapes : `pg_pallet`, `pg_indigo` (Anciens, `buff()`), `pg_mine`, `pg_birds`, `pg_ferry`, `pg_sevii`, `pg_echoes` (`echo_step()` selon `VAR_ECHO_STAGE`, `sail_to()` pour le ferry). Les états sont reprenables : `python3 resume_echo.py echo_12` (voir `RUN_POSTGAME_16_10.md`).
- La ROM de test doit être celle des correctifs ; sinon le ferry et Trois-Îles sont simulés par poke dans `stage_pg_ferry` / `go_isle`.
- `Auto(map,x,y,party=True,pre=(drapeaux),prevars={...})` : **`party=True` obligatoire** pour que les drapeaux/variables de préréglage soient appliqués (sinon ils sont ignorés en silence).
- Les objets hors caméra ne sont pas instanciés : approcher d'abord, puis agir (`cut_trees`, `smash_rocks`).
- Un légendaire masqué par `FLAG_HIDE_*` n'apparaît qu'au rechargement de la carte (OnTransition) : sortir puis rentrer.

