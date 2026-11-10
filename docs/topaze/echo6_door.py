#!/usr/bin/env python3
"""Echo 6 (Regirock) : la bouche du repaire de pierre dans la falaise de la Vallee des Ruines manquait (le repaire SixIsland_RuinValley_StoneDen existait mais aucune
porte n'y menait : decouvert par le bot a l'etape pg_echoes, 10/11). Ajoute la tuile de bouche de grotte en (24,13), le warp vers le repaire, les triggers "ferme"
tant que VAR_ECHO_STAGE < 16, et fait pointer la sortie du repaire sur ce warp. Idempotent. Usage : python3 docs/topaze/echo6_door.py --write"""
import json, sys, struct
W = '--write' in sys.argv
DX, DY = 24, 13
P = 'data/maps/SixIsland_RuinValley/map.json'; D = 'data/maps/SixIsland_RuinValley_StoneDen/map.json'
LAY = 'data/layouts/SixIsland_RuinValley/map.bin'
def load(p): return json.load(open(p))
def save(p, m): json.dump(m, open(p, 'w'), indent=2); open(p, 'a').write('\n')
pj, dj = load(P), load(D)
den = 'MAP_SIX_ISLAND_RUIN_VALLEY_STONE_DEN'
idx = next((i for i, w in enumerate(pj['warp_events']) if w['dest_map'] == den), None)
changed = False
if idx is None:
    pj['warp_events'].append({'x': DX, 'y': DY, 'elevation': 0, 'dest_map': den, 'dest_warp_id': '0'}); idx = len(pj['warp_events']) - 1; changed = True
have = {c['var_value'] for c in pj['coord_events'] if c.get('script', '').endswith('_DenLocked')}
for v in range(16):
    if str(v) not in have:
        pj['coord_events'].append({'type': 'trigger', 'x': DX, 'y': DY + 1, 'elevation': 0, 'var': 'VAR_ECHO_STAGE', 'var_value': str(v), 'script': 'SixIsland_RuinValley_EventScript_DenLocked'}); changed = True
for w in dj['warp_events']:
    if w['dest_warp_id'] != str(idx): w['dest_warp_id'] = str(idx); changed = True
lj = load('data/layouts/layouts.json')['layouts']
lay = next(l for l in lj if l.get('id') == 'LAYOUT_SIX_ISLAND_RUIN_VALLEY'); wd = lay['width']
b = bytearray(open(LAY, 'rb').read()); o = (DY * wd + DX) * 2; v = struct.unpack_from('<H', b, o)[0]
nv = (v & ~0x3ff & ~(3 << 10)) | 0xa9
tile_changed = nv != v
print('warp', idx, '| tuile', hex(v), '->', hex(nv), '| modifie', changed or tile_changed)
if W:
    if changed: save(P, pj); save(D, dj)
    if tile_changed: struct.pack_into('<H', b, o, nv); open(LAY, 'wb').write(b)
