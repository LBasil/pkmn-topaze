#!/usr/bin/env python3
"""Diversifie les equipes de dresseurs (parties a attaques par defaut uniquement) : remplace les repetitions
(doublon dans l'equipe, >2 d'une espece par carte, >GCAP au total) par des especes thematiques de meme palier.
Idempotent : apres un premier passage il n'y a plus de depassement. Met aussi a jour rebalance21_orig.json."""
import re, glob, json, collections, sys
sys.path.insert(0, 'docs/topaze')
T = open('src/data/trainers.h').read(); P = open('src/data/trainer_parties.h').read()
S_ = ''.join(open(f).read() for f in glob.glob('data/scripts/*.inc') + glob.glob('data/maps/*/scripts.inc'))
def F(*st): return list(st)   # (niveau_min, espece)
FAM = {
 'rattata': F((1,'RATTATA'),(20,'RATICATE')), 'zubat': F((1,'ZUBAT'),(22,'GOLBAT'),(42,'CROBAT')),
 'koffing': F((1,'KOFFING'),(35,'WEEZING')), 'grimer': F((1,'GRIMER'),(38,'MUK')), 'ekans': F((1,'EKANS'),(22,'ARBOK')),
 'drowzee': F((1,'DROWZEE'),(26,'HYPNO')), 'machop': F((1,'MACHOP'),(28,'MACHOKE')), 'houndour': F((1,'HOUNDOUR'),(24,'HOUNDOOM')),
 'poochy': F((1,'POOCHYENA'),(18,'MIGHTYENA')), 'sandshrew': F((1,'SANDSHREW'),(22,'SANDSLASH')), 'meowth': F((1,'MEOWTH'),(28,'PERSIAN')),
 'nidom': F((1,'NIDORAN_M'),(16,'NIDORINO')), 'nidof': F((1,'NIDORAN_F'),(16,'NIDORINA')), 'murkrow': F((1,'MURKROW')),
 'sneasel': F((1,'SNEASEL')), 'cubone': F((1,'CUBONE'),(28,'MAROWAK')), 'tentacool': F((1,'TENTACOOL'),(30,'TENTACRUEL')),
 'voltorb': F((1,'VOLTORB'),(30,'ELECTRODE')), 'magnemite': F((1,'MAGNEMITE'),(30,'MAGNETON')), 'vulpix': F((1,'VULPIX')),
 'growlithe': F((1,'GROWLITHE')), 'spinarak': F((1,'SPINARAK'),(22,'ARIADOS')), 'gastly': F((1,'GASTLY'),(25,'HAUNTER')),
 'shuppet': F((1,'SHUPPET'),(37,'BANETTE')), 'duskull': F((1,'DUSKULL'),(37,'DUSCLOPS')), 'misdreavus': F((1,'MISDREAVUS')),
 'sableye': F((1,'SABLEYE')), 'geodude': F((1,'GEODUDE'),(25,'GRAVELER')), 'onix': F((1,'ONIX')), 'rhyhorn': F((1,'RHYHORN'),(42,'RHYDON')),
 'larvitar': F((1,'LARVITAR'),(30,'PUPITAR')), 'nosepass': F((1,'NOSEPASS')), 'aron': F((1,'ARON'),(32,'LAIRON'),(42,'AGGRON')),
 'phanpy': F((1,'PHANPY'),(25,'DONPHAN')), 'numel': F((1,'NUMEL'),(33,'CAMERUPT')), 'swinub': F((1,'SWINUB'),(33,'PILOSWINE')),
 'smoochum': F((1,'SMOOCHUM'),(30,'JYNX')), 'delibird': F((1,'DELIBIRD')), 'shellder': F((1,'SHELLDER')), 'seel': F((1,'SEEL'),(34,'DEWGONG')),
 'snorunt': F((1,'SNORUNT')), 'spheal': F((1,'SPHEAL'),(32,'SEALEO')), 'pineco': F((1,'PINECO'),(31,'FORRETRESS')), 'skarmory': F((1,'SKARMORY')),
 'mawile': F((1,'MAWILE')), 'beldum': F((1,'BELDUM'),(20,'METANG')), 'scyther': F((1,'SCYTHER')), 'hitlee': F((1,'HITMONLEE')),
 'hitchan': F((1,'HITMONCHAN')), 'makuhita': F((1,'MAKUHITA'),(24,'HARIYAMA')), 'meditite': F((1,'MEDITITE'),(37,'MEDICHAM')),
 'mankey': F((1,'MANKEY'),(28,'PRIMEAPE')), 'abra': F((1,'ABRA'),(16,'KADABRA')), 'porygon': F((1,'PORYGON')), 'elekid': F((1,'ELEKID')),
 'magby': F((1,'MAGBY')), 'carvanha': F((1,'CARVANHA'),(30,'SHARPEDO')), 'slugma': F((1,'SLUGMA'),(38,'MAGCARGO')), 'teddiursa': F((1,'TEDDIURSA')),
}
FAM = {k: [(l, s) for l, s in v if re.search(r'#define SPECIES_%s\b' % s, open('include/constants/species.h').read())] for k, v in FAM.items()}
def sp2fam():
    d = {}
    for k, v in FAM.items():
        for l, s in v: d[s] = k
    return d
