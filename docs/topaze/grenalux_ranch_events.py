# Grand ranch de Grenalux : carte PalletTown_Ranch (PNJ, textes, connexions). A lancer apres grenalux_town.py. Idempotent.
import json, re
NPC = json.load(open('/tmp/grenalux_ranch_npc.json'))
M = 'PalletTown_Ranch'
AMB = [  # cle, gfx, mouvement, texte avant, texte apres l'attaque (ou None)
 ('hand1', 'WORKER_M', 'FACE_DOWN', ['This ranch runs from the town wall', 'to the far fences. It takes ten of', 'us to look after it all.'],
  ['The east fence was cut last night.', 'On a ranch this big, no one saw.']),
 ('hand2', 'CAMPER', 'FACE_LEFT', ['The east pasture is so far out, we', 'only check it twice a day.'],
  ['They took the tracker POKéMON from', 'the pens. The fence was cut open.']),
 ('girl', 'LITTLE_GIRL', 'WANDER_AROUND', ['I came to help, but I got lost', 'twice. The ranch is HUGE!'], None),
 ('slowpoke', 'SLOWPOKE', 'WANDER_AROUND', ['SLOWPOKE: ...Yawn.'], None),
 ('psyduck', 'PSYDUCK', 'WANDER_AROUND', ['PSYDUCK: Gwaa?', 'It looks like it has a headache.'], None),
 ('hand3', 'WORKER_M', 'FACE_RIGHT', ['The pens were shut tight last night.', 'Now look at this fence...'], None),
 ('doduo', 'DODUO', 'WANDER_AROUND', ['DODUO: Kwek! Kwek!', 'Its two heads argue about the hay.'], None),
 ('nidoranm', 'NIDORAN_M', 'WANDER_AROUND', ['NIDORAN: Gyuu!', 'Its ears twitch at every sound.'], None),
 ('nidoranf', 'NIDORAN_F', 'WANDER_AROUND', ['NIDORAN: Kyuu!', 'It nibbles the garnet-dusted grass.'], None),
 ('meowth', 'MEOWTH', 'WANDER_AROUND', ['MEOWTH: Nyaa!', 'It keeps the barn free of mice.'], None),
 ('jigglypuff', 'JIGGLYPUFF', 'WANDER_AROUND', ['JIGGLYPUFF: Jiggly...', 'It hums softly to the other animals.'], None)]
FLAGS = {'doduo': 'FLAG_GRENALUX_ONYBRIS_STRIKE', 'nidoranm': 'FLAG_GRENALUX_ONYBRIS_STRIKE', 'nidoranf': 'FLAG_GRENALUX_ONYBRIS_STRIKE', 'hand3': 'FLAG_HIDE_RANCH_CUT_HAND'}
def strs(lines): return ''.join('\t.string "%s%s"\n' % (l, '$' if i == len(lines) - 1 else '\\n') for i, l in enumerate(lines))
objs = []; scr = '''%s_MapScripts::
\tmap_script MAP_SCRIPT_ON_TRANSITION, %s_OnTransition
\tmap_script MAP_SCRIPT_ON_LOAD, %s_OnLoad
\t.byte 0

%s_OnTransition::
\tgoto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, %s_ShowHand
\tsetflag FLAG_HIDE_RANCH_CUT_HAND
\tend

%s_ShowHand::
\tclearflag FLAG_HIDE_RANCH_CUT_HAND
\tend

%s_OnLoad::
\tgoto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, %s_CutFence
\tend

%s_CutFence::
\tsetmetatile 27, 13, 0x001, FALSE
\tsetmetatile 27, 14, 0x001, FALSE
\tend
''' % ((M,) * 9); txt = ''
for key, gfx, mv, before, after in AMB:
    for l in before + (after or []): assert len(l) <= 36, l
    n = key.title(); x, y = NPC['r_' + key]
    objs.append({"local_id": "LOCALID_PALLET_RANCH_" + key.upper(), "type": "object", "graphics_id": "OBJ_EVENT_GFX_" + gfx, "x": x, "y": y, "elevation": 3,
                 "movement_type": "MOVEMENT_TYPE_" + mv, "movement_range_x": 1, "movement_range_y": 1, "trainer_type": "TRAINER_TYPE_NONE",
                 "trainer_sight_or_berry_tree_id": "0", "script": "%s_EventScript_%s" % (M, n), "flag": FLAGS.get(key, "0")})
    if after:
        scr += '\n%s_EventScript_%s::\n\tgoto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, %s_EventScript_%sStrike\n\tmsgbox %s_Text_%s, MSGBOX_NPC\n\tend\n' % (M, n, M, n, M, n)
        scr += '\n%s_EventScript_%sStrike::\n\tmsgbox %s_Text_%sStrike, MSGBOX_NPC\n\tend\n' % (M, n, M, n)
        txt += '\n%s_Text_%sStrike::\n%s' % (M, n, strs(after))
    else:
        scr += '\n%s_EventScript_%s::\n\tmsgbox %s_Text_%s, MSGBOX_NPC\n\tend\n' % (M, n, M, n)
    txt += '\n%s_Text_%s::\n%s' % (M, n, strs(before))
