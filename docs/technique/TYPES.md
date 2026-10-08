# Système de types

## Types des 151
Appliqués par script (`apply_types.py`, 66 espèces modifiées) dans `species_info.h`. Référence lisible : la page **Pokédex** du site joueur (`docs/pokedex.html`, générée depuis le code) et `docs/topaze/types_v0_raw.md` (première proposition brute).

Règles de cohérence retenues : Dracolosse Dragon/Vol, Léviator et Hypocéan Eau/Dragon, Ptéra Roche/Dragon, Nosferapti/Nosferalto Poison/Ténèbre, famille de Fantominus Spectre/Ténèbre, Miaouss/Persian Ténèbre, Krabboss Eau/Combat, Kangourex Normal/Combat, Ossatueur Sol/Spectre, Canarticho Combat/Vol.
Starters : Bulbizarre Plante/Sol, Salamèche Feu/Glace, Carapuce Eau/Acier.

## Le type Fée (index 18)
Gen 3 a 17 slots de type (0–16, dont `???` à 9). Fée est ajouté à l'index **18**, ce qui impose de toucher :
1. `TYPE_FAIRY 18` et `NUMBER_OF_MON_TYPES 19` (`include/constants/pokemon.h`).
2. `gTypeNames[TYPE_FAIRY]` = `"FAIRY"` (`battle_main.c`).
3. **12 lignes** dans `gTypeEffectiveness` (la table est triée par ordre d'insertion, terminée par `TYPE_FORESIGHT`, taille portée de 336 à **372** octets — l'oublier donne `excess elements in array initializer`) :
   - Fée super efficace contre Combat, Dragon, Ténèbre ; peu efficace contre Feu, Poison, Acier.
   - Poison et Acier super efficaces contre Fée ; Combat, Insecte, Ténèbre peu efficaces contre Fée ; Dragon sans effet sur Fée.
4. Puissance cachée : `((18 - 3) * typeBits) / 63 + 1` — on garde 15 types possibles, Fée exclu.
5. `tm_case.c` : `[TYPE_FAIRY] = 0x0d0` et `NUM_DISC_COLORS ((18 - 1) * 16)`.
6. `list_menu.c` : `sMenuInfoIcons[TYPE_FAIRY + 1] = { 32, 12, 0x04 }` ; l'icône est dessinée en (32, 0) dans `graphics/interface/menu_info.png` (feuille 128×128, 16 tuiles/ligne, palette `pokemon_types.pal` de 16 couleurs entièrement utilisées : fond rose = index 12).
7. `battle_message.c` : `gText_AFairyMove` + entrée de table ; `union_room.h` : entrée Fée.

### Catégorie physique/spéciale
Règle Gen 3 : selon le **type** de l'attaque (`type < TYPE_MYSTERY` = physique). Fée (18 ≥ 9) est donc spéciale sans code supplémentaire.

### Attaques de type Fée
Seules Covet, Hyper Voice et Sweet Kiss ont été retypées. Aucun nouveau move n'a été créé.

## Ajouter / modifier un type d'un Pokémon
1. Éditer `.types` dans `species_info.h`.
2. Vérifier que ses attaques de STAB existent (`level_up_learnsets.h`, voir DONNEES.md).
3. `make`, puis régénérer le site (`python3 tools/topaze/build_site.py`).
