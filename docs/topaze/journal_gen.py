#!/usr/bin/env python3
"""Genere src/data/topaze_journal.h : le JOURNAL (menu Start) = succes tries par sections.
kind  : F flag / V var>=val / T dresseur battu / S stat>=val (compteur) / D especes capturees>=val (compteur)
vis   : quand l'entree apparait (anti-spoil). Une entree terminee est toujours visible.
        A toujours | B(n) badges>=n | FL(flag) | VR(var,n) | PV(n) entree precedente finie (ou badges>=n si n>0)
Textes en anglais, 35 car. max par ligne, 3 lignes max."""
F, V, T, S, D = 0, 1, 2, 3, 4
SECTIONS = [  # (nom, drapeau de deblocage ou None) ; une section sans entree visible est masquee
    ("BADGES", None), ("STORY", None), ("SIDE QUESTS", None), ("GIFTS", None),
    ("BATTLE", None), ("COLLECTION", None), ("JOURNEY", None),
    ("POST-GAME", "FLAG_TOPAZE_POSTGAME"), ("ECHOES", "FLAG_TOPAZE_POSTGAME"),
    ("LEGENDS", None), ("RARE POKéMON", None),
]
SEC = {n: i for i, (n, _) in enumerate(SECTIONS)}
A = ("A", "0", 0)
def B(n): return ("B", "0", n)
def FL(f): return ("F", f, 0)
def VR(v, n): return ("V", v, n)
def PV(n=0): return ("P", "0", n)
VK = {"A": 0, "B": 1, "F": 2, "V": 3, "P": 4}
E = []
def add(sec, kind, ident, val, name, hint, vis=A, alt=("0", "0")):
    # alt = ("F"|"I", id) : autre condition qui vaut "fait" (flag / objet en sac)
    E.append([SEC[sec], kind, ident, val, name, hint, vis, 0, alt])
def tiers(sec, kind, ident, items):
    """items = [(val, name, hint)] ; le premier est visible d'emblee, les suivants apres le palier precedent"""
    for k, (val, name, hint) in enumerate(items):
        add(sec, kind, ident, val, name, hint, A if k == 0 else PV())

# ---- BADGES
for i, (nm, town, boss) in enumerate([
    ("KAY", "PYROPIA", "Fire"), ("SYLVESTRE", "TOURMALIA", "Bug / Grass"), ("HERA", "APATIA", "Dragon / Fairy"),
    ("GRIM", "BOURG QUARTZ", "Ice"), ("ACHLYS", "AMETHIOLITE", "Poison"), ("NOX", "HEMATOWN", "Dark"),
    ("EDDIE", "CHRONDROLIA", "Electric"), ("HEPHA", "OPANIHRUM", "Steel")], 1):
    add("BADGES", F, "FLAG_BADGE0%d_GET" % i, 0, "%s, %s" % (nm, town),
        "BADGE %d. Beat %s in\\n%s. %s specialist." % (i, nm, town, boss), A if i == 1 else PV())

