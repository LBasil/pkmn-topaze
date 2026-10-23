# Lieux et systèmes encore à refaire (liste de Basil, 22/10)

## Corrigé le 22/10 (build du soir)
- Centrale (Manoir 3F) : Selene bloque la pierre ; toucher le piédestal sans l'avoir battue la déclenche.
- Volcan B4F : Kronos/Gold/Silver déplacés d'une case (ils se tenaient dans la lave) ; texte de Kronos ne dit plus que le boss a la pierre (le joueur a le TOPAZ).
- Route Victoire 1F/2F/3F : plus de barrières de rochers (rochers « déjà tombés sur les interrupteurs »).
- Route Victoire 1F : Naomi devient une INFIRMIÈRE : combat, puis elle soigne à chaque discussion.
- Arène de Chrondrolia : plus de clé secrète.

## À refaire (non fait)
1. **Chrondrolia entière** (« Cramois'Île ») : intérieur de la centrale = ancien Manoir (recolorer/reconcevoir), scène du maire, rythme.
2. **Volcan Écume** : un seul rocher poussé sur 3 étages mène directement au boss (arrivée trop tôt) -> verrouiller / redessiner le parcours B1F-B4F.
3. **Eau / lave** : transitions bizarres au Manoir (Pokémon Mansion) et à Cramois'Île : une partie inondée de lave (obsidienne), l'autre inchangée -> homogénéiser.
4. **Route 23** : à refaire entièrement (contrôle des badges de la Ligue).
5. **Route Victoire** : refonte complète (+ infirmières à d'autres endroits possibles).
6. **POKéRADAR** : le refaire comme sur la capture de Basil (menu au choix : herbe / eau / etc., avec l'image du Pokémon).
7. Bourg Quartz : repaire seulement recoloré.
8. PNJ inutiles / mal placés routes 14, 15, haut de la route 13.
9. Îles Sevii, Bill, grotte Azurée à déplacer, Ligue/Plateau, intérieurs de la Tour Pokémon, Route 5 et 9, Tunnel Roche, Tour Spinelle (niveaux).
10. Sprites provisoires (Brice, Flora, N, Gold, Silver, Red, Kronos, Vesper, Selene, Hepha...).

## Retours du 23/10 (post-game et fin)
Corrigé : Mew placé près du camion (Apatia) ; Bill à la sortie d'Une-Île a maintenant un dialogue qui renvoie au Centre ; indices automatiques post-game (marin du ferry à Apatia, mine à Grenalux, flags 0x10F/0x110).
À faire :
- Dernier repaire : il manque un admin (Selene/Kronos/Vesper... à placer avant le boss).
- Cinématiques : trop peu de mise en scène (global) ; on ne comprend pas pourquoi le boss part (« il a tabassé Red »).
- ~~Défaite contre le boss : il faut refaire Lorelei~~ -> FAIT 23/10 : `FLAG_TOPAZE_BOSS_RETRY` (0x0FF) posé quand Chen est battu ; à l'entrée de la salle de Lorelei, le joueur est téléporté directement au boss, sans question (équipe soignée, warp salle du Champion, le script reprend à la partie boss).
- Mine de Grenalux = Mont Sélénite recopié, vide : à refaire / à remplir ; rien n'y mène à part l'indice.
- Vol pendant le Surf : avatar cassé (à reproduire ; demander à Basil le symptôme exact).

## Îles Sevii : passe d'ambiance faite le 23/10 (`docs/topaze/sevii_dress.py`)
Îles 1-2-3 « braise » (herbe ocre, sable cendre), îles 4-5 « automne » (feuillages roux, eau indigo), îles 6-7 « tropical » (émeraude, corail, eau turquoise). Ports, maisons, grottes et intérieurs inchangés. Reste : villes sans identité propre (décor, PNJ, dialogues), grottes, Mt Ember/Icefall/Tanoby à habiller, sprites provisoires, textes des Échos.

## Guidage post-game Sevii (23/10)
- **TIME COMPASS** (ancien VS Seeker, donné par Bill) : l'utiliser depuis le sac (`data/scripts/echo_compass.inc`, hook dans `FieldUseFunc_VsSeeker` quand `VAR_ECHO_STAGE >= 1`) dit la prochaine étape selon le stage (île + lieu, ou « voir Bill/Célio/Lorelei »). Les 21 stades sont couverts ; stade >= 22 : « les échos sont fermés ».
- Les joueurs peuvent aller sur toutes les îles dans le désordre (tous les pass) : le compas est le fil conducteur ; Bill/Célio répètent aussi le lieu. À faire : panneaux/PNJ de guidage dans chaque port, journal de quête.

## Guides de port Sevii (23/10)
Chaque port (îles 1 à 7) a un PNJ guide en (6,4) : présente l'île (2 paragraphes) puis, si `VAR_ECHO_STAGE >= 1`, lit la TIME COMPASS (`EventScript_EchoCompass`). Reste : décor par île, textes des villes, panneaux, journal de quête.
- Sevii 23/10 : panneaux d'île (7) et PNJ d'ambiance (Une-Île, Six-Îles, Sept-Îles) réécrits sur le thème « le temps se dérègle ».

## Mine de Grenalux raccourcie (23/10)
La porte de la mine (Grenalux) mène directement à l'étage de la vérité (GrenaluxMine_3F, warp 3) : ~20 pas au lieu de trois étages. Trois moments avant la vision : entrée silencieuse (« It is silent here »), murmure + secousse en (9,6) (« …remember… »), lueur des veines en (13,8), puis la vision et Mew (inchangés). Les cartes 1F/2F restent dans la ROM mais ne sont plus atteignables.
