#!/usr/bin/env python3
"""Séparation physique/spéciale PAR ATTAQUE (style Gen 4+, comme CFRU). Usage : python3 docs/topaze/split_moves.py <dépôt>
Par défaut le moteur garde la règle Gen 3 (par type) ; ce script ajoute FLAG_FORCE_PHYSICAL / FLAG_FORCE_SPECIAL
uniquement aux attaques dont la catégorie Gen 4 diffère de la règle par type. Idempotent."""
import re, sys
repo = sys.argv[1]; P = repo + '/src/data/battle_moves.h'
PHYS_TYPES = {'NORMAL','FIGHTING','FLYING','POISON','GROUND','ROCK','BUG','GHOST','STEEL'}
SPECIAL = set('''RAZOR_WIND SWIFT HYPER_BEAM TRI_ATTACK SNORE UPROAR WEATHER_BALL SPIT_UP HYPER_VOICE
GUST AIR_CUTTER AEROBLAST TWISTER DRAGON_BREATH
EMBER FLAMETHROWER FIRE_SPIN FIRE_BLAST HEAT_WAVE OVERHEAT ERUPTION BLAST_BURN
WATER_GUN HYDRO_PUMP SURF BUBBLE_BEAM BUBBLE WHIRLPOOL OCTAZOOKA MUDDY_WATER WATER_SPOUT HYDRO_CANNON WATER_PULSE
ABSORB MEGA_DRAIN GIGA_DRAIN SOLAR_BEAM PETAL_DANCE MAGICAL_LEAF FRENZY_PLANT
THUNDER_SHOCK THUNDERBOLT THUNDER ZAP_CANNON SHOCK_WAVE FLASH
CONFUSION PSYBEAM PSYCHIC DREAM_EATER FUTURE_SIGHT LUSTER_PURGE MIST_BALL EXTRASENSORY PSYCHO_BOOST
ICE_BEAM BLIZZARD AURORA_BEAM POWDER_SNOW ICY_WIND
ACID SLUDGE SMOG SLUDGE_BOMB MUD_SLAP MUD_SHOT ANCIENT_POWER SILVER_WIND SIGNAL_BEAM SHADOW_BALL DOOM_DESIRE'''.split())
DYNAMIC = {'HIDDEN_POWER'}  # type dynamique : on garde la règle par type
s = open(P).read(); n = 0
def fix(m):
    global n
    mv, body = m.group(1), m.group(2)
    if mv in DYNAMIC or mv == 'NONE': return m.group(0)
    power = int(re.search(r'\.power = (\d+)', body).group(1))
    if power == 0: return m.group(0)
    ty = re.search(r'\.type = TYPE_(\w+)', body).group(1)
    gen3_phys = ty in PHYS_TYPES
    want_phys = mv not in SPECIAL
    if gen3_phys == want_phys: return m.group(0)
    flag = 'FLAG_FORCE_PHYSICAL' if want_phys else 'FLAG_FORCE_SPECIAL'
    if flag in body: return m.group(0)
    n += 1
    body = re.sub(r'(\.flags = [^\n]*?),?\n', lambda f: (f.group(1) + ' | ' + flag + ',\n') if not f.group(1).rstrip().endswith('= 0') else '.flags = ' + flag + ',\n', body, count=1)
    return '[MOVE_%s] =%s' % (mv, body)
s = re.sub(r'\[MOVE_(\w+)\] =(\s*\{.*?\n    \})', fix, s, flags=re.S)
open(P, 'w').write(s); print(n, 'attaques marquées')
