# Audit des cartes extérieures (01-11-2026)
Outils (rejouables, sur Topaze ET sur FireRed d'origine) : `tools/topaze/maps/audit.py <racine> out.json` (taille, marchable, goulots, distances, événements inaccessibles) et `tools/topaze/maps/world_reach.py <racine> out.json` (graphe du monde via connexions + warps depuis la chambre du joueur, Surf autorisé). Origine clonée dans `../pret/orig_fr`. Rendus annotés : `mapkit.py` + annotation (rouge = Centre, jaune = Arène, bleu = Boutique, vert = portes, magenta = sorties, cyan = panneaux, blanc = PNJ).
Limites de la méthode : objets (arbres à couper, rochers, PNJ bloquants) ignorés ; l'eau est comptée non marchable pour les mesures de ville, marchable (Surf) pour l'accessibilité globale.

## 1. Villes : taille et proportions (origine → Topaze)
| Ville (type de l'arène) | Taille | % marchable | Couloirs 1 case | Centre→Arène (pas) | Verdict |
|---|---|---|---|---|---|
| Grenalux (aucune ; grenat) | 24×20 → 44×40 | 56 → 52 | 5 % | — | 4× plus grande que l'origine, éparse mais fluide ; thème grenat lisible |
| Opanihrum (Acier) | 48×40 → 42×44 | 44 → 46 | 5 % | 40 → 26 | Très bien : grille symétrique, forge Acier immédiatement lisible ; maisons toutes identiques (grises) donc peu repérables |
| Pyropia (Feu) | 48×40 → 48×40 | 47 → 51 | 8 % | 45 → 15 | Bien : lave/volcan clairs, Arène plus proche (15 contre 45) ; moitié basse très vide (3 maisons) |
| Tourmalia (Insecte/Plante) | 48×40 → 62×46 | 45 → 18 | 11 % | 11 → 41 | Thème parfait mais 82 % bloqué, 28 culs-de-sac, Arène à 41–72 pas (11–61 à l'origine) : la moins facile à parcourir |
| Spinellia (aucune ; Spectre) | 24×20 → 40×30 | 50 → 44 | 8 % | — | Cimetière évident, bonne densité de PNJ (13 contre 3) |
| Apatia (Dragon/Fée) | 48×40 → 48×40 | 32 → 31 | 4 % | 34 → 46 | Port + os de dragon ; Arène un peu plus loin, rien de gênant |
| Bourg Quartz (Glace) | 60×40 → 60×40 | 46 → 39 | 3 % | 84 → 63 | Neige/glace évidentes ; Arène bien plus proche qu'à l'origine |
| Amethiolite (Poison/Spectre) | 48×40 → 48×32 | 48 → 37 | 8 % | 17 → 56 | Château violet cohérent ; peu d'espaces larges (11 %), 29 culs-de-sac, Arène 56 pas |
| Hematown (Ténèbres/Spectre) | 66×55 → 66×55 | 25 → 31 | 5 % | 56 → 70 | Ville nocturne très lisible ; énorme (≈ 24 écrans), 41 culs-de-sac, 15 → 29 portes, 4 portails comme l'original |
| Chrondrolia (Électrik) | 24×20 → 28×20 | 31 → 40 | 5 % | 15 → 23 | Centrale + pylônes = Électrik évident ; compacte, très facile |
Cohérence types/décor : les 8 villes à Arène se lisent du premier coup d'œil (Acier, Feu, Plante/Insecte, Dragon, Glace, Poison/Spectre, Ténèbres, Électrik). Incohérence de documentation : `PARCOURS.md` ligne 31 dit Hera = Dragon/Fée, `parcours-joueur.md` dit Dragon/Vol (les dresseurs de l'arène sont Fée/Eau/Vol/Normal).

## 2. Déplacement (routes)
Toutes les routes refaites gardent un trajet bout à bout proche de l'origine (Route 1 : 56 vs 60 ; Route 12 : 90 vs 88 ; Route 13 : 87 vs 84 ; Route 14 : 73 vs 73 ; Route 24 : 43 vs 43). Exceptions voulues : Route 17 raccourcie (169 → 96 pas, 24×160 → 24×80), Route 4 verticale (40×84) + Route 4 Est (72×30), Route 2 plus courte (24×80 → 26×56), Route 3 (107 pas). Routes les plus étroites (cases libres 3×3 < 12 %) : Route 12 (5 %), Route 20 (7 %, mer), Route 22 (7 %, couloirs 20 %), Route 21 (mer), Route 25 (23 %, couloirs 17 %).

## 3. Accessibilité (graphe du monde depuis la chambre du joueur)
Chemin principal complet : aucune zone coupée sur le parcours principal (villes, routes, arènes). Défauts trouvés :
1. **Tourmalia : 6 warps « parqués » dans le coin (0,0..3)** vers HOUSE1, HOUSE2, BIKE_SHOP, HOUSE5 (intérieurs jamais atteignables). À supprimer.
2. **Bourg Quartz : 3 portes nord de la résidence (25..27, 4..5)** hors terrain marchable (porte arrière inaccessible ; l'entrée sud fonctionne).
3. **Éléments inaccessibles** : objet caché Baie Pêcha de la Route 24 (19,4) ; panneau « Trainer Tips » d'Hematown (53,24) ; panneau du manoir de Bourg Quartz (24,12) ; panneaux décor de Grenalux (gardien, baies : probablement voulus).
4. **Intérieurs orphelins** (plus aucune porte ne mène à eux) : `Route2_House`, `Route2_EastBuilding`, `Route16_NorthEntrance_1F/2F`, `SaffronCity_Connection`, plus 137 cartes « gabarit » non reliées (ANCIENT_LIBRARY, APOTHECARY, BERRY_BROOK… toutes avec un marin générique) : à garder si elles sont prévues, sinon à purger.
5. Tourmalia : Blue (48,6) et le policier (49,11) sont dans la zone nord réservée par script (voulu) ; sortie est = cabane-portail (3 connexions au lieu de 4, voulu).
Intérieurs Sevii non reliés au graphe (pas de bateau scripté dans l'analyse) : non évalué.

## 4. Orientation / densité
Moins de panneaux qu'à l'origine : Amethiolite 4 (origine 11), Tourmalia 4 (7), Apatia 4 (5). Plus de PNJ partout (Amethiolite 38 contre 16, Apatia 18 contre 8, Bourg Quartz 25 contre 15) : ville vivante mais attention aux PNJ qui coupent des goulots (déjà vérifié par BFS sur les barrages). Herbe haute : Route 17 passe de 0 à 143 cases, Route 3 de 117 à 260, Route 14 de 30 à 110 (plus de rencontres sauvages).

## 5. Recommandations (par priorité)
1. Nettoyer Tourmalia (6 warps parqués) et la porte arrière de Bourg Quartz ; déplacer l'objet de la Route 24 et les 2 panneaux.
2. Tourmalia : ajouter 2–3 panneaux vers l'Arène (41–72 pas) et élargir un axe ouest-est.
3. Amethiolite/Hematown : panneaux directionnels vers Arène et Centre ; 2–3 raccourcis pour les culs-de-sac.
4. Opanihrum : varier 3–4 maisons (couleurs/toits) pour les repérer.
5. Décider du sort des 137 cartes gabarit et des intérieurs orphelins.
6. Harmoniser la doc (type d'Hera).
