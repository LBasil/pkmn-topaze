#!/usr/bin/env python3
"""Audit de diversite : sauvages (especes distinctes par table) et dresseurs (repetitions d'une meme espece par carte / sur le parcours)."""
import json, re, glob, collections, sys
wj = json.load(open('src/data/wild_encounters.json'))
print('== SAUVAGES (FireRed) : tables a faible diversite')
for g in wj['wild_encounter_groups']:
    for e in g['encounters']:
        if 'FireRed' not in e['base_label']: continue
        for k in ('land_mons', 'water_mons', 'fishing_mons', 'rock_smash_mons'):
            if k in e:
                sp = [m['species'][8:] for m in e[k]['mons']]; d = len(set(sp))
                lim = {'land_mons': 5, 'water_mons': 2, 'fishing_mons': 3, 'rock_smash_mons': 2}[k]
                if d < lim: print('%-34s %-16s %d especes / %d : %s' % (e['map'][4:], k, d, len(sp), ','.join(sorted(set(sp)))))
T = open('src/data/trainers.h').read(); P = open('src/data/trainer_parties.h').read()
def party_of(tid):
    m = re.search(r'\[%s\] = \{(.*?)\n    \},' % tid, T, re.S)
    p = re.search(r'(?:ITEM|NO_ITEM)_(?:CUSTOM|DEFAULT)_MOVES\((\w+)\)', m.group(1)) if m else None
    return p.group(1) if p else None
def species(p):
    m = re.search(r'%s\[\] = \{(.*?)\n\};' % re.escape(p), P, re.S)
    return re.findall(r'\.species = SPECIES_(\w+)', m.group(1)) if m else []
S_ = ''.join(open(f).read() for f in glob.glob('data/maps/*/scripts.inc'))
def scr_trainer(sc):
    m = re.search(r'\n%s::\n(?:\t[^\n]*\n)*?\ttrainerbattle_\w+\s+(TRAINER_\w+)' % re.escape(sc), S_)
    return m.group(1) if m else None
order = {}
tot = collections.Counter()
print('\n== DRESSEURS : cartes ou une espece revient trop')
for f in sorted(glob.glob('data/maps/*/map.json')):
    n = f.split('/')[2]; j = json.load(open(f)); c = collections.Counter(); nt = 0; ntr = 0
    for o in j.get('object_events', []):
        if o.get('trainer_type') in ('TRAINER_TYPE_NORMAL', 'TRAINER_TYPE_SEE_ALL_DIRECTIONS', 'TRAINER_TYPE_BURIED'):
            t = scr_trainer(o['script']); p = party_of(t) if t else None
            if p:
                sp = species(p); c.update(sp); nt += 1; ntr += len(sp)
    tot.update(c)
    if nt >= 3 and ntr:
        top, k = c.most_common(1)[0]
        if k >= 5 or (k / ntr > .35 and k >= 4): print('%-34s %2d dresseurs %3d Pokemon : %s x%d (%d especes)' % (n, nt, ntr, top, k, len(c)))
print('\n== total sur tout le jeu (dresseurs normaux) : top 12')
print(tot.most_common(12))
