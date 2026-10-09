# Grenalux v6 : branche evenements (trajets des cinematiques par Dijkstra, panneaux, warps, connexions) et PNJ d'ambiance.
# A lancer apres grenalux_town.py (lit /tmp/grenalux_col.json et /tmp/grenalux_npc.json). Idempotent.
import sys, json, re
sys.path.insert(0,'docs/topaze')
from grenalux_paths import path,moves
f='data/maps/PalletTown/scripts.inc'; s=open(f).read()
def setblock(s,name,lines):
    pat=re.compile(r'(?m)^'+re.escape(name)+r'::\n(?:\t.*\n)*?\tstep_end\n')
    new=name+'::\n'+''.join('\t%s\n'%l for l in lines)+'\tstep_end\n'
    assert pat.search(s),name
    return pat.sub(lambda m:new,s,1)
OAK_SPAWN=(22,15); OAK_STAND=(9,10)
s=setblock(s,'PalletTown_Movement_OakWalkToPlayersDoor',moves(path(OAK_SPAWN,OAK_STAND))+['walk_in_place_faster_left'])
s=setblock(s,'PalletTown_Movement_OakExit',moves(path(OAK_STAND,OAK_SPAWN)))
T=path(OAK_STAND,(34,22))+[(35,22)]
s=setblock(s,'PalletTown_Movement_OakWalkToLabFromHouse',moves(T)+['walk_in_place_faster_up'])
s=setblock(s,'PalletTown_Movement_PlayerWalkToLabFromHouse',['walk_right']+moves(T[:-1]))
RL=path((22,2),(35,9))+[(36,9)]; RR=path((23,2),(35,9))+[(36,9)]
s=setblock(s,'PalletTown_Movement_RivalWalkToRanchLeft',moves(RL))
s=setblock(s,'PalletTown_Movement_RivalWalkToRanchRight',moves(RR))
s=setblock(s,'PalletTown_Movement_PlayerWalkToRanchLeft',['walk_down']+moves(RL[:-1]))
s=setblock(s,'PalletTown_Movement_PlayerWalkToRanchRight',['walk_down']+moves(RR[:-1]))
s=setblock(s,'PalletTown_Movement_OakEnterLeft',['walk_left']+['walk_up']*14)
s=setblock(s,'PalletTown_Movement_OakEnterRight',['walk_up']*14)
s=s.replace('opendoor 18, 6','opendoor 36, 8').replace('closedoor 18, 6','closedoor 36, 8')
s=s.replace('opendoor 18, 14','opendoor 35, 21').replace('closedoor 18, 14','closedoor 35, 21')
s=s.replace('setobjectxyperm LOCALID_PALLET_PROF_OAK, 13, 12','setobjectxyperm LOCALID_PALLET_PROF_OAK, 22, 15')
s=s.replace('setobjectxyperm LOCALID_PALLET_SIGN_LADY, 4, 16','setobjectxyperm LOCALID_PALLET_SIGN_LADY, 10, 16')
s=s.replace('setobjectxyperm LOCALID_PALLET_SIGN_LADY, 12, 2','setobjectxyperm LOCALID_PALLET_SIGN_LADY, 22, 2')
open(f,'w').write(s)
f='data/maps/PalletTown/map.json'; d=json.load(open(f))
def obj(lid,x,y):
    for o in d['object_events']:
        if o['local_id']==lid: o['x']=x;o['y']=y
obj('LOCALID_PALLET_SIGN_LADY',10,16); obj('LOCALID_PALLET_FAT_MAN',19,19); obj('LOCALID_PALLET_PROF_OAK',22,11)
obj('LOCALID_PALLET_ONYBRIS_GRUNT',22,6); obj('LOCALID_PALLET_RIVAL',23,16)
for w,(x,y) in zip(d['warp_events'],[(8,9),(36,8),(35,21),(8,21)]): w['x']=x;w['y']=y
for c in d['coord_events']:
    if c['script'].endswith('OakTriggerLeft'): c['x'],c['y']=22,1
    elif c['script'].endswith('OakTriggerRight'): c['x'],c['y']=23,1
    elif c['script'].endswith('SignLadyTrigger'): c['x'],c['y']=23,2
