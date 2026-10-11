# CHRONDROLIA (ex-Cinnabar, LAYOUT_CINNABAR_ISLAND) : evenements. A lancer apres chrondrolia_town.py. Idempotent.
# Warps 0..4 = manoir, arene, labo, centre, boutique (ordre conserve : les interieurs y renvoient). Warps 5+ = mer (Route 21 au nord, Route 20 a l'est).
import json, re, struct
D = json.load(open('/tmp/chrondrolia_doors.json')); N = json.load(open('/tmp/chrondrolia_npc.json'))
S = json.load(open('/tmp/chrondrolia_signs.json')); M = json.load(open('/tmp/chrondrolia_misc.json'))
Wd, Ht = 40, 36
def warp(x, y, dest, wid, el=0): return {"x": x, "y": y, "elevation": el, "dest_map": dest, "dest_warp_id": str(wid)}
def jdump(o, f): json.dump(o, open(f, 'w'), indent=2); open(f, 'a').write('\n')
# ---- cases de mer au bord de la carte
lay = {l.get('id'): l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id')}
g = struct.unpack('<%dH' % (Wd * Ht), open('data/layouts/CinnabarIsland/map.bin', 'rb').read())
def is_sea(x, y): return (g[y * Wd + x] >> 12) == 1 and (g[y * Wd + x] & 0xc00) == 0 and (x, y) not in {tuple(p) for p in M['pier1'] + M['pier2']}
NORTH = [x for x in range(16, 24) if is_sea(x, 0)]
EAST = [y for y in range(16, 30) if is_sea(Wd - 1, y)]
assert len(NORTH) == 8 and len(EAST) >= 8, (NORTH, EAST)
R21 = list(range(14, 24)); R20 = list(range(0, 20))
# ---- Chrondrolia
W = [None] * 5
W[0] = warp(*D['mansion'][0], 'MAP_POKEMON_MANSION_1F', 1); W[1] = warp(*D['gym'][0], 'MAP_CINNABAR_ISLAND_GYM', 1)
W[2] = warp(*D['lab'][0], 'MAP_CINNABAR_ISLAND_POKEMON_LAB_ENTRANCE', 1); W[3] = warp(*D['center'][0], 'MAP_CINNABAR_ISLAND_POKEMON_CENTER_1F', 0)
W[4] = warp(*D['mart'][0], 'MAP_CINNABAR_ISLAND_MART', 1)
for k, x in enumerate(NORTH): W.append(warp(x, 0, 'MAP_ROUTE21_SOUTH', k))                     # ids 5..12 ; dest_warp_id fixe plus bas
for k, y in enumerate(EAST): W.append(warp(Wd - 1, y, 'MAP_ROUTE20', 0))                         # ids 13.. (dest fixee plus bas)
r21 = {x: min(max(x, 16), 23) - 16 for x in R21}                                                 # x de la Route 21 -> indice de la case d'arrivee nord
f = 'data/maps/CinnabarIsland/map.json'; d = json.load(open(f))
# Route 21 Sud : warps sur la rangee du bas (x 14..23), destination = case de mer nord de Chrondrolia
r = json.load(open('data/maps/Route21_South/map.json'))
base21 = len([w for w in r['warp_events'] if w['dest_map'] != 'MAP_CINNABAR_ISLAND'])
r['warp_events'] = [w for w in r['warp_events'] if w['dest_map'] != 'MAP_CINNABAR_ISLAND'] + [warp(x, 49, 'MAP_CINNABAR_ISLAND', 5 + r21[x]) for x in R21]
r['connections'] = [cn for cn in r['connections'] if cn['map'] != 'MAP_CINNABAR_ISLAND']
jdump(r, 'data/maps/Route21_South/map.json')
for k, x in enumerate(NORTH): W[5 + k]['dest_warp_id'] = str(base21 + (min(max(16 + k, 14), 23) - 14))
# Route 20 : colonne de gauche (x=0)
r = json.load(open('data/maps/Route20/map.json'))
base20 = len([w for w in r['warp_events'] if w['dest_map'] != 'MAP_CINNABAR_ISLAND'])
ne = len(EAST)
r20 = {y: round(y * (ne - 1) / 19) for y in R20}
r['warp_events'] = [w for w in r['warp_events'] if w['dest_map'] != 'MAP_CINNABAR_ISLAND'] + [warp(0, y, 'MAP_CINNABAR_ISLAND', 13 + r20[y]) for y in R20]
r['connections'] = [cn for cn in r['connections'] if cn['map'] != 'MAP_CINNABAR_ISLAND']
jdump(r, 'data/maps/Route20/map.json')
for k in range(ne):
    ys = [y for y in R20 if r20[y] == k]; W[13 + k]['dest_warp_id'] = str(base20 + ys[len(ys) // 2])
d['warp_events'] = W; d['connections'] = []
# ---- PNJ
pos = {'OBJ_EVENT_GFX_WOMAN_2': N['woman'], 'OBJ_EVENT_GFX_OLD_MAN_1': N['oldman'], 'OBJ_EVENT_GFX_BILL': N['bill'], 'OBJ_EVENT_GFX_SEAGALLOP': N['gull']}
for o in d['object_events']: o['x'], o['y'] = pos[o['graphics_id']]
for cev in d['coord_events']: cev['x'], cev['y'] = D['gym'][0][0], D['gym'][0][1] + 1
labs = iter([S['lab1'], S['lab2']])
for b in d['bg_events']:
    if b['type'] != 'sign': continue
    s_ = b['script']
    b['x'], b['y'] = S['city'] if 'IslandSign' in s_ else S['gym'] if 'GymSign' in s_ else next(labs)
jdump(d, f)
# ---- textes, soin
f = 'data/maps/CinnabarIsland/text.inc'; s = open(f).read()
s = re.sub(r'(CinnabarIsland_Text_IslandSign::\n).*?\$"', r'\1    .string "CHRONDROLIA\\n"\n    .string "The Yellow City of Topaz$"', s, count=1, flags=re.S)
open(f, 'w').write(s)
f = 'src/data/heal_locations.h'; s = open(f).read()
x, y = D['center'][0]
s = re.sub(r'(HEAL_LOCATION_CINNABAR_ISLAND - 1\] = \{.*?\.x = )\d+(,\s*\.y = )\d+', r'\g<1>%d\g<2>%d' % (x, y + 1), s, count=1, flags=re.S)
open(f, 'w').write(s)
# ---- pas simples (warps sans tuile de porte) : mer de Chrondrolia, Routes 21 Sud / 20
f = 'src/field_control_avatar.c'; s = open(f).read()
if 'LAYOUT_CINNABAR_ISLAND' not in s:
    s = s.replace('|| gMapHeader.mapLayoutId == LAYOUT_ROUTE4_EAST;', '|| gMapHeader.mapLayoutId == LAYOUT_ROUTE4_EAST\n        || gMapHeader.mapLayoutId == LAYOUT_CINNABAR_ISLAND || gMapHeader.mapLayoutId == LAYOUT_ROUTE21_SOUTH || gMapHeader.mapLayoutId == LAYOUT_ROUTE20;')
    open(f, 'w').write(s)
print('evenements Chrondrolia ecrits', len(W), 'warps')
