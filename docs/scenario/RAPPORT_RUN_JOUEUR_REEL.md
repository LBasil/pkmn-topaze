# Rapport détaillé — run « joueur réel » de bout en bout (24/10)

Bot sans god mode : un seul Bulbizarre au départ, équipe entraînée en combat réel, achats au magasin, soins au Centre, PNJ parlés, CS apprises. 5 196 lignes de journal, **4 253 combats**, **268 soins**, **132 rotations d'équipe** (le bot change de lead pour partager l'XP via le menu Équipe).

## Verdict
- Les **8 arènes**, la **Route Victoire**, le **tournoi de la Ligue**, puis tout le post-game (Mine, oiseaux, ferry, Sevii, **Sulfura**) sont passés avec une équipe entraînée normalement (niveaux 66-69 à la fin).
- **Deux réserves** : (1) le Champion n'est pas battu proprement (blanc-out sur son Dracolosse 64, le harnais a posé l'état de fin) ; (2) les **Échos du Temps s'arrêtent au stade 21** (l'étape ne passe pas à 22 : les 6 derniers légendaires Kyogre…Jirachi ne sont pas atteints).
- Aucune régression ROM bloquante côté joueur ; 1 vrai bug ROM trouvé et corrigé (Piège de Roc).

## Parcours (équipe en fin d'étape)
| Étape | Niveaux d'équipe | Remarque |
|---|---|---|
| Départ | Bulbizarre 5 | Route 1 : Roucool + Rattata capturés |
| Arène 1 Argenta | 11-19 | Capture Mankey, Nidoran♀/♂, Rattata (Route 22), Goupix (Forêt de Jadielle) |
| Arène 2 Azuria | 24-25 | **Pic de difficulté : 18 défaites** avant de passer (Ondine) ; 3 séquences d'entraînement Route 4 / Route 4 Est |
| Arène 3 Carmin | 26-30 | Coupe nécessaire pour l'arène (arbre) |
| Arène 4 Céladopole | 35-43 | 1 défaite |
| Arène 5 Parmanie | 42-47 | 2 défaites (Safari : entraînement) |
| Arène 6 Safrania | 47-52 | 2 défaites |
| Arène 7 Cramois'Île | 51-52 | 1 défaite ; **évolutions par pierres ajoutées au bot** : Goupix→Feunard, Nidorina→Nidoqueen, Nidorino→Nidoking (pierres achetées Céladopole, 4F) |
| Arène 8 Jadielle | 53-58 | 1ʳᵉ tentative |
| Ligue | 57-60 | 3 blanc-outs en route vers le Champion |
| Post-game | 61-69 | Sulfura, Échos 1-21 |

## Ce qu'il a fallu capturer / obtenir pour passer
- **11 captures seulement** (aucune légendaire : les légendaires sont combattus, pas capturés) : Roucool, Rattata ×2, Mankey, Nidoran♀/♂, Rattata, Goupix.
- **Coupe** utilisée **26 fois** (Carmin, Azuria, Céladopole, Parmanie, Routes 8/10/12, Deux/Trois-Îles).
- **Achats** : Poké Balls ×10 + Potions ×5 (Jadielle, 3 080→580 ₽) ; Pierre Feu ×1 + Pierres Lune ×2 (Céladopole 4F, ~6 300 ₽).
- **Maître des capacités** : 40 utilisations (reproduit par le bot, voir « triches ») ; au final les attaques changent bien (ex. Goupix niv. 39 : Lance-Flamme/Rafale Psy/Choc Mental/Charge Feu).

## Blanc-outs (101 au total)
Route 17 (**56**, tous avant correction du bug « oubli d'attaque »), Arène d'Azuria (15), Ligue — Salle de Lorelei (9), Arène de Safrania (3), Arène de Cramois'Île (2), Céladopole (2), Sommet du Mont Brasier (2), 9 autres endroits ×1. **Conclusion : la difficulté réelle du jeu tient** ; la Route 17 et Azuria sont les endroits où un joueur normal souffre le plus.

## « Triches » du harnais (ce qui n'a pas été joué à la main)
143 entrées dans le journal, toutes tracées :
- **Variables de scène** (94) : Route Victoire (VAR_MAP_SCENE ×4, ×20 fois chacune : le bot ne pilote pas les cinématiques d'ouverture), Tour des Anciens (VAR_ELDERS_ROUND ×9), Îles (scènes d'arrivée, VAR_ECHO_STAGE posée 2 fois).
- **Drapeaux** (49) : CS (FLAG_GOT_HM04 / HM06 posés à One Island, 16 fois), trois drapeaux posés dans la Salle de Lorelei (2032-2034), Îles Écume (courants B3F/B4F arrêtés, 2 dresseurs), Trois-Îles (motards masqués), Bourg-Palette (lien R/S).
- **Fin du jeu** : Champion non battu (blanc-out Dracolosse 64) → les combats suivants sont sautés et l'état de fin (fin 1, post-game) est posé ; le générique est joué, l'état est ensuite restauré à la main (limite du harnais, le « CONTINUER » recharge un save plus ancien).
- **Maître des capacités** : écran non piloté, effet reproduit par écriture directe des attaques (même résultat que le PNJ du jeu).
- **Rotation d'équipe** : changement de lead via poke de l'ordre d'équipe quand le menu est inaccessible.

## Anomalies relevées sur le jeu lui-même (à regarder)
1. **Scène finale du repaire (Bourg Quartz) non jouée** à l'étape « victoire » (« scène finale du repaire non jouée »).
2. **Tournoi de la Ligue** : figé au tour 9, débloqué par le harnais (`league_finale`).
3. **Échos** : bloqué au stade 21 (Sevault Canyon → Centre Pokémon de Six-Îles, la suite ne se déclenche pas). À vérifier à la main : un joueur humain peut-il avancer ? (échos 7 à 10 passés par saut « skip » : `echo_7_skip`, `echo_10_skip`).
4. Sommet du Mont Brasier : gardes de Sulfura très durs pour des niveaux ~66 (Dracaufeu 65, Houndoom 63, Magmar 62) : 2 blanc-outs, puis passés.

## Bugs trouvés pendant la run
**ROM** : *Piège de Roc* (TopazeRockDamage) — compteur `u8` → boucle infinie à 256 → blocage dur du jeu en combat. Corrigé (`u16`).

**Bot** (ce qui causait les faux problèmes d'XP/blanc-outs) :
- Oubli d'attaque : choisissait toujours le slot 0 → movesets ruinés (56 blanc-outs Route 17). Remplacé par un choix de valeur d'attaque + Maître des capacités simulé.
- Évolution par pierre absente → ajoutée.
- Rochers Force déjà poussés : leur ancienne position JSON restait un mur (Mont Brasier extérieur scellé).
- Budget d'essais de poussée (8) épuisé par les allers-retours au Centre → 40.
- Trajet long (Route du Tison, ~130 cases) abandonné après 12 pas → reprise tant qu'il avance.
- Contrôle des listes du sac (curseur mémorisé), comptoir inaccessible au magasin de Céladopole 4F, Détection (Disable) bannie, arbre à couper automatique.

## Coût de la run
L'étape Sulfura a pris ~2 h de run à cause des 3 derniers bugs du bot (pas du jeu) : 11 échecs de l'étape avant correction.
