#!/usr/bin/env python3
"""Seconde passe des movepools avec les attaques Gen 4-9 (add_moves2.py) : signatures par role (setup, pieges, pivots, priorites,
recuperation), propagation aux evolutions, puis garde-fous (nombre d'attaques offensives, couverture).
A lancer APRES movepool_fix.py. Usage : python3 docs/topaze/movepool_fix2.py <depot>. Idempotent (n'ajoute que ce qui manque)."""
import re, sys, zlib
repo = sys.argv[1]
sys.path.insert(0, repo + '/docs/topaze')
from audit_movepool import load
sp, mv, learn = load(repo)
LEARN_PATH = repo + '/src/data/pokemon/level_up_learnsets.h'
L = open(LEARN_PATH).read()
ptr = dict(re.findall(r'\[SPECIES_(\w+)\] = (\w+),', open(repo + '/src/data/pokemon/level_up_learnset_pointers.h').read()))
ents = {}
for n in sp:
    var = ptr.get(n)
    if var and var not in ents: ents[var] = list(learn[n]['lv'])
CAP = 24
added = {}
unknown = set()
def hh(*a): return zlib.crc32('|'.join(a).encode())
def drop_weak(n, keep_types):
    e = ents[ptr[n]]
    c = [(mv[m]['power'], i) for i, (l, m) in enumerate(e) if m in mv and 0 < mv[m]['power'] < 45 and mv[m]['type'] not in keep_types
         and m not in ('HIDDEN_POWER', 'RETURN', 'FRUSTRATION', 'SELF_DESTRUCT', 'QUICK_ATTACK', 'MACH_PUNCH', 'AQUA_JET', 'ICE_SHARD', 'BULLET_PUNCH', 'SHADOW_SNEAK', 'SUCKER_PUNCH', 'ACCELEROCK', 'VACUUM_WAVE', 'JET_PUNCH', 'GRASSY_GLIDE', 'FAKE_OUT')]
    if not c: return False
    e.pop(min(c)[1]); return True
def drop_useless(n):
    """dernier recours : retire une attaque de statut tres peu utile."""
    e = ents[ptr[n]]
    junk = ('SPLASH', 'SWEET_SCENT', 'MUD_SPORT', 'WATER_SPORT', 'TICKLE', 'FLASH', 'KINESIS', 'FORESIGHT', 'ODOR_SLEUTH', 'MIND_READER', 'LOCK_ON', 'GRASS_WHISTLE', 'SMOKESCREEN', 'SAND_ATTACK', 'TAIL_WHIP', 'LEER', 'GROWL', 'STRING_SHOT', 'HARDEN', 'WITHDRAW', 'DEFENSE_CURL', 'FOCUS_ENERGY', 'POISON_GAS', 'SUPERSONIC', 'FLATTER', 'CHARM', 'SHARPEN', 'MINIMIZE', 'DOUBLE_TEAM', 'MIST', 'CAMOUFLAGE', 'COTTON_SPORE', 'SCARY_FACE', 'FAKE_TEARS', 'METAL_SOUND', 'SCREECH')
    for i, (l, m) in enumerate(e):
        if m in junk and l > 1:
            e.pop(i); return True
    return False
def add(n, move, lvl):
    if move not in mv: unknown.add(move); return False
    if n not in sp or ptr.get(n) is None: unknown.add(n); return False
    e = ents[ptr[n]]
    if any(m == move for _, m in e): return False
    if len(e) >= CAP and not drop_weak(n, set(sp[n]['types'])) and not drop_useless(n): return False
    e.append((max(1, min(lvl, 95)), move)); added.setdefault(n, []).append((lvl, move)); return True