# ---- STORY (chaine ; repli par nombre de badges si un maillon est saute)
add("STORY", F, "FLAG_GRENALUX_ONYBRIS_STRIKE", 0, "THE RANCH ATTACK", "ONYBRIS strikes GRENALUX. Beat the\\ngrunt on the road out of town.")
add("STORY", F, "FLAG_PIER_KRONOS_DONE", 0, "THE APATIA PIER", "Reach the harbor of APATIA in time\\nto save the APATITE.", PV(2))
add("STORY", F, "FLAG_RESCUED_MR_FUJI", 0, "SPINELLIA TOWER", "Calm the spirits of the TOWER in\\nSPINELLIA and find FUJI.", PV(3))
add("STORY", F, "FLAG_QUARTZ_DUEL_DONE", 0, "THE QUARTZ DUEL", "Clear the hideout under the GAME\\nCORNER, then play the casino duel.", PV(3))
add("STORY", F, "FLAG_AMETHYST_RAID_DONE", 0, "AMETHIOLITE RAID", "Help repel the ONYBRIS raid on\\nAMETHIOLITE.", PV(4))
add("STORY", F, "FLAG_HEMATEK_BOSS_DONE", 0, "HEMATEK TOWER", "Storm the ONYBRIS HQ in HEMATOWN.\\nClimb all the way up.", PV(5))
add("STORY", F, "FLAG_SEAFOAM_BOSS_DONE", 0, "SEAFOAM VOLCANO", "Sail from GRENALUX to the SEAFOAM\\nVOLCANO once CHRONDROLIA is safe.", PV(6))
add("STORY", F, "FLAG_VR_BOSS_DONE", 0, "VICTORY ROAD", "Beat the ONYBRIS guards inside\\nVICTORY ROAD (ROUTE 23).", PV(8))
add("STORY", F, "FLAG_SYS_GAME_CLEAR", 0, "POKéMON LEAGUE", "Win the LEAGUE tournament at the\\nINDIGO PLATEAU (needs 8 BADGES).", PV(8))
add("STORY", F, "FLAG_TOPAZE_POSTGAME", 0, "THE FINAL CHOICE", "Face the BOSS after the tournament\\nand decide JIRACHI's fate.", PV())

# ---- SIDE QUESTS (apparaissent avec la progression)
add("SIDE QUESTS", F, "FLAG_GOT_POKE_RADAR", 0, "THE POKé RADAR", "The MOVE COACH in a POKéMON CENTER\\nhas a gift for trainers. Use it\\nfrom the START menu.", B(1), ("I", "ITEM_10B"))
add("SIDE QUESTS", F, "FLAG_GRENALUX_TYPE_COURSE", 0, "THE TYPE MEMO", "The GRENALUX teacher has a type\\ncourse for you.", B(1))
add("SIDE QUESTS", F, "FLAG_GRENALUX_GEM_REWARD", 0, "RANCH REWARD", "Once the animals are home, talk to\\nthe ranch worker by the fence.", FL("FLAG_ONYBRIS_ANIMALS_FOUND"))
add("SIDE QUESTS", F, "FLAG_ONYBRIS_ANIMALS_FOUND", 0, "STRAYED ANIMALS", "Find the DODUO and 2 NIDORAN that\\nran off from the ranch (ROUTE 1).", FL("FLAG_GRENALUX_ONYBRIS_STRIKE"))
add("SIDE QUESTS", F, "FLAG_VIRIDIAN_TUTORIAL_DONE", 0, "THE CATCH DEMO", "The old man in OPANIHRUM shows how\\nto catch a POKéMON.", B(7))
for n, (fl, town) in zip([1, 2, 3, 3, 5], [("PEWTER", "PYROPIA"), ("CERULEAN", "TOURMALIA"), ("VERMILION", "APATIA"), ("LAVENDER", "SPINELLIA"), ("FUCHSIA", "AMETHIOLITE")]):
    add("SIDE QUESTS", F, "FLAG_TOPAZE_CELL_" + fl, 0, "CELL: " + town, "Hidden ONYBRIS cell in %s.\\nClear it and read the memo." % town, B(n))
add("SIDE QUESTS", F, "FLAG_TOPAZE_LEDGER_CELADON", 0, "QUARTZ LEDGER", "Find the account book in the lair\\nunder the GAME CORNER (QUARTZ).", B(4))

