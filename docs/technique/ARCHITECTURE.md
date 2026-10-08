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
| **Musée de Grenalux** (nouvelle carte) | `data/maps/PalletTown_Museum/` (intérieur = disposition du Musée d'Argenta, PNJ/textes propres), façade ajoutée dans `data/layouts/PalletTown/map.bin` à la place du jardin (copie des tuiles de la maison du joueur), warp 3 de `PalletTown/map.json` ; outils : `tools/topaze/maps/mapkit.py` |
| Ville de départ Grenalux | `PalletTown` (`text.inc`), `region_map_entry_strings.h` |
| Rival par défaut ZEPHYR | `data/text/new_game_intro.inc` |
| Team Onybris | ~58 fichiers (classe de dresseur + dialogues), remplacement de « TEAM ROCKET » / « ROCKET » dans les `.string` uniquement |

## Slots réutilisés (important)
Les champions occupent les emplacements des chefs d'arène d'origine : `Brock→Kay`, `Misty→Sylvestre`, `Lt. Surge→Hera`, `Erika→Grim`, `Koga→Achlys`, `Sabrina→Nox`, `Blaine→Eddie`, `Giovanni→Hepha`. Les **identifiants de code** (`TRAINER_LEADER_BROCK`, `sParty_LeaderBrock`…) n'ont pas été renommés : ne pas s'y fier pour le nom en jeu. Les sprites sont encore ceux d'origine.
