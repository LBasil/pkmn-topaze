# Outils et scripts

Python 3, aucune dépendance externe. Les scripts de `docs/topaze/` prennent **le chemin du dépôt en argument** (`python3 docs/topaze/leaders_data.py .`) ; `build_site.py` se lance depuis la racine.

| Script | Rôle | Idempotent ? |
|---|---|---|
| `docs/topaze/leaders_data.py` | Écrit les équipes des 8 champions dans `trainer_parties.h` / `trainers.h` | Réécrit les équipes (rejouable) |
| `docs/topaze/learnsets_stab.py` | Ajoute les attaques STAB aux apprentissages | Oui (ignore les attaques déjà apprises) |
| `docs/topaze/harder_world.py` | Monte les niveaux des dresseurs et des herbes | **Non** : l'effet s'additionne |
| `tools/topaze/build_site.py` | Génère `docs/data/*.js` pour le site joueur | Oui |

Le script d'application des types (`apply_types.py`) n'est pas versionné : il a été exécuté une fois et le résultat est dans `species_info.h`.

## Le site joueur (`docs/`)
Site statique (HTML + JS sans dépendance), pensé pour **GitHub Pages** (Settings → Pages → branche `topaze`, dossier `/docs`).
- Pages : `index`, `guide`, `pokedex`, `movedex`, `types`, `champions`, `wild`.
- Les données (`docs/data/*.js`) sont **générées** depuis les sources C : après toute modification de stats, types, attaques, champions ou rencontres → `python3 tools/topaze/build_site.py` puis commit.
- `build_site.py` lit directement `species_info.h`, `battle_moves.h`, `level_up_learnsets.h`, `trainer_parties.h`, `wild_encounters.json` et la table d'efficacité de `battle_main.c` par expressions régulières : si ces formats changent, adapter le script.
- Test local : `cd docs && python3 -m http.server 8000`.
