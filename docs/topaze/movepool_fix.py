#!/usr/bin/env python3
"""Mise a niveau des movepools : (1) echelle de STAB par type (precoce / intermediaire / puissant) pour chaque espece selon ses types ACTUELS,
(2) signatures modernes (Gen 4+) pour les especes emblematiques, (3) propagation aux evolutions, le tout dans la limite de 24 entrees.
Usage : python3 docs/topaze/movepool_fix.py <depot>. Idempotent."""
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
def hh(*a): return zlib.crc32('|'.join(a).encode())
CAP = 24
added = {}   # espece -> [(lvl, move)]
def room(n):
    return len(ents[ptr[n]]) < CAP
def drop_weak(n, keep_types):
    """libere une place : retire l'attaque offensive la plus faible hors STAB (puissance < 45), jamais une attaque apprise au-dela du niveau 1 si utile."""
    e = ents[ptr[n]]
    c = [(mv[m]['power'], i) for i, (l, m) in enumerate(e) if m in mv and 0 < mv[m]['power'] < 45 and mv[m]['type'] not in keep_types and m not in ('HIDDEN_POWER','RETURN','FRUSTRATION','SELF_DESTRUCT')]
    if not c: return False
    e.pop(min(c)[1]); return True
def add(n, move, lvl, tag=''):
    if move not in mv or n not in sp or ptr.get(n) is None: return False
    e = ents[ptr[n]]
    if any(m == move for _, m in e): return False
    if not room(n) and not drop_weak(n, set(sp[n]['types'])): return False
    e.append((max(1, min(lvl, 95)), move)); added.setdefault(n, []).append((lvl, move)); return True
def known(n):
    return {m for _, m in ents[ptr[n]]} | set(learn[n]['tm'])
# ---------- (1) echelle de STAB
top = {}
for t in {m['type'] for m in mv.values()}:
    top[t] = sorted([m['power'] for m in mv.values() if m['type'] == t and m['power'] > 1], reverse=True)
def pick(n, ty, lo, hi, lvl, phys):
    have = known(n)
    c = [m for m, i in mv.items() if i['type'] == ty and lo <= i['power'] <= hi and m not in have and i['effect'] not in ('EXPLOSION','OHKO','RAMPAGE','SKY_ATTACK','RAZOR_WIND','SOLAR_BEAM','SKULL_BASH','FUTURE_SIGHT','BIDE','COUNTER','MIRROR_COAT','ROLLOUT','FURY_CUTTER','TRIPLE_KICK','MAGNITUDE','FLAIL','ERUPTION','WEATHER_BALL','FOCUS_PUNCH','ENDEAVOR','SPIT_UP','LOW_KICK','HIDDEN_POWER','RETURN','FRUSTRATION','PRESENT','PSYWAVE','BEAT_UP','REVENGE','SMELLINGSALT','SNORE','FACADE','UPROAR','LEVEL_DAMAGE','SONICBOOM','DRAGON_RAGE','SUPER_FANG')]
    if not c: return None
    c.sort(key=lambda m: (mv[m]['phys'] != phys, hh(n, m)))
    return c[0]
for n, s in sp.items():
    if n.startswith('UNOWN') or n == 'EGG' or ptr.get(n) is None or s['bst'] < 150: continue
    if n in ('METAPOD', 'KAKUNA', 'SILCOON', 'CASCOON', 'DITTO', 'SMEARGLE', 'WYNAUT', 'WOBBUFFET', 'SHEDINJA', 'UNOWN'): continue
    phys = s['atk'] >= s['spa']
    for t in s['types']:
        if t in ('NORMAL', 'MYSTERY'): continue
        def has(pw, lvmax):
            return any(m in mv and mv[m]['type'] == t and mv[m]['power'] >= pw and l <= lvmax for l, m in ents[ptr[n]]) or any(m in mv and mv[m]['type'] == t and mv[m]['power'] >= pw for m in learn[n]['tm'])
        st = s['stage']
        if not has(35, 25):
            m = pick(n, t, 35, 65, 0, phys)
            if m: add(n, m, (10 if st == 0 else 18) + hh(n, t) % 5)
        if (st >= 1 or s['final']) and not has(60, 42):
            m = pick(n, t, 60, 95, 0, phys)
            if m: add(n, m, 28 + hh(n, t, 'b') % 8 + (0 if st >= 1 else 6))
        t3 = min(85, top[t][1] if len(top[t]) > 1 else 85)
        if s['final'] and s['bst'] >= 420 and not has(t3, 70):
            m = pick(n, t, t3, 150, 0, phys)
            if m: add(n, m, 44 + hh(n, t, 'c') % 10)
