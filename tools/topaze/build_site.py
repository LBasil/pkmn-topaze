#!/usr/bin/env python3
"""Génère le site joueur (docs/data/*.js) à partir des sources du jeu.
Usage : python3 tools/topaze/build_site.py   (depuis la racine du dépôt)
Les pages HTML (docs/*.html) lisent ces fichiers ; ne pas éditer data/*.js à la main."""
import re, json, os
R = os.getcwd()
def rd(p): return open(os.path.join(R, p), encoding='utf-8').read()

TYPES = ['Normal','Fighting','Flying','Poison','Ground','Rock','Bug','Ghost','Steel','???','Fire','Water','Grass','Electric','Psychic','Ice','Dragon','Dark','Fairy']
def tname(const):  # TYPE_FIRE -> Fire
    k = const.replace('TYPE_','')
    return {'FIGHTING':'Fighting','FLYING':'Flying','NORMAL':'Normal','POISON':'Poison','GROUND':'Ground','ROCK':'Rock','BUG':'Bug','GHOST':'Ghost','STEEL':'Steel','MYSTERY':'???','FIRE':'Fire','WATER':'Water','GRASS':'Grass','ELECTRIC':'Electric','PSYCHIC':'Psychic','ICE':'Ice','DRAGON':'Dragon','DARK':'Dark','FAIRY':'Fairy'}[k]
def pretty(s): return ' '.join(w.capitalize() for w in s.split('_'))

# --- noms ---
names = re.findall(r'\[SPECIES_(\w+)\] = _\("([^"]*)"\)', rd('src/data/text/species_names.h'))
species = [(c, n) for c, n in names if c != 'NONE'][:151]
sname = {c: n for c, n in species}
mnames = {c: n for c, n in re.findall(r'\[MOVE_(\w+)\]\s*= _\("([^"]*)"\)', rd('src/data/text/move_names.h'))}
anames = {c: n for c, n in re.findall(r'\[ABILITY_(\w+)\] = _\("([^"]*)"\)', rd('src/data/text/abilities.h'))}

# --- pokédex ---
si = rd('src/data/pokemon/species_info.h')
lv_ptr = dict(re.findall(r'\[SPECIES_(\w+)\] = (\w+),', rd('src/data/pokemon/level_up_learnset_pointers.h')))
lv_src = rd('src/data/pokemon/level_up_learnsets.h')
def learnset(label):
    m = re.search(r'%s\[\] = \{(.*?)LEVEL_UP_END' % label, lv_src, re.S)
    return [[int(l), mnames.get(mv, mv)] for l, mv in re.findall(r'LEVEL_UP_MOVE\(\s*(\d+),\s*MOVE_(\w+)\)', m.group(1))] if m else []
dex = []
for i, (c, n) in enumerate(species, 1):
    m = re.search(r'\[SPECIES_%s\] =\s*\{(.*?)\n    \}' % c, si, re.S).group(1)
    g = lambda k: int(re.search(k + r' = (\d+)', m).group(1))
    st = [g(k) for k in ('baseHP','baseAttack','baseDefense','baseSpAttack','baseSpDefense','baseSpeed')]
    t = re.search(r'types = \{(TYPE_\w+), (TYPE_\w+)\}', m).groups()
    ty = [tname(t[0])] + ([tname(t[1])] if t[1] != t[0] else [])
    ab = [anames.get(a, a) for a in re.search(r'abilities = \{ABILITY_(\w+), ABILITY_(\w+)\}', m).groups() if a != 'NONE']
    dex.append(dict(n=i, name=n.title().replace('Mr. Mime','Mr. Mime'), types=ty, stats=st, bst=sum(st), abilities=ab, moves=learnset(lv_ptr[c])))

# --- attaques ---
bm = rd('src/data/battle_moves.h')
moves = []
for c, body in re.findall(r'\[MOVE_(\w+)\] =\s*\{(.*?)\n    \}', bm, re.S):
    if c == 'NONE' or c not in mnames: continue
    g = lambda k: int(re.search(k + r' = (-?\d+)', body).group(1))
    ty = tname(re.search(r'\.type = (TYPE_\w+)', body).group(1))
    p = g(r'\.power')
    fl = re.search(r'\.flags = ([^\n]*)', body).group(1)
    if p == 0: cat = 'Status'
    elif 'FLAG_FORCE_PHYSICAL' in fl: cat = 'Physical'
    elif 'FLAG_FORCE_SPECIAL' in fl: cat = 'Special'
    else: cat = 'Special' if ty in ('Fire','Water','Grass','Electric','Psychic','Ice','Dragon','Dark','Fairy') else 'Physical'
    moves.append(dict(name=mnames[c], type=ty, cat=cat, power=p, acc=g(r'\.accuracy'), pp=g(r'\.pp'), prio=g(r'\.priority')))

