# SPINELLIA (ex-Lavanville, LAYOUT_LAVENDER_TOWN 40x30) : evenements. A lancer apres spinellia_town.py. Idempotent.
# Les routes 8 / 10 / 12 gardent leurs tilesets d'origine : plus de connexions de carte, pas simples (comme Amethiolite).
import json, re
D = json.load(open('/tmp/spinellia_doors.json')); N = json.load(open('/tmp/spinellia_npc.json')); S = json.load(open('/tmp/spinellia_signs.json'))
def warp(x, y, dest, wid, el=0): return {"x": x, "y": y, "elevation": el, "dest_map": dest, "dest_warp_id": str(wid)}
def jdump(o, f): json.dump(o, open(f, 'w'), indent=2); open(f, 'a').write('\n')
f = 'data/maps/LavenderTown/map.json'; d = json.load(open(f))
ORDER = ['tower', 'center', 'vol', 'house1', 'house2', 'mart']          # ordre d'origine des warps (les interieurs y renvoient par index)
orig = d['warp_events'][:6]
W = [warp(D[k][0], D[k][1], o['dest_map'], o['dest_warp_id']) for k, o in zip(ORDER, orig)]
NX = [18, 19, 20, 21]; SX = [18, 19]; WY = [14, 15, 16]
base = len(W)
def side(name, town_cells, route_cells, first):
    f2 = f'data/maps/{name}/map.json'; r = json.load(open(f2))
    kp = [w for w in r['warp_events'] if w['dest_map'] != 'MAP_LAVENDER_TOWN']
    r['warp_events'] = kp + [warp(x, y, 'MAP_LAVENDER_TOWN', first + i) for i, (x, y) in enumerate(route_cells)]
    r['connections'] = [c for c in r['connections'] if c['map'] != 'MAP_LAVENDER_TOWN']
    jdump(r, f2); return len(kp)
n10 = side('Route10', None, [(8 + i, 79) for i in range(4)], base)
n12 = side('Route12', None, [(11 + i, 0) for i in range(2)], base + 4)
n8 = side('Route8', None, [(71, 9 + i) for i in range(3)], base + 6)
for i, x in enumerate(NX): W.append(warp(x, 0, 'MAP_ROUTE10', n10 + i))
for i, x in enumerate(SX): W.append(warp(x, 29, 'MAP_ROUTE12', n12 + i))
for i, y in enumerate(WY): W.append(warp(0, y, 'MAP_ROUTE8', n8 + i))
d['warp_events'] = W; d['connections'] = []
POS = {'LITTLE_GIRL': 'girl', 'WORKER_M': 'worker', 'BOY': 'boy'}
for o in d['object_events']:
    o['x'], o['y'] = N[POS[o['graphics_id'].replace('OBJ_EVENT_GFX_', '')]]
SG = {'SilphScopeNotice': 'notice', 'TownSign': 'town', 'PokemonTowerSign': 'tower', 'VolunteerHouseSign': 'vol'}
for b in d['bg_events']:
    if b['type'] == 'sign': b['x'], b['y'] = S[SG[b['script'].split('_')[-1]]]
jdump(d, f)
f = 'data/maps/LavenderTown/text.inc'; s = open(f).read()
s = s.replace('The Noble Purple Town', 'The Spinel Tower Town'); open(f, 'w').write(s)
f = 'src/data/heal_locations.h'; s = open(f).read(); x, y = D['center']
s = re.sub(r'(HEAL_LOCATION_LAVENDER_TOWN - 1\] = \{.*?\.x = )\d+(,\s*\.y = )\d+', r'\g<1>%d\g<2>%d' % (x, y + 1), s, count=1, flags=re.S); open(f, 'w').write(s)
f = 'src/field_control_avatar.c'; s = open(f).read()
if 'LAYOUT_LAVENDER_TOWN' not in s:
    s = s.replace('|| gMapHeader.mapLayoutId == LAYOUT_ROUTE14;', '|| gMapHeader.mapLayoutId == LAYOUT_ROUTE14 || gMapHeader.mapLayoutId == LAYOUT_LAVENDER_TOWN || gMapHeader.mapLayoutId == LAYOUT_ROUTE10 || gMapHeader.mapLayoutId == LAYOUT_ROUTE12 || gMapHeader.mapLayoutId == LAYOUT_ROUTE8;', 1)
    open(f, 'w').write(s)
print('evenements Spinellia ecrits', len(W), 'warps')
