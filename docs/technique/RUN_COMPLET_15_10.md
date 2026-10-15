# Run complet automatique (15-16/10) : de la chambre aux crédits

Outil : `tools/topaze/emu/bench/run_full.py` (autopilote mGBA, ROM de debug en mode dieu). Étapes jouées dans l'ordre : ranch, école, labo, quête Route 1, Opanihrum, arènes 1 à 8, cottage de Bill, S.S. Anne, Tour Spinelle, Bourg Quartz, Amethiolite, Hematown + tour, Chrondrolia (clé, raid), volcan Écume / Kronos, arène de Giovanni-Hepha, Route 22 → Route 23 → Route Victoire (1F-2F, repaire 1F-3F, Red, opale), Plateau Indigo, tournoi (9 matchs), salle du Champion (Chen, boss, légendaires), Temple de la renommée, **3 fins**, générique « THE END ».

## Défauts réels trouvés et corrigés
1. **Parc Safari occupé** : sortie impossible dans certains états (corrigé en amont de ce run, commit « Safari »).
2. **Étangs / mer non surfables** (altitude de débarquement) : règle de Surf modélisée ; plusieurs sorties de la mer étaient réellement fermées.
3. **Blaine (Eddie)** : après sa défaite, `VAR_MAP_SCENE_CINNABAR_ISLAND` forçait le détour Bill / Sevii. Corrigé : la variable passe à 4, plus de détour forcé.
4. **Route 22 : entrée est scellée par les arbres** : le joueur restait coincé entre Opanihrum et la Ligue. Corridor ouvert (x39-43, y7-8) dans `data/layouts/Route22/map.bin`.
5. **Plateau Indigo : la porte de la Ligue ne s'ouvrait jamais.** Le Pokédex National est actif dès le début (`new_game.c`), or la garde du Centre bloquait la porte tant que `FLAG_SYS_CAN_LINK_WITH_RS` (lien Hoenn à One Island) n'était pas posé. Corrigé : plus aucun verrou (`IndigoPlateau_PokemonCenter_1F/scripts.inc`). Vérifié en émulateur sur la ROM finale.

## Vérifié de bout en bout
- Repaire de la Route Victoire 1F → 3F, scène de Red et de l'opale (`FLAG_VR_BOSS_DONE`).
- Tournoi : tours 0 à 8 gagnés, porte du Champion ouverte, Chen, boss, double combat légendaires (Zapdos, Articuno, Mewtwo en renfort), Temple de la renommée, générique.
- Les trois vœux de Jirachi posent bien `VAR_TOPAZE_ENDING` = 1 / 2 / 3 ; la fin 1 pose `FLAG_TOPAZE_POSTGAME` ; les fins 2 et 3 mènent au Plateau Indigo (`FLAG_SYS_GAME_CLEAR`).

## Limites honnêtes (ce que le bot ne prouve pas)
- Le bot joue en **mode dieu** avec un seul Pokémon : il ne teste pas l'équilibrage des combats. Les blanc-outs contre Vesper (Gengar + Destin Lié) et contre N (Chant Canon) sont des limites du bot ; Vesper est sauté par drapeau, le tournoi est rejoué jusqu'à réussite.
- Énigmes de Force de la Route Victoire **non rejouées** (cartes vanille) : variables posées à 100. Quiz des arènes répondus par le bot.
- Sevii (îles 1-7) **non joué** ; aucune des quêtes optionnelles ; post-game (Red, Giovanni, Argent, Conseil des Anciens) non joué.
- Pour la correction de la garde, les états de la chaîne dataient de l'ancienne ROM : le drapeau a été posé à la main pour continuer, et la porte a été revérifiée seule sur la ROM finale.
- Textes = placeholders anglais, sprites provisoires (hors périmètre).

## Pièges du banc de test
Voir `tools/topaze/emu/bench/README.md` : menu de combat bloqué (cadre Sac), `plan_objs`, soin automatique (`heal`, `heal_battle`), états `scenelong_*` sauvegardés quand une scène dépasse 150 appuis.
