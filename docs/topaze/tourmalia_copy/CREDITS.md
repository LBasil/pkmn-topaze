# Tourmalia v23 : copie exacte de la carte d'inspiration

Les pixels de la ville viennent d'une capture de carte d'un **fan-game** que Basil a envoyee comme inspiration (auteur inconnu).
La carte est decoupee telle quelle en tuiles (copie exacte, aucune retouche artistique, 92 couleurs fusionnees en 36 pour tenir dans 11 palettes GBA).

- **Prototype / usage prive uniquement.** Avant toute diffusion publique de la ROM : obtenir l'accord de l'auteur et le crediter, ou remplacer ces tuiles par des graphismes originaux.
- Source : `34805252-image.png` (piece jointe de la conversation du 30-10), grille 16 px, decalage (10, 0), 84 x 46 cases.
- Donnees derivees dans ce dossier : `grid.pkl` (indices de metatuiles + pixels), `pal.pkl` (fusion des couleurs + palettes), `crop.png` (recadrage).
- Regenerer : `python3 docs/topaze/tourmalia_copy.py` puis `tourmalia_river_events.py` puis `fog_strips.py`.
