# Décisions de conception

| Décision | Raison |
|---|---|
| Base **pokefirered** + agbcc (pas d'« expansion ») | Dépôt de référence, compile avec le compilateur d'origine, reproductible. Une expansion (types/talents/phases modernes) pourra être réévaluée plus tard. |
| 151 Pokémon de Kanto seulement en v1 | Périmètre maîtrisable ; les types sont revus pour toute la dex. |
| Types retravaillés + Fée | Le fil narratif : une aura a muté les types il y a 10 ans. |
| Starters conservés mais redessinés | Garder l'identité classique (Plante/Feu/Eau) avec une seconde couleur. |
| Fée à l'index 18 | Évite de renuméroter les 17 types existants. |
| CT infinies, CS oubliables | Confort de jeu ; moins de blocages sans tests. |
| Coupe/Force/etc. en vraies attaques | Les CS ne sont plus des « slots morts ». |
| Monde ≈ +12 % de niveau | Compenser les Pokémon plus polyvalents grâce aux STAB. |
| Texte en anglais | Limites de la Gen 3 ; pas de coût de traduction en v1. |
| Champions dans les slots des chefs d'arène | Réutilise sprites, musiques, scripts et flags : zéro risque de blocage. |
| Pas de scripts narratifs sans test | Un script mal écrit peut bloquer la partie ; reportés au premier test sur machine. |
