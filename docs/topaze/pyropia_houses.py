# PYROPIA : 2 maisons enterrables supplementaires (copies de l'interieur HOUSE2) + 6 PNJ d'ambiance en ville (textes provisoires, anglais).
# A lancer AVANT pyropia_events.py. Idempotent. Ajoute les cartes au groupe des interieurs de Pyropia et leurs scripts a data/event_scripts.s.
import json, os, re
HOUSES = {
    'House3': {'warp': 11, 'objs': [('OBJ_EVENT_GFX_WOMAN_2', 3, 3, 'MOVEMENT_TYPE_FACE_DOWN', 'Mother',
                                      "My boy trains at the GYM every\\nday.\\pHe always comes home smelling of\\nsmoke and sulfur.$"),
                                     ('OBJ_EVENT_GFX_LITTLE_BOY', 6, 3, 'MOVEMENT_TYPE_FACE_LEFT', 'Boy',
                                      "I'm going to be a GYM LEADER\\none day!\\pLEADER KAY says I need a strong\\nFIRE POKéMON first.$")]},
    'House4': {'warp': 12, 'objs': [('OBJ_EVENT_GFX_GENTLEMAN', 3, 3, 'MOVEMENT_TYPE_FACE_RIGHT', 'Gentleman',
                                      "This house sits right on an old\\nlava tube.\\pThe floor is warm even in winter.\\nI never pay for heating!$"),
                                     ('OBJ_EVENT_GFX_OLD_WOMAN', 5, 4, 'MOVEMENT_TYPE_FACE_LEFT', 'OldWoman',
                                      "When the volcano rumbles, the\\nwhole town gathers by the\\nCRATERS.\\pOur ancestors said the fire speaks.$")]},
}
for name, h in HOUSES.items():
    d = 'data/maps/PewterCity_%s' % name; os.makedirs(d, exist_ok=True)
    base = json.load(open('data/maps/PewterCity_House2/map.json'))
    base['id'] = 'MAP_PEWTER_CITY_%s' % name.upper(); base['name'] = 'PewterCity_%s' % name
    base['warp_events'] = [dict(x=x, y=7, elevation=0, dest_map='MAP_PEWTER_CITY', dest_warp_id=str(h['warp'])) for x in (3, 4, 5)]
    base['object_events'] = []; scr = 'PewterCity_%s_MapScripts::\n\t.byte 0\n' % name; txt = ''
    for (gfx, x, y, mv, nm, text) in h['objs']:
        base['object_events'].append({"type": "object", "graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": mv, "movement_range_x": 1, "movement_range_y": 1,
                                      "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0", "script": 'PewterCity_%s_EventScript_%s' % (name, nm), "flag": "0"})
        scr += '\nPewterCity_%s_EventScript_%s::\n\tmsgbox PewterCity_%s_Text_%s, MSGBOX_NPC\n\tend\n' % (name, nm, name, nm)
        t = text.replace('\\n', '\\n"\n    .string "').replace('\\p', '\\p"\n    .string "')
        txt += '\nPewterCity_%s_Text_%s::\n    .string "%s"\n' % (name, nm, t)
    json.dump(base, open(d + '/map.json', 'w'), indent=2); open(d + '/map.json', 'a').write('\n')
    open(d + '/scripts.inc', 'w').write(scr); open(d + '/text.inc', 'w').write(txt.lstrip('\n'))
# groupe + event_scripts.s
f = 'data/maps/map_groups.json'; s = open(f).read()
for name in HOUSES:
    if '"PewterCity_%s"' % name not in s: s = s.replace('    "PewterCity_House2"\n', '    "PewterCity_House2",\n    "PewterCity_%s"\n' % name, 1) if name == 'House3' else s.replace('    "PewterCity_House3"\n', '    "PewterCity_House3",\n    "PewterCity_%s"\n' % name, 1)
open(f, 'w').write(s)
f = 'data/event_scripts.s'; s = open(f).read()
for name in HOUSES:
    for kind in ('scripts', 'text'):
        line = '\t.include "data/maps/PewterCity_%s/%s.inc"\n' % (name, kind)
        if line not in s:
            prev = '\t.include "data/maps/PewterCity_House2/%s.inc"\n' % kind if name == 'House3' else '\t.include "data/maps/PewterCity_House3/%s.inc"\n' % kind
            s = s.replace(prev, prev + line, 1)
open(f, 'w').write(s)
# PNJ d'ambiance en ville
NPCS = {'Miner': "The crater lake never cools.\\pKAY says that's why the FIRE\\nPOKéMON here are so strong.$",
        'Kid': "The stairs are warm! Even in\\nwinter!\\pI like to sit on them.$",
        'Scientist': "I measure the lava every morning.\\pIt's rising. A little. Don't tell\\nthe MAYOR.$",
        'Guide': "The MUSEUM has two entrances,\\nbut only one exhibit worth seeing:\\pthe fossils in the east wing.$",
        'Grandma': "Careful near the CAIRN.\\nThe flame there has never gone\\nout, not once.$",
        'Camper': "I came to see the volcano.\\pNow I can't stop looking at the\\nlava lake. It's hypnotic.$"}
f = 'data/maps/PewterCity/scripts.inc'; s = open(f).read()
if 'PewterCity_EventScript_Miner' not in s:
    s += '\n' + ''.join('PewterCity_EventScript_%s::\n\tmsgbox PewterCity_Text_%s, MSGBOX_NPC\n\tend\n\n' % (k, k) for k in NPCS)
    open(f, 'w').write(s)
f = 'data/maps/PewterCity/text.inc'; s = open(f).read()
if 'PewterCity_Text_Miner' not in s:
    for k, t in NPCS.items():
        t = t.replace('\\n', '\\n"\n    .string "').replace('\\p', '\\p"\n    .string "')
        s += '\nPewterCity_Text_%s::\n    .string "%s"\n' % (k, t)
    open(f, 'w').write(s)
print('maisons et PNJ Pyropia ecrits')
