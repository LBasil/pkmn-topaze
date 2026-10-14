#!/usr/bin/env python3
"""Maisons « décoratives » rendues enterrables : 4 intérieurs génériques (GenericHouse_A..D) dont les sorties sont des warps
MAP_DYNAMIC (le moteur mémorise la porte d'entrée), + un warp sur chaque porte (comportement MB_WARP_DOOR) sans warp dans les
villes/routes. NON rejouable (git checkout data docs avant de relancer). Voir docs/topaze/audit_doors.py."""
import json, re, sys, struct, glob, os
sys.path[:0] = ['/tmp/gx', 'docs/topaze', 'tools/topaze/maps']
import route_test as R
rd = lambda p: open(p).read(); wr = lambda p, s: open(p, 'w').write(s)
def save(p, m): json.dump(m, open(p, 'w'), indent=2); open(p, 'a').write('\n')
def box(label, boxes):
    out = label + '::\n'
    for bi, bx in enumerate(boxes):
        for li, l in enumerate(bx):
            assert len(re.sub(r'\{[^}]*\}', 'X', l)) <= 35, (len(l), l)
            ll = li == len(bx) - 1; lb = bi == len(boxes) - 1
            out += '    .string "' + l + ('$' if ll and lb else '\\p' if ll else '\\n') + '"\n'
    return out

TPL = {'A': 'CeruleanCity_House3', 'B': 'PewterCity_House1', 'C': 'FiveIsland_House1', 'D': 'CeladonCity_House1'}
EXTRA = {'D': [('OBJ_EVENT_GFX_WOMAN_1', 8, 4)]}
SKIP = ('OBJ_EVENT_GFX_NIDORAN_M', 'OBJ_EVENT_GFX_ROCKET_M')
CHILD = ('OBJ_EVENT_GFX_LITTLE_BOY', 'OBJ_EVENT_GFX_LITTLE_GIRL', 'OBJ_EVENT_GFX_BOY')
ADULT_T = [
 [['Come in, come in! Careful with the', 'rug.'], ['Since the AURA, even my slippers', 'change color. I am not joking.']],
 [['Our town is quiet. Too quiet.'], ['TEAM ONYBRIS only wants the stones,', 'they say. That worries me more.']],
 [['My husband says types are just', 'labels. I say they are habits.'], ['And habits can change, dear.']],
 [['Is it true GRENAT came from the old', 'mine? My grandfather swore it.']],
 [['A trainer! Look after your partner.', 'They remember every kindness.']],
 [['I would offer tea, but the kettle', 'is sulking. WATER type now.']],
]
CHILD_T = [
 [['I saw a trainer beat a whole gym', 'with ONE POKéMON!']],
 [['Mom says never touch the shiny', 'rocks. I touched one. It tickled.']],
 [['When I grow up I will study the', 'AURA, like the teacher!']],
 [['Shh! My POKéMON is hiding. It is', 'bad at hide and seek.']],
 [['Do you have a POKéDEX? Can I see?', 'No? Okay.']],
 [['I drew a new type. It beats', 'everything. Don\'t tell the teacher.']],
]
# ---- layout / maps
g = json.load(open('data/maps/map_groups.json'))
names = {k: 'GenericHouse_' + k for k in TPL}
g['gMapGroup_IndoorPallet'] += list(names.values()); save('data/maps/map_groups.json', g)
for k, tm in TPL.items():
    t = json.load(open('data/maps/%s/map.json' % tm)); n = names[k]
    objs = []
    for o in t['object_events']:
        if o['graphics_id'] in SKIP: continue
        objs.append((o['graphics_id'], o['x'], o['y']))
    objs += EXTRA.get(k, [])
    eo = []
    for i, (gfx, x, y) in enumerate(objs):
        role = 'Child' if gfx in CHILD else 'Resident'
        eo.append({"type": "object", "graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": "MOVEMENT_TYPE_FACE_DOWN", "movement_range_x": 0, "movement_range_y": 0,
                   "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0", "script": 'GenericHouse_A_EventScript_' + role, "flag": "0"})
    m = {kk: vv for kk, vv in t.items() if kk not in ('object_events', 'warp_events', 'coord_events', 'bg_events', 'connections')}
    m['id'] = 'MAP_GENERIC_HOUSE_' + k; m['name'] = n; m['connections'] = None
    m['object_events'] = eo
    m['warp_events'] = [dict(x=w['x'], y=w['y'], elevation=0, dest_map='MAP_DYNAMIC', dest_warp_id='0') for w in t['warp_events']]
    m['coord_events'] = []; m['bg_events'] = []
    os.makedirs('data/maps/' + n, exist_ok=True); save('data/maps/%s/map.json' % n, m)
    body = n + '_MapScripts::\n\t.byte 0\n'
    if k == 'A':
        body += '\nGenericHouse_A_EventScript_Resident::\n\tlock\n\tfaceplayer\n\trandom %d\n\tswitch VAR_RESULT\n' % len(ADULT_T)
        body += ''.join('\tcase %d, GenericHouse_A_EventScript_Adult%d\n' % (i, i) for i in range(len(ADULT_T))) + '\tend\n\n'
        for i in range(len(ADULT_T)): body += 'GenericHouse_A_EventScript_Adult%d::\n\tmsgbox GenericHouse_A_Text_Adult%d\n\trelease\n\tend\n\n' % (i, i)
        body += 'GenericHouse_A_EventScript_Child::\n\tlock\n\tfaceplayer\n\trandom %d\n\tswitch VAR_RESULT\n' % len(CHILD_T)
        body += ''.join('\tcase %d, GenericHouse_A_EventScript_Kid%d\n' % (i, i) for i in range(len(CHILD_T))) + '\tend\n\n'
        for i in range(len(CHILD_T)): body += 'GenericHouse_A_EventScript_Kid%d::\n\tmsgbox GenericHouse_A_Text_Kid%d\n\trelease\n\tend\n\n' % (i, i)
        txt = ''.join(box('GenericHouse_A_Text_Adult%d' % i, b) + '\n' for i, b in enumerate(ADULT_T)) + ''.join(box('GenericHouse_A_Text_Kid%d' % i, b) + '\n' for i, b in enumerate(CHILD_T))
    else: txt = ''
    wr('data/maps/%s/scripts.inc' % n, body); wr('data/maps/%s/text.inc' % n, txt)