# ---- GIFTS (cadeaux de PNJ)
for fl, nm, hint, n in [
    ("FLAG_GOT_OLD_ROD", "THE OLD ROD", "Somebody hands out a fishing rod\\nto a beginner angler.", 1),
    ("FLAG_GOT_BICYCLE", "A BIKE FOR YOU", "A bike shop owner is generous with\\nthe right paperwork.", 1),
    ("FLAG_GOT_HM01", "A HELPFUL CUT", "A captain has a way to cut through\\nthe trees. Find him.", 1),
    ("FLAG_GOT_ITEMFINDER", "THE ITEMFINDER", "A man guarding a gate will give\\nyou an ITEMFINDER.", 2),
    ("FLAG_GOT_COIN_CASE", "THE COIN CASE", "A restaurant owner hands out a\\nCOIN CASE.", 3),
    ("FLAG_GOT_GOOD_ROD", "THE GOOD ROD", "A fisherman has a better rod for\\nyou if you ask kindly.", 3),
    ("FLAG_GOT_HM04", "STRENGTH TRAINING", "A retired warden wants his teeth\\nback. In return: STRENGTH.", 4),
    ("FLAG_GOT_POKE_FLUTE", "THE POKé FLUTE", "A radio man rewards you for tuning\\nthe tower, then hands you a FLUTE.", 4),
    ("FLAG_GOT_HM02", "SPREAD YOUR WINGS", "A house on a long road teaches\\nthe art of flying.", 5),
    ("FLAG_GOT_SUPER_ROD", "THE SUPER ROD", "The fishing guru lives in a house\\nby the water. Impress him.", 5),
    ("FLAG_GOT_LAPRAS_FROM_SILPH", "A GIFT FROM SILPH", "A grateful employee gives you a\\nrare POKéMON.", 6),
    ("FLAG_GOT_HITMON_FROM_DOJO", "DOJO PRIZE", "Win the fighting dojo duel and pick\\nyour prize.", 6),
    ("FLAG_GOT_EEVEE", "A FRIEND ON THE ROOF", "Somebody on a rooftop is offering a\\nPOKé BALL.", 5),
    ("FLAG_GOT_FOSSIL_FROM_MT_MOON", "ANCIENT TREASURE", "Pick a fossil in the mountain cave.\\nA scientist will bring it to life.", 2)]:
    add("GIFTS", F, fl, 0, nm, hint, B(n))

# ---- BATTLE (compteurs)
tiers("BATTLE", S, "GAME_STAT_BATTLES_WON", [
    (10, "GETTING STARTED", "Win 10 battles."), (50, "ON A ROLL", "Win 50 battles."),
    (100, "SEASONED FIGHTER", "Win 100 battles."), (250, "VETERAN", "Win 250 battles."),
    (500, "WAR MACHINE", "Win 500 battles."), (1000, "LIVING LEGEND", "Win 1000 battles.")])
tiers("BATTLE", S, "GAME_STAT_TRAINERS_BEATEN", [
    (5, "CHALLENGER", "Defeat 5 trainers."), (25, "RIVAL CRUSHER", "Defeat 25 trainers."),
    (75, "DOJO MASTER", "Defeat 75 trainers."), (150, "UNDEFEATED", "Defeat 150 trainers."),
    (300, "TRAINER TERROR", "Defeat 300 trainers.")])
tiers("BATTLE", S, "GAME_STAT_CRITS_DEALT", [
    (1, "LUCKY STRIKE", "Land a critical hit."), (25, "SHARP EYE", "Land 25 critical hits."),
    (100, "CRITICAL MASS", "Land 100 critical hits."), (300, "HEADHUNTER", "Land 300 critical hits."),
    (750, "PURE PRECISION", "Land 750 critical hits.")])
tiers("BATTLE", S, "GAME_STAT_EVOLVED_POKEMON", [
    (1, "FIRST EVOLUTION", "Evolve a POKéMON."), (10, "EVOLUTION FAN", "Evolve 10 POKéMON."),
    (30, "NATURAL SELECTION", "Evolve 30 POKéMON.")])

# ---- COLLECTION (captures, shiny, pokedex...)
tiers("COLLECTION", S, "GAME_STAT_POKEMON_CAPTURES", [
    (1, "FIRST CATCH", "Catch a wild POKéMON."), (25, "COLLECTOR", "Catch 25 POKéMON."),
    (100, "BALL THROWER", "Catch 100 POKéMON."), (250, "SAFARI KING", "Catch 250 POKéMON."),
    (500, "GOTTA CATCH EM ALL", "Catch 500 POKéMON.")])