# --- table des types ---
te = rd('src/battle_main.c')
blk = re.search(r'gTypeEffectiveness\[\d+\] =\s*\{(.*?)\n\};', te, re.S).group(1)
mul = {'TYPE_MUL_NO_EFFECT':0,'TYPE_MUL_NOT_EFFECTIVE':0.5,'TYPE_MUL_SUPER_EFFECTIVE':2}
chart = {}
for a, d, m in re.findall(r'(TYPE_\w+), (TYPE_\w+), (TYPE_MUL_\w+)', blk):
    if a in ('TYPE_FORESIGHT','TYPE_ENDTABLE'): continue
    chart.setdefault(tname(a), {})[tname(d)] = mul[m]
tlist = [t for t in TYPES if t != '???']

# --- champions ---
tp = rd('src/data/trainer_parties.h')
leaders = [('Kay','Pyropia','Fire','Brock'),('Sylvestre','Tourmalia','Bug / Grass','Misty'),('Hera','Apatia','Dragon / Flying','LtSurge'),('Grim','Bourg Quartz','Ice','Erika'),('Achlys','Amethiolite','Poison','Koga'),('Nox','Hematown','Dark','Sabrina'),('Eddie','Chrondrolia','Electric','Blaine'),('Hepha','Opanihrum','Steel','Giovanni')]
champs = []
for i, (nm, city, ty, slot) in enumerate(leaders, 1):
    arr = re.search(r'sParty_Leader%s\[\] = \{(.*?)\n\};' % slot, tp, re.S).group(1)
    team = []
    for lvl, sp, it, mv in re.findall(r'\.lvl = (\d+),\s*\.species = SPECIES_(\w+),(?:\s*\.heldItem = ITEM_(\w+),)?\s*\.moves = \{([^}]*)\}', arr):
        team.append(dict(species=sname[sp].title(), lvl=int(lvl), item=pretty(it) if it else '', moves=[mnames.get(x.strip()[5:], x.strip()[5:]) for x in mv.split(',') if x.strip() and x.strip() != 'MOVE_NONE']))
    champs.append(dict(n=i, name=nm, city=city, type=ty, team=team))

# --- rencontres sauvages ---
wj = json.load(open(os.path.join(R, 'src/data/wild_encounters.json')))['wild_encounter_groups'][0]['encounters']
wild = []
kinds = [('land_mons','Grass'),('water_mons','Surf'),('rock_smash_mons','Rock Smash'),('fishing_mons','Fishing')]
for e in wj:
    if not e['map'].endswith(('')) : continue
    for key, label in kinds:
        if key in e:
            mons = {}
            for m in e[key]['mons']:
                s = m['species'].replace('SPECIES_','')
                if s not in sname: continue
                mons.setdefault(sname[s].title(), []).append((m['min_level'], m['max_level']))
            for sp, lv in mons.items():
                wild.append(dict(map=pretty(e['map'].replace('MAP_','')), how=label, species=sp, min=min(a for a,_ in lv), max=max(b for _,b in lv), slots=len(lv)))

os.makedirs(os.path.join(R, 'docs/data'), exist_ok=True)
def out(name, var, obj):
    open(os.path.join(R, 'docs/data/%s.js' % name), 'w', encoding='utf-8').write('window.%s = %s;\n' % (var, json.dumps(obj, ensure_ascii=False, separators=(',', ':'))))
out('pokedex', 'POKEDEX', dex); out('moves', 'MOVES', moves); out('types', 'TYPES', dict(list=tlist, chart=chart))
out('champions', 'CHAMPIONS', champs); out('wild', 'WILD', wild)
print(len(dex), 'pokémon,', len(moves), 'attaques,', len(champs), 'champions,', len(wild), 'lignes sauvages')
