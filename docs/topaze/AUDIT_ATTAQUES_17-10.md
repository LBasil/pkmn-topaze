# Audit attaques et movepools (17/10/2026, build 22h15)

## Attaques par type (426)
Normal 131 · Psy 29 · Combat 26 · Plante 26 · Eau 22 · Feu 21 · Vol 17 · Ténèbres 17 · Glace 16 · Sol 16 · Poison 16 · Électrik 15 · Insecte 14 · Spectre 14 · Roche 12 · Acier 12 · Fée 11 · Dragon 10.
Scripts : `add_moves.py` (72 attaques Gen 4+), `add_moves_learn.py` (1re distribution), `movepool_fix.py` (échelle de STAB + signatures + évolutions), `audit_movepool.py` (mesure).

## Règles vérifiées pour chaque espèce (types ACTUELS du hack)
- Par type : une attaque de STAB ≥ 35 de puissance avant le niv. 25, ≥ 60 avant le niv. 42 (dès le 2e stade), ≥ 85 (ou la 2e plus forte du type) pour les formes finales de BST ≥ 420.
- Catégorie (physique/spéciale) choisie selon la meilleure stat offensive.
- Limite 24 entrées par espèce (Rappel d'attaques) ; une évolution hérite des ajouts de son pré-stade.
- Exceptions volontaires : Métamorph, Mime/Qulbutoké, Cocons, Wynaut, Évoli-like inchangés, Kecleon/Castform/Girafarig/Aipom (Normal 70).
## Résultat
110 espèces complétées (150 attaques), ~85 signatures modernes (Flare Blitz, Moonblast, Dragon Pulse, Brave Bird, Flash Cannon…). Formes finales BST ≥ 300 : 6 à 24 attaques offensives, sauf Qulbutoké (1, par design).
