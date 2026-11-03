# Comparaison avec la VF officielle de Rouge Feu (BPRF)

Méthode : textes de script extraits de la ROM FR (fournie par Basil) et du FireRed EN reconstruit (pret) ; alignement des deux par les pointeurs `loadword` des scripts (2725 EN / 2726 FR), puis appariement sur la structure (\p, \n, nombres, longueur) avec vérification de continuité. ~2120 paires fiables.

## Résultat
- 1276 de nos dialogues ont exactement le même anglais que Rouge Feu ; 1131 ont repris la formulation officielle (reformatée : espace avant ! ? :, accents des majuscules, lignes ≤35, noms Topaze conservés).
- 100 écartés volontairement (noms de dresseurs localisés par Nintendo mais gardés en anglais chez nous : JED/LEA → ALI/LISE, MR. FUJI, KANTO…).
- Nom officiel de Daisy : NINA (remplace MARGUERITE).

## Conventions de la VF officielle (à suivre pour nos textes originaux)
- Registre familier et oral : « J'suis », « T'es », « y'a », « J'dois m'trouver… », « Moi j'suis naze ! » (≈50 occurrences) ; contractions j'/t' très fréquentes.
- Tutoiement dominant (≈750 « tu/te/ton » contre ≈120 « vous » : le « vous » est réservé aux messages système, aux vendeurs et aux infirmières).
- Phrases courtes, exclamations nombreuses ; pas de tournure littérale de l'anglais (« Pas encore. Finis d'abord… » → plutôt « Reviens quand tu auras… »).
- TRAINER TIPS = ASTUCE ; Fossile DOME ; « {PLAYER} reçoit le/la X ! » (présent) pour les objets reçus ; onomatopées adaptées (MACHOPEUR : « Chop ! Chop ! Chop ! »).
- La VF GBA n'a pas d'espace avant ! ? : — nous gardons l'espace (typographie correcte) partout.

## Reste à faire avec cette base
- Réécrire dans le même registre les ~4300 textes Topaze originaux (tournures littérales).
- Faire le même appariement pour les chaînes système (combat, menus, descriptions d'objets, entrées de Pokédex, descriptions d'attaques).
