# Inspiration : les hacks basés sur CFRU

**CFRU** (Complete FireRed Upgrade, de Skeli789) est un *patch binaire* en C/ASM appliqué à une ROM FireRed : il alimente notamment Radical Red, Unbound et d'autres. Il n'est **pas utilisable tel quel** avec Topaze (qui part du code source décompilé pokefirered : les deux approches ne se combinent pas). On s'en **inspire** : on reproduit chez nous les fonctionnalités qui apportent le plus, en C, dans le dépôt.
(Liste établie de mémoire sur ces hacks connus, pas à partir de leur documentation actuelle : à recouper.)

Remarque : un projet communautaire (`cawtds/pokefirered`) porte une partie de pokeemerald-expansion sur pokefirered ; il ne désactive que Teachy TV et l'aide. À étudier plus tard comme source de code, sans changer de base maintenant (risque élevé, aucun test possible).

## Fait dans Topaze
| Idée CFRU | Réalisation |
|---|---|
| Split physique/spécial **par attaque** | `FLAG_FORCE_PHYSICAL/SPECIAL` + macro `MOVE_IS_PHYSICAL` (voir TYPES.md) ; 56 exceptions Gen 4 |
| Type Fée | Complet (table, icône, attaques) |
| CS sans les apprendre | Scripts + `PartyHasMonWithSurf()` |
| Multi Exp. intégré, texte rapide, course partout, CT infinies | Voir ARCHITECTURE.md |
| Équipes de champions « sérieuses » (objets, IV élevés, 4–5 Pokémon, attaques perso) | `leaders_items.py` : objets tenus par chaque champion (objets de type, Baie Sitrus, Restes pour l'as) |
| Attaques rééquilibrées | `balance_moves.py` |

## Faisable ensuite (par ordre de rapport qualité/risque)
1. **Données seules** (sûr) : objets/EV/natures des dresseurs importants, équipes de la Ligue, rematchs, difficulté « Hard » via un drapeau.
2. **Petites règles moteur** (C simple) : taux de critique Gen 6 (1/16), brûlure 1/16 des PV, paralysie à ½ vitesse, Choix de talents en Gen 3 (talents cachés), Pierres Évolutives étendues.
3. **Confort scripté** : Répétiteur d'attaques dans chaque Centre Pokémon, recharge de Repousse automatique, accès au PC partout (objet), GPS/Pokédex amélioré, sélection du Pokémon qui utilise la CS (déjà possible via menu).
4. **Gros chantiers** (à ne faire qu'avec des tests) : Pokémon suiveur, DexNav, Méga-évolution / Capacités Z, mode Nuzlocke intégré, nouveaux talents. Chacun demande code étendu **et** graphismes.

## Comment on avance
Chaque ligne du 1 et 2 est un jalon autonome : code + doc + case dans TESTS.md. Les gros chantiers ne démarrent qu'une fois la ROM jouée et la base validée.