s = rd('data/event_scripts.s')
for kind in ('scripts', 'text'):
    anchor = '\t.include "data/maps/GrenaluxMine_3F/%s.inc"\n' % kind
    assert anchor in s
    s = s.replace(anchor, anchor + ''.join('\t.include "data/maps/%s/%s.inc"\n' % (n, kind) for n in names.values()), 1)
wr('data/event_scripts.s', s)

# ---- doors without a warp
DOORS = {0x69}
cnt = 0; idx = 0
for d in sorted(glob.glob('data/maps/*/map.json')):
    name = d.split('/')[2]
    if name.startswith('GenericHouse'): continue
    try: nav = R.Nav(name)
    except Exception: continue
    mj = json.load(open(d))
    if mj.get('map_type') not in ('MAP_TYPE_TOWN', 'MAP_TYPE_CITY', 'MAP_TYPE_ROUTE'): continue
    signs = {(b['x'], b['y']) for b in mj.get('bg_events', [])}
    miss = [(x, y) for y in range(nav.h) for x in range(nav.w) if (nav.attr(x, y) & 0x1ff) in DOORS and (x, y) not in nav.warps and (x, y) not in signs]
    if not miss: continue
    lid = mj['layout']; L = json.load(open('data/layouts/layouts.json'))['layouts']; l = [z for z in L if z.get('id') == lid][0]
    v = list(struct.unpack('<%dH' % (l['width'] * l['height']), open(l['blockdata_filepath'], 'rb').read()))
    for (x, y) in miss:
        k = 'ABCD'[idx % 4]; idx += 1
        v[y * l['width'] + x] &= ~0x0C00                      # la porte devient franchissable
        mj['warp_events'].append({"x": x, "y": y, "elevation": 0, "dest_map": "MAP_GENERIC_HOUSE_" + k, "dest_warp_id": "0"}); cnt += 1
    open(l['blockdata_filepath'], 'wb').write(struct.pack('<%dH' % len(v), *v)); save(d, mj)
    print(name, len(miss))
print('doors fixed', cnt)
