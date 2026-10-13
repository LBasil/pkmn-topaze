# Pokémon Topaze — parcours du joueur : audit de mi-parcours (13/10/2026)
*3 badges, 5 événements de pierre. Dernière vérification : barrages par BFS, courbe de niveaux, mots d'origine résiduels, texte par zone.*

## 1. Le pitch (rappel)
Il y a 10 ans une Aura a muté les types. Aujourd'hui la TEAM ONYBRIS vole une pierre par ville et veut « libérer » les Pokémon des humains. Le joueur (et son PENDENTIF, qui est le vrai GRENAT) suit leurs traces ; Onybris a presque toujours une longueur d'avance, mais monte en puissance : sbires → cadre (VESPER) → admin (KRONOS) → le boss, jamais vu.

## 2. Les 5 événements de pierre
| # | Ville | Pierre | Ce qui se passe | Rôle du joueur |
|---|---|---|---|---|
| 1 | Grenalux | GRENAT | attaque EN DIRECT (ranch, école, labo) | combat un sbire, reçoit le PENDENTIF |
| 2 | Pyropia | PYROPE | volé avant l'arrivée (musée) ; BROCK conservateur | enquête |
| 3 | Tourmalia | TOURMALINE | volée avant l'arrivée ; ville bouclée par la police | badge 2, le rival remplace la police |
| 4 | Apatia | APATITE | **sauvée** : prêtée au capitaine du S.S. ANNE, le joueur arrive à temps (VESPER battue/fuit) | première victoire sur Onybris |
| 5 | Spinellia | SPINELLE | tentative RATÉE (les morts se lèvent, Ossatueur au 6F), puis l'admin KRONOS arrive après que le joueur a apaisé l'esprit, écrase le joueur SANS combat et part avec | échec scénarisé |
Cohérence : les 2 échecs d'Onybris (Apatia + tentative de Spinellia) justifient la phrase de FUJI « ils sont devenus plus agressifs » et l'arrivée de l'admin.

## 3. Parcours dans l'ordre (état du monde, verrous, personnages, niveaux)
| Étape | Verrou / barrage | Personnages | Dresseurs (niv. max) | Sauvages | Statut |
|---|---|---|---|---|---|
| Grenalux (ex-Bourg Palette) | sortie nord bloquée jusqu'au labo | rival, Chêne, maman, prof | — | — | validé, testé émulateur |
| Route 1 | — | 3 animaux (quête) | 0 | 3–7 | validé |
| Opanihrum | arène (Hepha) verrouillée jusqu'aux badges 1–7 | — | — | — | validé |
| Route 2 / Forêt Calcinée | — | — | 5 (8) | 4–8 | validé |
| Route 3 | — | — | 8 (16) | 7–9 | validé |
| Pyropia | — | KAY (arène), BROCK (musée) | arène (Feu, 15–20) | — | validé |
| Route 4 / 4 Est | — | — | 1 (14) / 5 (16) | 8–16 | validé |
| Tourmalia | nord fermé (police) jusqu'au badge 2, puis rival ; sud + est fermés jusqu'au S.S. TICKET ; arbre à couper à l'est | SYLVESTRE (arène Insecte/Plante 19–23), rival | — | — | validé |
| Route 24 | impasse (pont) | sbire à la PÉPITE | 6 (22) | 17–21 | validé |
| Route 25 + chaumière | — | MISTY (équipe scénarisée), 2 sbires, ticket | 9 (24) | 18–22 | validé, testé émulateur |
| Route 5 / chemin souterrain / Route 6 | passage | — | 0 / 6 (25) | 20–26 | validé |
| Apatia | arène FERMÉE et sortie est bloquée (5 policiers) jusqu'à la CS COUPE ; port = ticket | HERA (Dragon/Vol 25–31), MAJOR BOB | — | — | validé |
| S.S. ANNE | — | rival TERRY (24–26), VESPER (cadre), capitaine (CUT), HERA + MAJOR BOB (2F) | marins d'origine (non revus) | — | validé |
| Route 11 | joignable seulement après COUPE ; Ronflex sur la Route 12 | indices Onybris | 10 (28) | 22–27 | à valider ; grotte des Taupiqueurs mise de côté |
| Route 9 / 10 | arbre à couper à l'est de Tourmalia | indices Onybris | 9 (29) / 6 (29) | 25–30 | validé ; Tunnel Roche + centrale : intérieurs plus tard |
| Spinellia | ouest + sud fermés (police) jusqu'à la scène de FUJI/KRONOS ; retour nord libre | FUJI, KRONOS | Tour : canaux d'origine | — | à valider |

