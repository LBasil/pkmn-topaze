# Documentation technique — Pokémon Topaze

Pour développeurs et contributeurs. Base : [pret/pokefirered](https://github.com/pret/pokefirered) (commit `037335f4`), langage C + assembleur GBA, compilateur `agbcc`.

| Document | Contenu |
|---|---|
| [COMPILATION.md](COMPILATION.md) | Installer la chaîne, compiler, lancer, dépanner |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Carte du dépôt : où se trouve chaque donnée modifiée |
| [TYPES.md](TYPES.md) | Le type Fée et la table des types (modifier les types, ajouter un type) |
| [DONNEES.md](DONNEES.md) | Pokémon, attaques, apprentissages, dresseurs, rencontres, difficulté |
| [OUTILS.md](OUTILS.md) | Scripts Python (`docs/topaze/`, `tools/topaze/`) et le site joueur |
| [INSPIRATION_CFRU.md](INSPIRATION_CFRU.md) | Ce qu'on reprend des hacks CFRU (Radical Red…), fait / à faire |
| [DECISIONS.md](DECISIONS.md) | Choix de conception et leurs raisons |
| [TESTS.md](TESTS.md) | Check-list de test en jeu, limites connues, TODO |

## Principes de travail
- **Branche `topaze`** ; `main` reste vide.
- Chaque jalon = un commit autonome qui **compile** (`make -j$(nproc) firered`).
- Les modifications de masse passent par un **script Python reproductible** (voir OUTILS.md), jamais à la main sur 151 entrées.
- Rien n'est « validé » tant qu'il n'a pas été joué : voir TESTS.md.
- Le texte du jeu reste en **anglais** (limite de caractères Gen 3, pas de traduction prévue en v1).
