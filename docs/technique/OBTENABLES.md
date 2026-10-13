# Audit des Pokémon obtenables (13/10)

Script : `docs/topaze/audit_obtenables.py` (sauvages + cadeaux/œufs/combats scriptés + échanges + évolutions + élevage des pré-évolutions ; Zarbi exclus).

**Résultat : 386 / 386 obtenables** (statique ; Porygon = lot de la salle de jeux de Bourg Quartz, ajouté à la main).

Sources des Pokémon de Johto/Hoenn :
- **Sauvages** : tables des îles Sevii (`docs/topaze/sevii_wild.py`, 46 tables, niveaux d'origine).
- **Starters** : cadeaux des Échos 1-6 (Germignon, Héricendre, Kaiminus, Arcko, Poussifeu, Gobou).
- **Légendaires** : Raikou/Entei/Suicune (Échos 1-3), Regice/Registeel/Regirock (Échos 4-6), Celebi puis Kyogre/Groudon/Rayquaza/Latias/Latios/Jirachi (Écho 7, Sevault Canyon).
- **Fossiles Lileep/Anorith** : sauvages à Ruin Valley (V1).

À vérifier plus tard (non testé de bout en bout) : Illumise/Volbeat (genre), Porygon2 (évolution par échange d'objet), Castform, Feebas (pêche), Shedinja (évolution de Ninjask).
