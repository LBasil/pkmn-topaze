# Pokémon Topaze — résumé de reprise (13/10/2026)

## Contexte
ROM hack de Pokémon FireRed (décompilation pret/pokefirered, C + agbcc). Dépôt GitHub `LBasil/pkmn-topaze`, branche `topaze` (à attacher et cloner en début de session ; compiler : `make tools -j8 && make -j8 firered`, voir le doc « résumé de session » et `docs/technique/`). Basil = chef de projet et directeur créatif, il écrit en français. Claude = responsable technique avec carte blanche. Le texte du jeu reste en ANGLAIS pour l'instant (placeholders ; traduction FR plus tard, tout est dans les `text.inc`).

## Règles de travail à garder (très important)
1. **Montrer les cartes.** Dès qu'on parle de PNJ, d'objets, de panneaux, de dresseurs ou de Pokémon sauvages d'un lieu, ENVOYER une capture de la carte avec les éléments annotés (rendu `PYTHONDONTWRITEBYTECODE=1 python3 tools/topaze/maps/mapkit.py render <LAYOUT_ID> out.png`, puis cercles et libellés par couleur : jaune = PNJ, rouge = dresseurs/objets, bleu = panneaux, vert = sorties ; agrandir x2). Basil relit les rendus et on itère.
2. **Cohérence avant tout.** Les Pokémon (sauvages ET dresseurs), les textes et le décor doivent s'accorder : types réels du hack (lire `src/data/pokemon/species_info.h`, attaques dans `level_up_learnsets.h`, table des types `docs/data/types.js`), thème du lieu (ex. forêt brûlée → faune des cendres, pas des insectes), lore (une Aura a muté les types il y a 10 ans ; l'abandon ne concerne que certains lieux), histoire déjà écrite. Vérifier aussi les textes d'origine FireRed devenus faux (noms de lieux, types, Pokémon).
3. « Ce qui est fait n'est plus à faire » ; tenir `docs/technique/ARCHITECTURE.md` à jour ; garder l'ancienne version dans une branche `<ville>-v<N>-reference` quand Basil demande un essai ; committer et pousser à la fin de chaque tâche (pas de `__pycache__`) ; mettre à jour les docs du Projet claude.ai (`claude/*.md`, outil Projects).
4. Rester focus sur le **début du scénario**, dans l'ordre du jeu, sans anticiper trop loin. Quand Basil dit « je valide », marquer VALIDÉ dans ARCHITECTURE.md.
5. Tester dans l'émulateur (mGBA, banc `tools/topaze/emu/`, `mkdbg.sh` construit la ROM de debug ; `gTopazeDbg[6]` = `VAR_GRENALUX_OPENING`+1, `[7]` = partenaire).
6. À la fin du jeu : vérifier que **tous les Pokémon sont accessibles** (sauvages, évolutions, échanges/événements). Pokémon sauvages globaux à placer ensuite.

## État d'avancement (début de jeu)
- **Grenalux : TERMINÉ.** Ouverture jouée en émulateur : village paisible → rival → attaque d'Onybris au ranch → choix du partenaire en urgence (Bulbizarre/Carapuce/Salamèche) → combat contre le sbire → maman + PENDENTIF (le vrai grenat, importance cachée) → école (cours des types, TYPE MEMO, combat contre le rival avec le starter opposé) → labo (Pokédex + 5 balls). Ville en deux états (paisible / après l'attaque). Plus de colis de Chêne. Quête du ranch : Doduo + 2 Nidoran fuient sur la Route 1, il faut leur parler **aux trois**, ils rentrent ; l'ouvrier donne 1 Potion + 5 Poké Balls. Script détaillé : `claude/script-grenalux.md`.
- **Route 1 : peuplée** (aucun dresseur ; vendeur Potion, garçon, promeneuse sur les types, panneau ; herbe Roucool/Rattata niv. 3–7, Piafabec rare).
- **Opanihrum : début de jeu VALIDÉ.** Plus de colis de Chêne, plus de barrage ; le vieil homme propose la démo de capture en OUI/NON (+ Teachy TV). Arène (Hepha, Acier) verrouillée jusqu'aux badges 1–7. Script : `claude/script-opanihrum.md`.
- **Route 2 : OK** (aucun dresseur, objets, randonneur, mineur, panneaux ; panneau de la forêt déplacé devant l'entrée).
- **Forêt Calcinée : refonte « faune des cendres » VALIDÉE.** Sauvages : Taupiqueur, Goupix (Feu/Psy), Racaillou, Nosferapti, Fantominus, Pikachu, rares Chenipan/Aspicot. 5 dresseurs devenus campeurs/randonneurs/pique-niqueuse (équipes niv. 6–8). Compilé, vérifié en émulateur.
- Les 10 villes et la plupart des routes sont cartographiées et validées (voir `claude/revue-villes.md`).

## Prochaines étapes (dans l'ordre)
1. **Pyropia** (Kay, Feu) : inventaire des PNJ/panneaux/objets/dresseurs sur la carte annotée, textes, équipes cohérentes avec les types, événements de début de scénario (comme pour Grenalux/Opanihrum), test émulateur.
2. Route 3 et suite du parcours dans l'ordre (le Doc « Parcours du joueur — Pokémon Topaze » : onze étapes, une gemme par ville, verrous/CS) ; à chaque lieu : carte annotée envoyée, faune et dresseurs cohérents avec décor et types.
3. Plus tard : scènes de Bill et des îles Sevii, mine de Grenalux après la Ligue, pendentif/gemme, passe globale sur les Pokémon sauvages (accessibilité de tous), eau animée, déplacer la grotte Azurée.

## Pièges techniques utiles
- Flags/vars de l'ouverture : `VAR_GRENALUX_OPENING` (0 début, 1 ranch, 2 école, 3 labo, 4 fini) ; flags 0x4BD–0x4CA utilisés (voir `include/constants/flags.h`).
- Après changement de carte : `rm -f build/firered/data/maps.o; make -j8 firered`. Les scripts `*_events.py` réécrivent d'anciens warps/événements : ne pas les relancer sans vérifier (ex. panneau Route 2 déplacé à la main).
- Les identifiants de code (`TRAINER_BUG_CATCHER_*`, `sParty_BugCatcher*`) ne sont pas renommés : ne pas s'y fier pour la classe réelle en jeu.
- Warps à pas simple entre tilesets différents : `IsTopazeStepWarpMap()` (`src/field_control_avatar.c`).