Courbe de niveaux : R3 10–16 → Kay 15–20 → R4/4E 13–16 → Sylvestre 19–23 → R24/25 19–24 → R5/6 20–26 → Hera 25–31 → R9/10/11 25–30. Cohérente.

## 4. Vérifications faites
- **Barrages (BFS sur la collision + objets)** : Apatia est, Spinellia ouest et sud, Tourmalia sud/est/ouest. Deux fuites trouvées et CORRIGÉES : Apatia est (cases (47,17) et (47,21) contournaient les 3 policiers → 5 policiers) et Spinellia sud (cases (18,28) et (21,28) → 4 policiers). Tourmalia nord est fermé par déclencheurs de coordonnées (pas par collision).
- **Mots d'origine résiduels** (ROCKET, Bourg Palette, Jadielle, Argenta, Azuria, Carmin, Lavanville, SILPH) : tous nettoyés sur le parcours ; le SILPH SCOPE n'est plus requis (fantôme du 6F et sauvages de la Tour toujours visibles) et ses mentions sont retirées.
- **Classe d'entraîneur** TEAM_ROCKET s'affiche « TEAM ONYBRIS » ; le nom du rival est remplacé par celui choisi par le joueur.

## 5. Points ouverts (par priorité)
1. ~~Routes 7/8/12~~ FAIT : R8 sauvages 24–29, R7 25–30, R12 25–31, deux dresseurs bas remontés.
2. ~~Eau et pêche~~ FAIT : plages remises à l'échelle de chaque zone (espèces à revoir au cas par cas).
3. **Matchs retour** des routes 9/10/11 et des anciennes routes non remontés ; dresseurs des arènes (Apatia, Tourmalia) non revus.
4. **Intérieurs différés** : Tour Spinelle (canaux au niveau d'origine ≈ 20 vs routes 28), Tunnel Roche, centrale ; grotte des Taupiqueurs (au choix de Basil).
5. **Personnages importants** pas encore placés : Giovanni, Red, Gold, Silver, Brice (randonneur ordinaire pour l'instant), Flora, N ; MISTY ne revient pas après la Route 25 ; Bill (disparu) à traiter plus tard.
6. **Sprites provisoires** : MAJOR BOB (ceinture noire), KRONOS/VESPER (sprites de sbire), HERA (ancien sprite de Surge), doublons Brock/Kay/Misty/Sylvestre.
7. **Tests émulateur** : seuls Grenalux, la chaumière de la Route 25 et la scène du 7F de la Tour ont été joués ; le reste est compilé, non joué.
8. Fin de projet : vérifier que **tous les Pokémon sont obtenables**.

## 6. Suite décidée (13/10, après l'audit)
- De Spinellia on prend la Route 8, puis le CHEMIN SOUTERRAIN (entrée est de la Route 8 → Route 7) jusqu'à BOURG QUARTZ (Céladon). Hematown reste hors chemin : le garde de la porte ouest de la Route 8 est assoiffé (thé de la vieille dame du manoir de Bourg Quartz, mécanique d'origine), la ville est « fermée par le conseil à cause des voleurs ».
- Indices posés sur la Route 8 : les hommes en noir sont passés par le chemin souterrain vers la ville froide (Bourg Quartz).
- Bourg Quartz : le repaire sous le GAME CORNER est l'ANCIEN REPAIRE ROCKET repris par Onybris (histoire racontée par les PNJ). Boss du repaire = VESPER (B4F). La sortie ouest (Route 16) est bloquée par la police tant que Vesper n'est pas battue.
- Après Vesper : duel HAUT/BAS au casino (meilleur des 3, une seule chance) pour la pierre QUARTZ : gagné = le joueur l'a, perdu = Onybris l'a (FLAG_QUARTZ_STONE_WON). Twist à prévoir selon la branche.
- Restant : arène de GRIM (Glace, badge 4), pierre = QUARTZ, cameo Giovanni plus tard.

## Hematown — QG n°3 sur 5 (avant-avant-dernier)
Ville occupée par ONYBRIS, tour HEMATEK = quartier général. BRICE, FLORA et N (premiers "forts" du jeu) montent affronter le MASTER, un étage chacun (3F, 6F, 9F), le joueur reste un étage derrière. Le joueur bat KRONOS au 11F ; derrière la porte, le boss écrase les trois alliés avec un seul Pokémon et part avec l'HEMATITE (volée sous nos yeux, pas de cadeau de Nox). Le boss reste invisible (ombre noire), il a regardé le joueur. Plus tard : volcan Écume = QG n°4 (Gold + Silver), dernier QG avant la Ligue (Red). Nox donne badge + CT46 après la défaite d'ONYBRIS dans la tour.

## Chrondrolia (étape 7) — arrivée
Joueur : Hematown -> Grenalux -> SURF sud (Route 21) -> Chrondrolia. Route 19 / volcan SEAFOAM fermés (éruption). Ville paisible, aucun policier ni Onybris visible ; les habitants jurent que la pierre n'est pas là. Centrale expliquée par la chaleur du volcan. Notes : Artikodin près de Bourg Quartz, Électhor dans la centrale, Sulfura dans le volcan (légendaires, plus tard).

## Chrondrolia — événement (badge 7)
Eddie battu -> blackout, le maire (taupe) dit avoir utilisé le joueur pour la clé secrète, la centrale est occupée ; SELENE (2e combat) garde le TOPAZ au 3F ; le joueur GAGNE la pierre (TOPAZ). Selene : l'éruption de la mer = leur oeuvre, le MAITRE est dans le volcan SEAFOAM. La mer (Route 19/20) et les grottes SEAFOAM s'ouvrent -> prochain QG (n°4, Gold + Silver).


## Volcan ÉCUME (Seafoam) — QG n°4 (V1)
- Cave convertie en volcan : palettes basalte + eau remplacée par de la LAVE (tileset primaire GeneralSeafoam), faune sauvage feu/roche (Slugma, Magcargo, Geodude, Graveler, Torkoal + chauves-souris), niveaux +6.
- Accessible après le raid de Chrondrolia (mer rouverte). 1F : GOLD + SILVER (provisoires : sprites Brendan/Bleu) rencontrent le joueur à l'une des deux entrées (« on passe devant, tu nettoies derrière »).
- B1F–B3F : 2 sbires par étage + sbire battu qui raconte le passage de Gold/Silver (crescendo : ils ouvrent la voie).
- B4F : Gold et Silver KO (battus par le grand patron en 1 Pokémon chacun), KRONOS combat le joueur (Arbok 47, Weezing 47, Nidoking 48, Crobat 48, Alakazam 50), indice : la pierre part vers le DERNIER QG près de la Ligue (Red). Moltres remplace Artikodin (combat optionnel, N55).
- Flags : 0x0B4 FLAG_SEAFOAM_ALLIES_MET, 0x0B5 FLAG_SEAFOAM_BOSS_DONE. Script : docs/topaze/seafoam_volcano.py + seafoam_lava.py + seafoam_scenario.py.

## Retour à Opanihrum : la FONDERIE (badge 8) puis ROUTE VICTOIRE = QG n°5 (V1)
- **Fonderie** (arène d'Hepha, Acier) : intérieur recoloré (sol acier sombre, flèches de spin en braise), Hepha (pic Winona, sprite Crush Girl, provisoires) : Magneton 52, Forretress 53, Skarmory 54, Scizor 55, Steelix 56, Aggron 58 ; 8 forgerons Acier (43–49) ; CT47 Aile d'acier ; Hepha dit que ses fourneaux ont forgé la porte de la Route Victoire et que des hommes en noir y sont entrés. Script : gym_opanihrum.py + gym_opanihrum_trainers.py.
- **Route 23** : gardes de badges d'origine (8e = badge d'Hepha). Au pied de la grotte (déclencheurs y=32, x2..8) RED, muet, regarde la grotte, salue et y entre seul (FLAG_VR_RED_MET 0x0B6).
- **Route Victoire 1F/2F** : anciens dresseurs devenus sbires Onybris (niv. 50–53) ; 3F : challengers d'origine inchangés (niveaux à revoir) ; VESPER (3e duel : Arbok 54, Gengar 54, Crobat 55, Muk 55, Hypno 56) garde la sortie est de la 2F.
- **LE REPÈRE d'Onybris (3 salles sous la Route Victoire, QG n°5)** : échelle cachée au mur nord de la grande salle NE de la 2F (30,1). Tileset de la Ligue recoloré en obsidienne (sol noir-violet, parois cramoisi, emblèmes en braise). Les sorties de la grotte (est de la 2F) sont fermées par une brume noire tant que le finale n'a pas eu lieu.
  - **Salle des gardes** (1F du repaire) : hall à statues (4 sbires), alcôve au trésor (sbire + Rappel Max), chambre du commandement où VESPER (3e duel) garde la porte ; Bonbon Rare caché.
  - **Salle des Pierres** (2F du repaire) : dix piédestaux en cercle autour de l'emblème. 7 pierres volées y reposent (Grenat, Pyrope, Tourmaline, Spinelle, Quartz, Amethiolite, Hématite) ; 3 piédestaux vides : APATITE, TOPAZE et OPALE (l'opale est portée par Red). SELENE (3e duel) garde la porte du trône.
  - **Salle du trône** (3F du repaire) : finale : Red à genoux avec l'opale, un cri PSYCHIQUE (Mewtwo, jamais montré) arrache l'opale des mains de Red, le TOPAZE du sac du joueur et appelle l'APATITE à distance ; les sept pierres de la Salle des Pierres s'envolent (les piédestaux se vident), puis noir ; Red, abîmé, soigne le joueur (FLAG_VR_BOSS_DONE 0x0B7). Les dix pierres sont désormais aux mains du patron (psychique : twist Mewtwo à confirmer à la Ligue).
  - Scripts : lair_tileset.py, lair_layouts.py, lair_build.py (+ victory_road.py). Les salles sont des copies des salles de la Ligue (Lance, Champion, Lorelei), à redessiner plus tard si besoin.
