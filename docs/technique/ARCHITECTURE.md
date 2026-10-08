# Architecture : où est quoi

Le dépôt est celui de pokefirered ; seuls les éléments modifiés pour Topaze sont listés.

## Données
| Sujet | Fichier |
|---|---|
| Stats, **types**, talents des 151 | `src/data/pokemon/species_info.h` (`.types = {A, B}`) |
| Attaques (type, puissance, effet) | `src/data/battle_moves.h` |
| Apprentissage par niveau | `src/data/pokemon/level_up_learnsets.h` (`LEVEL_UP_MOVE(lvl, move)`, 20 max par Pokémon) |
| Dresseurs (classe, nom) | `src/data/trainers.h` |
| Équipes des dresseurs | `src/data/trainer_parties.h` |
| Rencontres sauvages | `src/data/wild_encounters.json` (régénère un `.h` au build) |
| Cartes, scripts, dialogues | `data/maps/<Carte>/{map.json,scripts.inc,text.inc}` |
| Noms de lieux | `src/data/region_map/region_map_entry_strings.h` |

## Système de types (voir TYPES.md)
| Sujet | Fichier |
|---|---|
| Constantes `TYPE_FAIRY`, `NUMBER_OF_MON_TYPES` | `include/constants/pokemon.h` |
| Table d'efficacité `gTypeEffectiveness[372]`, nom du type | `src/battle_main.c`, `include/battle_main.h` |
| Puissance cachée (exclut Fée) | `src/battle_script_commands.c` |
| Couleur des disques de CT | `src/tm_case.c` |
| Icône de type dans les menus | `src/list_menu.c` + `graphics/interface/menu_info.png` |
| Message « une attaque de type… » | `src/battle_message.c` |
| Union Room (types affichés) | `src/data/union_room.h` |

