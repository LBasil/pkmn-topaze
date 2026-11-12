# Bot « joueur réel » de Pokémon Topaze

Pilote d'émulateur (mGBA headless) qui joue le jeu **sans mode dieu** : vrais combats, captures, Centres Pokémon, entraînement,
objets, CS, vélo, ferry. Sert de test de bout en bout du scénario (les 3 fins) et de détecteur de défauts de cartes/scripts.

## Pré-requis (chemins en dur)
- Dépôt dans `/home/claude/pkmn-topaze` (cwd = racine du dépôt) ; copies de travail des scripts dans `/tmp/gx` (les scripts y font `sys.path.insert`).
- Lanceur d'émulateur `/tmp/gx/h`, ROM de debug `/tmp/gx/dbg2.gba` + `dbg2.elf` (`build_dbg_fr.sh`), états dans `/tmp/gx/st`.
- Un état n'est valable que pour la ROM qui l'a produit : après toute modification du code C, refaire la chaîne.

## Fichiers
| Fichier | Rôle |
|---|---|
| `tz.py` | base émulateur : `Emu`, touches, lecture mémoire, `Auto` (préréglages) |
| `run_full.py` | étapes (`STAGES`) en mode dieu, navigation (`go`, `route`, `exits`), scènes, arènes |
| `real.py` | cerveau de combat (`Brain`, `BattleMixin`) ; connaissance des adversaires, fuite, oubli de capacité |
| `real_run.py` | classe `Real` : pas de mode dieu, soins au Centre, `hop` (portes) |
| `play.py` | classe `Player` : entraînement (`ensure`, `grind_map`), vélo, Repousse ; `python3 play.py <étapes…>` |
| `opponents.py` / `.json` | 749 dresseurs (équipe, niveaux, IA) ; `need_level()` |
| `ends.py` | de `league_won` vers la fin 2 ou 3 (`ends.py 1` = fin 2, `ends.py 2` = fin 3) |
| `refuge.py`, `refuge_king.py` | chaîne de la fin 2 : 16 postes de gardes, puis chef des chasseurs |
| `reconq.py` | chaîne de la fin 3 : 7 arènes rebelles, hub, 7 Seigneurs |
| `gates.py`, `spin.py`, `fin.py`, `rev.py`, `mkdbg2.py` | utilitaires de test |

## Utilisation
```
sh /tmp/gx/build_dbg_fr.sh                         # ROM de debug
python3 /tmp/gx/run_full.py ranch school lab route1q opan   # mode dieu jusqu'à Opanihrum
python3 /tmp/gx/play.py gym1 … victory league      # joueur réel jusqu'à la Ligue (états real_<étape>.ss)
python3 /tmp/gx/ends.py 1 ; python3 /tmp/gx/refuge.py ; python3 /tmp/gx/refuge_king.py   # fin 2
python3 /tmp/gx/ends.py 2 ; python3 /tmp/gx/reconq.py end3_done                          # fin 3
```
Les journaux vont dans des fichiers ; surveiller les jalons avec `grep "SAVE real_"`.

## Limites connues
- Le bot n'entraîne que la tête d'équipe jusqu'au niveau cible : les duels de fin de partie (chefs rebelles jusqu'au niv. 88-91) demandent plusieurs entraînements.
- Pas d'utilisation des Super Bonbons ; le Pokédex de la fin 2 (200/300 espèces pour Ho-Oh/Deoxys) n'est pas rempli en vrai.
- Les soins en plein scénario peuvent déposer le bot ailleurs : chaque étape revérifie sa carte (`_scene_map`, `_healing`).
