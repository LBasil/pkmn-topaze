# Éditeur de cartes Topaze (v1)

Application web locale, sans dépendance à installer (Python 3 + Pillow, déjà requis par `mapkit.py`).

```bash
python3 tools/topaze/editor/server.py        # puis ouvrir http://localhost:8765
```
Le serveur lit et écrit directement `data/maps/<Carte>/map.json` et `data/layouts/<X>/map.bin`. Un enregistrement sans modification ne change aucun octet (vérifié sur les 455 cartes) ; tout se défait avec `git checkout`.

## Fonctions de la v1
- Liste des cartes (filtre), palette de métatuiles avec les vrais graphismes (tampons rectangulaires par glisser), pinceau, remplissage, pipette (clic droit), annuler/rétablir (Ctrl+Z / Ctrl+Y), Ctrl+S.
- Collisions et altitudes (case rouge = bloquant) : masquées par défaut, case « collisions » ou touche C ; toujours visibles avec l'outil Collision ; les tuiles peintes reçoivent la collision/altitude choisies à gauche (défaut 0 / 3).
- Événements : PNJ (avec leur sprite), panneaux, warps, déclencheurs — création, déplacement par glisser, édition de tous les champs avec auto-complétion (graphics, mouvements, flags, vars, cartes), suppression. Portée de vue des dresseurs.
- Avertissements : warp vers une carte inconnue, événement hors carte, graphics_id inconnu, layout partagé entre plusieurs cartes.

## Après une modification de carte
`rm -f build/firered/data/maps.o && make -j8 firered` (sinon la ROM garde les anciennes cartes).

## Pas encore (versions suivantes)
Création de carte et de connexions, édition des textes et des scripts, bouton « compiler et tester », contrôle des raccords, vérification du dest_warp_id, redimensionnement de carte.

## Dialogues / traduction FR (page /dialogues)
`python3 tools/topaze/editor/server.py` puis ouvrir http://localhost:8765/dialogues (lien aussi dans l'editeur de cartes).
- Pour chaque texte d'une carte : qui parle (sprite, case), conditions d'apparition (flags / variables / badges / dresseur battu), l'anglais en boites de jeu, la saisie du francais, plan de la carte avec le PNJ entoure.
- Saisie : une ligne vide = nouvelle boite de texte ; 35 caracteres max par ligne (compteur rouge) ; « Retour auto » coupe a 35 et fait des boites de 2 lignes. Ctrl+S enregistre.
- Stockage : `i18n/fr/<Carte>.json` (texte FR + copie de l'EN traduit ; si l'EN change, la carte passe en « a revoir »).
- ROM francaise : `sh tools/topaze/i18n/build_lang.sh fr` -> `Topaze_FR.gba` (les sources restent en anglais ; un texte non traduit reste en anglais). ROM anglaise : `build_lang.sh en`.
- Perimetre v1 : dialogues des cartes (4182 textes). Pas encore : textes C (menus, objets, attaques), noms.
