#!/usr/bin/env python3
"""Audit des niveaux de dresseurs : par carte, niveau max des dresseurs (scripts `trainerbattle_*`) face aux sauvages de la carte.
Usage (depuis la racine) : python3 tools/topaze/audit/levels.py [--flag]. Les rematchs (suffixes _2.._5 / VS Seeker) apparaissent aussi."""
import os, re, sys, json, glob
sys.path.insert(0, 'tools/topaze/emu/bench'); sys.path.insert(0, '/tmp/gx')
import partykit as pk

def trainer_levels(name):
    s = open('src/data/trainers.h').read()
    m = re.search(r'\[%s\] = \{(.*?)\n    \},' % name, s, re.S)
    if not m: return []
    p = re.search(r'(?:ITEM|NO_ITEM)_(?:CUSTOM|DEFAULT)_MOVES\((\w+)\)', m.group(1))
    if not p: return []
    t = open('src/data/trainer_parties.h').read()
    b = re.search(r'%s\[\] = \{(.*?)\n\};' % p.group(1), t, re.S)
    return [int(x) for x in re.findall(r'\.lvl = (\d+)', b.group(1))] if b else []

def wild_levels():
    out = {}
    try: j = json.load(open('src/data/wild_encounters.json'))
    except Exception: return out
    for g in j.get('wild_encounter_groups', []):
        for e in g.get('encounters', []):
            lv = []
            for k, v in e.items():
                if isinstance(v, dict) and 'mons' in v: lv += [x['max_level'] for x in v['mons']]
            if lv: out[e['map']] = (min(lv), max(lv))
    return out

def main():
    wl = wild_levels(); rows = []
    for sc in sorted(glob.glob('data/maps/*/scripts.inc')):
        name = os.path.basename(os.path.dirname(sc)); txt = open(sc).read()
        for tr in sorted(set(re.findall(r'trainerbattle_\w+\s+(TRAINER_\w+)', txt))):
            lv = trainer_levels(tr)
            if lv: rows.append((name, tr, max(lv), wl.get('MAP_' + re.sub(r'(?<!^)(?=[A-Z])', '_', name).upper())))
    return rows

if __name__ == '__main__':
    rows = main()
    for n, t, m, w in rows:
        print('%-34s %-40s max %3d  sauvages %s' % (n, t, m, w or '-'))
