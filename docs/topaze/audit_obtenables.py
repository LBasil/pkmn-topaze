#!/usr/bin/env python3
"""Audit : quels Pokemon (1-386) sont obtenables ? Sources : sauvages (wild_encounters.json), givemon/giveegg, setwildbattle/StartLegendary,
echanges, evolutions et reproduction (fermeture). Sortie : liste des manquants. Lancer depuis la racine du depot."""
import json, re, glob, os
os.chdir(os.path.join(os.path.dirname(__file__), '..', '..'))
sp = {}  # nom -> id
for m in re.finditer(r'#define SPECIES_(\w+)\s+(\d+)', open('include/constants/species.h').read()):
    n, i = m.group(1), int(m.group(2))
    if 1 <= i <= 411 and not n.startswith('OLD_UNOWN') and not n.endswith('_EGG') and n != 'UNOWN_B' and not n.startswith('UNOWN_'): sp[n] = i
src = {}
def add(n, why):
    if n in sp: src.setdefault(n, set()).add(why)
for g in json.load(open('src/data/wild_encounters.json'))['wild_encounter_groups']:
    for e in g['encounters']:
        for k, v in e.items():
            if isinstance(v, dict) and 'mons' in v:
                for mo in v['mons']: add(mo['species'].replace('SPECIES_', ''), 'wild:' + e['map'])
for f in glob.glob('data/**/*.inc', recursive=True) + glob.glob('data/*.s'):
    t = open(f, errors='ignore').read()
    for m in re.finditer(r'\b(givemon|giveegg|setwildbattle|seteggmon)\s+SPECIES_(\w+)', t): add(m.group(2), m.group(1) + ':' + os.path.basename(os.path.dirname(f)))
    for m in re.finditer(r'\bStartLegendaryBattle|setvar VAR_0x8004, SPECIES_(\w+)', t):
        if m.group(1): add(m.group(1), 'script:' + os.path.basename(os.path.dirname(f)))
for f in glob.glob('src/**/*.[ch]', recursive=True):
    t = open(f, errors='ignore').read()
    if 'ingame_trade' in f or 'trade' in f:
        for m in re.finditer(r'\.(?:species|requestedSpecies)\s*=\s*SPECIES_(\w+)', t): add(m.group(1), 'trade')
for f in ['data/maps/PalletTown_ProfessorOaksLab/scripts.inc']:
    for m in re.finditer(r'setvar PLAYER_STARTER_SPECIES, SPECIES_(\w+)', open(f).read()): add(m.group(1), 'starter')
# evolutions
ev = open('src/data/pokemon/evolution.h').read() if os.path.exists('src/data/pokemon/evolution.h') else ''
edges = []
for m in re.finditer(r'\[SPECIES_(\w+)\]\s*=\s*\{(.*?)\}\},', ev, re.S):
    for t in re.finditer(r'SPECIES_(\w+)\}', m.group(2) + '}'): edges.append((m.group(1), t.group(1)))
ok = set(src)
ch = True
while ch:
    ch = False
    for a, b in edges:
        if a in ok and b not in ok and b in sp: ok.add(b); src.setdefault(b, set()).add('evo:' + a); ch = True
    # reproduction : pre-evolutions (base form via breeding of obtained evolved line)
    for a, b in edges:
        if b in ok and a not in ok and a in sp: ok.add(a); src.setdefault(a, set()).add('breed:' + b); ch = True
miss = sorted((n for n in sp if n not in ok), key=lambda n: sp[n])
print(len(ok), '/', len(sp), 'obtenables ; manquants :', len(miss))
for n in miss: print(' ', sp[n], n)
print('edges', len(edges))
