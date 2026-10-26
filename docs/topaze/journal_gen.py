#!/usr/bin/env python3
"""Genere src/data/topaze_journal.h : le JOURNAL (menu Start) = liste d'objectifs triee par sections.
kind: F flag set / V var >= val / T dresseur battu.  Textes en anglais, 35 car. max par ligne."""
import re
F, V, T = 0, 1, 2
# (nom section, drapeau de deblocage ou None)
SECTIONS = [
    ("BADGES", None),
    ("STORY", None),
    ("SIDE QUESTS", None),
    ("POST-GAME", "FLAG_TOPAZE_POSTGAME"),
    ("ECHOES", "FLAG_TOPAZE_POSTGAME"),
    ("LEGENDS", "FLAG_TOPAZE_POSTGAME"),
    ("RARE POKéMON", "FLAG_TOPAZE_POSTGAME"),
]
E = []
def add(sec, kind, ident, val, name, hint):
    E.append((sec, kind, ident, val, name, hint))

# 0 BADGES
for i, (nm, town, boss) in enumerate([
    ("KAY", "PYROPIA", "Fire"), ("SYLVESTRE", "TOURMALIA", "Bug / Grass"), ("HERA", "APATIA", "Dragon / Fairy"),
    ("GRIM", "BOURG QUARTZ", "Ice"), ("ACHLYS", "AMETHIOLITE", "Poison"), ("NOX", "HEMATOWN", "Dark"),
    ("EDDIE", "CHRONDROLIA", "Electric"), ("HEPHA", "OPANIHRUM", "Steel")], 1):
    add(0, F, "FLAG_BADGE0%d_GET" % i, 0, "%s, %s" % (nm, town),
        "BADGE %d. Beat %s in\\n%s. %s specialist." % (i, nm, town, boss))
# 1 STORY
add(1, F, "FLAG_GRENALUX_ONYBRIS_STRIKE", 0, "THE RANCH ATTACK", "ONYBRIS strikes GRENALUX. Beat the\\ngrunt on the road out of town.")
add(1, F, "FLAG_GRENALUX_GEM_REWARD", 0, "THE TRUE GRENAT", "A ranch worker in GRENALUX has the\\ntrue GRENAT stone for you.")
add(1, F, "FLAG_PIER_KRONOS_DONE", 0, "THE APATIA PIER", "Reach the harbor of APATIA in time\\nto save the APATITE.")
add(1, F, "FLAG_RESCUED_MR_FUJI", 0, "SPINELLIA TOWER", "Calm the spirits of the TOWER in\\nSPINELLIA and find FUJI.")
add(1, F, "FLAG_QUARTZ_DUEL_DONE", 0, "THE QUARTZ DUEL", "Clear the hideout under the GAME\\nCORNER, then play the casino duel.")
add(1, F, "FLAG_AMETHYST_RAID_DONE", 0, "AMETHIOLITE RAID", "Help repel the ONYBRIS raid on\\nAMETHIOLITE.")
add(1, F, "FLAG_HEMATEK_BOSS_DONE", 0, "HEMATEK TOWER", "Storm the ONYBRIS HQ in HEMATOWN.\\nClimb all the way up.")
add(1, F, "FLAG_SEAFOAM_BOSS_DONE", 0, "SEAFOAM VOLCANO", "Sail from GRENALUX to the SEAFOAM\\nVOLCANO once CHRONDROLIA is safe.")
add(1, F, "FLAG_VR_BOSS_DONE", 0, "VICTORY ROAD", "Beat the ONYBRIS guards inside\\nVICTORY ROAD (ROUTE 23).")
add(1, F, "FLAG_SYS_GAME_CLEAR", 0, "POKéMON LEAGUE", "Win the LEAGUE tournament at the\\nINDIGO PLATEAU (needs 8 BADGES).")
add(1, F, "FLAG_TOPAZE_POSTGAME", 0, "THE FINAL CHOICE", "Face the BOSS after the tournament\\nand decide JIRACHI's fate.")
# 2 SIDE QUESTS
add(2, F, "FLAG_GOT_POKE_RADAR", 0, "THE POKé RADAR", "Get the RADAR from the aide in the\\nROUTE 2 east building. Use it from\\nthe START menu.")
add(2, F, "FLAG_GRENALUX_TYPE_COURSE", 0, "THE TYPE MEMO", "The GRENALUX teacher has a type\\ncourse for you.")
add(2, F, "FLAG_ONYBRIS_ANIMALS_FOUND", 0, "STRAYED ANIMALS", "Find the DODUO and 2 NIDORAN that\\nran off from the ranch (ROUTE 1).")
add(2, F, "FLAG_VIRIDIAN_TUTORIAL_DONE", 0, "THE CATCH DEMO", "The old man in OPANIHRUM shows how\\nto catch a POKéMON.")
for fl, town in [("PEWTER", "PYROPIA"), ("CERULEAN", "TOURMALIA"), ("VERMILION", "APATIA"), ("LAVENDER", "SPINELLIA"), ("FUCHSIA", "AMETHIOLITE")]:
    add(2, F, "FLAG_TOPAZE_CELL_" + fl, 0, "CELL: " + town, "Hidden ONYBRIS cell in %s.\\nClear it and read the memo." % town)
