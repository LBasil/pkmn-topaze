# Données de jeu

## Pokémon
- 151 espèces de Kanto seulement (v1). `species_info.h` contient aussi les espèces de Johto/Hoenn (héritage de pokefirered) : elles sont **ignorées** par les outils et non rencontrables.
- Retouches de stats (jalon 3, à valider en jeu) : Tortank DEF 100→95 ; Mackogneur DEF 80→75 ; Léviator ATK 125→120, PV 95→90 ; Dracaufeu DEF 78→83, DEF SPE 85→90.

## Attaques
- **Coupe** : Plante, 60. **Force** : Roche. **Éclate-Roc** : puissance 60. **Flash** : `EFFECT_HIT`, 30, 100 %, Électrique. Les effets hors combat (couper un arbre, déplacer un rocher…) sont inchangés.
- **Équilibrage (jalon 4)**, script `docs/topaze/balance_moves.py` (25 attaques) :
  - Précision relevée sur les grosses attaques instables : Hydrocanon 80→85, Blizzard 70→80, Fatal-Foudre 70→80, Lance-Flammes… Déflagration 85→90, Plaquage-like Écrasement 75→85, Mégacoup 75→80, Coup-Croix 80→85, Poing Karaté… Poing Dynamik 50→60, Bombe Œuf 75→80, Sacrifice 80→85 ; piégeages (Danse-Flamme/Tourniquet/Tomberoche/Claquoir) 70-75→85.
  - Attaques trop faibles : Fouet Lianes 35→45 (PP 10→25), Purédpois 20→30 (préc. 70→80), Léchouille 20→30, Coud'Boue 20→35 (PP 10→15), Larcin 40→60, Implore 40→60, Sabotage 20→50.
  - **Cohérence des CS** : Coupe 60→65 (préc. 95→100), Vol 70→90 (attaque en 2 tours), Flash 30→40, Plongée 60→80 ; Surf 95, Force 80, Cascade 80 inchangées. Hiérarchie : Coupe < Éclate-Roc < Force = Cascade < Vol < Surf.
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