tiers("COLLECTION", D, "0", [
    (10, "POKéDEX ROOKIE", "Own 10 different species."), (25, "POKéDEX STUDENT", "Own 25 different species."),
    (50, "POKéDEX FAN", "Own 50 different species."), (100, "POKéDEX EXPERT", "Own 100 different species."),
    (150, "POKéDEX PROFESSOR", "Own 150 different species.")])
tiers("COLLECTION", S, "GAME_STAT_SHINIES_SEEN", [
    (1, "SPARKLE SPOTTED", "Meet a shiny POKéMON in the wild."), (5, "SHINY SPOTTER", "Meet 5 shiny POKéMON in the wild.")])
tiers("COLLECTION", S, "GAME_STAT_SHINIES_CAUGHT", [
    (1, "SHINY HUNTER", "Catch a shiny POKéMON."), (3, "SHINY COLLECTOR", "Catch 3 shiny POKéMON."),
    (10, "SHINY MASTER", "Catch 10 shiny POKéMON.")])
tiers("COLLECTION", S, "GAME_STAT_FISHING_CAPTURES", [
    (1, "FIRST BITE", "Catch a POKéMON with a rod."), (10, "ANGLER", "Reel in 10 POKéMON."),
    (30, "SEA DOG", "Reel in 30 POKéMON.")])
tiers("COLLECTION", S, "GAME_STAT_HATCHED_EGGS", [
    (1, "EGG HATCHER", "Hatch an EGG."), (10, "NURSERY STAR", "Hatch 10 EGGS.")])
add("COLLECTION", S, "GAME_STAT_POKEMON_TRADES", 1, "SWAP MEET", "Trade a POKéMON with someone.")

# ---- JOURNEY
tiers("JOURNEY", S, "GAME_STAT_STEPS", [
    (1000, "FIRST STEPS", "Walk 1000 steps."), (10000, "WANDERER", "Walk 10000 steps."),
    (50000, "MARATHON", "Walk 50000 steps."), (100000, "GLOBETROTTER", "Walk 100000 steps.")])
tiers("JOURNEY", S, "GAME_STAT_USED_CUT", [(10, "LUMBERJACK", "Cut down 10 trees."), (50, "FOREST FELLER", "Cut down 50 trees.")])
tiers("JOURNEY", S, "GAME_STAT_USED_ROCK_SMASH", [(10, "ROCK BREAKER", "Smash 10 rocks."), (40, "QUARRYMAN", "Smash 40 rocks.")])
add("JOURNEY", S, "GAME_STAT_JUMPED_DOWN_LEDGES", 50, "LEAP OF FAITH", "Hop down 50 ledges.")
add("JOURNEY", S, "GAME_STAT_GOT_RAINED_ON", 20, "SINGING IN THE RAIN", "Get caught in the rain 20 times.")
add("JOURNEY", S, "GAME_STAT_SHOPPED", 20, "BIG SPENDER", "Shop at a POKé MART 20 times.")
add("JOURNEY", S, "GAME_STAT_SAVED_GAME", 10, "CAREFUL PLAYER", "Save your game 10 times.")
add("JOURNEY", S, "GAME_STAT_USED_ITEMFINDER", 10, "TREASURE HUNTER", "Use the ITEMFINDER 10 times.", FL("FLAG_GOT_ITEMFINDER"))

