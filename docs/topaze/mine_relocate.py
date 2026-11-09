#!/usr/bin/env python3
"""Mine de Grenalux raccourcie : les étages 1F/2F ne sont plus jamais visités (la porte mène à 3F).
Les PNJ, objets et objets cachés posés là par mine_fill.py étaient donc perdus : on les déplace dans la zone
de 3F réellement atteignable (celle de l'arrivée, warp 3). Idempotent. Les scripts/textes/flags ne bougent pas (labels globaux)."""
import json, sys
sys.path.insert(0, '/home/claude/pkmn-topaze/tools/topaze/maps')
import analyze as A
ROOT = '/home/claude/pkmn-topaze/'
R = A.Root(ROOT)
r = A.analyse_map(R, 'MAP_GRENALUX_MINE_3F', lambda R_, l: R_.grid(l))
cell, co = r[2][2], r[2][5]
P3 = ROOT + 'data/maps/GrenaluxMine_3F/map.json'
m3 = json.load(open(P3))
arrive = m3['warp_events'][3]
zone = {c for c, k in co.items() if k == co[(arrive['x'], arrive['y'])]}
busy = {(o['x'], o['y']) for o in m3['object_events']} | {(b['x'], b['y']) for b in m3['bg_events']} | {(c['x'], c['y']) for c in m3['coord_events']} | {(w['x'], w['y']) for w in m3['warp_events']}
def free(c, taken):
    if c not in zone or c in busy or c in taken: return False
    if any(abs(c[0] - b[0]) + abs(c[1] - b[1]) < 2 for b in taken): return False
    nb = sum(1 for d in A.D4 if (c[0] + d[0], c[1] + d[1]) in zone)
    return nb >= 3 and not any(abs(c[0] - e[0]) + abs(c[1] - e[1]) < 3 for e in {(9, 6), (13, 8), (14, 11), (14, 9)})
taken = set(); spots = []
for y in (4, 5, 3, 16, 15, 12, 13, 9, 10):            # salles en haut d'abord, puis le couloir
    for x in range(4, 19, 3):
        if free((x, y), taken): spots.append((x, y)); taken.add((x, y))
moves = []
for fl in ('1F', '2F'):
    P = ROOT + 'data/maps/GrenaluxMine_%s/map.json' % fl
    m = json.load(open(P))
    keep = [o for o in m['object_events'] if o['graphics_id'] not in ('OBJ_EVENT_GFX_WORKER_M', 'OBJ_EVENT_GFX_ITEM_BALL')]
    out = [o for o in m['object_events'] if o not in keep]
    hid = [b for b in m['bg_events'] if b['type'] == 'hidden_item']
    if not out and not hid: continue
    m['object_events'] = keep; m['bg_events'] = [b for b in m['bg_events'] if b not in hid]
    json.dump(m, open(P, 'w'), indent=2); open(P, 'a').write('\n')
    moves += [('o', o) for o in out] + [('h', b) for b in hid]
# le vieux ballon de 3F (24,6) et le caché (28,29) sont dans des zones coupées : on les ramène aussi
for o in list(m3['object_events']):
    if (o['x'], o['y']) not in zone and o['graphics_id'] == 'OBJ_EVENT_GFX_ITEM_BALL': m3['object_events'].remove(o); moves.append(('o', o))
for b in list(m3['bg_events']):
    if b['type'] == 'hidden_item' and (b['x'], b['y']) not in zone: m3['bg_events'].remove(b); moves.append(('h', b))
need = len(moves)
assert need <= len(spots), (need, len(spots))
for (k, e), (x, y) in zip(moves, spots):
    e['x'], e['y'] = x, y
    (m3['object_events'] if k == 'o' else m3['bg_events']).append(e)
json.dump(m3, open(P3, 'w'), indent=2); open(P3, 'a').write('\n')
print('déplacés:', need, 'sur', spots[:need])
