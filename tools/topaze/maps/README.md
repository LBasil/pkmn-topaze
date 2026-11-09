# Outils de cartes (sans Porymap)

`mapkit.py` lit/écrit `map.bin` et dessine une carte en PNG avec ses vraies tuiles :

```bash
python3 tools/topaze/maps/mapkit.py render LAYOUT_PALLET_TOWN /tmp/grenalux.png
```
Les cartes se modifient par script Python (copie de blocs de métatuiles entre zones) puis `map.json` (objets, warps, panneaux) ; les nouvelles cartes s'ajoutent dans `data/maps/map_groups.json` et leurs `scripts.inc`/`text.inc` dans `data/event_scripts.s`. Exemple : le musée de Grenalux (voir ARCHITECTURE.md).

## Analyseur de cohérence (`analyze.py`)

```bash
python3 tools/topaze/maps/analyze.py . --ref <racine_firered> --out /tmp/rapport.json --md docs/scenario/ANALYSE_CARTES.md
```
Passe sur toutes les maps (4 s) : tuiles valides, warps (destination, retour, case, position (0,0) jamais placée), connexions (réciproques, bords qui se raccordent),
événements (hors carte, sur un mur, empilés, script inexistant), déplacement (rebords à sens unique, sortie impossible, PNJ/panneaux inatteignables, comptoirs gérés),
rencontres sauvages (herbe sans table / table sans herbe) et accessibilité GLOBALE depuis la chambre du joueur (warps + connexions + warps de script + points de Vol).
`--ref` : un problème n'est « nouveau » que s'il n'existe pas déjà à la même position dans FireRed d'origine (le jeu d'origine a lui-même du bruit : ~800 alertes). Codes : E = casse le jeu, W = à vérifier, I = info.
