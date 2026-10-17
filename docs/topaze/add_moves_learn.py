#!/usr/bin/env python3
"""Distribue les attaques ajoutees par add_moves.py dans les learnsets (par type et par force). Idempotent."""
import re, sys, zlib
repo = sys.argv[1]
R = lambda p: open(repo + '/' + p).read()
src = R('docs/topaze/add_moves.py')
moves = [l.split('|') for l in src.split("M = '''")[1].split("'''")[0].strip().split('\n')]
info = {}   # nom -> (types, bst)
for n, b in re.findall(r'\[SPECIES_(\w+)\]\s*=\s*\{(.*?)\n    \},', R('src/data/pokemon/species_info.h'), re.S):
    t = re.findall(r'\.types = \{TYPE_(\w+), TYPE_(\w+)\}', b)
    if not t: continue
    st = sum(int(x) for x in re.findall(r'\.base(?:HP|Attack|Defense|Speed|SpAttack|SpDefense) = (\d+)', b))
    info[n] = (set(t[0]), st)
FAIRY_EXTRA = '''SNUBBULL GRANBULL MARILL AZUMARILL AZURILL TOGEPI TOGETIC SKITTY DELCATTY MAWILE RALTS KIRLIA GARDEVOIR
PLUSLE MINUN IGGLYBUFF CLEFFA PICHU SPINDA ALTARIA SWABLU'''.split()
for n in FAIRY_EXTRA:
    if n in info: info[n][0].add('FAIRY')
ptr = dict(re.findall(r'\[SPECIES_(\w+)\] = (\w+),', R('src/data/pokemon/level_up_learnset_pointers.h')))
ptr.pop('NONE', None)
L = R('src/data/pokemon/level_up_learnsets.h')
done_var = {}
def need(power, bst):
    return bst >= (480 if power >= 110 else 400 if power >= 85 else 300 if power >= 65 else 0)
def h(*a): return zlib.crc32('|'.join(a).encode())
cnt = {m[0]: 0 for m in moves}
for sp, var in sorted(ptr.items()):
    if sp not in info or var in done_var: continue
    types, bst = info[sp]
    add = []
    for ty in sorted(types):
        cand = [m for m in moves if m[2] == ty and need(int(m[4]) or 60, bst)]
        cand.sort(key=lambda m: h(sp, m[0]))
        k = 3 if bst >= 450 else 2
        if ty == 'FAIRY' and 'FAIRY' not in {x for x in info[sp][0] if x == 'FAIRY' and sp not in FAIRY_EXTRA}: k = 2
        for m in cand[:k]: add.append(m)
    if not add: continue
    done_var[var] = True
    mm = re.search(r'static const u16 %s\[\] = \{\n(.*?)    LEVEL_UP_END' % var, L, re.S)
    if not mm: continue
    ents = re.findall(r'    LEVEL_UP_MOVE\((\d+), (MOVE_\w+)\),\n', mm.group(1))
    have = {e[1] for e in ents}
    for m in add:
        if 'MOVE_' + m[0] in have or len(ents) >= 24: continue   # le Move Relearner tient 24 attaques + Annuler
        p = int(m[4]) or 60
        base = 14 if p <= 40 else 20 if p <= 55 else 26 if p <= 70 else 33 if p <= 85 else 40 if p <= 100 else 46 if p <= 120 else 54
        lvl = min(95, base + h(sp, m[0], 'l') % 6 + (4 if bst < 300 else 0))
        ents.append((str(lvl), 'MOVE_' + m[0])); cnt[m[0]] += 1
    ents.sort(key=lambda e: int(e[0]))  # tri stable par niveau
    new = ''.join('    LEVEL_UP_MOVE(%s, %s),\n' % e for e in ents)
    L = L[:mm.start(1)] + new + L[mm.end(1):]
open(repo + '/src/data/pokemon/level_up_learnsets.h', 'w').write(L)
print('especes modifiees:', len(done_var))
for m in moves: print('%-16s %3d especes' % (m[0], cnt[m[0]]))