S2F = sp2fam()
POOL = {
 'ROCKET': 'rattata zubat koffing grimer ekans drowzee machop houndour poochy sandshrew meowth nidom nidof murkrow sneasel cubone voltorb magnemite spinarak tentacool carvanha growlithe'.split(),
 'SCIENT': 'magnemite voltorb koffing grimer porygon elekid abra drowzee magby beldum'.split(),
 'GHOST': 'gastly shuppet duskull misdreavus cubone sableye murkrow zubat'.split(),
 'ROCK': 'geodude onix machop rhyhorn sandshrew cubone larvitar nosepass aron phanpy numel zubat mankey'.split(),
 'STEEL': 'magnemite aron pineco skarmory mawile beldum scyther onix'.split(),
 'ICE': 'swinub smoochum delibird shellder seel snorunt spheal sneasel'.split(),
 'FIGHT': 'mankey machop hitlee hitchan makuhita meditite abra'.split(),
}
CLASSPOOL = {'TEAM_ROCKET': 'ROCKET', 'SCIENTIST': 'SCIENT', 'CHANNELER': 'GHOST', 'HIKER': 'ROCK', 'RUIN_MANIAC': 'ROCK', 'BIKER': 'ROCKET', 'JUGGLER': 'GHOST', 'BLACK_BELT': 'FIGHT', 'SUPER_NERD': 'SCIENT', 'ENGINEER': 'SCIENT', 'BURGLAR': 'ROCKET', 'CUE_BALL': 'FIGHT'}
MAPPOOL = {'ViridianCity_Gym': 'STEEL', 'CeladonCity_Gym': 'ICE', 'SaffronCity_Dojo': 'FIGHT', 'RockTunnel_1F': 'ROCK', 'RockTunnel_B1F': 'ROCK', 'PokemonTower_3F': 'GHOST', 'PokemonTower_4F': 'GHOST', 'PokemonTower_5F': 'GHOST', 'PokemonTower_6F': 'GHOST', 'PokemonTower_7F': 'GHOST'}
GCAP, MCAP = 12, 2
def info(tid):
    m = re.search(r'\[%s\] = \{(.*?)\n    \},' % tid, T, re.S)
    if not m: return None
    cl = re.search(r'trainerClass = TRAINER_CLASS_(\w+)', m.group(1)); p = re.search(r'((?:ITEM|NO_ITEM)_(?:CUSTOM|DEFAULT)_MOVES)\((\w+)\)', m.group(1))
    return (cl.group(1), p.group(1), p.group(2)) if cl and p else None
def scr(sc):
    m = re.search(r'\n%s::\n(?:\t[^\n]*\n)*?\ttrainerbattle_\w+\s+(TRAINER_\w+)' % re.escape(sc), S_)
    return m.group(1) if m else None
def block(n): return re.search(r'(%s\[\] = \{)(.*?)(\n\};)' % re.escape(n), P, re.S)
def stage(fam, lvl):
    best = FAM[fam][0][1]
    for l, s in FAM[fam]:
        if lvl >= l: best = s
    return best
# collecte (carte, classe, party) sans doublons de party
jobs = []; seen = set(); gc = collections.Counter()
for f in sorted(glob.glob('data/maps/*/map.json')):
    n = f.split('/')[2]
    for o in json.load(open(f)).get('object_events', []):
        if o.get('trainer_type', 'TRAINER_TYPE_NONE') == 'TRAINER_TYPE_NONE': continue
        t = scr(o['script']); i = info(t) if t else None
        if not i or i[2] in seen or i[0] in ('LEADER', 'ELITE_FOUR', 'CHAMPION'): continue
        if i[1].endswith('CUSTOM_MOVES') and i[0] not in ('TEAM_ROCKET',): pass
        seen.add(i[2]); jobs.append((n, i[0], i[1], i[2]))
for n, c, k, p in jobs:
    b = block(p)
    if b: gc.update(re.findall(r'\.species = SPECIES_(\w+)', b.group(2)))
orig = json.load(open('docs/topaze/rebalance21_orig.json'))
P2 = P; changes = 0; mc = collections.defaultdict(collections.Counter); rr = collections.Counter()
for n, c, k, p in jobs:
    if k.endswith('CUSTOM_MOVES'): continue
    b = block(p)
    if not b: continue
    pool = POOL[MAPPOOL.get(n) or CLASSPOOL.get(c, '')] if (MAPPOOL.get(n) or c in CLASSPOOL) else None
    body = b.group(2); mons = re.findall(r'\.lvl = (\d+),\s*\n\s*\.species = SPECIES_(\w+)', body)
    inparty = collections.Counter(s for _, s in mons); new = []; idx = 0
    def rep(m):
        global changes
        nonlocal_idx[0] += 1; l, s = int(m.group(1)), m.group(3)
        fam = S2F.get(s)
        over = fam and (inparty[s] > 1 or mc[n][s] >= MCAP or gc[s] > GCAP)
        if pool and over:
            used = {S2F.get(x) for x in cur}
            cand = [q for q in pool if q not in used and q != fam]
            if cand:
                cand.sort(key=lambda q: (gc[stage(q, l)] + mc[n][stage(q, l)] * 3, pool.index(q)))
                ns = stage(cand[0], l)
                inparty[s] -= 1; gc[s] -= 1; gc[ns] += 1; mc[n][ns] += 1; cur.append(ns)
                orig['parties'].get(p) and orig['parties'][p].__setitem__(nonlocal_idx[0]-1, [orig['parties'][p][nonlocal_idx[0]-1][0], 'SPECIES_' + ns]); changes += 1
                return '.lvl = %d,%s.species = SPECIES_%s' % (l, m.group(2), ns)
        mc[n][s] += 1; cur.append(s); return m.group(0)
    nonlocal_idx = [0]; cur = []
    nb = re.sub(r'\.lvl = (\d+),(\s*\n\s*)\.species = SPECIES_(\w+)', rep, body)
    P2 = P2.replace(b.group(0), b.group(1) + nb + b.group(3))
open('src/data/trainer_parties.h', 'w').write(P2)
json.dump(orig, open('docs/topaze/rebalance21_orig.json', 'w'))
print('remplacements :', changes)