add(2, F, "FLAG_TOPAZE_LEDGER_CELADON", 0, "QUARTZ LEDGER", "Find the account book in the lair\\nunder the GAME CORNER (QUARTZ).")
# 3 POST-GAME
add(3, V, "VAR_ELDERS_ROUND", 20, "COUNCIL OF ELDERS", "At the LEAGUE: 20 veterans wait in\\nthe first hall. Beat them all.")
add(3, F, "FLAG_TOPAZE_GOT_TICKETS", 0, "FERRY TICKETS", "Talk to the sailor at the ferry\\nin APATIA for the old tickets.")
add(3, F, "FLAG_GOT_HM06", 0, "ROCK SMASH", "The man in the EMBER SPA (KINDLE\\nROAD, ONE ISLAND) gives ROCK SMASH.")
add(3, T, "TRAINER_TEAM_ROCKET_GRUNT_44", 0, "MT. EMBER GUARDS", "Two guards watch the ruby cave at\\nMT. EMBER (ONE ISLAND). Beat them.")
add(3, F, "FLAG_TOPAZE_RUBY_GIVEN", 0, "THE RUBY", "Find the RUBY at the bottom of the\\nRUBY PATH (MT. EMBER), give it to\\nCELIO in ONE ISLAND.")
add(3, F, "FLAG_LEARNED_YES_NAH_CHANSEY", 0, "CHANSEY PASSWORD", "In the DOTTED HOLE (SIX ISLAND),\\nreach the SAPPHIRE room: a thief\\nreveals the warehouse password.")
add(3, F, "FLAG_DEFEATED_ROCKETS_IN_WAREHOUSE", 0, "ROCKET WAREHOUSE", "MEADOW (FIVE ISLAND): use password\\nat the warehouse door, clear it\\nand win back the SAPPHIRE.")
add(3, F, "FLAG_TOPAZE_SAPPHIRE_GIVEN", 0, "THE SAPPHIRE", "Give the SAPPHIRE to CELIO (ONE\\nISLAND) to start the NETWORK\\nMACHINE.")
# 4 ECHOES
for fl, nm, hint in [
    ("FLAG_ECHO_BEAST_DONE", "RAIKOU", "RAIKOU. Go north of the town on\\nONE ISLAND: KINDLE ROAD."),
    ("FLAG_ECHO_BEAST2_DONE", "ENTEI", "ENTEI. Go to CAPE BRINK on\\nTWO ISLAND."),
    ("FLAG_ECHO_BEAST3_DONE", "SUICUNE", "SUICUNE. Cross the BOND BRIDGE\\non THREE ISLAND."),
    ("FLAG_ECHO_BEAST4_DONE", "REGICE", "REGICE. ICEFALL CAVE on FOUR\\nISLAND, to the very back."),
    ("FLAG_ECHO_BEAST5_DONE", "REGISTEEL", "REGISTEEL. The MEADOW on\\nFIVE ISLAND."),
    ("FLAG_ECHO_BEAST6_DONE", "REGIROCK", "REGIROCK. RUIN VALLEY on\\nSIX ISLAND."),
    ("FLAG_DONE_ECHO_CELEBI", "CELEBI", "CELEBI. SEVAULT CANYON on\\nSEVEN ISLAND (the mossy cave).")]:
    add(4, F, fl, 0, nm, hint + "\\nEach ECHO opens after the last one.")
