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

## Volcan Écume et mer de Route 21 (23/10)
- Volcan : plus de raccourci. Principe voulu par Basil : peu importe l'entrée, on doit tout parcourir. La scène du boss (B4F) vérifie que les 6 sbires de B1F/B2F/B3F sont battus (`CountGrunts`) ; sinon texte « chaleur » avec le nombre restant et retour en B3F (12,10). Les rochers restent mais ne servent plus de raccourci (mécanique à reconsidérer en refonte).
- Route 21 Nord : la mer violette (palette 4 de general_route21n) devient bleu sombre « ciel de cendres » pour se raccorder à la Route 21 Sud (avant : mer mauve illisible, transition brutale).
- Route Victoire (refonte à venir) : garder les rochers déjà tombés sur les interrupteurs (demande de Basil).

## Route 23 / Plateau (24/10)
- Palette « aube » (or olive, eau turquoise tiède) pour Route 23 et Plateau Indigo (`docs/topaze/route23_dress.py`, tilesets `general_dawn` / `indigo_dawn`) : la route de la Ligue se lève après la nuit bleue de la Route 22.
- Pas fait : refonte du tracé (7 gardes alignés d'origine). Route Victoire : refonte du tracé non faite non plus (rochers déjà tombés, infirmière présente).

## Cinématique du repaire refaite (23/10)
- **Dernier gardien : KRONOS** (3e admin, 3F du repaire ; `TRAINER_AQUA_LEADER` réaffecté : Arbok 60, Weezing 60, Nidoking 61, Crobat 61, Alakazam 62). Il n'est pas là pour gagner : « le boss m'a demandé cinq minutes de ton temps ».
- Explication donnée au joueur (ce qui manquait) : le pendentif est un **phare** (« tu étais la lampe ») : Onybris n'a jamais eu besoin de rattraper le joueur, seulement de le laisser courir après les pierres. Red n'est pas battu : l'Opale quitte ses mains, c'est tout.
- Voix du boss (« ??? », toujours invisible) : remercie, annonce que le vœu dort au bout de la Ligue (« là où les champions marchent »), invite à gagner le tournoi, « Time is the one thing nobody gets back ». Kronos s'enfuit (fumigène) ; Red se relève, regarde vers la Ligue (il vient aussi).
- Testé en émulateur : scène complète jusqu'à `FLAG_VR_BOSS_DONE`.
- Infirmière déplacée à la 2F de la Route Victoire, près de l'échelle (32,2) ; Naomi redevient sbire.

## Lore : pourquoi le tournoi, alors que le boss a les pierres ? (23/10, corrigé)
Règles posées (dites au joueur par Kronos puis par la voix du boss, repaire 3F) :
1. Les dix pierres sont à lui ; le **cœur** de l'ensemble (le pendentif GRENAT du joueur) ne peut pas être pris : un grenat arraché à son gardien se brise.
2. JIRACHI dort sous la Ligue et ne se réveille que pour un **CHAMPION qui porte le cœur**. Le boss pourrait grimper le tournoi, l'étoile dormirait à travers lui.
3. Il a donc besoin que le joueur devienne Champion avec le pendentif, puis il surgit à la porte (salle du Champion, après Chen/Oak) et prend le vœu de celui qui le tient (« I came for what a CHAMPION wakes »).
4. Pourquoi le joueur y va : récupérer les pierres et arrêter le dérèglement du temps ; le boss lui laisse le choix de rester chez lui (« nothing wakes, the clocks keep bending »).
Cohérent avec : Misty (« le gagnant rencontre JIRACHI »), Hall of Fame (« il se réveille pour toi »), les trois fins.

## Scène des alliés au Plateau (23/10)
Sortie du repaire -> premier passage au Centre du Plateau : Flora, Brice et Misty comprennent le piège (`FLAG_TOPAZE_BRIEFING` 0x111, `IndigoPlateau_PokemonCenter_1F_EventScript_Briefing`, déclenchée à l'entrée). Ils en font un duel : le vœu va d'abord au Champion ; le boss ne peut le prendre qu'en le battant, « dans un lieu que tu as choisi, avec une équipe que tu as construite ». Flora soigne l'équipe. Le tournoi n'est plus subi : c'est la partie jouée par le joueur.

## Onybris « grande organisation » (23/10, 10h) — FAIT
- **Journal télé** : écran vert au mur nord des 17 Centres (bg_event aux cases x11–13, y1, face au nord). 5 paliers selon la progression (badges 0–2 / 3–4 / 5–6 / 7–8 / repaire fini), 2 reportages au hasard par palier, 1 texte « silence » après le Champion. Du « vols isolés » → « bandes organisées » → « ville muette » → « voix à la radio » → « silhouettes sur la route du Plateau ». Script `Topaze_EventScript_NewsTV` dans `data/scripts/topaze_news.inc`.
- **Recruteurs** : PNJ sprite sbire (non-combattant) dans chaque Centre, visibles de 4 badges jusqu'au Champion battu (`FLAG_TOPAZE_HIDE_RECRUITER` = 0x112, posé par `Topaze_EventScript_RecruiterCheck` appelé dans chaque OnTransition). 3 paliers × 2 répliques (raisons humaines, hiérarchie sbires/cadres/« quelqu'un que personne ne nomme », Hematown tombée sans cri, « le chemin doit rester libre pour lui »).
- À faire ensuite (proposé) : retours des trois cadres avant la fin ; sbires visibles pendant le tournoi.
- **Cameos des cadres (23/10, ordre corrigé)** : SELENE au Centre de Lavanville (badge 3 seulement, après Spinellia), KRONOS au Centre de Céladopole (badges 4–5), VESPER au Centre de Parmanie (badges 5–6). Sans combat, au téléphone avec le boss : « sept branches », « milliers de bouches qui sont d’accord », « nous attendons là où tu vas ». Flags 0x113/0x114/0x115 (`FLAG_TOPAZE_HIDE_*`), scripts dans `topaze_news.inc`. Reste : sbires visibles pendant le tournoi.
- **Sbires du Plateau (23/10)** : 6 sbires silencieux flanquent la place devant le Centre (après le repaire, jusqu'au Champion battu ; `FLAG_TOPAZE_HIDE_PLATEAU_GRUNTS` 0x116, `IndigoPlateau_Exterior_EventScript_GruntsCheck`). Une phrase chacun, aucun combat (« Nobody here will touch you. Orders. »). Principe validé par Basil : les villes vivent et ne sont plus de simples étapes.

## Contenu de ville : quêtes annexes Onybris (23/10, modèle posé à Pyropia)
Principe (demande de Basil : « pas juste entrer – badge – partir ») : chaque ville aura une petite quête optionnelle liée à Onybris : un **témoin** (indice), une **cellule** de 2 sbires dans une maison, un **mémo** qui prouve l'ampleur du réseau (« BRANCH 4 of 7… Report to V. »), une **récompense** utile.
- Générateur idempotent : `docs/topaze/town_cells.py` (une fonction par ville ; réaffecte des slots de dresseurs inutilisés en sbires Onybris).
- **Pyropia (fait)** : témoin sur la rue (13,8) devant la porte de la maison 3 ; cellule dans PewterCity_House3 (Ekans/Zubat 14 + Koffing/Grimer 15, TRAINER_GUITARIST/KINDLER) ; mémo au mur nord (9,1) = 2 Rare Candy ; flag 0x117 `FLAG_TOPAZE_CELL_PEWTER`.
- À décliner : Tourmalia, Apatia, Spinellia (Lavanville), Bourg Quartz, Parmanie, Hematown, Chrondrolia, Sevii (via le compas). Flags libres à partir de 0x118.