## Règles de jeu modifiées
| Changement | Où |
|---|---|
| CT infinies | `src/party_menu.c` : 3 appels `RemoveBagItem` supprimés pour `item < ITEM_HM01` |
| CS oubliables | `src/party_menu.c` : `IsMoveHm()` retourne `FALSE` |
| Coupe/Force/Éclate-Roc/Flash devenues des attaques | `src/data/battle_moves.h` |
| **CS sans les apprendre** (Coupe, Éclate-Roc, Force, Cascade, Surf) — **il faut avoir la CS dans le sac** (CS01/06/04/07/03) **et l'insigne** ; aucun Pokémon n'a besoin de la connaître | `data/scripts/field_moves.inc`, `data/scripts/surf.inc` : `checkpartymove` + test remplacés par `setvar VAR_RESULT, 0` (le Pokémon de tête joue l'animation) ; `src/field_player_avatar.c` : `PartyHasMonWithSurf()` renvoie TRUE hors surf. Les **insignes** restent exigés. Vol/Téléport/Flash/Plongée : inchangés (il faut toujours la CS). |
| **Multi Exp. intégré** (tous les Pokémon vivants gagnent de l'XP) | `src/battle_script_commands.c` (3 tests `HOLD_EFFECT_EXP_SHARE` neutralisés, commentés « Topaze ») |
| **Texte rapide** par défaut | `src/new_game.c` (`OPTIONS_TEXT_SPEED_FAST`) |
| **Course partout** (intérieurs, grottes) | `src/bike.c` : `IsRunningDisallowed()` ignore `gMapHeader.allowRunning` |
| Monde plus dur | `docs/topaze/harder_world.py` (appliqué une fois aux données) |
| Champions | `src/data/trainer_parties.h` (`sParty_Leader*`), `docs/topaze/leaders_data.py` |

## Textes et narration
| Élément | Fichier |
|---|---|
| Ouverture : Zéphyr arrête le joueur et le conduit au ranch | `PalletTown_EventScript_OakTrigger` (scripts.inc) réécrit ; objet `LOCALID_PALLET_RIVAL` (GFX Blue) caché par `FLAG_HIDE_PALLET_RIVAL` ; mouvements `walk_to_ranch` ; scène intérieure : `PalletTown_RivalsHouse/scripts.inc` (`OpeningScene`, déclenchée par `VAR_GRENALUX_OPENING`=1) |
| Première rencontre ONYBRIS (Grenalux) | Grunt `TRAINER_TEAM_ROCKET_GRUNT_22` (Rattata/Zubat niv. 4), objet `LOCALID_PALLET_ONYBRIS_GRUNT` dans `PalletTown/map.json`, caché par `FLAG_HIDE_GRENALUX_ONYBRIS_GRUNT` (levé après le combat du rival dans le labo, `PalletTown_ProfessorOaksLab`) ; scripts/textes dans `PalletTown/scripts.inc|text.inc` |
| **Musée de Grenalux** (nouvelle carte) | `data/maps/PalletTown_Museum/` (intérieur = disposition du Musée de Pyropia (ex-Argenta), PNJ/textes propres), façade ajoutée dans `data/layouts/PalletTown/map.bin` à la place du jardin (copie des tuiles de la maison du joueur), warp 3 de `PalletTown/map.json` ; outils : `tools/topaze/maps/mapkit.py` |
| **Grenalux v3 – décors GBA d'Émeraude, plan original** | `docs/topaze/import_emerald_tiles.py` importe les tilesets d'Émeraude (`gTileset_GeneralEmerald`, `gTileset_PetalburgEmerald`, sans animation d'eau) depuis le dépôt public pret/pokeemerald (à cloner dans `../pokeemerald`) ; `docs/topaze/grenalux_emerald.py` assemble le village (maisons, labo, musée copiés d'Émeraude, chemins en sable auto-tuilés, bassin sud relié à la route 21, arbres, fleurs, panneaux) et branche `LAYOUT_PALLET_TOWN` sur ces tilesets. Portes : joueur (6,7), ranch (18,6), labo (18,14), musée (6,14). **Thème GRENAT** : `grenat_palette.py` recolore les palettes (végétation bordeaux, sable rosé, eau violet nuit, toits grenat) et `grenalux_crystals.py` dessine par code des cristaux de grenat (2 grandes grappes, 1 moyenne, petits cristaux ; palette secondaire 7). Ordre de régénération : `import_emerald_tiles.py` → `grenat_palette.py` → `grenalux_emerald.py` → `grenalux_crystals.py`. Ancienne version dessinée à la main : `grenalux_original.py` (v2, conservée pour mémoire). Les trajets des cinématiques sont recalculés (Dijkstra sur la grille de collision) et écrits dans `PalletTown/scripts.inc`. |
| **Grenalux v5 – grande ville 44×36 (référence v5)** | `docs/topaze/grenalux_big.py` (ordre : `import_emerald_tiles.py` → `grenat_palette.py` → `grenalux_big.py`) : avenue nord-sud, grande rue est-ouest, place centrale avec îlot et monument de cristal, bassin sud relié à la route 21, 4 bâtiments utiles (joueur (8,9), ranch (36,8), labo (35,21), musée (8,21)) et 6 maisons décoratives, potager, ~34 arbres, cristaux. Connexions : route 1 décalée de 10 (ouverture en x=22..23), route 21 décalée de 14 (eau en x=21..23). `heal_locations.json` : respawn (8,10). **La v4 (24×20) reste la référence** : branche `grenalux-v4-reference` et `docs/topaze/reference/` (carte, map.json, scripts, image) ; ses scripts (`grenalux_emerald.py`, `grenalux_crystals.py` en `__main__`) restent exécutables mais il faut alors remettre les dimensions 24×20 dans `layouts.json` et `map.json`. |
| **Grenalux v6 – ville vivable (version actuelle)** | `docs/topaze/grenalux_town.py` puis `grenalux_events.py` (ordre : `import_emerald_tiles.py` → `grenat_palette.py` → `git checkout fa8f0d0 -- data/layouts/layouts.json` → `grenalux_town.py` → `grenalux_events.py`). Plan d'occupation avec assertions (aucun chevauchement, portes et PNJ atteignables), toits en variantes de palette (11 ardoise-violet, 12 ocre), lampadaires de cristal, cristaux gardiens de l'avenue, carrière de blocs + entrée de mine à l'est, bassin avec promenade, potager, bosquets, chemins de portes par BFS, 6 PNJ d'ambiance (textes provisoires). Mêmes portes/coordonnées d'événements que la v5 sauf panneau du labo (36,22). Les versions v4 (24×20) et v5 (44×36) restent archivées : branches `grenalux-v4-reference`, `grenalux-v5-reference` et `docs/topaze/reference/`. |
| Ville de départ Grenalux | `PalletTown` (`text.inc`), `region_map_entry_strings.h` |
| Rival par défaut ZEPHYR | `data/text/new_game_intro.inc` |
| Team Onybris | ~58 fichiers (classe de dresseur + dialogues), remplacement de « TEAM ROCKET » / « ROCKET » dans les `.string` uniquement |

## Slots réutilisés (important)
Les champions occupent les emplacements des chefs d'arène d'origine : `Brock→Kay`, `Misty→Sylvestre`, `Lt. Surge→Hera`, `Erika→Grim`, `Koga→Achlys`, `Sabrina→Nox`, `Blaine→Eddie`, `Giovanni→Hepha`. Les **identifiants de code** (`TRAINER_LEADER_BROCK`, `sParty_LeaderBrock`…) n'ont pas été renommés : ne pas s'y fier pour le nom en jeu. Les sprites sont encore ceux d'origine.
