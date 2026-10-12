# AMETHIOLITE (ex-Parmanie, LAYOUT_FUCHSIA_CITY) : evenements. A lancer apres amethiolite_town.py. Idempotent.
# Ordre complet : amethiolite_town -> amethiolite_events -> route20_events (recompose les warps de la Route 19).
import json, re
D = json.load(open('/tmp/amethiolite_doors.json')); N = json.load(open('/tmp/amethiolite_npc.json'))
S = json.load(open('/tmp/amethiolite_signs.json')); M = json.load(open('/tmp/amethiolite_misc.json'))
def warp(x, y, dest, wid, el=0): return {"x": x, "y": y, "elevation": el, "dest_map": dest, "dest_warp_id": str(wid)}
def jdump(o, f): json.dump(o, open(f, 'w'), indent=2); open(f, 'a').write('\n')
f = 'data/maps/FuchsiaCity/map.json'; d = json.load(open(f))
C = 'MAP_FUCHSIA_CITY_'
orig = [dict(dest_map=C + m, dest_warp_id=i) for m, i in (('SAFARI_ZONE_ENTRANCE', 2), ('WARDENS_HOUSE', 1), ('MART', 1), ('SAFARI_ZONE_OFFICE', 1), ('GYM', 1), ('HOUSE1', 1), ('POKEMON_CENTER_1F', 1), ('HOUSE2', 1), ('HOUSE2', 3), ('HOUSE2', 3), ('HOUSE3', 0))]   # warps d'origine
ORDER = ['safari', 'warden', 'mart', 'office', 'gym', 'house1', 'center', 'house2', 'house3']
OLD = [0, 1, 2, 3, 4, 5, 6, 7, 10]                  # ancien index -> nouvel index (8,9 : portes arrieres de la maison 2, supprimees)
W = []
for k, oi in zip(ORDER, OLD):
    o = orig[oi]; W.append(warp(D[k][0][0], D[k][0][1], o['dest_map'], o['dest_warp_id']))
SX = [x for x in range(20, 28)]; WY = [13, 14, 15]; EY = [13, 14, 15]; HB = 31          # sorties ouest / est : y de la ville ; Route 18 : y8..10, Route 15 : y10..12
base = len(W)
for i, x in enumerate(SX): W.append(warp(x, HB, 'MAP_ROUTE19', i))
for i, y in enumerate(WY): W.append(warp(0, y, 'MAP_ROUTE18', None))
for i, y in enumerate(EY): W.append(warp(47, y, 'MAP_ROUTE15', None))
# Route 19 : liens vers la ville EN PREMIER (route20_events ajoute ensuite ceux de la Route 20)
r19 = json.load(open('data/maps/Route19/map.json'))
keep = [w for w in r19['warp_events'] if w['dest_map'] != 'MAP_FUCHSIA_CITY']
r19['warp_events'] = [warp(x - 12, 0, 'MAP_FUCHSIA_CITY', base + i) for i, x in enumerate(SX)] + keep
r19['connections'] = [c for c in r19['connections'] if c['map'] != 'MAP_FUCHSIA_CITY']
jdump(r19, 'data/maps/Route19/map.json')
def side(name, ys_city, x_route, ys_route, first_idx):
    f2 = f'data/maps/{name}/map.json'; r = json.load(open(f2))
    kp = [w for w in r['warp_events'] if w['dest_map'] != 'MAP_FUCHSIA_CITY']
    r['warp_events'] = kp + [warp(x_route, ys_route[i], 'MAP_FUCHSIA_CITY', first_idx + i) for i, y in enumerate(ys_city)]
    r['connections'] = [c for c in r['connections'] if c['map'] != 'MAP_FUCHSIA_CITY']
    jdump(r, f2); return len(kp)
