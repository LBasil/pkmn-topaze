# Banc de scénarios (copie de travail du 13/10)
Copiés tels quels depuis /tmp/gx (chemins en dur : `/tmp/gx`, `/home/claude/pkmn-topaze` ; à adapter).
- `mkdbg2.py` : construit la ROM de debug (équipe forte, drapeaux/variables préchargés, mode « dieu », pas de combat) et la remet à zéro ; sauvegarde aussi `.map` et `.elf`.
- `drive.py` : pilote mGBA (harnais `harness.c`) ; `tz.py` : classe `T` (boot sur une carte, marche BFS, `scene()` qui joue dialogues/combats jusqu'au retour du contrôle, `chain` de warps, portes à collision, escaliers).
- `spin.py` : BFS avec cases-flèches (le joueur continue tout droit sur sol normal après une flèche, jusqu'à une case d'arrêt 0x58 ou un obstacle). `xreach.py` : atteignabilité statique à travers les warps.
- Audit statique des dresseurs dans les couloirs : `docs/topaze/audit_couloirs.py`.
Adresses utiles (ROM de debug) : gMain 0x030030f0 (callback2 +4, inBattle +0x439 bit0), sLockFieldControls 0x03000f9c, gObjectEvents 0x02036e38 (0x24 par objet, coordonnées +7 à +0x10).
