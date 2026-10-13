# Passe de test émulateur du 13/10 (Hematown → repaire)

Méthode : ROM de debug (équipe forte, mode « dieu », pas de combats sauvages) + scénarios scriptés (`tools/topaze/emu`, voir EMULATEUR.md). Chaque scène a été jouée en entier, captures à l'appui. Tri : **B** = bloquant, **G** = gênant, **C** = cosmétique.

## Joué sans anomalie
Hematown (arrivée des alliés, 3F, 11F : Kronos + ombre du boss), Chrondrolia (raid, blackout, maire), usine/plante 1F→3F (Selene, Topaze), volcan 1F (alliés des deux côtés) et B4F (Kronos), Fonderie (Hepha, badge 8 + CT), Route 23 (scène de Red), Route Victoire (accessibilité 1F→2F→3F et échelle du repaire, statique), repaire 1F → 2F → 3F (scène finale, `FLAG_VR_BOSS_DONE`).

## Bugs trouvés et corrigés
| # | Gravité | Où | Problème | Correctif |
|---|---|---|---|---|
| 1 | **B** | Repaire 1F | L'échelle (6,5) vers 2F était **solide** : la salle est copiée de la salle de Lance dont la porte ne s'ouvre que par script. | `lair_layouts.py` écrit directement l'état ouvert (porte (6,4)-(6,5)). |
| 2 | **B** | Repaire 3F | À l'arrivée (6,12), les cases (5..7, 11..12) étaient la porte d'entrée de la salle de Lorelei, fermée : joueur **coincé** dès l'arrivée. | Cases passées en sol ouvert. |
| 3 | **B** | Repaire 1F | Vesper (6,9) vue 5 : il vient se planter en (6,13), à la sortie du couloir d'accès large d'1 case → joueur enfermé. | Vesper en (6,7), vue 4 (le combat se joue dans la salle, on le contourne). |
| 4 | **B** | Fonderie | Takashi (10,2) vue 3 : il descend en (10,4) dans le seul couloir menant à Hepha → **Hepha inaccessible**. | Vue réduite à 1 (il combat sans bouger). |

## Observations non corrigées
- **C** : un objet sombre « N » au bord est du volcan 1F (probablement un rocher foncé) ; à vérifier visuellement.
- **C** : les noms par défaut aléatoires (ex. « KAY ») peuvent coïncider avec un nom de personnage.
- **G** : Topaze (plante 3F) n'offre aucun objet, seulement un message.
- **C** : le sprite d'un dresseur arrivé sur (6,13) du repaire n'est pas visible (calque) — sans conséquence après le correctif 3.

## Leçon de conception (à appliquer partout)
Un dresseur qui voit le joueur **s'arrête sur la case voisine et y reste**. Ne jamais mettre un dresseur dont la ligne de vue traverse un couloir d'1 case (sans contournement) : l'approche le bouche. Vérifier avec `spin_bfs` + case d'arrêt du dresseur.

## Reste à tester (même méthode)
Spinellia (portes), Routes 8 / souterrain, Bourg Quartz (Vesper/Grim), Amethiolite (zoo, Safari), Route Victoire en jeu (boulons/interrupteurs), puis audit systématique « dresseur dans un couloir d'1 case » sur toutes les cartes.

Captures : `docs/technique/captures/` (`lair1-vesper-corridor.png`, `lair1-vesper-bloque.png`, `fonderie-hepha.png`).
