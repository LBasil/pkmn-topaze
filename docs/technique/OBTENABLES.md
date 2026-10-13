# Audit des Pokémon obtenables (13/10)

Script : `docs/topaze/audit_obtenables.py` (sauvages + cadeaux/œufs/combats scriptés + échanges + évolutions + élevage des pré-évolutions).

Résultat : **222 / 361 obtenables** (les 25 Zarbi OLD_UNOWN sont exclus).

Manquants : 
- **Gen 1 (3)** : Kicklee, Tygnon, Porygon — en vanilla ce sont des lots (Dojo, Salle de jeux) ; le script ne détecte pas les lots (valeur dans une variable). À vérifier à la main dans Bourg Quartz et Hematown.
- **Gen 2 (29)** : starters Johto, Hoothoot, Chinchou, Sunkern, Girafarig, Gligar, Snubbull, Corsola, Tyrogue, Miltank, Sudowoodo, Porygon2, Raikou/Entei/Suicune, Celebi…
- **Gen 3 (107)** : presque toute la génération.

Proposition V1 (à valider) : les îles Sevii (post-game) deviennent la source des Pokémon de Johto et Hoenn, une île = un biome (voir PARCOURS.md), plus quelques cadeaux scénarisés (starters via les rivaux/anciens). Légendaires : Raikou/Entei/Suicune et Celebi en post-game, Hoenn (Regis, Latis, Kyogre/Groudon/Rayquaza…) via les ruines Sevii.