# ---- POST-GAME (section ouverte apres la fin ; le reste se devoile en chaine)
add("POST-GAME", V, "VAR_ELDERS_ROUND", 20, "COUNCIL OF ELDERS", "At the LEAGUE: 20 veterans wait in\\nthe first hall. Beat them all.")
add("POST-GAME", F, "FLAG_TOPAZE_GOT_TICKETS", 0, "FERRY TICKETS", "Talk to the sailor at the ferry\\nin APATIA for the old tickets.", PV())
add("POST-GAME", F, "FLAG_GOT_HM06", 0, "ROCK SMASH", "The man in the EMBER SPA (KINDLE\\nROAD, ONE ISLAND) gives ROCK SMASH.", PV())
add("POST-GAME", T, "TRAINER_TEAM_ROCKET_GRUNT_44", 0, "MT. EMBER GUARDS", "Two guards watch the ruby cave at\\nMT. EMBER (ONE ISLAND). Beat them.", PV())
add("POST-GAME", F, "FLAG_TOPAZE_RUBY_GIVEN", 0, "THE RUBY", "Find the RUBY at the bottom of the\\nRUBY PATH (MT. EMBER), give it to\\nCELIO in ONE ISLAND.", PV())
add("POST-GAME", F, "FLAG_LEARNED_YES_NAH_CHANSEY", 0, "CHANSEY PASSWORD", "In the DOTTED HOLE (SIX ISLAND),\\nreach the SAPPHIRE room: a thief\\nreveals the warehouse password.", PV())
add("POST-GAME", F, "FLAG_DEFEATED_ROCKETS_IN_WAREHOUSE", 0, "ROCKET WAREHOUSE", "MEADOW (FIVE ISLAND): use password\\nat the warehouse door, clear it\\nand win back the SAPPHIRE.", PV())
add("POST-GAME", F, "FLAG_TOPAZE_SAPPHIRE_GIVEN", 0, "THE SAPPHIRE", "Give the SAPPHIRE to CELIO (ONE\\nISLAND) to start the NETWORK\\nMACHINE.", PV())

add("POST-GAME", F, "FLAG_POSTGAME_DONE", 0, "THE FINAL TEST", "BASIL waits beside MEWTWO, deep in\\nCERULEAN CAVE. The hardest 1-on-1.", VR("VAR_ECHO_STAGE", 22))

# ---- ECHOES (chaine)
for k, (fl, nm, hint) in enumerate([
    ("FLAG_ECHO_BEAST_DONE", "RAIKOU", "RAIKOU. Go north of the town on\\nONE ISLAND: KINDLE ROAD."),
    ("FLAG_ECHO_BEAST2_DONE", "ENTEI", "ENTEI. Go to CAPE BRINK on\\nTWO ISLAND."),
    ("FLAG_ECHO_BEAST3_DONE", "SUICUNE", "SUICUNE. Cross the BOND BRIDGE\\non THREE ISLAND."),
    ("FLAG_ECHO_BEAST4_DONE", "REGICE", "REGICE. ICEFALL CAVE on FOUR\\nISLAND, to the very back."),
    ("FLAG_ECHO_BEAST5_DONE", "REGISTEEL", "REGISTEEL. The MEADOW on\\nFIVE ISLAND."),
    ("FLAG_ECHO_BEAST6_DONE", "REGIROCK", "REGIROCK. RUIN VALLEY on\\nSIX ISLAND."),
    ("FLAG_DONE_ECHO_CELEBI", "CELEBI", "CELEBI. SEVAULT CANYON on\\nSEVEN ISLAND (the mossy cave).")]):
    add("ECHOES", F, fl, 0, nm, hint + "\\nEach ECHO opens after the last one.", A if k == 0 else PV())
add("ECHOES", V, "VAR_ECHO_STAGE", 22, "THE SUMMIT", "SEVAULT CANYON, SEVEN ISLAND:\\nclimb to the north cave, to the top\\nSILVER and GIOVANNI wait there.", PV())

# ---- LEGENDS (visibles une fois le sommet franchi)
SUMMIT = VR("VAR_ECHO_STAGE", 22)
for fl, nm in [("KYOGRE", "KYOGRE"), ("GROUDON", "GROUDON"), ("RAYQUAZA", "RAYQUAZA"), ("LATIAS", "LATIAS"), ("LATIOS", "LATIOS"), ("JIRACHI", "JIRACHI")]:
    add("LEGENDS", F, "FLAG_DONE_ECHO_" + fl, 0, nm, "%s rests in the legends cave,\\nat the top of SEVAULT CANYON." % nm, SUMMIT)