- Décision de fond à valider : le patron n'est toujours pas vu ; Red perd lui aussi ; l'OPALE NOIRE (10e pierre, clé de la porte de la Route Victoire) est prise par RED sur la place d'Opanihrum avant le joueur (Hepha le raconte) ; Red l'emporte dans la grotte et le patron la lui prend (elle n'est plus dans sa main à la sortie).

## Ligue, boss et trois fins (13/10, validé par Basil)
- Ligue = tournoi de 11 combats (voir claude/ligue-tournoi.md) ; le boss s'incruste après Chen pour prendre le vœu de Jirachi.
- **Vœu du boss : libérer tous les Pokémon des humains, plus jamais de Poké Balls.** Il ne le dit qu'à la Ligue ; avant, Onybris « libère » seulement les Pokémon des zones.
- Les 3 fins sont trois réponses à la même question que pose le boss :
  1. **Laisser partir Jirachi** : le boss est battu, l'Aura se calme, le jeu continue (post-game, `FLAG_TOPAZE_POSTGAME`).
  2. **Plus de Poké Balls** : le vœu du boss, exaucé par le joueur (fin « monde calme »).
  3. **Tous les légendaires à soi** : le miroir sombre du boss (Mewtwo, oiseaux, Mew, Celebi dans le PC).
- Le boss dit au joueur qu'il garde ses Pokémon en Balls : le choix 2 est celui qui lui donne raison.
- **Le boss a deux combats** : (1) son équipe ; (2) les légendaires qu'il a capturés, **Artikodin, Électhor, Sulfura + Mewtwo** (`TRAINER_LEAGUE_BOSS_2`, 755 dresseurs au total). Entre les deux : « chaque légendaire pris dérègle un peu plus l'horloge du monde » (secousse d'écran).
- **Idée à développer (Basil)** : le temps se dérègle au fur et à mesure qu'il capture des légendaires (indices à poser sur le parcours : horloges, jour/nuit, PNJ décalés). Son nom viendra plus tard.
- **Retours (V1)** : Brice, Flora et Misty sont au Centre Pokémon du Plateau Indigo (dialogues avant/après le titre de Champion). N et Gold sont dans le tournoi ; Red/Giovanni/Silver en post-game ; Bill (disparu) reste à traiter avec les îles Sevii.

## Légendaires et Quartz (13/10)
- **Les oiseaux sont les captifs du boss** : Électhor (centrale) et Moltres (volcan) ne sont PAS croisables avant la Ligue (`FLAG_TOPAZE_POSTGAME` requis pour les afficher). Après la fin 1 (boss battu), ils retournent dans leur lieu d'origine, capturables. Artikodin : seulement aperçu aux jumelles de la Route 15 ouest (pas de rencontre).
- **Twist Quartz (V1)** : le boss réagit au duel du casino. Gagné : « tu m'as pris QUARTZ… un coup de chance » ; perdu : « merci de l'avoir perdu ». Aucun autre effet : les pierres du joueur sont de toute façon arrachées au repaire.
- **Souhait de Basil (à placer)** : croiser dans le scénario tous les anciens Champions, membres du Conseil des 4 et Maîtres (gen 1-3). Les salles Bruno/Agatha/Lance sont libres (hors trajet) : candidates pour un « Conseil des Anciens » en post-game.
- **Mine de Grenalux** : elle s'ouvre après la Ligue (post-game fin 1). Intérieur à décider.
