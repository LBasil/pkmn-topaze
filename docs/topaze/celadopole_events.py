# CELADOPOLE (ex-Celadon, LAYOUT_CELADON_CITY 60x40) : evenements. A lancer apres celadopole_town.py. Idempotent.
# Les routes 16 / 7 gardent leurs tilesets d'origine : plus de connexions de carte avec la ville, pas simples.
import json, re, struct
D = json.load(open('/tmp/celadopole_doors.json')); N = json.load(open('/tmp/celadopole_npc.json')); S = json.load(open('/tmp/celadopole_signs.json')); M = json.load(open('/tmp/celadopole_misc.json'))
def warp(x, y, dest, wid, el=0): return {"x": x, "y": y, "elevation": el, "dest_map": dest, "dest_warp_id": str(wid)}
def jdump(o, f): json.dump(o, open(f, 'w'), indent=2); open(f, 'a').write('\n')
def grid(n, w, h): return struct.unpack('<%dH' % (w * h), open('data/layouts/%s/map.bin' % n, 'rb').read())
f = 'data/maps/CeladonCity/map.json'; d = json.load(open(f))
orig = d['warp_events'][:10]
# ordre d'origine : 0 casino, 1-2 grand magasin, 3 condo, 4 centre, 5 echange de lots, 6 arene, 7 resto, 8 maison, 9 hotel (10-12 : toit du condo)
DK = [D['gc'][0], D['dept'][0], D['dept'][1], D['condo'][0], D['center'][0], D['gc'][1], D['gym'][0], D['rest'][0], D['house1'][0], D['hotel'][0]]
W = [warp(x, y, o['dest_map'], o['dest_warp_id'], o['elevation']) for (x, y), o in zip(DK, orig)]
for (x, y), o in zip(M['roof'], d['warp_events'][10:13]): W.append(warp(x, y, o['dest_map'], o['dest_warp_id'], o['elevation']))
assert len(W) == 13
def side(name, cells, first, other, x_expected):
    f2 = f'data/maps/{name}/map.json'; r = json.load(open(f2))
    lay = {'Route16': (48, 20), 'Route7': (24, 20)}[name]; g = grid(name, *lay)
    for (x, y) in cells: assert (g[y * lay[0] + x] & 0xc00) == 0, (name, x, y)
    kp = [w for w in r['warp_events'] if w['dest_map'] != 'MAP_CELADON_CITY']
    r['warp_events'] = kp + [warp(x, y, 'MAP_CELADON_CITY', first + i) for i, (x, y) in enumerate(cells)]
    r['connections'] = [c for c in r['connections'] if c['map'] != 'MAP_CELADON_CITY']
    r['object_events'] = [o for o in r['object_events'] if not (o.get('type') == 'clone' and o.get('target_map') == 'MAP_CELADON_CITY')]
    jdump(r, f2); return len(kp)
n16 = side('Route16', [(47, y - 10) for (_, y) in M['exitW']], 13, None, 47)
n7 = side('Route7', [(0, y - 10) for (_, y) in M['exitE']], 16, None, 0)
for i, (x, y) in enumerate(M['exitW']): W.append(warp(x, y, 'MAP_ROUTE16', n16 + i))
for i, (x, y) in enumerate(M['exitE']): W.append(warp(x, y, 'MAP_ROUTE7', n7 + i))
d['warp_events'] = W; d['connections'] = []
d['object_events'] = [o for o in d['object_events'] if o.get('type') != 'clone']
SC = {'RocketGrunt1': 'grunt1', 'FatMan': 'fat', 'Poliwrath': 'poli', 'LittleGirl': 'girl', 'Woman': 'woman', 'OldMan2': 'oldman2', 'SoftboiledTutor': 'tutor', 'RocketGrunt2': 'grunt2', 'OldMan1': 'oldman1', 'Boy': 'boy', 'ItemEther': 'ether', 'SilphCoScientist': 'scientist'}
trees = [o for o in d['object_events'] if o.get('script') == 'EventScript_CutTree']
assert len(trees) == 2
trees[0]['x'], trees[0]['y'] = N['tree1']; trees[1]['x'], trees[1]['y'] = N['tree2']
for o in d['object_events']:
    k = (o.get('script') or '').replace('CeladonCity_EventScript_', '')
    if k in SC: o['x'], o['y'] = N[SC[k]]
SG = {'CitySign': 'city', 'GymSign': 'gym', 'DeptStoreSign': 'dept', 'MansionSign': 'mansion', 'GameCornerSign': 'gamecorner', 'PrizeExchangeSign': 'prize', 'TrainerTips1': 'tips1', 'TrainerTips2': 'tips2'}
for b in d['bg_events']:
    if b['type'] == 'sign': b['x'], b['y'] = S[SG[b['script'].replace('CeladonCity_EventScript_', '')]]; b['elevation'] = 0
    elif b['type'] == 'hidden_item': b['x'], b['y'] = N['hidden']; b['elevation'] = 0
for o in d['object_events']: o['elevation'] = 0
jdump(d, f)
f = 'data/maps/CeladonCity/text.inc'; s = open(f).read()
s = s.replace('The City of Rainbow Dreams', 'The Amethyst Dream City'); open(f, 'w').write(s)
f = 'src/data/heal_locations.json'; h = json.load(open(f)); x, y = D['center'][0]
for e in h['heal_locations']:
    if e['id'] == 'HEAL_LOCATION_CELADON_CITY': e['x'], e['y'] = x, y + 1
jdump(h, f)
f = 'src/field_control_avatar.c'; s = open(f).read()
if 'LAYOUT_CELADON_CITY' not in s:
    s = s.replace('|| gMapHeader.mapLayoutId == LAYOUT_ROUTE8;', '|| gMapHeader.mapLayoutId == LAYOUT_ROUTE8 || gMapHeader.mapLayoutId == LAYOUT_CELADON_CITY || gMapHeader.mapLayoutId == LAYOUT_ROUTE16 || gMapHeader.mapLayoutId == LAYOUT_ROUTE7;', 1)
    assert 'LAYOUT_CELADON_CITY' in s; open(f, 'w').write(s)
print('evenements Celadopole ecrits', len(W), 'warps')