sg={'PalletTown_EventScript_OaksLabSign':(36,22),'PalletTown_EventScript_PlayersHouseSign':(10,9),'PalletTown_EventScript_RivalsHouseSign':(37,9),
 'PalletTown_EventScript_TownSign':(21,10),'PalletTown_EventScript_TrainerTips':(10,15),'PalletTown_EventScript_MuseumSign':(11,21)}
for b in d['bg_events']:
    if b['script'] in sg: b['x'],b['y']=sg[b['script']]
for c in d['connections']:
    if c['direction']=='up': c['offset']=10
    if c['direction']=='down': c['offset']=14
json.dump(d,open(f,'w'),indent=2); open(f,'a').write('\n')

# ---- PNJ d'ambiance
NPC = json.load(open('/tmp/grenalux_npc.json'))
d = json.load(open('data/maps/PalletTown/map.json'))
d['object_events'] = [o for o in d['object_events'] if not o['local_id'].startswith('LOCALID_PALLET_AMB_')]
AMB = [('MINER', 'miner', 'OBJ_EVENT_GFX_WORKER_M', 'MOVEMENT_TYPE_FACE_LEFT',
        ['The vein under this hill is old.', 'Garnet grows like frost in the dark.', 'We cut only what the mine lets go.']),
       ('OLDMAN', 'oldman', 'OBJ_EVENT_GFX_OLD_MAN_1', 'MOVEMENT_TYPE_FACE_RIGHT',
        ['My grandfather carried the first', 'crystal up from the mine. They say', 'the monument still hums at night.']),
       ('GIRL', 'girl', 'OBJ_EVENT_GFX_LITTLE_GIRL', 'MOVEMENT_TYPE_WANDER_AROUND',
        ['The pond turns purple at dusk!', 'I think the garnet colors it.']),
       ('BOY', 'boy', 'OBJ_EVENT_GFX_LITTLE_BOY', 'MOVEMENT_TYPE_WANDER_AROUND',
        ['I found a tiny crystal by the pond.', 'It glows if you hold it to the sun!']),
       ('SCIENTIST', 'scientist', 'OBJ_EVENT_GFX_SCIENTIST', 'MOVEMENT_TYPE_FACE_UP',
        ['The lab measures the aura of every', 'crystal in town. The readings keep', 'rising, and nobody knows why.']),
       ('GARDENER', 'gardener', 'OBJ_EVENT_GFX_WORKER_F', 'MOVEMENT_TYPE_FACE_DOWN',
        ['These berries are for ranch animals.', 'They are not for picking, sorry!', 'The pens are east, beyond the trees.']),
       ('LADY', 'lady', 'OBJ_EVENT_GFX_BEAUTY', 'MOVEMENT_TYPE_FACE_RIGHT',
        ['Garnet is the stone of this town.', 'Red roofs, red trees, red stone...', 'Even the grass blushes here.'])]
txt = open('data/maps/PalletTown/text.inc').read(); scr = open('data/maps/PalletTown/scripts.inc').read()
import re
scr = re.sub(r'\nPalletTown_EventScript_Amb\w+::\n(?:\t.*\n)*', '', scr); txt = re.sub(r'\nPalletTown_Text_Amb\w+::\n(?:\t.*\n)*', '', txt)
for name, key, gfx, mv, lines in AMB:
    x, y = NPC[key]
    d['object_events'].append({"local_id": "LOCALID_PALLET_AMB_" + name, "type": "object", "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
        "movement_type": mv, "movement_range_x": 1, "movement_range_y": 1, "trainer_type": "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": "0", "script": "PalletTown_EventScript_Amb" + name.title(), "flag": "0"})
    if 'PalletTown_EventScript_Amb' + name.title() + '::' not in scr:
        scr += '\nPalletTown_EventScript_Amb%s::\n\tmsgbox PalletTown_Text_Amb%s, MSGBOX_NPC\n\tend\n' % (name.title(), name.title())
        body = '\\n'.join(lines[:-1]) + ('\\n' if len(lines) > 1 else '')
        out = ''
        for i, l in enumerate(lines): out += '\t.string "%s%s"\n' % (l, '$' if i == len(lines) - 1 else '\\n')
        txt += '\nPalletTown_Text_Amb%s::\n%s' % (name.title(), out)
