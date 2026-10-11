# CHRONDROLIA (ex-Cinnabar, LAYOUT_CINNABAR_ISLAND) : evenements. A lancer apres chrondrolia_town.py. Idempotent.
# Warps 0..4 = manoir, arene, labo, centre, boutique (ordre conserve : les interieurs y renvoient). Warps 5+ = mer (Route 21 au nord, Route 20 a l'est).
import json, re, struct
D = json.load(open('/tmp/chrondrolia_doors.json')); N = json.load(open('/tmp/chrondrolia_npc.json'))
S = json.load(open('/tmp/chrondrolia_signs.json')); M = json.load(open('/tmp/chrondrolia_misc.json'))
Wd, Ht = 28, 20
def warp(x, y, dest, wid, el=0): return {"x": x, "y": y, "elevation": el, "dest_map": dest, "dest_warp_id": str(wid)}
def jdump(o, f): json.dump(o, open(f, 'w'), indent=2); open(f, 'a').write('\n')
# ---- cases de mer au bord de la carte
lay = {l.get('id'): l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id')}
g = struct.unpack('<%dH' % (Wd * Ht), open('data/layouts/CinnabarIsland/map.bin', 'rb').read())
def is_sea(x, y): return (g[y * Wd + x] >> 12) == 1 and (g[y * Wd + x] & 0xc00) == 0 and (x, y) not in {tuple(p) for p in M['pier1'] + M['pier2']}
R21W = list(range(0, 5)) + list(range(14, 24))              # Route 21 Sud : cases d'eau de la rangee du bas (meme largeur 24 : x identique)
NORTH = [x for x in R21W if is_sea(x, 0)]
EAST = [y for y in range(Ht) if is_sea(Wd - 1, y)]            # Route 20 : colonne x=0, meme hauteur 20 : y identique
assert NORTH == R21W and len(EAST) >= 8, (NORTH, EAST)
# ---- Chrondrolia
W = [None] * 5
W[0] = warp(*D['mansion'][0], 'MAP_POKEMON_MANSION_1F', 1); W[1] = warp(*D['gym'][0], 'MAP_CINNABAR_ISLAND_GYM', 1)
W[2] = warp(*D['lab'][0], 'MAP_CINNABAR_ISLAND_POKEMON_LAB_ENTRANCE', 1); W[3] = warp(*D['center'][0], 'MAP_CINNABAR_ISLAND_POKEMON_CENTER_1F', 0)
W[4] = warp(*D['mart'][0], 'MAP_CINNABAR_ISLAND_MART', 1)
W.append(warp(*D['house'][0], 'MAP_ROUTE19_UNUSED_HOUSE', 0))        # warp 5 : maison des habitants (interieur recycle : Route19_UnusedHouse)
HB = 6
f = 'data/maps/CinnabarIsland/map.json'; d = json.load(open(f))
r = json.load(open('data/maps/Route21_South/map.json'))
keep21 = [w for w in r['warp_events'] if w['dest_map'] != 'MAP_CINNABAR_ISLAND']; base21 = len(keep21)
r['warp_events'] = keep21 + [warp(x, 49, 'MAP_CINNABAR_ISLAND', HB + NORTH.index(x)) for x in NORTH]
r['connections'] = [cn for cn in r['connections'] if cn['map'] != 'MAP_CINNABAR_ISLAND']
jdump(r, 'data/maps/Route21_South/map.json')
for x in NORTH: W.append(warp(x, 0, 'MAP_ROUTE21_SOUTH', base21 + NORTH.index(x)))
r = json.load(open('data/maps/Route20/map.json'))
keep20 = [w for w in r['warp_events'] if w['dest_map'] != 'MAP_CINNABAR_ISLAND']; base20 = len(keep20)
e0 = HB + len(NORTH)
r['warp_events'] = keep20 + [warp(0, y, 'MAP_CINNABAR_ISLAND', e0 + EAST.index(y)) for y in EAST]
r['connections'] = [cn for cn in r['connections'] if cn['map'] != 'MAP_CINNABAR_ISLAND']
jdump(r, 'data/maps/Route20/map.json')
for y in EAST: W.append(warp(Wd - 1, y, 'MAP_ROUTE20', base20 + EAST.index(y)))
d['warp_events'] = W; d['connections'] = []
# ---- interieur de la maison (Route19_UnusedHouse recyclee)
h = json.load(open('data/maps/Route19_UnusedHouse/map.json'))
h.update(region_map_section='MAPSEC_CINNABAR_ISLAND', music='MUS_CINNABAR', show_map_name=True)
h['warp_events'] = [warp(x, 7, 'MAP_CINNABAR_ISLAND', 5) for x in (3, 4, 5)]
ob = lambda g, x, y, mv, sc: {"type": "object", "graphics_id": g, "x": x, "y": y, "elevation": 3, "movement_type": mv, "movement_range_x": 1, "movement_range_y": 1,
                              "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0", "script": sc, "flag": "0"}
h['object_events'] = [ob('OBJ_EVENT_GFX_OLD_MAN_1', 2, 2, 'MOVEMENT_TYPE_FACE_DOWN', 'Route19_UnusedHouse_EventScript_Engineer'),
                      ob('OBJ_EVENT_GFX_LITTLE_GIRL', 6, 4, 'MOVEMENT_TYPE_LOOK_AROUND', 'Route19_UnusedHouse_EventScript_Girl')]
jdump(h, 'data/maps/Route19_UnusedHouse/map.json')
open('data/maps/Route19_UnusedHouse/scripts.inc', 'w').write('''Route19_UnusedHouse_MapScripts::
	.byte 0

Route19_UnusedHouse_EventScript_Engineer::
	msgbox Route19_UnusedHouse_Text_Engineer, MSGBOX_NPC
	end

Route19_UnusedHouse_EventScript_Girl::
	msgbox Route19_UnusedHouse_Text_Girl, MSGBOX_NPC
	end
''')
open('data/maps/Route19_UnusedHouse/text.inc', 'w').write('''Route19_UnusedHouse_Text_Engineer::
    .string "I keep the PLANT running. Every pylon\\n"
    .string "on this island is wired to it.\\p"
    .string "The aura that scrambled the types ten\\n"
    .string "years ago? It never touched the grid.\\p"
    .string "If anything, the TOPAZ hums louder\\n"
    .string "ever since.$"

Route19_UnusedHouse_Text_Girl::
    .string "My dad says the lights never went out,\\n"
    .string "not even once.\\p"
    .string "The gym leader is the only one who\\n"
    .string "can make them flicker!$"
''')
f2 = 'data/event_scripts.s'; t = open(f2).read()
if 'Route19_UnusedHouse/text.inc' not in t:
    t = t.replace('\t.include "data/maps/Route19_UnusedHouse/scripts.inc"\n', '\t.include "data/maps/Route19_UnusedHouse/scripts.inc"\n\t.include "data/maps/Route19_UnusedHouse/text.inc"\n'); open(f2, 'w').write(t)
# ---- PNJ
pos = {'OBJ_EVENT_GFX_WOMAN_2': N['woman'], 'OBJ_EVENT_GFX_OLD_MAN_1': N['oldman'], 'OBJ_EVENT_GFX_BILL': N['bill'], 'OBJ_EVENT_GFX_SEAGALLOP': N['gull']}
for o in d['object_events']: o['x'], o['y'] = pos[o['graphics_id']]
for cev in d['coord_events']: cev['x'], cev['y'] = D['gym'][0][0], D['gym'][0][1] + 1
nl = 0; bg = []
for b in d['bg_events']:
    if b['type'] == 'sign':
        s_ = b['script']
        if 'PokemonLabSign' in s_:
            nl += 1
            if nl > 1: continue                       # un seul panneau pour le labo
        b['x'], b['y'] = S['city'] if 'IslandSign' in s_ else S['gym'] if 'GymSign' in s_ else S['lab']
    bg.append(b)
d['bg_events'] = bg
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
