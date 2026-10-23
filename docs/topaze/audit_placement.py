#!/usr/bin/env python3
"""Audit de placement : objets sur case bloquee, objets superposes, objet sur warp, case devant une porte occupee."""
import sys, glob, json, collections
sys.path[:0] = ['/tmp/gx', 'docs/topaze', 'tools/topaze/maps']
import route_test as R
out = collections.defaultdict(list)
for f in sorted(glob.glob('data/maps/*/map.json')):
    n = f.split('/')[2]
    try: nav = R.Nav(n)
    except Exception: continue
    j = json.load(open(f)); nav.objs = set()
    warps = {(w['x'], w['y']) for w in j['warp_events']}
    seen = collections.Counter()
    for o in j['object_events']:
        c = (o['x'], o['y']); seen[c] += 1
        nm = o['graphics_id'][14:] + ':' + o.get('script','?').split('EventScript_')[-1][:18]
        if not (0 <= c[0] < nav.w and 0 <= c[1] < nav.h): out[n].append(f'HORS CARTE {c} {nm}'); continue
        if c in warps: out[n].append(f'SUR WARP {c} {nm}')
        elif nav.blocked(*c) and o.get('flag','0') in ('0', 0) and 'ITEM_BALL' not in o['graphics_id']:
            out[n].append(f'SUR CASE BLOQUEE {c} {nm}')
    for c, k in seen.items():
        if k > 1: out[n].append(f'SUPERPOSES {c} x{k}')
    for (x, y) in warps:
        for (fx, fy) in [(x, y+1)]:
            if any((o['x'], o['y']) == (fx, fy) and o.get('trainer_type') == 'TRAINER_TYPE_NONE' and o.get('movement_type') in ('MOVEMENT_TYPE_FACE_DOWN','MOVEMENT_TYPE_FACE_UP','MOVEMENT_TYPE_FACE_LEFT','MOVEMENT_TYPE_FACE_RIGHT','MOVEMENT_TYPE_NONE') for o in j['object_events']):
                out[n].append(f'DEVANT PORTE {x},{y} occupee en ({fx},{fy})')
tot = 0
for n, l in out.items():
    for s in l: print(n, s); tot += 1
print(tot, 'signalements')
