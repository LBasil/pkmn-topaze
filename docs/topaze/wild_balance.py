#!/usr/bin/env python3
"""Equilibrage des Pokemon sauvages des zones a exigence de badge (zones du temps / de capture, journal A_REFAIRE : « Nom (badge N) »).
Repere : une zone qui demande N badges se situe un peu sous le niveau max du champion N (table LEAD, deduite de trainers.h).
Si l'ecart depasse 6 niveaux, toute la zone est decalee pour atteindre champion-3 (l'ecart relatif entre especes est conserve).
Idempotent. Usage : python3 docs/topaze/wild_balance.py [--dry]"""
import re, json, sys
DRY = '--dry' in sys.argv
LEAD = [16, 22, 29, 38, 44, 53, 56, 60]    # niveau max du champion n°k+1 (Kay, Sylvestre, Hera, Grim, Achlys, Nox, Eddie, Hepha)
j = open('docs/scenario/A_REFAIRE.md').read()
req = {}
for m in re.finditer(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\s*\(([^()]*)\)', j):
    n, t = m.groups()
    b = re.search(r'\b(?:badge\s*|b)(\d)\b', t) or re.fullmatch(r'\s*(\d)\s*', t)
    if b: req.setdefault(n, int(b.group(1)))
p = 'src/data/wild_encounters.json'
D = json.load(open(p)); enc = D['wild_encounter_groups'][0]['encounters']
byname = {}
for e in enc:
    nm = ''.join(w.capitalize() for w in e['map'].replace('MAP_', '').lower().split('_')); byname.setdefault(nm, []).append(e)
changed = 0
for n, b in sorted(req.items(), key=lambda kv: kv[1]):
    top = LEAD[min(b, 8) - 1]            # niveau max du champion du N-ieme badge : repere d'une zone qui en demande N
    for e in byname.get(n, []):
        lists = [v['mons'] for k, v in e.items() if isinstance(v, dict) and 'mons' in v and k != 'fishing_mons']   # la peche garde ses niveaux de canne
        ms = [m for l in lists for m in l]
        if not ms: continue
        hi = max(m['max_level'] for m in ms)
        # une zone legerement sous le champion est voulue (captures a faire monter) ; on ne releve que si l'ecart depasse 6 niveaux
        if hi >= top - 6: continue
        d = (top - 3) - hi
        print('%-18s badge %d  max %2d -> %2d (champion %d, decalage +%d)' % (n, b, hi, hi + d, top, d))
        for m in ms: m['min_level'] += d; m['max_level'] += d
        changed += 1
if not DRY:
    json.dump(D, open(p, 'w'), indent=2); open(p, 'a').write('\n')
print(changed, 'tables remises a l\'echelle')