k18 = side('Route18', WY, 59, [8, 9, 10], base + len(SX)); k15 = side('Route15', EY, 0, [10, 11, 12], base + len(SX) + len(WY))
for i in range(len(WY)): W[base + len(SX) + i]['dest_warp_id'] = str(k18 + i)
for i in range(len(EY)): W[base + len(SX) + len(WY) + i]['dest_warp_id'] = str(k15 + i)
W.append(warp(D['safari'][1][0], D['safari'][1][1], orig[0]['dest_map'], orig[0]['dest_warp_id']))          # l'arche du Safari fait 2 cases de large
W.append(warp(D['gym'][1][0], D['gym'][1][1], orig[4]['dest_map'], orig[4]['dest_warp_id']))          # v7 : la porte de l'arene fait 2 cases de large (arche du monument)
d['warp_events'] = W; d['connections'] = []
# ---- PNJ, panneaux, objet cache
POS = {'FAT_MAN': 'erik', 'SLOWPOKE': 'pen_slowpoke', 'VOLTORB': 'pen_voltorb', 'YOUNGSTER': 'youngster', 'CHANSEY': 'pen_chansey', 'LITTLE_BOY': 'littleboy', 'LAPRAS': 'pen_lapras',
       'OLD_MAN_1': 'oldman', 'VAR_0': 'pen_fossil', 'KANGASKHAN': 'pen_kangaskhan', 'BUG_CATCHER': 'tutor', 'LASS': 'lass'}
trees = iter(['tree1', 'tree2', 'tree3', 'tree4'])
for o in d['object_events']:
    g = o['graphics_id'].replace('OBJ_EVENT_GFX_', '')
    key = next(trees) if g == 'CUT_TREE' else POS[g]
    o['x'], o['y'] = N[key]
SG = {'CitySign': 'city', 'SafariZoneSign': 'safarizone', 'GymSign': 'gym', 'WardensHomeSign': 'warden', 'VoltorbSign': 'pen_voltorb', 'SlowpokeSign': 'pen_slowpoke', 'ChanseySign': 'pen_chansey',
      'KangaskhanSign': 'pen_kangaskhan', 'FossilMonSign': 'pen_fossil', 'LaprasSign': 'pen_lapras', 'SafariGameSign': 'safarigame'}
for b in d['bg_events']:
    if b['type'] == 'sign': b['x'], b['y'] = S[SG[b['script'].split('_')[-1]]]
    elif b['type'] == 'hidden_item': b['x'], b['y'] = N['hidden']
jdump(d, f)
# ---- interieurs : la maison 2 n'a plus de porte arriere (ses sorties renvoient toutes a la porte avant), la maison 3 passe de l'index 10 a 8
h2 = json.load(open('data/maps/FuchsiaCity_House2/map.json'))
for w in h2['warp_events']:
    if w['dest_map'] == 'MAP_FUCHSIA_CITY': w['dest_warp_id'] = '7'
jdump(h2, 'data/maps/FuchsiaCity_House2/map.json')
h3 = json.load(open('data/maps/FuchsiaCity_House3/map.json'))
for w in h3['warp_events']:
    if w['dest_map'] == 'MAP_FUCHSIA_CITY': w['dest_warp_id'] = '8'
jdump(h3, 'data/maps/FuchsiaCity_House3/map.json')
# ---- texte du panneau, reapparition
f = 'data/maps/FuchsiaCity/text.inc'; s = open(f).read()
s = re.sub(r'(FuchsiaCity_Text_CitySign::\n).*?\$"', r'\1    .string "AMETHIOLITE CITY\\n"\n    .string "The Amethyst Lake Town$"', s, count=1, flags=re.S); open(f, 'w').write(s)
f = 'src/data/heal_locations.h'; s = open(f).read(); x, y = D['center'][0]
s = re.sub(r'(HEAL_LOCATION_FUCHSIA_CITY - 1\] = \{.*?\.x = )\d+(,\s*\.y = )\d+', r'\g<1>%d\g<2>%d' % (x, y + 1), s, count=1, flags=re.S); open(f, 'w').write(s)
# ---- pas simples
f = 'src/field_control_avatar.c'; s = open(f).read()
if 'LAYOUT_FUCHSIA_CITY' not in s:
    s = s.replace('|| gMapHeader.mapLayoutId == LAYOUT_ROUTE20', '|| gMapHeader.mapLayoutId == LAYOUT_ROUTE20 || gMapHeader.mapLayoutId == LAYOUT_FUCHSIA_CITY || gMapHeader.mapLayoutId == LAYOUT_ROUTE18 || gMapHeader.mapLayoutId == LAYOUT_ROUTE15', 1)
    open(f, 'w').write(s)
print('evenements Amethiolite ecrits', len(W), 'warps')