add("LEGENDS", T, "TRAINER_BIKER_1", 0, "RED, THE SUMMIT", "RED trains at the very top of the\\nSEVAULT summit. Talk to him for a\\n1-on-1: the hardest fight of all.", SUMMIT)

# ---- RARE (apparaissent avec la progression)
add("RARE POKéMON", F, "FLAG_FOUGHT_ARTICUNO", 0, "ARTICUNO", "It sleeps in a quartz clearing\\nbehind a tree near BOURG QUARTZ.", B(4))
add("RARE POKéMON", F, "FLAG_FOUGHT_ZAPDOS", 0, "ZAPDOS", "The POWER PLANT, ROUTE 10. Four\\nchannelers ring it: beat them all.", B(5))
add("RARE POKéMON", F, "FLAG_FOUGHT_MOLTRES", 0, "MOLTRES", "MT. EMBER summit, ONE ISLAND.\\nNeeds ROCK SMASH and STRENGTH.", FL("FLAG_TOPAZE_POSTGAME"))
add("RARE POKéMON", F, "FLAG_FOUGHT_MEWTWO", 0, "MEWTWO", "TOURMALIA: follow the sand path in\\nthe NW forest to a hollow trunk.\\nCERULEAN CAVE, to the very bottom.", B(7))
add("RARE POKéMON", F, "FLAG_FOUGHT_MEW_TRUCK", 0, "MEW", "A strange truck is parked near the\\nAPATIA docks.", FL("FLAG_SYS_GAME_CLEAR"))

# une etape finie implique les precedentes de la meme chaine (sauts de scenes, anciennes sauvegardes)
for sec in ("BADGES", "STORY", "ECHOES"):
    idx = [i for i, e in enumerate(E) if e[0] == SEC[sec]]
    for i in idx[:-1]:
        E[i][7] = 1
assert len(SECTIONS) <= 12
for e in E:
    lines = e[5].split("\\n")
    assert len(lines) <= 3, (e[4], len(lines))
    for line in lines:
        assert len(line) <= 35, (line, len(line))
    assert len(e[4]) <= 24, (e[4], len(e[4]))
# longueur max d'une section visible (JOURNAL_MAX_ENTRIES)
from collections import Counter
mx = max(Counter(e[0] for e in E).values())
assert mx <= 40, mx
out = ["// GENERE par docs/topaze/journal_gen.py - ne pas editer a la main", ""]
for k, (n, g) in enumerate(SECTIONS):
    out.append('static const u8 sJS_%d[] = _("%s");' % (k, n))
for k, e in enumerate(E):
    out.append('static const u8 sJN_%d[] = _("%s");' % (k, e[4]))
    out.append('static const u8 sJH_%d[] = _("%s");' % (k, e[5]))
out.append("")
out.append("static const struct TopazeJournalSection sJournalSections[] = {")
for k, (n, g) in enumerate(SECTIONS):
    out.append('    { sJS_%d, %s },' % (k, g or "0"))
out.append("};\n")
out.append("static const struct TopazeJournalEntry sJournalEntries[] = {")
AK = {"0": 0, "F": 1, "I": 2}
for k, (sec, kd, i2, v, nm, h, vis, imp, alt) in enumerate(E):
    out.append('    { %d, %d, %d, %s, %d, %s, %d, %d, %d, %s, sJN_%d, sJH_%d },' % (sec, kd, VK[vis[0]], i2, v, vis[1], vis[2], imp, AK[alt[0]], alt[1], k, k))
out.append("};")
open("src/data/topaze_journal.h", "w").write("\n".join(out) + "\n")
print(len(E), "entries, max/section", mx)