SIG = '''
CHARIZARD:AIR_SLASH:46|CHARIZARD:DRAGON_PULSE:50|BLASTOISE:FLASH_CANNON:46|VENUSAUR:EARTH_POWER:46|VENUSAUR:GIGA_DRAIN:30
PIDGEOT:HEAT_WAVE:46|RATICATE:SWORDS_DANCE:36|RAICHU:ALLURING_VOICE:26|NINETALES:SCORCHING_SANDS:48|ARCANINE:RAGING_FURY:56
POLIWRATH:AXE_KICK:46|ALAKAZAM:PSYBLADE:50|MACHAMP:BODY_PRESS:44|MACHAMP:AXE_KICK:48|GOLEM:BODY_PRESS:44|GOLEM:HIGH_HORSEPOWER:46
RAPIDASH:PSYBLADE:50|CLOYSTER:SHELL_SIDE_ARM:50|DUGTRIO:THOUSAND_ARROWS:60|HITMONLEE:AXE_KICK:36|HITMONTOP:TRIPLE_AXEL:40|HITMONCHAN:HAMMER_ARM:40
LAPRAS:FREEZE_DRY:42|LAPRAS:HEAL_PULSE:30|SNORLAX:BODY_PRESS:42|SNORLAX:BELLY_DRUM:36|VAPOREON:HEAL_PULSE:44|FLAREON:RAGING_FURY:50|JOLTEON:ALLURING_VOICE:30
PORYGON:TECHNO_BLAST:56|DRAGONITE:MULTI_ATTACK:60|DRAGONITE:DRAGON_ENERGY:70|MEWTWO:PSYBLADE:60|MEWTWO:EXPANDING_FORCE:55|MEW:JUDGMENT:75
AERODACTYL:PRECIPICE_BLADES:60|OMASTAR:ARMOR_CANNON:60|KABUTOPS:AXE_KICK:46|ARTICUNO:GLACIAL_LANCE:70|MOLTRES:MAGMA_STORM:60|ZAPDOS:THUNDERCLAP:60
MEGANIUM:HEAL_PULSE:44|FERALIGATR:SUPERCELL_SLAM:56|TYPHLOSION:MAGMA_STORM:60|STEELIX:BODY_PRESS:46|STEELIX:STEEL_BEAM:56|SCIZOR:STEEL_BEAM:56|SCIZOR:AXE_KICK:46
HERACROSS:AXE_KICK:46|URSARING:AXE_KICK:46|URSARING:BODY_PRESS:44|GRANBULL:ALLURING_VOICE:26|SUICUNE:SHELL_SIDE_ARM:56|ENTEI:RAGING_FURY:56|RAIKOU:THUNDERCLAP:56
TYRANITAR:BODY_PRESS:46|TYRANITAR:PRECIPICE_BLADES:60|BLISSEY:HEAL_PULSE:36|UMBREON:SNARL:36|ESPEON:EXPANDING_FORCE:44|SNEASEL:AXE_KICK:36
BLAZIKEN:AXE_KICK:46|SWAMPERT:SUPERCELL_SLAM:56|SCEPTILE:LEAF_STORM:50|GARDEVOIR:ALLURING_VOICE:28|GALLADE:PSYBLADE:50|SALAMENCE:DRAGON_ENERGY:62
METAGROSS:BODY_PRESS:46|METAGROSS:STEEL_BEAM:56|FLYGON:DRAGON_PULSE:42|CRADILY:BODY_PRESS:40|ARMALDO:AXE_KICK:46|MILOTIC:HEAL_PULSE:44|MILOTIC:ALLURING_VOICE:30
LATIAS:HEAL_PULSE:40|LATIOS:PSYBLADE:55|KYOGRE:JUDGMENT:75|GROUDON:PRECIPICE_BLADES:60|RAYQUAZA:MULTI_ATTACK:70|RAYQUAZA:DRAGON_ENERGY:70
REGIROCK:BODY_PRESS:50|REGICE:GLACIAL_LANCE:60|REGISTEEL:STEEL_BEAM:56|REGISTEEL:BODY_PRESS:44|DEOXYS:PSYBLADE:60|JIRACHI:STEEL_BEAM:60|CELEBI:HEAL_PULSE:40
SHARPEDO:AXE_KICK:40|HARIYAMA:BODY_PRESS:40|SLAKING:BODY_PRESS:46|EXPLOUD:ALLURING_VOICE:30|SWELLOW:TRIPLE_AXEL:50|AGGRON:BODY_PRESS:46|AGGRON:STEEL_BEAM:60
'''
for chunk in SIG.replace('\n', '|').split('|'):
    if not chunk.strip(): continue
    n, m, l = chunk.split(':')
    add(n, m, int(l))
for n in list(added):
    for e in sp[n]['evo']:
        for lvl, m in added[n]:
            add(e, m, lvl)
# ---------- ecriture
for var, e in ents.items():
    e.sort(key=lambda x: x[0])
    m = re.search(r'(static const u(?:16|32) %s\[\] = \{\n)(.*?)(    LEVEL_UP_END)' % var, L, re.S)
    if not m: continue
    body = ''.join('    LEVEL_UP_MOVE(%d, MOVE_%s),\n' % (l, mm) for l, mm in e)
    L = L[:m.start(2)] + body + L[m.end(2):]
open(LEARN_PATH, 'w').write(L)
print('especes modifiees :', len(added), '| attaques ajoutees :', sum(len(v) for v in added.values()))
print('inconnus :', sorted(unknown))
