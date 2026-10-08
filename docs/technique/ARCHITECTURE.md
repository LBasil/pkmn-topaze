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
| Monde plus dur | `docs/topaze/harder_world.py` (appliqué une fois aux données) |
| Champions | `src/data/trainer_parties.h` (`sParty_Leader*`), `docs/topaze/leaders_data.py` |

## Textes et narration
| Élément | Fichier |
|---|---|
| Ville de départ Grenalux | `PalletTown` (`text.inc`), `region_map_entry_strings.h` |
| Rival par défaut ZEPHYR | `data/text/new_game_intro.inc` |
| Team Onybris | ~58 fichiers (classe de dresseur + dialogues), remplacement de « TEAM ROCKET » / « ROCKET » dans les `.string` uniquement |

## Slots réutilisés (important)
Les champions occupent les emplacements des chefs d'arène d'origine : `Brock→Kay`, `Misty→Sylvestre`, `Lt. Surge→Hera`, `Erika→Grim`, `Koga→Achlys`, `Sabrina→Nox`, `Blaine→Eddie`, `Giovanni→Hepha`. Les **identifiants de code** (`TRAINER_LEADER_BROCK`, `sParty_LeaderBrock`…) n'ont pas été renommés : ne pas s'y fier pour le nom en jeu. Les sprites sont encore ceux d'origine.
