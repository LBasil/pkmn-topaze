# Pokémon Topaze — notes de projet

Base : pret/pokefirered (commit 037335f4), compilée avec agbcc.
Jalon 0 : `make compare_firered` -> pokefirered.gba: OK (SHA1 identique à l'original).

Document de conception : voir le doc partagé (types des 151, villes, histoire, jalons).
Prochain jalon : Jalon 1 — nouveaux types des 151 Pokémon (src/data/pokemon/base_stats.h).

## Équilibrage des stats (jalon 3)
Retouches légères, à valider en jeu : Blastoise DEF 100→95 ; Machamp DEF 80→75 (Acier) ; Gyarados ATK 125→120, PV 95→90 (Eau/Dragon, peu de faiblesses) ; Dracaufeu DEF 78→83, DEF SPE 85→90 (Feu/Glace, très fragile).