# ---------- (2) signatures modernes
SIG = '''
IVYSAUR:SEED_BOMB:26|VENUSAUR:EARTH_POWER:42|VENUSAUR:ENERGY_BALL:36|VENUSAUR:WOOD_HAMMER:50|VENUSAUR:BULLDOZE:30
CHARMELEON:FIRE_FANG:24|CHARMELEON:ICE_FANG:28|CHARIZARD:FLARE_BLITZ:46|CHARIZARD:FROST_BREATH:34|CHARIZARD:ICICLE_CRASH:52|CHARIZARD:DRAGON_TAIL:40
WARTORTLE:AQUA_JET:24|WARTORTLE:IRON_HEAD:30|BLASTOISE:FLASH_CANNON:40|BLASTOISE:GYRO_BALL:34|BLASTOISE:AQUA_TAIL:46
PIKACHU:NUZZLE:10|PIKACHU:SHADOW_SNEAK:18|PIKACHU:HEX:28|RAICHU:DISCHARGE:32|RAICHU:WILD_CHARGE:44|RAICHU:SHADOW_CLAW:36
CLEFABLE:MOONBLAST:44|CLEFABLE:DAZZLING_GLEAM:36|CLEFAIRY:DRAINING_KISS:18|WIGGLYTUFF:PLAY_ROUGH:40|JIGGLYPUFF:FAIRY_WIND:14
GENGAR:DARK_PULSE:38|GENGAR:SHADOW_CLAW:26|GENGAR:HEX:22|GENGAR:VENOSHOCK:30|GASTLY:HEX:20
ALAKAZAM:ZEN_HEADBUTT:30|ALAKAZAM:AURA_SPHERE:50|MACHAMP:DRAIN_PUNCH:36|MACHAMP:STONE_EDGE:50|MACHOKE:DRAIN_PUNCH:34
ARCANINE:FLARE_BLITZ:44|ARCANINE:FIRE_FANG:22|ARCANINE:THUNDER_FANG:30|ARCANINE:WILD_CHARGE:50|GROWLITHE:FIRE_FANG:20
GYARADOS:AQUA_TAIL:34|GYARADOS:DRAGON_PULSE:40|GYARADOS:ICE_FANG:28|GYARADOS:DRAGON_TAIL:46|GYARADOS:HURRICANE:60
DRAGONITE:DRAGON_PULSE:50|DRAGONITE:DRAGON_RUSH:56|DRAGONITE:HURRICANE:64|DRAGONITE:AQUA_TAIL:44|DRAGONAIR:DRAGON_TAIL:36|DRATINI:DRAGON_TAIL:30
ARTICUNO:HURRICANE:61|ARTICUNO:FREEZE_DRY:50|ARTICUNO:AIR_SLASH:36|ZAPDOS:HURRICANE:61|ZAPDOS:DISCHARGE:55|ZAPDOS:AIR_SLASH:36
MOLTRES:HURRICANE:61|MOLTRES:LAVA_PLUME:46|MOLTRES:SEARING_SHOT:57|MOLTRES:AIR_SLASH:36
MEWTWO:AURA_SPHERE:55|MEWTWO:ZEN_HEADBUTT:30|MEW:AURA_SPHERE:55|MEW:DRAINING_KISS:40|MEW:ENERGY_BALL:60
TYRANITAR:STONE_EDGE:54|TYRANITAR:DARK_PULSE:58|TYRANITAR:IRON_HEAD:44|TYRANITAR:DRAGON_TAIL:50|PUPITAR:ROCK_POLISH:36
SCIZOR:X_SCISSOR:33|SCIZOR:BULLET_PUNCH:11|SCIZOR:IRON_HEAD:48|SCIZOR:U_TURN:26|SCYTHER:X_SCISSOR:33|SCYTHER:AIR_SLASH:40|SCYTHER:U_TURN:24
HERACROSS:X_SCISSOR:34|HERACROSS:DRAIN_PUNCH:42|HERACROSS:ROCK_POLISH:20|PINSIR:X_SCISSOR:30|PINSIR:LUNGE:40
SNEASEL:NIGHT_SLASH:36|SNEASEL:ICICLE_CRASH:44|SNEASEL:FOUL_PLAY:40|UMBREON:DARK_PULSE:46|UMBREON:FOUL_PLAY:50
ESPEON:ZEN_HEADBUTT:34|ESPEON:DAZZLING_GLEAM:50|VAPOREON:SCALD:36|VAPOREON:AQUA_JET:28|JOLTEON:DISCHARGE:42|JOLTEON:THUNDER_FANG:34|FLAREON:FLARE_BLITZ:44|FLAREON:FIRE_FANG:30
SNORLAX:DRAIN_PUNCH:36|SNORLAX:ZEN_HEADBUTT:40|LAPRAS:SCALD:40|LAPRAS:ICICLE_CRASH:52|LAPRAS:DRAGON_PULSE:56|LAPRAS:FREEZE_DRY:48
STARMIE:SCALD:36|STARMIE:POWER_GEM:44|STARMIE:ENERGY_BALL:52|CHARIZARD:AIR_SLASH:38
ONIX:STONE_EDGE:46|STEELIX:IRON_HEAD:36|STEELIX:HEAD_SMASH:56|STEELIX:EARTH_POWER:50|STEELIX:GYRO_BALL:42
GOLEM:HEAD_SMASH:56|RHYDON:HEAD_SMASH:60|RHYDON:EARTH_POWER:50|DONPHAN:ICE_FANG:34|DONPHAN:HEAD_SMASH:56
MAGNEZONE:FLASH_CANNON:46|MAGNETON:FLASH_CANNON:40|MAGNETON:DISCHARGE:36|PORYGON2:DISCHARGE:36|PORYGON:DISCHARGE:32
GARDEVOIR:MOONBLAST:48|GARDEVOIR:DAZZLING_GLEAM:40|KIRLIA:DRAINING_KISS:24|BLISSEY:MOONBLAST:56|BLISSEY:DAZZLING_GLEAM:44|CHANSEY:DRAINING_KISS:30
AZUMARILL:PLAY_ROUGH:36|AZUMARILL:AQUA_JET:20|AZUMARILL:AQUA_TAIL:44|MARILL:AQUA_JET:18
BLAZIKEN:FLARE_BLITZ:50|BLAZIKEN:DRAIN_PUNCH:40|SWAMPERT:EARTH_POWER:48|SWAMPERT:AQUA_TAIL:44|SCEPTILE:LEAF_STORM:55|SCEPTILE:DRAGON_PULSE:44|SCEPTILE:ENERGY_BALL:42
SALAMENCE:DRAGON_RUSH:55|SALAMENCE:BRAVE_BIRD:62|SALAMENCE:DRAGON_PULSE:48|METAGROSS:IRON_HEAD:42|METAGROSS:ZEN_HEADBUTT:46|METAGROSS:BULLET_PUNCH:34
MILOTIC:SCALD:40|MILOTIC:DRAGON_PULSE:52|CRADILY:ENERGY_BALL:40|ARMALDO:X_SCISSOR:36|ARMALDO:STONE_EDGE:52
FLYGON:DRAGON_PULSE:40|FLYGON:EARTH_POWER:50|FLYGON:U_TURN:34|SWELLOW:BRAVE_BIRD:50|PIDGEOT:BRAVE_BIRD:56|PIDGEOT:AIR_SLASH:36|FEAROW:DRILL_RUN:40
CROBAT:AIR_SLASH:34|CROBAT:CROSS_POISON:30|GOLBAT:AIR_SLASH:28|ZUBAT:AIR_SLASH:30|NOCTOWL:AIR_SLASH:32|XATU:AIR_SLASH:36|XATU:ZEN_HEADBUTT:30
HOUNDOOM:DARK_PULSE:40|HOUNDOOM:FLARE_BLITZ:50|HOUNDOUR:FIRE_FANG:22|ENTEI:FLARE_BLITZ:52|SUICUNE:SCALD:40|RAIKOU:WILD_CHARGE:52|RAIKOU:DISCHARGE:44
LUGIA:AIR_SLASH:44|LUGIA:HURRICANE:66|HO_OH:FLARE_BLITZ:60|HO_OH:BRAVE_BIRD:54|CELEBI:LEAF_STORM:60|CELEBI:ENERGY_BALL:40
LATIAS:DRAGON_PULSE:40|LATIOS:DRAGON_PULSE:40|LATIAS:DAZZLING_GLEAM:60|KYOGRE:SCALD:50|GROUDON:EARTH_POWER:60|GROUDON:STONE_EDGE:56|RAYQUAZA:DRAGON_PULSE:50|RAYQUAZA:DRACO_METEOR:70
REGIROCK:STONE_EDGE:46|REGIROCK:HEAD_SMASH:70|REGISTEEL:FLASH_CANNON:46|REGISTEEL:IRON_HEAD:30|REGICE:FREEZE_DRY:46
DEOXYS:PSYCHIC:55|SHIFTRY:DARK_PULSE:46|MIGHTYENA:CRUNCH:30|ABSOL:NIGHT_SLASH:36|ABSOL:FOUL_PLAY:52|SABLEYE:SHADOW_CLAW:26|SABLEYE:POWER_GEM:34|MAWILE:PLAY_ROUGH:28|MAWILE:IRON_HEAD:32
LEDIAN:AIR_SLASH:36|BEAUTIFLY:AIR_SLASH:36|WURMPLE:LUNGE:15|BANETTE:SHADOW_CLAW:30|BANETTE:HEX:40|DUSKNOIR:SHADOW_SNEAK:24|MISDREAVUS:HEX:30|MISMAGIUS:HEX:30|SHEDINJA:SHADOW_SNEAK:20|SHEDINJA:X_SCISSOR:30
'''
for chunk in SIG.replace('\n', '|').split('|'):
    if not chunk.strip(): continue
    n, m, l = chunk.split(':')
    add(n, m, int(l))
# ---------- (3) propagation aux evolutions : une evolution apprend ce que son stade precedent a gagne ici
for n in list(added):
    for e in sp[n]['evo']:
        for lvl, m in added[n]:
            add(e, m, lvl)
# ---------- ecriture (tri par niveau, stable)
for var, e in ents.items():
    e.sort(key=lambda x: x[0])
    m = re.search(r'(static const u16 %s\[\] = \{\n)(.*?)(    LEVEL_UP_END)' % var, L, re.S)
    if not m: continue
    body = ''.join('    LEVEL_UP_MOVE(%d, MOVE_%s),\n' % (l, mm) for l, mm in e)
    L = L[:m.start(2)] + body + L[m.end(2):]
open(LEARN_PATH, 'w').write(L)
print('especes modifiees :', len(added), '| attaques ajoutees :', sum(len(v) for v in added.values()))
