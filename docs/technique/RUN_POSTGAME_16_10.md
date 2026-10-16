# Run du post-game (16/10) : de la fin 1 au Canyon Sevault

Suite de `RUN_COMPLET_15_10.md`. Même autopilote (`tools/topaze/emu/bench/run_full.py`), étapes `ending1`, `pg_pallet`, `pg_indigo`, `pg_mine`, `pg_birds`, `pg_ferry`, `pg_sevii`, `pg_echoes`. ROM de debug en mode dieu, équipe renforcée par `buff()` (niv. 100) pour les 20 Anciens.

## Joué et vérifié
| Étape | Résultat |
|---|---|
| Fin 1 + générique, départ à Grenalux | OK (le moteur ramène à Grenalux via le point de reprise) |
| Brice / Flora / Misty au Centre du Plateau | OK |
| Conseil des Anciens (20 combats) | OK avec le bot renforcé ; sans renfort, 1 Pokémon = blanc-outs |
| Mine de Grenalux (vision, fuite de Mew) | OK (`FLAG_MEW_FLED`) |
| Mew sous le camion d'Apatia | OK (`FLAG_FOUGHT_MEW_TRUCK`) |
| Artikodin (arbre à couper), Électhor | OK |
| Ferry Apatia → île 1 (billets du marin) | OK **après correctif** |
| Écho 1 Raikou, 2 Entei, 3 Suicune | OK (Suicune **après correctif**) |
| Écho 5 Registeel, 6 Regirock, 7 Celebi | OK |
| Scène finale de Sevault (Argent, Giovanni, Red) + 6 légendaires de Hoenn | OK (Kyogre, Groudon, Rayquaza, Latias, Latios, Jirachi) |
| Cadeaux : 5 starters au Centre de l'île 1, Arcko chez Lorelei | joués ; niveau 30 (voir rapport de ressenti) |

## Défauts réels trouvés et corrigés
1. **Ferry inaccessible** : `VAR_MAP_SCENE_ONE_ISLAND_POKEMON_CENTER_1F` n'était jamais ≥ 1 sans la quête Rubis/Saphir d'origine, donc le marin d'Apatia répondait « le bateau est parti ». Le marin pose maintenant la variable à 7 en post-game (`VermilionCity_EventScript_OpenSeviiFerry`). Vérifié sur la ROM, depuis l'état naturel.
2. **Motards de Trois-Îles** : barrière dépendante de la quête Lostelle (Joyful Game Corner). Le Pont du Lien (Suicune) était inatteignable. `ThreeIsland_Port_OnTransition` masque motards et défenseurs en post-game. Vérifié.
3. **Salle du Conseil = piège** : l'entrée se refermait derrière le joueur, sans sortie. Entrée ouverte en post-game, collision retirée sur la colonne centrale, et déclencheur de sortie en (6,12) (la case n'a pas de comportement de warp). Vérifié : sortie vers le Centre du Plateau.
4. **Garde du Plateau** (déjà dans le run précédent) : porte de la Ligue bloquée.

## Non joué par le bot (à vérifier à la main)
- **Sulfura (Mont Brasier)** : le chemin exige la CS06 (Éclate-Roc, donnée à la source chaude de la Route Braise) et la CS04 (Force). Analyse statique : le sommet est atteignable. Le bot oscille entre la Route Braise et l'entrée, car il ne sait ni briser les rochers ni pousser les rochers Force du Mont Brasier.
- **Régice (grotte Glacon, écho 4)** : la cascade de l'entrée et les glaces de la grotte ne sont pas franchissables par le bot. Écho 4 sauté par poke de `VAR_ECHO_STAGE` (10 → 11) pour poursuivre ; cadeau de Lorelei (stade 11) joué.
- Captures : les Poké Balls ne sont pas implémentées dans le bot ; il bat les légendaires, ce qui avance les mêmes scripts (`WON` pose les drapeaux « fait »).
- Équilibrage : bot en mode dieu.

## Améliorations du banc
- `exits()` : une sortie par composante d'arrivée distincte (une poche voisine pouvait masquer la bonne : Chemin d'eau de l'île 6).
- `go()` : un objet masqué par son drapeau HIDE n'est plus un obstacle statique (Sevault, rocher-légendaire).
- `route_test.NOWALK` : comportements jamais franchissables (cascade = 19).
- `plan_objs()` tolère les objets « clone » sans `movement_type`.
- `cut_trees()` ne dépend plus des objets vivants (les arbres hors caméra ne sont pas instanciés) ; `smash_rocks()` ajouté.
- `sail_to(t, île)` : menu du Seagallop (page 1 « Autres »), `echo_step()` : pilote des Échos par `VAR_ECHO_STAGE`.

## Suite (16/10, retours appliqués)
Le flux des Échos a changé : cadeaux et annonces passent par le compas (voir ARCHITECTURE.md). Tests isolés sur ROM de debug : Raikou 1 -> 4, Entei 4 -> 7, Suicune 7 -> 9, Lorelei 11 -> 13, Registeel 13 -> 16, Regirock 16 -> 19, Celebi 19 -> 21, scène de Sevault 21 -> 22, Conseil des Anciens 3 -> 5 (interlude passé). `echo_step` du bot (stades ECHO_PC) n'est plus parcouru qu'au stade 0 ; l'enchaînement complet de bout en bout n'a pas été rejoué (le bot bute sur le retour Kindle Road -> port quand on part de ce point).