add(4, V, "VAR_ECHO_STAGE", 22, "THE SUMMIT", "SEVAULT CANYON, SEVEN ISLAND:\\nclimb to the north cave, to the top\\nSILVER and GIOVANNI wait there.")
# 5 LEGENDS
for fl, nm in [("KYOGRE", "KYOGRE"), ("GROUDON", "GROUDON"), ("RAYQUAZA", "RAYQUAZA"), ("LATIAS", "LATIAS"), ("LATIOS", "LATIOS"), ("JIRACHI", "JIRACHI")]:
    add(5, F, "FLAG_DONE_ECHO_" + fl, 0, nm, "%s rests in the legends cave,\\nat the top of SEVAULT CANYON.\\nOpens once the summit is cleared." % nm)
add(5, T, "TRAINER_BIKER_1", 0, "RED, THE SUMMIT", "RED trains at the very top of the\\nSEVAULT summit. Talk to him for a\\n1-on-1: the hardest fight of all.")
# 6 RARE
add(6, F, "FLAG_FOUGHT_ARTICUNO", 0, "ARTICUNO", "It sleeps in a quartz clearing\\nbehind a tree near BOURG QUARTZ.")
add(6, F, "FLAG_FOUGHT_ZAPDOS", 0, "ZAPDOS", "The POWER PLANT, ROUTE 10. Four\\nchannelers ring it: beat them all.")
add(6, F, "FLAG_FOUGHT_MOLTRES", 0, "MOLTRES", "MT. EMBER summit, ONE ISLAND.\\nNeeds ROCK SMASH and STRENGTH.")
add(6, F, "FLAG_FOUGHT_MEWTWO", 0, "MEWTWO", "CERULEAN CAVE (TOURMALIA), the\\nvery bottom.")
add(6, F, "FLAG_FOUGHT_MEW_TRUCK", 0, "MEW", "A strange truck is parked near the\\nAPATIA docks.")

assert len(SECTIONS) <= 8
for e in E:
    lines = e[5].split("\\n")
    assert len(lines) <= 3, (e[4], len(lines))
    for line in lines:
        assert len(line) <= 35, (line, len(line))
    assert len(e[4]) <= 24, e[4]
out = ["// GENERE par docs/topaze/journal_gen.py - ne pas editer a la main", ""]
for k, (n, g) in enumerate(SECTIONS):
    out.append('static const u8 sJS_%d[] = _("%s");' % (k, n))
for k, (sec, kd, i2, v, nm, h) in enumerate(E):
    out.append('static const u8 sJN_%d[] = _("%s");' % (k, nm))
    out.append('static const u8 sJH_%d[] = _("%s");' % (k, h))
out.append("")
out.append("static const struct TopazeJournalSection sJournalSections[] = {")
for k, (n, g) in enumerate(SECTIONS):
    out.append('    { sJS_%d, %s },' % (k, g or "0"))
out.append("};\n")
out.append("static const struct TopazeJournalEntry sJournalEntries[] = {")
for k, (sec, kd, i2, v, nm, h) in enumerate(E):
    out.append('    { %d, %d, %s, %d, sJN_%d, sJH_%d },' % (sec, kd, i2, v, k, k))
out.append("};")
open("src/data/topaze_journal.h", "w").write("\n".join(out) + "\n")
print(len(E), "entries")
