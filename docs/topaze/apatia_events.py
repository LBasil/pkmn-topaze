# APATIA (ex-Vermilion, LAYOUT_VERMILION_CITY 48x40) : evenements. A lancer apres apatia_town.py. Idempotent.
# Les Routes 6 / 11 gardent leurs tilesets d'origine : plus de connexions de carte, pas simples (comme Celadopole / Spinellia).
# Les 10 warps d'origine (ponton x3, 7 batiments) ne bougent pas : les batiments sont conserves a leur place.
import json, struct
D = json.load(open('/tmp/apatia_doors.json')); N = json.load(open('/tmp/apatia_npc.json')); S = json.load(open('/tmp/apatia_signs.json')); M = json.load(open('/tmp/apatia_misc.json'))
def warp(x, y, dest, wid, el=0): return {"x": x, "y": y, "elevation": el, "dest_map": dest, "dest_warp_id": str(wid)}
def jdump(o, f): json.dump(o, open(f, 'w'), indent=2); open(f, 'a').write('\n')
def grid(n, w, h): return struct.unpack('<%dH' % (w * h), open('data/layouts/%s/map.bin' % n, 'rb').read())
f = 'data/maps/VermilionCity/map.json'; d = json.load(open(f))
base = [w for w in d['warp_events'] if w['dest_map'] not in ('MAP_ROUTE6', 'MAP_ROUTE11')]
assert len(base) == 10
for w in base:
    if w['dest_map'] == 'MAP_VERMILION_CITY_GYM': w['x'], w['y'] = D['gym'][0]          # l'arene est montee sur le plateau
def side(name, cells, first):
    f2 = f'data/maps/{name}/map.json'; r = json.load(open(f2)); lay = {'Route6': (24, 40), 'Route11': (72, 20)}[name]; g = grid(name, *lay)
    for (x, y) in cells: assert (g[y * lay[0] + x] & 0xc00) == 0, (name, x, y)
    kp = [w for w in r['warp_events'] if w['dest_map'] != 'MAP_VERMILION_CITY']
    r['warp_events'] = kp + [warp(x, y, 'MAP_VERMILION_CITY', first + i) for i, (x, y) in enumerate(cells)]
    r['connections'] = [c for c in r['connections'] if c['map'] != 'MAP_VERMILION_CITY']
    r['object_events'] = [o for o in r['object_events'] if not (o.get('type') == 'clone' and o.get('target_map') == 'MAP_VERMILION_CITY')]
    jdump(r, f2); return len(kp)
# connexions d'origine : Route 6 'down' offset -12 (route x = ville x - 12) ; Route 11 'left' offset -10 (route y = ville y - 10)
n6 = side('Route6', [(x - 12, 39) for (x, _) in M['exitN']], 10)
n11 = side('Route11', [(0, y - 10) for (_, y) in M['exitE']], 13)
W = list(base)
for i, (x, y) in enumerate(M['exitN']): W.append(warp(x, y, 'MAP_ROUTE6', n6 + i))
for i, (x, y) in enumerate(M['exitE']): W.append(warp(x, y, 'MAP_ROUTE11', n11 + i))
d['warp_events'] = W; d['connections'] = []
SC = {'Woman': 'woman', 'OldMan1': 'oldman1', 'OldMan2': 'oldman2', 'Machop': 'machop', 'Sailor': 'sailor', 'FerrySailor': 'ferry', 'OaksAide': 'aide'}
for o in d['object_events']:
    k = (o.get('script') or '').replace('VermilionCity_EventScript_', '')
    if k in SC: o['x'], o['y'] = N[SC[k]]
    elif o.get('script') == 'EventScript_CutTree': o['x'], o['y'] = N['tree']
SG = {'CitySign': 'city', 'HarborSign': 'harbor', 'SnorlaxNotice': 'notice', 'GymSign': 'gym'}
for b in d['bg_events']:
    k = (b.get('script') or '').replace('VermilionCity_EventScript_', '')
    if b['type'] == 'sign' and k in SG: b['x'], b['y'] = S[SG[k]]; b['elevation'] = 0
jdump(d, f)
f = 'src/field_control_avatar.c'; s = open(f).read()
if 'LAYOUT_VERMILION_CITY' not in s:
    s = s.replace('|| gMapHeader.mapLayoutId == LAYOUT_ROUTE7;', '|| gMapHeader.mapLayoutId == LAYOUT_ROUTE7 || gMapHeader.mapLayoutId == LAYOUT_VERMILION_CITY || gMapHeader.mapLayoutId == LAYOUT_ROUTE6 || gMapHeader.mapLayoutId == LAYOUT_ROUTE11;', 1)
    assert 'LAYOUT_VERMILION_CITY' in s; open(f, 'w').write(s)
print('evenements Apatia ecrits', len(W), 'warps')