import os
os.makedirs('data/maps/' + M, exist_ok=True)
open('data/maps/%s/scripts.inc' % M, 'w').write(scr); open('data/maps/%s/text.inc' % M, 'w').write(txt.lstrip('\n'))
scr += '\n%s_EventScript_BarnDoor::\n\tmsgbox %s_Text_BarnDoor, MSGBOX_SIGN\n\tend\n' % (M, M)
txt += '\n%s_Text_BarnDoor::\n%s' % (M, strs(['The barn door is bolted shut.', 'Feed and tools are stored inside.']))
open('data/maps/%s/scripts.inc' % M, 'w').write(scr); open('data/maps/%s/text.inc' % M, 'w').write(txt.lstrip('\n'))
d = {"id": "MAP_PALLET_TOWN_RANCH", "name": M, "layout": "LAYOUT_PALLET_TOWN_RANCH", "music": "MUS_PALLET", "region_map_section": "MAPSEC_PALLET_TOWN",
     "requires_flash": False, "weather": "WEATHER_SUNNY", "map_type": "MAP_TYPE_TOWN", "allow_cycling": True, "allow_escaping": False,
     "allow_running": True, "show_map_name": False, "floor_number": 0, "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
     "connections": [{"map": "MAP_PALLET_TOWN", "offset": 0, "direction": "left"}],
     "object_events": objs, "warp_events": [], "coord_events": [], "bg_events": [{"type": "sign", "x": 24, "y": 5, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": "%s_EventScript_BarnDoor" % M}]}
json.dump(d, open('data/maps/%s/map.json' % M, 'w'), indent=2); open('data/maps/%s/map.json' % M, 'a').write('\n')
# ville : connexion vers le ranch
f = 'data/maps/PalletTown/map.json'; t = json.load(open(f))
t['connections'] = [c for c in t['connections'] if c['direction'] != 'right'] + [{"map": "MAP_PALLET_TOWN_RANCH", "offset": 0, "direction": "right"}]
json.dump(t, open(f, 'w'), indent=2); open(f, 'a').write('\n')
# groupe de cartes et inclusions
f = 'data/maps/map_groups.json'; g = open(f).read()
if '"PalletTown_Ranch"' not in g: g = g.replace('"PalletTown_Museum"\n', '"PalletTown_Museum",\n    "PalletTown_Ranch"\n', 1); open(f, 'w').write(g)
f = 'data/event_scripts.s'; e = open(f).read()
if 'PalletTown_Ranch/scripts.inc' not in e:
    e = e.replace('\t.include "data/maps/PalletTown_Museum/scripts.inc"\n', '\t.include "data/maps/PalletTown_Museum/scripts.inc"\n\t.include "data/maps/PalletTown_Ranch/scripts.inc"\n', 1)
    e = e.replace('\t.include "data/maps/PalletTown_Museum/text.inc"\n', '\t.include "data/maps/PalletTown_Museum/text.inc"\n\t.include "data/maps/PalletTown_Ranch/text.inc"\n', 1)
    open(f, 'w').write(e)
print('grand ranch : evenements ecrits')
