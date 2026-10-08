# Données de jeu

## Pokémon
- 151 espèces de Kanto seulement (v1). `species_info.h` contient aussi les espèces de Johto/Hoenn (héritage de pokefirered) : elles sont **ignorées** par les outils et non rencontrables.
- Retouches de stats (jalon 3, à valider en jeu) : Tortank DEF 100→95 ; Mackogneur DEF 80→75 ; Léviator ATK 125→120, PV 95→90 ; Dracaufeu DEF 78→83, DEF SPE 85→90.

## Attaques
- **Coupe** : Plante, 60. **Force** : Roche. **Éclate-Roc** : puissance 60. **Flash** : `EFFECT_HIT`, 30, 100 %, Électrique. Les effets hors combat (couper un arbre, déplacer un rocher…) sont inchangés.
- Apprentissage : **~130 attaques STAB** ajoutées par `docs/topaze/learnsets_stab.py`, par palier d'évolution (niv. 13/31, 20/38, 28/44 selon le stade). Limite : 20 entrées par apprentissage (le script la respecte). Format normalisé `LEVEL_UP_MOVE(1, …)`.

## Dresseurs
- Source de vérité des champions : `docs/topaze/leaders_data.py` → écrit `sParty_Leader*`. Équipes (niveaux, IV progressifs 40→120, attaques personnalisées) visibles sur la page **Gym Champions** du site.
- Format : `struct TrainerMonNoItemCustomMoves { .iv .lvl .species .moves }`, équipes de 4 à 5 Pokémon (6 possible : max du jeu).
- Dresseurs « ordinaires » : niveau ×1,12 (minimum +1) via `harder_world.py`, **hors** tableaux `Leader`, `EliteFour`, `Champion`, `RSChampion`.

## Rencontres sauvages
`wild_encounters.json` : `land_mons` +2 niveaux si le maximum < 10, sinon +3 ; les Zarbi (Unown) sont exclus. Ne pas relancer le script deux fois (l'effet s'additionne).

## Textes
Gen 3 : 1 octet par caractère, tables de largeur fixe. « ONYBRIS » (7) est plus long que « ROCKET » (6) : surveiller les débordements de boîtes de texte et d'enseignes. La classe de dresseur `TEAM ONYBRIS` tient dans 12 caractères.
Les identifiants internes (`MAPSEC_ROCKET_HIDEOUT`, `MUS_ENCOUNTER_ROCKET`, `LOCALID_*ROCKET*`…) gardent « ROCKET » à dessein.
