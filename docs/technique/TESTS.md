# Tests, limites et TODO

> Rien de ce qui suit n'a encore été joué : aucun émulateur n'était disponible lors du développement. La ROM **compile**, c'est tout ce qui est vérifié.

## Check-list de premier test (mGBA, nouvelle sauvegarde)
**Démarrage**
- [ ] Nom de ville « GRENALUX » (panneau, carte) ; rival par défaut « ZEPHYR ».
- [ ] Dialogues de Maman (chaussons) et du professeur (herbes, « Come with me to my LAB, kid. »).
**Types**
- [ ] Page de résumé : les types affichés correspondent au Pokédex du site ; l'icône « FAIRY » est lisible (menus, CT).
- [ ] Combat : Fée → Dragon = ×2 ; Dragon → Fée = 0 ; Acier → Fée = ×2.
- [ ] Puissance cachée ne donne jamais Fée.
**Règles**
- [ ] CT : enseigner une CT ne la consomme pas. CS : on peut oublier Coupe/Surf/etc. depuis le menu.
- [ ] Coupe inflige des dégâts de type Plante ; l'arbre se coupe toujours.
**Champions** (équipes sur la page Gym Champions)
- [ ] Les 8 combats démarrent, 4–5 Pokémon, attaques correctes, difficulté adaptée.
**Textes**
- [ ] « TEAM ONYBRIS » partout ; pas de débordement de boîte (Game Corner, Tour Pokémon, Silph Co.).
**CS sans apprentissage et confort (jalon 4)**
- [ ] Face à un arbre / rocher cassable / bloc de force, avec un Pokémon qui ne connaît pas la CS : la proposition apparaît (si l'insigne est obtenu) et l'animation passe sans plantage.
- [ ] Surf depuis la berge sans Pokémon « Surf » ; Cascade en remontant une chute.
- [ ] Si le Pokémon de tête est un **œuf** : le message affiche « EGG » (à corriger si gênant).
- [ ] Les combats donnent de l'XP à toute l'équipe ; l'XP totale par combat reste raisonnable.
- [ ] Courir dans un bâtiment, une grotte ; texte rapide par défaut sur nouvelle sauvegarde.
**Split physique/spécial et objets (jalon 5)**
- [ ] Gengar / Alakazam : Shadow Ball inflige des dégâts spéciaux (utilise Atq. Spé) ; Bite et Fire Punch utilisent l'Attaque.
- [ ] Counter ne répond qu'aux coups physiques, Mirror Coat aux coups spéciaux.
- [ ] Hidden Power : catégorie suit toujours son type.
- [ ] Les champions tiennent leurs objets (la Baie Sitrus soigne, les Restes soignent chaque tour).
**Stabilité**
- [ ] Sauvegarder / recharger ; évoluer ; apprentissage d'attaques sans plantage (limite de 20 par Pokémon).

## Tests réels (banc mGBA sans écran)
- [x] Intro, noms, dialogues Maman/Chen, choix du starter (Salamèche Feu/Glace), premier combat rival gagnable, efficacité des types (Mud-Slap super efficace).
- [x] **CS sans les apprendre** : avec les badges, le prompt « Would you like to SURF? » apparaît sans Surf dans l'équipe, et le joueur navigue (Route 21 atteinte).
- [x] Course (B) disponible dès le début et en intérieur (bug trouvé : les chaussures n'étaient données qu'à Argenta, corrigé dans `new_game.c`).
- [x] Combat sauvage (Roucool niv. 5, Griffe, gain d'EXP, montée de niveau), vitesse de texte par défaut = FAST, style de combat SHIFT, sauvegarde en jeu.
- [x] Coupe/Roche/Force/Flash : même mécanisme que Surf (script `setvar VAR_RESULT, 0`), vérifié par lecture, non rejoué en jeu.
- [x] Multi Exp global : un Clefairy niv. 3 resté dans l'équipe a gagné un niveau après un combat sauvage gagné par le Pokémon de tête (équipe de test fabriquée avec `tools/topaze/emu/mkmon.py`).
- [x] Type Fée : Clefairy (FEE/SPECTRE) s'affiche avec la pastille rose « FAIRY » dans le résumé ; carte « Met in GRENALUX » correcte.
- [x] Textes ONYBRIS : aucune ligne ne dépasse 36 caractères (max des textes d'origine : 40), pas de débordement attendu.
- [x] Split physique/spécial : `MOVE_IS_PHYSICAL` est utilisé partout (dégâts, Hustle, suivi des dégâts) ; pas de test chiffré en jeu.
- [x] Brûlure 1/16 des PV vérifiée en combat (160 PV max : −10 par tour). Paralysie ½ vitesse : changement de code simple, non mesuré.
- [x] **Répétiteur d'attaques** dans tous les Centres Pokémon (infirmière, gratuit) : testé avec une ROM de debug (départ au Centre d’Opanihrum, Salamèche niv. 20) : question, choix du Pokémon, liste des attaques réapprenables. Astuce de test : voir `tools/topaze/emu/README.md` (ROM de debug, `TOPAZE_ROM`).
- [x] Objets tenus des champions : combat contre le champion de Pyropia (KAY) : 1er Pokémon Goupix avec **Charbon** (lu en mémoire de combat).
- [x] Coupe en jeu (Vermilion, badge 2, sans l'apprendre) : invite « Would you like to CUT it? », l'arbre disparaît.
- [x] Split par attaque mesuré : avec Attaque 300 / Atq. Spé. 5, **Coup-Glace** (Glace, forcée physique) met le Goupix KO d'un coup, alors que **Lance-Flammes** (spéciale) ne lui retire rien.
- [ ] Seul reste non mesuré : la vitesse paralysée (changement d'une ligne, relu dans le code).

- [x] **CS dans le sac obligatoire** : sans CS01, l'arbre affiche seulement « This tree looks like it can be CUT down! » ; avec CS01 + badge, « CHARMANDER used CUT! ». Même contrôle pour Surf (CS03), Force (CS04), Éclate-Roc (CS06), Cascade (CS07).

- [x] **Grenalux v3 (décors d'Émeraude)** : sortie de la maison du joueur sur la nouvelle carte vérifiée à l'émulateur (rendu correct, porte/warp OK). Cinématique du rival (trajet nord → ranch → scène d'ouverture) vérifiée à l'émulateur (`tools/topaze/emu/t_intro.py`). À confirmer sur ton ordinateur : retour d'Oak au labo (après les 8 badges), collisions (ruisseau, puits, parterres), panneaux.
- [x] **Grunt ONYBRIS à Grenalux** : après le combat du rival, un grunt arrête le joueur sur la route (maintenant x=12, y=4), dialogue Jirachi/aura, combat Rattata+Zubat niv. 4 gagnable avec le starter, puis il disparaît.

- [x] **Musée de Grenalux** : la porte de la façade mène à l'intérieur (carte neuve), le conservateur parle (GRENAT / aura), la sortie ramène devant la porte.

- [x] **Ouverture selon le document de conception** : sans Pokémon, Zéphyr arrête le joueur à la sortie nord, l'emmène jusqu'au ranch (maison en haut à droite) ; scène **dans l'intérieur du ranch** (père de Zéphyr, Prof. Chêne et Zéphyr présents ; vol des Pokémon pisteurs par Onybris), puis arrivée au labo et choix du starter. Variable `VAR_GRENALUX_OPENING` (1 = scène à jouer, 2 = faite), drapeau `FLAG_HIDE_RANCH_SCENE`.

- [x] **Trois frappes d'Onybris (version « après coup »)** : ranch (raconté par le père de Zéphyr), musée (vitrine vide, conservateur et vieil homme changent de dialogue) et labo (assistants et ordinateur : fichiers sur les gemmes copiés), tous déclenchés par `FLAG_GRENALUX_ONYBRIS_STRIKE` posé quand le grunt de la route est battu. Testé : dialogues du musée. Reste à tester en jeu : dialogues du labo (même mécanisme).

- [x] **Trois fins** : choix de Jirachi dans la Salle d'Honneur (menu à 3 choix, `VAR_TOPAZE_ENDING`, `FLAG_TOPAZE_POSTGAME` pour la fin 1). Testé : fin 1 (menu, texte, enregistrement au Panthéon, sauvegarde). Fins 2 et 3 : même mécanisme, textes non vus en jeu ; la fin 2 ne retire pas encore réellement les Pokémon.

- [x] **Postgame (après la fin 1)** : l'inconnu de la route 22 (Giovanni jamais nommé, `TRAINER_PLAYER_LEAF`, 6 Pokémon niv. 66-72), puis RED dans la grotte de Tourmalia (`TRAINER_PLAYER_RED`, niv. 76-82, texte muet), puis épilogue avec Silver. Testé : dialogues et début du combat contre l'inconnu. Non testé : RED et l'épilogue (même mécanisme).

- [x] **Ligue = tournoi de 11 combats** (remplace le placeholder + Conseil des 4) : 9 matchs dans la 1re salle (poule SEKO, MAY, BRENDAN, GOLD, CRYSTAL double ; 16e LEAF ; quart ZÉPHYR ; demi BLUE double ; finale N), puis salle du Champion : **OAK** (champion en titre) et le **boss d'Onybris** qui s'incruste pour le vœu de Jirachi (double, placeholder), puis Panthéon/Jirachi. **Boss en 2 combats** (équipe, puis Artikodin/Électhor/Sulfura/Mewtwo, `TRAINER_LEAGUE_BOSS_2`) ; reprise possible entre les deux. **Brice/Flora/Misty** au Centre du Plateau Indigo (testé : dialogues). `VAR_TOURNAMENT_ROUND` 0-8, soin entre les matchs, porte ouverte à la fin (`FLAG_DEFEATED_LORELEI`). Salles Bruno/Agatha/Lance retirées du trajet. Générateurs : `docs/topaze/league_build.py`, `league_arena.py`, `league_champ.py`. **Testé de bout en bout en émulateur** (`bench/league_pool_test.py`, `league_finale_test.py`) : 9 matchs → porte → OAK → boss → Jirachi → Panthéon → crédits. Sprites provisoires (SEKO scientifique, GOLD/CRYSTAL/N dresseurs génériques, Zéphyr = Blue = même sprite) ; équipes et textes = placeholders anglais.

- [x] **Grenalux v6** (44×36, `grenalux_town.py`) : ROM compilée, sortie de la maison → avenue → déclencheur du rival → ranch vérifiés à l'émulateur (`t_big.py`), rendu en jeu (lampadaires, cristaux) correct. À confirmer : routes 1/21, collisions de la carrière et de la mine, dialogues des 6 PNJ d'ambiance, scène d'Oak après la Ligue.

- [x] **Grand ranch** (`t_ranch.py`) : de la grande rue, passage par l'ouverture est puis traversée vers la carte du ranch sans écran de chargement (carte 4/5), rendu correct (enclos, animaux, écurie). À confirmer : dialogues, clôture coupée, impossibilité de passer les clôtures.

- [x] **Grand ranch avant/après attaque** (`t_ranch2.py`, flag posé en mémoire) : clôture ouverte, pisteurs disparus, ouvrier présent à la brèche ; avant : clôture intacte et animaux présents. Dialogues non lus en jeu.

- [x] **Grenalux – validation complète (v6)** (banc `tools/topaze/emu/townlib.py`, `opening.py`, `t_town*.py` : trajets avec relecture de position) :
  - 6 panneaux + panneau du ranch, sage-femme/panneau « Trainer Tips » (dame de la sortie nord), 8 PNJ d'ambiance (vieil homme, mineur, scientifique, dame, jardinière, ouvriers du ranch…), décors interactifs (monument, cristaux gardiens, mine, grange du ranch) : textes lus, aucun débordement de boîte (limite 36 caractères vérifiée par script) ; 3 textes trop longs corrigés (vieil homme, garçon, jardinière).
  - 4 portes aller-retour (maison, ranch/Daisy, labo, musée) ; arrivée de Maman après KO (respawn (8,10) → maison), combat du grunt (déclenchement de la vue + combat), scène d'Oak après la Ligue (déclenchement et trajet).
  - Ouverture complète rejouée de bout en bout : sortie de la maison → déclencheur du rival → ranch → labo → choix du starter → combat du rival → avenue.
  - Avant/après l'attaque : musée (conservateur), labo (assistants), ranch (clôture, pisteurs, ouvrier).
  - **Bug trouvé et corrigé** : les connexions Grenalux ↔ Route 1 / Route 21 étaient décalées (décalage non opposé côté route) **et** affichaient des tuiles brouillées (tilesets différents : Émeraude vs FR). Remplacées par des **warps** (nord : (22..23,0) ↔ Route 1 (12..13,39) ; sud/eau : (21..23,35) ↔ Route 21 N (7..9,0)) avec un test dans `src/field_control_avatar.c` (`IsTopazeStepWarpMap`) pour qu'un warp s'active en marchant sur une case ordinaire. Nord vérifié aller-retour ; **sud (surf) non testé** (pas de CS dans le banc).
  - Non testés en jeu : textes des animaux du ranch et des enfants (PNJ errants, même script), combat du grunt jusqu'à la victoire (fin de la séquence « strike » vue seulement via le drapeau), Oak jusqu'à l'entrée du labo.

### Opanihrum v1 (validation en émulateur, ROM de test avec warps Grenalux -> Opanihrum)
  - Banc : `tools/topaze/emu/t_opan0.py` (Grenalux -> Opanihrum, drapeaux de l'ouverture levés par écriture mémoire), `t_opan1..4.py` ; `TOPAZE_COL=/tmp/opanihrum_col.json` fait lire au planificateur la grille d'Opanihrum.
  - OK : Centre, Boutique (scène du colis d'Oak incluse), École, Maison (entrée/sortie) ; arène verrouillée (message + saut en arrière sur les deux cases) puis déverrouillée (les deux portes mènent à l'intérieur) ; vieil homme à la porte nord (barrage puis tutoriel) ; sorties nord/ouest/sud vers Route 2/22/1 et retours (tuiles propres, plus de brouillage) ; dialogues de 3 PNJ.
  - Non testés : PNJ errant « boy » (déplacements), arrivée en venant de la Route 1 sans ROM de test (même warps, vérifiés par les indices), combats d'arène (inchangés).

### Route 1 du dégradé (émulateur)
  - Banc : `tools/topaze/emu/t_route1a.py` (Grenalux -> Route 1) et `t_route1b.py` (`TOPAZE_COL=/tmp/route1_col.json`) : trajet complet suivant le chemin du sud au nord (herbes hautes évitées), entrée dans Opanihrum, retour par le warp. OK dans les deux sens ; le bord de carte est violet (neutre). v3 : la case d'arrivée (12,53) est une case-warp, le banc la quitte (UP) avant de planifier et la bloque ensuite, sinon le planificateur repasse dessus et retourne à Grenalux. Non testés : rencontres en herbe haute, dialogues du garçon et de la vendeuse.
  - Non testé : rencontres sauvages dans les herbes hautes, dialogue du garçon et du vendeur (textes seulement modifiés).

## À REPRENDRE : noms et équipes (placeholders)
Tout ce qui a été inventé par Claude est **provisoire** et sera repassé avec Basil : noms, équipes, niveaux, dialogues et sprites des personnages du tournoi de la Ligue (Jasper, Coralie, Boris, Alma, Ruben), de l'inconnu de la route 22 et de Red (équipe/niveaux), des dresseurs de la Ligue, des textes d'arène et des lignes de PNJ réécrites, des CT données par les champions, des noms de badges et des trois textes de fin.
**Ne sont pas des placeholders** (viennent des notes de Basil) : les 12 villes, les 8 champions (Kay, Sylvestre, Hera, Grim, Achlys, Nox, Eddie, Hepha) et leurs types, l'intrigue Onybris/Jirachi, les trois fins (principe), le postgame Giovanni puis Red avec cinématique Silver, le format de la Ligue.

## Limites connues
- Sprites des champions = ceux des chefs d'arène d'origine.
- Hepha utilise le slot de Giovanni (arène d’Opanihrum).
- Villes renommées (script `docs/topaze/rename_towns.py`) mais géographie de Kanto conservée : Grenalux=Bourg Palette, Opanihrum=Jadielle, Pyropia=Argenta, Tourmalia=Azuria, Apatia=Carmin, Bourg Quartz=Céladopole, Amethiolite=Parmanie, Hematown=Safrania, Chrondrolia=Cramois’Île, Spinellia=Lavanville. Reste : cartes originales (ambiance de chaque ville) et noms de lieux composés (Forêt, Grotte, Grand Magasin) liés au code de la carte région.
- Ossatueur : branche d'évolution Sol/Spectre reportée (nécessite une nouvelle espèce et un sprite).

## Pokémon suiveur (follower) — étude, non implémenté
Faisable techniquement (le moteur pokeemerald-expansion a un système de followers), mais pas ici et pas maintenant :
1. **Code** : porter un système de follower dans pokefirered (gestion d'un object event supplémentaire, collisions, passage de portes, surf/vélo, scripts de cinématique). Risque élevé de blocages (un banc de test mGBA existe maintenant : `tools/topaze/emu/`).
2. **Graphismes** : il faut un **sprite overworld par espèce** (151 minimum, 16×32 avec 9 images) ; pokefirered n'en fournit pas. À créer ou à récupérer (licences !).
Piste réaliste : faire d'abord le jeu jouable, puis ajouter un follower **limité aux espèces qui ont un sprite** (starters + Pikachu), les autres restant dans la balle.

## TODO
- Suite des scripts de Grenalux (le blocage sans Pokémon est celui d'origine ; reste le reste de l'ouverture : attaque d'Onybris sur le labo, etc.).
- Cartes et villes originales (12 villes, 8 arènes), Ligue en tournoi, trois fins, post-game (Giovanni puis Red).
- Équilibrage après premiers tests ; équipes thématiques des dresseurs de route.
- Vérifier s'il existe une « expansion » FireRed maintenue à adopter.

### Pyropia v2 (émulateur)
  - ROM de test jetable : sortie nord de Grenalux redirigée vers le sud de Pyropia (patch temporaire de `PalletTown/map.json`, restauré ensuite). Banc : `tools/topaze/emu/t_pyro_a.py` (arrivée), `t_pyro_b.py` (portes), `t_pyro_c.py` (PNJ, panneaux, sorties) avec `TOPAZE_COL=/tmp/pyropia_col.json`.
  - OK : Arène, Centre, Boutique, Musée (2 ailes), 2 maisons : entrée et sortie ; 3 PNJ parlent ; 5 panneaux lisibles ; sortie est ↔ Route 3 et sud ↔ Route 2 dans les deux sens. v3c : 4 maisons + musée (2 portes) entrent/sortent bien, 9 PNJ parlent. Piège de banc : `TOPAZE_COL` ne doit pas être défini pour `opening.py`/`t_pyro_a.py` (sinon l'émulateur ne démarre pas), et `TOPAZE_ROM`/`TOPAZE_COL` ne persistent pas d'un appel shell à l'autre. v3 : le planificateur monte et descend par les escaliers (murs infranchissables), tous les tests ci-dessus repassent.
  - Corrigé : les maisons décoratives avaient une porte sans warp (maintenant fenêtre).
  - Non testés : gagner l'arène de Kay (inchangée), objet caché, ambiance des Routes 2 et 3 (encore d'origine).

### Route 2 v1 (émulateur)
  - ROM jetables : Grenalux nord redirigé vers le sud (warps 2,3) puis vers le nord (warps 4,5) de la Route 2. Bancs : `t_route2a.py`/`t_route2b.py` (sud), `t_route2c.py`/`t_route2d.py` (nord).
  - OK : chemin sud jusqu'au portail et entrée dans l'entrée sud de la forêt ; chemin nord depuis Pyropia jusqu'au portail et entrée dans l'entrée nord ; falaise étanche (assertion de non-communication dans le script).
  - Non testés : PNJ (randonneur, mineur), panneaux, objets (Elixir, Antiparalysie), herbes hautes, traversée de la forêt (inchangée, verte), sorties vers Opanihrum/Pyropia dans les deux sens.

  - v2 : entrée sud de la forêt testée avec la forêt calcinée (transition d'intro « CINDER FOREST » vue ; image encore verte avant recoloration, corrigée ensuite, non revérifiée à l'écran). Banc `t_route2e.py`.

### Forêt calcinée v2 (émulateur)
  - ROM jetable : Grenalux nord redirigé vers la porte sud de la forêt. Bancs `t_forest_a.py`/`t_forest_b.py`. OK : arrivée à la porte sud, marche sur le sentier, cendres qui tombent, PNJ visible. Non testés : traversée complète (les dresseurs bloquent la marche), sortie nord, combats, objets, panneaux.
- [x] **Mine de Grenalux (post-game, fin 1)** : 3 étages (copies des layouts de Mt Moon, groupe `gMapGroup_IndoorPallet` : un groupe ne doit pas dépasser 127 cartes), entrée en (39,24) de Grenalux (porte à coord event : scellée avant `FLAG_TOPAZE_POSTGAME`). 3F : scène de la vérité sur l'Aura (placeholder, à valider), Mew apparaît puis fuit (`FLAG_MEW_FLED`). **Apatia** : le chauffeur et Mew « sous le camion » apparaissent à (16..17,19) une fois Mew parti ; Mew capturable (niv. 50, `FLAG_FOUGHT_MEW_TRUCK`). Testé en émulateur : porte scellée/ouverte, trajet 1F→2F→3F, scène complète, apparition + combat de Mew à Apatia, Mew absent avant la fuite. Pas de sprite de camion (placeholder), pas de faune sauvage dans la mine.

## Conseil des Anciens (post-game)
- `bench/elders_test.py` : 20 combats enchaînés dans la 1re salle de la Ligue (FLAG_TOPAZE_POSTGAME, VAR_ELDERS_ROUND 0→20), récompense (Master Ball placeholder) au 20e. OK en émulateur.

## Écho 1 (post-game, île 1)
- `bench/echo1_bill_test.py` (Bill : compas, VAR_ECHO_STAGE 0→1), `echo1_raikou_test.py` (Raikou niv. 45 sur la Kindle Road (12,120), stage 1→2), `echo1_celio_test.py` (Celio donne Germignon, stage 2→3). OK en émulateur. Note : le banc ne peut pas démarrer à y>127 (octet signé) ; le test de la scène vanilla 'MeetCelio' est contourné en posant VAR_MAP_SCENE=7.

## Écho 2 (post-game, île 2)
- `bench/echo2_bill_test.py <étape>` (3→4 annonce, 5→6 cadeau Héricendre/Cyndaquil) et `echo2_entei_test.py` (Entei niv. 48 au Cap Brink (12,29), 4→5). OK en émulateur.

## Écho 3 (post-game, île 3)
- `bench/echo3_celio_test.py <étape>` (6→7 annonce, 8→9 cadeau Kaiminus/Totodile) et `echo3_suicune_test.py` (Suicune niv. 50 au Bond Bridge (30,10), 7→8). OK en émulateur.

## Écho 4 (post-game, île 4)
- `bench/echo4_lorelei_test.py <étape>` (9→10 annonce, 11→12 cadeau Arcko/Treecko) et `echo4_regice_test.py` (Regice niv. 52 dans Icefall Cave Back (12,15), 10→11 ; sprite provisoire = rocher). OK en émulateur. Les Rockets/Lorelei de la scène vanilla sont cachés en post-game.

## Échos 5 et 6 (post-game, îles 5 et 6)
- `bench/echo56_giver_test.py <étape> <bill|celio>` (12→13, 14→15 Bill ; 15→16, 17→18 Celio) et `echo56_beast_test.py <map> <x> <y> <étape> <hold> <5|6>` : Registeel niv. 54 au Meadow (6,32), Regirock niv. 56 à Ruin Valley (14,23) (sprites provisoires = rocher). OK en émulateur.

## Écho 7 (finale, île 7)
- `bench/echo7_sevault_test.py <étape> <up> <left> <ESPÈCE>` : Celebi (stage 19→20) et Latias (stage 21) au sommet de Sevault Canyon ; Bill 18→19 et 20→21 via `echo56_giver_test.py`. OK en émulateur ; sprites provisoires = rocher sauf Celebi.

## Chaîne des Échos (statique)
- `docs/topaze/audit_echos.py` : vérifie que chaque étape de `VAR_ECHO_STAGE` (1-21) est posée puis lue par un script. Résultat : CHAINE OK (Bill/Celio/Lorelei alternent 0→21 sans trou). Le parcours complet en un seul run émulateur n'est pas faisable (surf entre îles) : chaque étape est testée isolément (`bench/echo*_test.py`).

## Scène de l'île 7 : Silver / Giovanni / Red
- `bench/echo8_scene_test.py` : déclencheur (17,8) au stage 21, dialogues, combat SILVER (nouveau, 6 Pokémon 68-72) puis GIOVANNI (`TRAINER_PLAYER_LEAF`), départ, Red salue seul, stage 22. OK en émulateur (le test passe les combats en mode dieu). Les légendaires de Sevault n'apparaissent maintenant qu'au stage 22 (`echo7_sevault_test.py` : utiliser l'étape 22 pour Kyogre etc.).

## Grenalux — scène d'ouverture au ranch (test téléphone)
- Émulateur : escorte du rival (sortie nord) → ranch → père/OAK/rival → 2 sbires → choix du starter → combat sbire 1 → maman + pendentif → `VAR_GRENALUX_OPENING`=2, joueur libre en (11,6). OK.
- Entrée en marchant seul vers l'est (OPENING=0) : même scène. OK.
- Raccord de sol ranch↔Grenalux vérifié visuellement (chemin continu).
