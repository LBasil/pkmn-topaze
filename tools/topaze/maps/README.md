# Outils de cartes (sans Porymap)

`mapkit.py` lit/écrit `map.bin` et dessine une carte en PNG avec ses vraies tuiles :

```bash
python3 tools/topaze/maps/mapkit.py render LAYOUT_PALLET_TOWN /tmp/grenalux.png
```
Les cartes se modifient par script Python (copie de blocs de métatuiles entre zones) puis `map.json` (objets, warps, panneaux) ; les nouvelles cartes s'ajoutent dans `data/maps/map_groups.json` et leurs `scripts.inc`/`text.inc` dans `data/event_scripts.s`. Voir `GRENALUX.md` dans `docs/technique` pour l'exemple du musée.
