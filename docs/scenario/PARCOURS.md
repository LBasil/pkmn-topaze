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

