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
- [x] **Répétiteur d'attaques** dans tous les Centres Pokémon (infirmière, gratuit) : testé avec une ROM de debug (départ au Centre de Jadielle, Salamèche niv. 20) : question, choix du Pokémon, liste des attaques réapprenables. Astuce de test : voir `tools/topaze/emu/README.md` (ROM de debug, `TOPAZE_ROM`).
- [x] Objets tenus des champions : combat contre le champion de Argenta/Pewter (KAY) : 1er Pokémon Goupix avec **Charbon** (lu en mémoire de combat).
- [x] Coupe en jeu (Vermilion, badge 2, sans l'apprendre) : invite « Would you like to CUT it? », l'arbre disparaît.
- [x] Split par attaque mesuré : avec Attaque 300 / Atq. Spé. 5, **Coup-Glace** (Glace, forcée physique) met le Goupix KO d'un coup, alors que **Lance-Flammes** (spéciale) ne lui retire rien.
- [ ] Seul reste non mesuré : la vitesse paralysée (changement d'une ligne, relu dans le code).

- [x] **CS dans le sac obligatoire** : sans CS01, l'arbre affiche seulement « This tree looks like it can be CUT down! » ; avec CS01 + badge, « CHARMANDER used CUT! ». Même contrôle pour Surf (CS03), Force (CS04), Éclate-Roc (CS06), Cascade (CS07).

- [x] **Grunt ONYBRIS à Grenalux** : après le combat du rival, un grunt arrête le joueur sur la route (x=10, y=6), dialogue Jirachi/aura, combat Rattata+Zubat niv. 4 gagnable avec le starter, puis il disparaît.

- [x] **Musée de Grenalux** : la porte de la façade mène à l'intérieur (carte neuve), le conservateur parle (GRENAT / aura), la sortie ramène devant la porte.

- [x] **Ouverture selon le document de conception** : sans Pokémon, Zéphyr arrête le joueur à la sortie nord, l'emmène jusqu'au ranch (maison en haut à droite) ; scène **dans l'intérieur du ranch** (père de Zéphyr, Prof. Chêne et Zéphyr présents ; vol des Pokémon pisteurs par Onybris), puis arrivée au labo et choix du starter. Variable `VAR_GRENALUX_OPENING` (1 = scène à jouer, 2 = faite), drapeau `FLAG_HIDE_RANCH_SCENE`.

- [x] **Trois frappes d'Onybris (version « après coup »)** : ranch (raconté par le père de Zéphyr), musée (vitrine vide, conservateur et vieil homme changent de dialogue) et labo (assistants et ordinateur : fichiers sur les gemmes copiés), tous déclenchés par `FLAG_GRENALUX_ONYBRIS_STRIKE` posé quand le grunt de la route est battu. Testé : dialogues du musée. Reste à tester en jeu : dialogues du labo (même mécanisme).

## Limites connues
- Sprites des champions = ceux des chefs d'arène d'origine.
- Hepha utilise le slot de Giovanni (arène de Jadielle).
- Pas de nouvelle ville/arène : les cartes sont celles de Kanto (travail Porymap à venir).
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