open('data/maps/PalletTown/scripts.inc', 'w').write(scr); open('data/maps/PalletTown/text.inc', 'w').write(txt)
json.dump(d, open('data/maps/PalletTown/map.json', 'w'), indent=2); open('data/maps/PalletTown/map.json', 'a').write('\n')
print('evenements Grenalux v6 ecrits')

# ---- sorties nord (route 1) et sud (route 21) : WARPS et non connexions.
# Une connexion entre cartes de tilesets differents (Route 1 = tileset FR, Grenalux = tilesets d'Emeraude) affiche les
# quelques rangees voisines avec le mauvais tileset (tuiles brouillees). Le warp (fondu) evite ce defaut ; les warps
# conservent l'etat de surf. La connexion est du cote est (ranch) reste, car meme tileset.
def warp(x, y, dest, wid): return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)}
f = 'data/maps/PalletTown/map.json'; t = json.load(open(f))
t['connections'] = [c for c in t['connections'] if c['direction'] == 'right']
t['warp_events'] = t['warp_events'][:4] + [warp(22, 0, 'MAP_ROUTE1', 0), warp(23, 0, 'MAP_ROUTE1', 1),
    warp(21, 35, 'MAP_ROUTE21_NORTH', 0), warp(22, 35, 'MAP_ROUTE21_NORTH', 1), warp(23, 35, 'MAP_ROUTE21_NORTH', 2)]
json.dump(t, open(f, 'w'), indent=2); open(f, 'a').write('\n')
for mp, direction, warps in (('Route1', 'down', [warp(12, 39, 'MAP_PALLET_TOWN', 4), warp(13, 39, 'MAP_PALLET_TOWN', 5)]),
                             ('Route21_North', 'up', [warp(7, 0, 'MAP_PALLET_TOWN', 6), warp(8, 0, 'MAP_PALLET_TOWN', 7), warp(9, 0, 'MAP_PALLET_TOWN', 8)])):
    f = 'data/maps/%s/map.json' % mp; m = json.load(open(f))
    m['connections'] = [c for c in m['connections'] if c['direction'] != direction]
    m['warp_events'] = warps
    m['object_events'] = [o for o in m['object_events'] if o.get('type') != 'clone']
    json.dump(m, open(f, 'w'), indent=2); open(f, 'a').write('\n')

# ---- decors interactifs (lecture avec A) : monument, cristaux gardiens, mine, buissons a baies
d = json.load(open('data/maps/PalletTown/map.json')); txt = open('data/maps/PalletTown/text.inc').read(); scr = open('data/maps/PalletTown/scripts.inc').read()
d['bg_events'] = [b for b in d['bg_events'] if not b['script'].startswith('PalletTown_EventScript_Scenery')]
import re
scr = re.sub(r'\nPalletTown_EventScript_Scenery\w+::\n(?:\t.*\n)*', '', scr); txt = re.sub(r'\nPalletTown_Text_Scenery\w+::\n(?:\t.*\n)*', '', txt)
SC = {'Monument': ([(22, 23)], ['A giant garnet crystal.', 'It hums softly, as if alive.']),
      'Guardian': ([(19, 10), (26, 10)], ['A garnet crystal, tall as a house.', 'It watches over the road north.']),
      'Mine': ([(39, 24)], ['The old mine, sealed for safety.', 'Something glints deep inside...']),
      'Berries': ([(x, y) for y in (5, 7) for x in range(29, 33)], ['Berry bushes for the ranch animals.', 'They are not for picking!'])}
for name, (cells, lines) in SC.items():
    for (x, y) in cells:
        d['bg_events'].append({"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": "PalletTown_EventScript_Scenery" + name})
    if 'PalletTown_EventScript_Scenery%s::' % name not in scr:
        scr += '\nPalletTown_EventScript_Scenery%s::\n\tmsgbox PalletTown_Text_Scenery%s, MSGBOX_SIGN\n\tend\n' % (name, name)
        txt += '\nPalletTown_Text_Scenery%s::\n%s' % (name, ''.join('\t.string "%s%s"\n' % (l, '$' if i == len(lines) - 1 else '\\n') for i, l in enumerate(lines)))
open('data/maps/PalletTown/scripts.inc', 'w').write(scr); open('data/maps/PalletTown/text.inc', 'w').write(txt)
json.dump(d, open('data/maps/PalletTown/map.json', 'w'), indent=2); open('data/maps/PalletTown/map.json', 'a').write('\n')
