# Lieux et systèmes encore à refaire (liste de Basil, 22/10)

## Corrigé le 22/10 (build du soir)
- Centrale (Manoir 3F) : Selene bloque la pierre ; toucher le piédestal sans l'avoir battue la déclenche.
- Volcan B4F : Kronos/Gold/Silver déplacés d'une case (ils se tenaient dans la lave) ; texte de Kronos ne dit plus que le boss a la pierre (le joueur a le TOPAZ).
- Route Victoire 1F/2F/3F : plus de barrières de rochers (rochers « déjà tombés sur les interrupteurs »).
- Route Victoire 1F : Naomi devient une INFIRMIÈRE : combat, puis elle soigne à chaque discussion.
- Arène de Chrondrolia : plus de clé secrète.

## À refaire (non fait)
1. **Chrondrolia entière** (« Cramois'Île ») : intérieur de la centrale = ancien Manoir (recolorer/reconcevoir), scène du maire, rythme.
2. ~~**Volcan Écume**~~ (déjà verrouillé : la fin ne s'ouvre qu'une fois les 6 sbires des étages battus, aucun raccourci) : un seul rocher poussé sur 3 étages mène directement au boss (arrivée trop tôt) -> verrouiller / redessiner le parcours B1F-B4F.
3. **Eau / lave** : transitions bizarres au Manoir (Pokémon Mansion) et à Cramois'Île : une partie inondée de lave (obsidienne), l'autre inchangée -> homogénéiser.
4. **Route 23** : à refaire entièrement (contrôle des badges de la Ligue).
5. **Route Victoire** : refonte complète (+ infirmières à d'autres endroits possibles).
6. **POKéRADAR** : le refaire comme sur la capture de Basil (menu au choix : herbe / eau / etc., avec l'image du Pokémon).
7. Bourg Quartz : repaire redessiné (fait le 23/10, voir section dédiée).
8. PNJ inutiles / mal placés routes 14, 15, haut de la route 13.
9. Îles Sevii, Bill, grotte Azurée à déplacer, Ligue/Plateau, intérieurs de la Tour Pokémon, Route 5 et 9, Tunnel Roche, Tour Spinelle (niveaux).
10. Sprites provisoires (Brice, Flora, N, Gold, Silver, Red, Kronos, Vesper, Selene, Hepha...).

## Retours du 23/10 (post-game et fin)
Corrigé : Mew placé près du camion (Apatia) ; Bill à la sortie d'Une-Île a maintenant un dialogue qui renvoie au Centre ; indices automatiques post-game (marin du ferry à Apatia, mine à Grenalux, flags 0x10F/0x110).
À faire :
- Dernier repaire : admin KRONOS ajouté (fait, voir plus bas).
- Cinématiques : trop peu de mise en scène (global) ; on ne comprend pas pourquoi le boss part (« il a tabassé Red »).
- ~~Défaite contre le boss : il faut refaire Lorelei~~ -> FAIT 23/10 : `FLAG_TOPAZE_BOSS_RETRY` (0x0FF) posé quand Chen est battu ; à l'entrée de la salle de Lorelei, le joueur est téléporté directement au boss, sans question (équipe soignée, warp salle du Champion, le script reprend à la partie boss).
- Mine de Grenalux = Mont Sélénite recopié, vide : **remplie le 23/10** (`docs/topaze/mine_fill.py`) : 3 mineurs qui racontent la veine (« les murs bourdonnent », « la lueur n'est pas celle de nos lampes »), 3 objets au sol, 4 objets cachés (flags 0x126-0x12C). Elle reste courte et muette à dessein ; la géométrie (copie du Mont Sélénite) n'est pas redessinée.
- Route Victoire 1F–3F : déjà refaite (progression, tileset), pas de redessin supplémentaire.
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
- **Fait (23/10)** : Tourmalia (Cerulean House3, branche 2, signé K, 20-21, PP Plus ; flag 0x118), Apatia (Vermilion House2, branche 6, 26-27, 3 Rappels ; 0x119), Lavanville (House2, branche 5, 29-30, 2 Élixirs ; 0x11A), Parmanie (House3, branche 1, 35-36, 2 PP Plus ; 0x11B). Mémos signés V / K / S, numérotés 1 à 7 : le joueur comprend que le réseau compte sept branches.
- À décliner : Bourg Quartz, Hematown, Chrondrolia, Sevii (via le compas). Flags libres à partir de 0x11C.
- Correctif : lignes de texte > 35 caractères dans la quête de Pyropia (version envoyée à 10h40) raccourcies.

## Routes 13-15 (23/10, main game)
Basil : « tout sauf trop de dresseurs » (mal placés, hors thème). Fait : 6 motards deviennent des **sbires Onybris** (Jared R13 ; Gerald, Malik, Isaac R14 ; Ernest, Alex R15) : classe TEAM_ROCKET, sprite sbire, nom GRUNT, textes réécrits (« we are not a gang, we are a union », « the boss pays better than the gym ever did »…). Script idempotent `docs/topaze/routes_onybris.py`. Les Pokémon (poison/électrik de motard) restent. Non fait : repositionnement fin des dresseurs (pas de cas précis identifié), Manoir/Cramois'Île lave-eau (rendu normal en carte ; attend une capture de Basil pour cibler l'endroit exact).

## Audit global des cartes (23/10, demandé par Basil)
- Outil : `docs/topaze/audit_global.py` (455 cartes : raccords de bord entre cartes voisines, sorties séparées avec/sans PNJ). Résultat : **un seul bug réel, causé par moi** (témoin de Parmanie posé dans l'unique couloir de la maison 3 → déplacé en (34,24)). Tous les autres barrages sont voulus (police de Lavanville/Parmanie/Apatia, arbre à couper d'Apatia, rocher Force de la Route Victoire 3F). Ruines/cartes 'Tanoby', 'Safari', 'Mt Ember' : séparations d'origine (échelles, trous).
- Cartes passées à l'œil (rendu + PNJ/warps) : Grenalux, Route 1, Opanihrum, Route 2, Pyropia, Route 3, Route 4, Route 4 Est, Tourmalia, Routes 5, 9, 10, 20, 21S, 23, Bourg Quartz, Parmanie, Lavanville, Apatia. Les villes sont cohérentes.
- Défauts visuels notés, **non corrigés** : (1) Route 4 : énorme aplat de roche vide (le massif) autour de la petite zone nord ; (2) Route 4 Est : le chemin passe du lilas au sable par blocs carrés au raccord Mont Sélénite/forêt ; (3) Route 5 : deux murs de forêt très larges de chaque côté ; (4) Route 10 : tombes éparses autour du Centre ; (5) Route 23 : toujours le long couloir de bâtiments d'origine (refonte prévue) ; (6) raccord eau Cramois'Île / Route 20 : eau plus sombre côté route (léger) ; (7) Cerulean : warps fantômes aux cases (0,0)-(0,3) inaccessibles (inoffensifs).
- Pas encore revus à l'œil : Hematown, routes 6, 7, 8, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21N, 22, Plateau, Sevii (laissées de côté), intérieurs (grottes, tours, repaire).
- **Revue visuelle complétée (23/10, 11h)** : en plus des cartes citées, passées à l'œil : Hematown (Saffron), Routes 8, 11, 12, 13, 15, 16, 17, 18, 22, Céladopole. Aucun défaut bloquant (raccords, chemins, PNJ). Défauts cosmétiques seulement : transitions neige→violet de la Route 17 par blocs ; transition gris/vert « dithering » en carrés de la Route 4 Est ; vastes aplats de roche (Route 4) et de façades (pourtour d'Hematown). Pas corrigés : demanderaient une refonte de tuiles. Reste à faire : Route 23 + Route Victoire (refonte du tracé), intérieurs (grottes, tours, repaire).
- **Audit 3 (23/10, 11h30)** : outils `audit_placement.py` (objets sur case bloquée/superposés/devant une porte), `audit_stuck.py` (arrivée de warp coincée / warp vers carte inexistante), `audit_pockets.py` (loot ou PNJ inaccessible). Résultat : rien de bloquant sur le chemin principal (cas relevés = comptoirs de Centre, eau pour Surf, warps fantômes vanille). Corrigés : 5 textes avec des noms d'origine (Cerulean → SEA COTTAGE, Cinnabar → CHRONDROLIA au musée de Pyropia, Fuchsia → PARMANIE à l'arène d'Hematown, Saffron → HEMATOWN et SILPH → HEMATEK, Centre d'Hematown).

## Revue des intérieurs (23/10)
Passés en revue à l'œil : Seafoam 1F–B4F (volcan), Route de la Victoire 1F–3F, Repaire (1F–3F), QG Onybris B1F–B4F, Centrale (PowerPlant), Manoir 1F–3F/B1F.
Résultat : aucun faux raccord, aucun passage bloqué, aucun PNJ bloquant. Les avertissements de audit_stuck restants sont des warps dynamiques (ascenseurs, Union Room…) et des îles Sevii (mises de côté).
Reste à refaire (inchangé) : layout Route 23 / Route de la Victoire, QG Bourg Quartz, Chrondrolia, cohérence lave/eau Manoir (capture de Basil requise).

## Centrale de Chrondrolia refaite (23/10)
Les 4 étages (ex-Manoir) sont redessinés par `docs/topaze/centrale_redo.py` (bibliothèque `centrale_lib.py`, originaux dans `centrale_orig/`, contrôle `centrale_check.py`).
- 1F hall des turbines : 4 turbines, transformateurs, banques de consoles, allées en caillebotis jaune (= chemin principal), monte-charge (plot rouge) vers la chaufferie.
- 2F galerie des commandes, 3F salle du cœur (couloir de caillebotis jusqu'au piédestal rouge du TOPAZ), B1F chaufferie (chaudières + racks de tuyaux).
- Motif : plot rouge = point spécial (monte-charge, piédestal). Dialogues vanille du Manoir réécrits (fantômes, puzzle, résidents).
Règle posée par Basil : œil absolu romhacker + UI/UX sur TOUTES les maps (routes, villes, intérieurs, extérieurs). Inventaire noté en cours.

## Route 23 refaite (23/10)
Générateur `docs/topaze/route23_v2.py` (original conservé dans `docs/topaze/route21_src/r23_orig.bin`), tilesets dédiés `GeneralRoute23V2` / `IndigoRoute23V2`. Les 4 portails de badges (Tonnerre, Arc-en-ciel, Âme, Marais) sont séparés par de vraies sections de route : chemin de sable sinueux, forêts, étangs, rochers, murets à escaliers, façades scellées (impossible de contourner l'arche, vérifié par assertion). Gardes + déclencheurs recalés (var_value n-1). Testé en émulateur : 3 badges → bloqué à Arc-en-ciel ; 4 → passe Arc-en-ciel, bloqué à Âme ; 6+ → tout passe.
- Piège trouvé : `include/topaze_fog_strips.h` (raccords de cartes) réécrit des métatuiles/tuiles « inutilisés » de la carte → après un changement de tileset, relancer `python3 docs/topaze/fog_strips.py` (sinon cases noires en damier). Fait.
- **Arènes redessinées (23/10)** : Basil a trouvé que les arènes reprenaient le décor de l'ANCIEN type du champion. Refaites de zéro, une salle par type, en tuiles dessinées en code (`docs/topaze/gym_art.py` + un script par arène, idempotents, `--write`) : Pyropia/Feu (`gym_fire.py`, caldeira + rivières de lave), Apatia/Vol-Dragon-Fée (`gym_sky.py`, terrasse dans le ciel, gouffres + ponts), Parmanie/Poison (`gym_toxic.py`, laboratoire-grotte, bassins toxiques, sentier en S), Opanihrum/Acier (`gym_steel.py`, fonderie à cloisons en zigzag), Bourg Quartz/Glace (`gym_ice.py`, palais de glace, lac gelé). Toutes testées à l'émulateur (chemin jusqu'au champion). Gardées telles quelles (thème déjà cohérent) : Chrondrolia (Électrik), Tourmalia (Plante), Nox (Spectre). Intérieurs de maisons/Centres laissés en l'état (accord Basil).
- **Passe « tout ce qui est faisable sans test » (23/10)** : Route 23 et Route de la Victoire déjà refaites (voir plus haut) ; salles de la Ligue = salles d'arène vanille, cohérentes avec le tournoi, laissées telles quelles ; Routes 4 Est, 5, 9, 17 revues à l'œil, aucun défaut gênant (raccords par plaques, murs de forêt hors champ). **Équilibrage** : Tunnel Roche (dresseurs +6 → ~28-30, sauvages +8) et Tour Spinelle (dresseurs +4 → ~29-31, sauvages +5), via `rebalance21.py`. **Audits** (placement, warps coincés, loot inaccessible, portes) relancés sur toutes les cartes : rien de bloquant (restes = comptoirs, warps dynamiques, îles Sevii vanille, quiz de Chrondrolia).
- **Chrondrolia (Électrik)** : plan à quiz conservé (portes intactes), laboratoire reteinté indigo sombre + murs jaunes (`gym_electric_tint.py`, palettes 7/8/12 du tileset cinnabar_gym). Tourmalia (jardin) et Nox (sombre) vérifiées en jeu : cohérentes.
- **Sevii thématisées par légendaire (23/10)** : `sevii_dress.py` génère maintenant une teinte par île, + météo (`weather` des cartes) + une phrase dans chaque guide de port. Île 1 braise + orage (Raikou, Mt Brasier : cendres volcaniques), île 2 braise + soleil (Entei), île 3 « marée » + pluie (Suicune), île 4 givre + neige (Régice), île 5 acier gris + ombre (Registeel), île 6 pierre rouille + tempête de sable (Regirock), île 7 tropical (légendaires de Hoenn). Sécheresse écartée (cassée en overworld). Après tout changement de tilesets : relancer `fog_strips.py`.
- **Grottes/forêts Sevii** (`sevii_caves.py`, à lancer après `sevii_dress.py`) : Lost Cave (île 5) gris acier, Tunnel Dunsparce + Forêt de Baies (île 3) bleu-vert marée, Dotted Hole / Altering Cave (île 6) rouille, Pattern Bush ocre, Tanoby Key tropical. Icefall (île 4) et Mt Brasier étaient déjà dans le thème. Intérieurs Navel Rock / ruines de Tanoby inchangés.
- **Vol (23/10)** : les points d'arrivée (`src/data/heal_locations.json`) étaient restés aux coordonnées d'origine dans 4 villes redessinées : Parmanie (hors carte !), Tourmalia (case bloquée), Chrondrolia, Route 4. Recalés devant la porte du Centre ; les 16 autres vérifiés. **QoL** : un Pokémon de type Vol propose FLY dans son menu (équipe) sans l'avoir appris, si le joueur a la CS Vol (HM02) dans le sac et le badge correspondant (`SetPartyMonFieldSelectionActions`, src/party_menu.c ; testé en émulateur). Nouvel audit `audit_town_paths.py` (portes isolées dans villes/routes) : rien d'anormal sur le parcours (restes = Safari, Sevii vanille, centrale de Route 10 et Algues Écume fermées, portes fantômes de Tourmalia/Céladopole).
- Reste : cosmétique de transitions (Route 4 Est, 17, 5, 10, abords d'Hematown, couture eau Cinnabar/Route 20), Manoir lave/eau (attend une capture), sprites provisoires ; îles Sevii mises de côté.

## Route Victoire : vraie progression (23/10, demande de Basil)
Avant : on parcourait les 3 étages et on était bloqué pile à la sortie. Maintenant (`docs/topaze/victory_road_progress.py`) :
- **1F** : un éboulis ONYBRIS (barrière de rochers en (4–5, 8–9)) scelle le couloir menant à l'échelle de la 2F tant que `FLAG_VR_BOSS_DONE` n'est pas posé ; en s'approchant, texte « tunnel effondré exprès… courant d'air froid au nord-est ». Le joueur peut seulement revenir en arrière.
- Le **passage visible** : une échelle dans l'alcove nord-est de la 1F (18,1), l'infirmière juste à côté (19,2) → entrée du repaire. Le repaire (3 salles, Kronos, Red) est donc au milieu de la route, plus à la fin.
- Scène d'entrée au repaire (première fois, flag 0x11C `FLAG_TOPAZE_LAIR_ENTERED`) : haut-parleur « laissez-le entrer, le maître veut qu'il voie tout ».
- Le boss battu, les entrées du repaire ramènent à la 1F (échelle (18,1)), l'éboulis a disparu : on continue 2F, 3F puis la sortie, qui n'est plus bloquée (mur de brume et échelle de la 2F supprimés).
- Testé en émulateur : blocage, échelle, scène d'entrée, éboulis levé après `VR_BOSS_DONE`.

## Repaire de Bourg Quartz (23/10)
`docs/topaze/celadon_hideout_redo.py` : histoire Onybris cohérente (plus de « ancien QG Rocket », « Mt Moon »…). Le repaire = **branche n°3 du réseau, la branche de l'argent** (le casino blanchit le butin). Textes de tous les sbires et de Vesper réécrits ; scène d'entrée à la B1F (flag 0x11E) ; **livre de comptes** à la B3F en (8,8) : « BRANCH 3 of 7 », donne 1 PP Max une fois (flag 0x11D) ; l'indice mène vers la clé de l'ascenseur. Disposition des 4 étages (labyrinthe à flèches, ascenseur à clé) inchangée : elle fonctionne et reste lisible. 

### Passe 2 : plans redessinés, « abandonné par Rocket, repris par Onybris »
`docs/topaze/hq_build.py` (+ `hq_lib.py`, `hq_floors.py`, entrées d'origine dans `hideout_orig/`) régénère tout, idempotent.
- **Deux couches visuelles** : l'ancienne base Rocket = palettes poussiéreuses beige/gris (variantes des métatuiles sur des ids inutilisés du tileset + palettes 8/9/11, aucune constante `METATILE_SilphCo_*` déplacée) ; les zones reprises par Onybris = bleu glacé d'origine. Seul le chemin accueil → couloir → sécurité/ascenseur est « refait » : on voit la reprise avancer pièce par pièce.
- **B1F neuve** (28x30) : accueil bleu (escalier du casino en (12,2)), couloir, dortoir Rocket (deux escaliers vers la B2F, gardé par une barrière que lève le sbire en (7,13)), réserve, bureau de sécurité bleu avec l'ascenseur. **B4F neuve** (24x26) : remise à clé, grand hall rouille, barrière + deux gardes (à interpeller) menant au bureau bleu de Vesper, sas bleu de l'ascenseur. **B2F/B3F** : labyrinthes à flèches conservés, rouille ; ailes reprises en bleu (le livre de comptes passe dans le bureau bleu de la B3F, en (15,7)).
- **Lore Rocket rétabli** dans les textes (emblème rouge sous la peinture, « Rocket est parti, Onybris s'est installé, une salle bleue à la fois », labyrinthe/pièges laissés par Rocket, clé de l'ascenseur de Rocket perdue) ; Game Corner : façade de l'ancien gang, tampon Rocket derrière l'affiche.
- Testé en émulateur : tous les escaliers (B1F↔B2F×2, B2F↔B3F, B3F↔B4F, casino), barrière B1F, clé, deux gardes B4F → barrière levée → bureau de Vesper, ascenseur.

## Diversité dresseurs / sauvages (23/10)
- `diversify_trainers.py` : équipes à attaques par défaut re-thématisées (Rocket, Scientifiques, Channelers, Randonneurs…), max 2 d'une espèce par carte, ~12 au total ; Arène Céladopole (Glace), Jadielle (Acier), Dojo (Combat), Tunnel Roche, Tour Pokémon. 257 remplacements. Plus aucune carte « 50 Arbok ».
- `wild_diversify.py` : 89 créneaux sauvages variés (Mt Lune B1F, Tour Pokémon, Mt Brasier, Port Trois-Îles, Routes 6/7/8/10/11/16/22/23/25, tables d'eau). Aucune espèce perdue du Pokédex.
- Hepha : équipe d'origine conservée sur demande de Basil (Magneton, Arbok, Machamp, Golem, Tortank 55-60) ; l'équipe Acier 52-58 reste dans gym_opanihrum_trainers.py si besoin.

## Niveaux Sevii + Centre One Island (23/10)
- `sevii_levels.py` : planchers de niveau des dresseurs par île (One 58, Mt Brasier 60, Two 60, Three 61, Four 62, Five 64, Six 65, Seven 66), 91 équipes ; Anciens/Echo inchangés (69–72).
- `sevii_wild_levels.py` : sauvages = plancher − 5 (min plancher − 18), évolutions suivies ; Ledyba/Magby/Wooper non évolués pour rester obtenables.
- Centre One Island : scientifique (Move Coach) à côté de l'infirmière (6,2), comme dans tous les Centres ; Bill dehors caché hors scène d'arrivée.

## Écho 1 : parcours vers Raikou (23/10)
`echo1_sparks.py` : après Bill, 3 étincelles (sprite Voltorb) sur la route Kindle (11,61), (11,81), (11,101) ; chacune dit un texte et disparaît ; la 3e déclenche tonnerre et fait apparaître Raikou (12,120). Raikou n'est plus visible avant. Flags 0x130–0x135. À généraliser aux Échos 2–7 si Basil valide. Sprite de Raikou refait (recoloration d'Entei, provisoire).
