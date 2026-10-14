# Éditeur de cartes Topaze (v1)

Application web locale, sans dépendance à installer (Python 3 + Pillow, déjà requis par `mapkit.py`).

```bash
python3 tools/topaze/editor/server.py        # puis ouvrir http://localhost:8765
```
Le serveur lit et écrit directement `data/maps/<Carte>/map.json` et `data/layouts/<X>/map.bin`. Un enregistrement sans modification ne change aucun octet (vérifié sur les 455 cartes) ; tout se défait avec `git checkout`.

## Fonctions de la v1
- Liste des cartes (filtre), palette de métatuiles avec les vrais graphismes (tampons rectangulaires par glisser), pinceau, remplissage, pipette (clic droit), annuler/rétablir (Ctrl+Z / Ctrl+Y), Ctrl+S.
- Collisions et altitudes visibles (case rouge = bloquant) et éditables ; les tuiles peintes reçoivent la collision/altitude choisies à gauche (défaut 0 / 3).
- Événements : PNJ (avec leur sprite), panneaux, warps, déclencheurs — création, déplacement par glisser, édition de tous les champs avec auto-complétion (graphics, mouvements, flags, vars, cartes), suppression. Portée de vue des dresseurs.
- Avertissements : warp vers une carte inconnue, événement hors carte, graphics_id inconnu, layout partagé entre plusieurs cartes.

## Après une modification de carte
`rm -f build/firered/data/maps.o && make -j8 firered` (sinon la ROM garde les anciennes cartes).

## Pas encore (versions suivantes)
Création de carte et de connexions, édition des textes et des scripts, bouton « compiler et tester », contrôle des raccords, vérification du dest_warp_id, redimensionnement de carte.
