#!/usr/bin/env python3
"""Branche la centrale v2 : map.bin, layouts.json, map.json (warps, objets, panneaux), scripts. A lancer apres centrale_v2.py (importe)."""
import sys, json, struct, re
sys.path.insert(0, 'docs/topaze')
import centrale_v2 as c
NAMES = {'1F': 'PokemonMansion_1F', '2F': 'PokemonMansion_2F', '3F': 'PokemonMansion_3F', 'B1F': 'PokemonMansion_B1F'}
floors = c.build_all()
# layouts.json
lj = json.load(open('data/layouts/layouts.json'))
for l in lj['layouts']:
    for n, m in floors.items():
        if l.get('id') == 'LAYOUT_POKEMON_MANSION_' + n:
            l['width'], l['height'] = m.w, m.h; l['secondary_tileset'] = 'gTileset_PowerPlant'
json.dump(lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
for n, m in floors.items():
    open('data/layouts/%s/map.bin' % NAMES[n], 'wb').write(struct.pack('<%dH' % (m.w * m.h), *[v for r in m.g for v in r]))
def W(x, y, dest, wid, el=0): return {'x': x, 'y': y, 'elevation': el, 'dest_map': dest, 'dest_warp_id': str(wid)}
def pad(m, dest, wid):
    px, py = m.pads[0]; return [W(px, py, dest, wid)]
WARPS = {
 '1F': [W(5, 24, 'MAP_POKEMON_MANSION_3F', 0), W(16, 24, 'MAP_CINNABAR_ISLAND', 0), W(28, 24, 'MAP_POKEMON_MANSION_2F', 0)] + pad(floors['1F'], 'MAP_POKEMON_MANSION_B1F', 0),
 '2F': [W(11, 12, 'MAP_POKEMON_MANSION_1F', 2)],
 '3F': [W(12, 16, 'MAP_POKEMON_MANSION_1F', 0)],
 'B1F': pad(floors['B1F'], 'MAP_POKEMON_MANSION_1F', 3)}
# objets : script -> (x, y, mouvement)
POS = {
 '1F': {'PokemonMansion_1F_EventScript_Ted': (12, 10, 'DOWN'), 'PokemonMansion_1F_EventScript_Johnson': (24, 22, 'LEFT')},
 '2F': {'PokemonMansion_2F_EventScript_Arnie': (6, 11, 'RIGHT')},
 '3F': {'PokemonMansion_3F_EventScript_Simon': (18, 8, 'LEFT'), 'PokemonMansion_3F_EventScript_Braydon': (8, 12, 'RIGHT')},
 'B1F': {'PokemonMansion_B1F_EventScript_Lewis': (14, 9, 'DOWN'), 'PokemonMansion_B1F_EventScript_Ivan': (8, 18, 'RIGHT')}}
BALLS = {  # flag -> (x, y)
 'FLAG_HIDE_POKEMON_MANSION_1F_CARBOS': (4, 4), 'FLAG_HIDE_POKEMON_MANSION_1F_ESCAPE_ROPE': (31, 9), 'FLAG_HIDE_POKEMON_MANSION_1F_PROTEIN': (3, 23),
 'FLAG_HIDE_POKEMON_MANSION_2F_CALCIUM': (19, 4), 'FLAG_HIDE_POKEMON_MANSION_2F_ZINC': (20, 11), 'FLAG_HIDE_POKEMON_MANSION_2F_HP_UP': (1, 12),
 'FLAG_HIDE_POKEMON_MANSION_3F_MAX_POTION': (24, 4), 'FLAG_HIDE_POKEMON_MANSION_3F_IRON': (24, 12),
 'FLAG_HIDE_POKEMON_MANSION_B1F_TM22': (2, 4), 'FLAG_HIDE_POKEMON_MANSION_B1F_TM14': (25, 4), 'FLAG_HIDE_POKEMON_MANSION_B1F_FULL_RESTORE': (3, 12),
 'FLAG_HIDE_POKEMON_MANSION_B1F_SECRET_KEY': (2, 18)}
SIGNS = {'PokemonMansion_2F_EventScript_DiaryJuly5th': (4, 7), 'PokemonMansion_2F_EventScript_DiaryJuly10th': (10, 7),
         'PokemonMansion_3F_EventScript_DiaryFeb6th': (5, 7), 'PokemonMansion_B1F_EventScript_DiarySep1st': (5, 14)}
HIDDEN = {'FLAG_HIDDEN_ITEM_POKEMON_MANSION_3F_RARE_CANDY': (1, 12), 'FLAG_HIDDEN_ITEM_POKEMON_MANSION_B1F_ELIXIR': (26, 12), 'FLAG_HIDDEN_ITEM_POKEMON_MANSION_1F_MOON_STONE': (2, 12)}
for n, nm in NAMES.items():
    f = 'data/maps/%s/map.json' % nm; mj = json.load(open(f)); m = floors[n]
    mj['warp_events'] = WARPS[n]
    for o in mj['object_events']:
        if o.get('script') in POS[n]:
            x, y, d = POS[n][o['script']]; o['x'], o['y'] = x, y; o['movement_type'] = 'MOVEMENT_TYPE_FACE_' + d
        elif o.get('flag') in BALLS: o['x'], o['y'] = BALLS[o['flag']]
        else: print('objet non place', n, o.get('script'))
    bg = []
    for b in mj['bg_events']:
        if b.get('script', '').endswith('_Statue'): continue
        if b.get('script') in SIGNS: b['x'], b['y'] = SIGNS[b['script']]
        elif b.get('flag') in HIDDEN: b['x'], b['y'] = HIDDEN[b['flag']]
        bg.append(b)
    mj['bg_events'] = bg
    for o in mj['object_events'] + mj['bg_events']:
        if 'x' in o and (m.blocked(o['x'], o['y']) and o['type'] != 'sign'): print('!! sur case bloquee', n, o)
    json.dump(mj, open(f, 'w'), indent=2); open(f, 'a').write('\n')
    # scripts : plus de puzzle des statues
    sf = 'data/maps/%s/scripts.inc' % nm; s = open(sf).read()
    s = re.sub(r'\tmap_script MAP_SCRIPT_ON_LOAD, \w+\n', '', s)
    s = re.sub(r'\w+_OnLoad::\n.*?\tend\n\n?', '', s, flags=re.S)
    s = re.sub(r'\w+_EventScript_Statue::\n.*?\tend\n\n?', '', s, flags=re.S)
    open(sf, 'w').write(s)
print('ok')
