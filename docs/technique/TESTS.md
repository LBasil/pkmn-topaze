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
**Stabilité**
- [ ] Sauvegarder / recharger ; évoluer ; apprentissage d'attaques sans plantage (limite de 20 par Pokémon).

## Limites connues
- Sprites des champions = ceux des chefs d'arène d'origine.
- Hepha utilise le slot de Giovanni (arène de Jadielle).
- Pas de nouvelle ville/arène : les cartes sont celles de Kanto (travail Porymap à venir).
- Ossatueur : branche d'évolution Sol/Spectre reportée (nécessite une nouvelle espèce et un sprite).

## Pokémon suiveur (follower) — étude, non implémenté
Faisable techniquement (le moteur pokeemerald-expansion a un système de followers), mais pas ici et pas maintenant :
1. **Code** : porter un système de follower dans pokefirered (gestion d'un object event supplémentaire, collisions, passage de portes, surf/vélo, scripts de cinématique). Non testable sans émulateur : risque élevé de blocages.
2. **Graphismes** : il faut un **sprite overworld par espèce** (151 minimum, 16×32 avec 9 images) ; pokefirered n'en fournit pas. À créer ou à récupérer (licences !).
Piste réaliste : faire d'abord le jeu jouable, puis ajouter un follower **limité aux espèces qui ont un sprite** (starters + Pikachu), les autres restant dans la balle.

## TODO
- Scripts de Grenalux (rival, blocage sans Pokémon, attaques d'Onybris).
- Cartes et villes originales (12 villes, 8 arènes), Ligue en tournoi, trois fins, post-game (Giovanni puis Red).
- Équilibrage après premiers tests ; équipes thématiques des dresseurs de route.
- Vérifier s'il existe une « expansion » FireRed maintenue à adopter.
