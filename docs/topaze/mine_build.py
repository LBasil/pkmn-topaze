#!/usr/bin/env python3
"""MINE DE GRENALUX (post-game, fin 1) : 3 etages (copies des layouts de MtMoon 1F/B1F/B2F), la verite sur l'AURA (scene au 3F),
Mew qui s'enfuit -> se cache sous le camion du port d'APATIA (capturable). Idempotent (marqueur dans flags.h)."""
import json, re, shutil, os, sys
rd = lambda p: open(p).read(); wr = lambda p, s: open(p, 'w').write(s)
if 'FLAG_MEW_FLED' in rd('include/constants/flags.h'): print('already'); sys.exit(0)
def sub(p, old, new, cnt=1):
    s = rd(p); assert old in s, (p, old[:70]); wr(p, s.replace(old, new, cnt))
def save(p, m): json.dump(m, open(p, 'w'), indent=2); open(p, 'a').write('\n')
def box(label, boxes):
    out = label + '::\n'
    for bi, bx in enumerate(boxes):
        for li, l in enumerate(bx):
            assert len(re.sub(r'\{[^}]*\}', 'X', l)) <= 35, (len(l), l)
            ll = li == len(bx) - 1; lb = bi == len(boxes) - 1
            out += '    .string "' + l + ('$' if ll and lb else '\\p' if ll else '\\n') + '"\n'
    return out

# ---- flags ----
f = 'include/constants/flags.h'
for n, name in ((0x0BA, 'FLAG_MEW_FLED'), (0x0BB, 'FLAG_FOUGHT_MEW_TRUCK'), (0x0BC, 'FLAG_MINE_ITEM_1'), (0x0BD, 'FLAG_MINE_ITEM_2'),
                (0x0BE, 'FLAG_HIDE_MINE_MEW'), (0x0BF, 'FLAG_HIDE_MEW_TRUCK')):
    sub(f, '#define FLAG_0x%03X               0x%03X' % (n, n), '#define %-24s 0x%03X' % (name, n))

# ---- layouts ----
SRC = {'1F': ('MtMoon_1F', 'LAYOUT_MT_MOON_1F'), '2F': ('MtMoon_B1F', 'LAYOUT_MT_MOON_B1F'), '3F': ('MtMoon_B2F', 'LAYOUT_MT_MOON_B2F')}
p = 'data/layouts/layouts.json'; j = json.load(open(p))
for fl, (srcmap, srclid) in SRC.items():
    name = 'GrenaluxMine_' + fl; lid = 'LAYOUT_GRENALUX_MINE_' + fl
    base = [l for l in j['layouts'] if l.get('id') == srclid][0]
    sdir = os.path.dirname(base['blockdata_filepath']); ddir = 'data/layouts/' + name
    os.makedirs(ddir, exist_ok=True)
    for fn in ('map.bin', 'border.bin'): shutil.copy(sdir + '/' + fn, ddir + '/' + fn)
    e = dict(base); e['id'] = lid; e['name'] = name + '_Layout'
    e['border_filepath'] = ddir + '/border.bin'; e['blockdata_filepath'] = ddir + '/map.bin'
    j['layouts'].append(e)
json.dump(j, open(p, 'w'), indent=2); open(p, 'a').write('\n')

# ---- groupe de cartes ----
g = json.load(open('data/maps/map_groups.json'))
g['gMapGroup_IndoorPallet'] += ['GrenaluxMine_1F', 'GrenaluxMine_2F', 'GrenaluxMine_3F']
save('data/maps/map_groups.json', g)
# les cartes doivent etre declarees dans group_order deja existant (groupe Dungeons existant)

# ---- cartes ----
def mapjson(name, fl, warps, objs, coords=(), bgs=()):
    return {"id": "MAP_GRENALUX_MINE_" + fl, "name": name, "layout": "LAYOUT_GRENALUX_MINE_" + fl, "music": "MUS_MT_MOON",
            "region_map_section": "MAPSEC_PALLET_TOWN", "requires_flash": False, "weather": "WEATHER_NONE", "map_type": "MAP_TYPE_UNDERGROUND",
            "allow_cycling": True, "allow_escaping": False, "allow_running": True, "show_map_name": True, "floor_number": 0,
            "battle_scene": "MAP_BATTLE_SCENE_NORMAL", "connections": None, "object_events": list(objs),
            "warp_events": [dict(x=x, y=y, elevation=0, dest_map=dm, dest_warp_id=str(di)) for (x, y, dm, di) in warps],
            "coord_events": list(coords), "bg_events": list(bgs)}
def npc(gfx, x, y, script, flag='0', face='DOWN', local=None):
    o = {"type": "object", "graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": "MOVEMENT_TYPE_FACE_" + face,
         "movement_range_x": 0, "movement_range_y": 0, "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0", "script": script, "flag": flag}
    return {"local_id": local, **o} if local else o
def ball(x, y, script, flag): return npc('OBJ_EVENT_GFX_ITEM_BALL', x, y, script, flag, 'DOWN')
M1, M2, M3 = 'GrenaluxMine_1F', 'GrenaluxMine_2F', 'GrenaluxMine_3F'
def src_warps(srcmap): return json.load(open(f'data/maps/{srcmap}/map.json'))['warp_events']
# 1F : 3 echelles vers le 2F + sortie sud vers Grenalux (warp 9 de PalletTown)
w1 = [(w['x'], w['y'], 'MAP_GRENALUX_MINE_2F', w['dest_warp_id']) for w in src_warps('MtMoon_1F')[:3]] + [(18, 37, 'MAP_PALLET_TOWN', 9)]
w2 = [(w['x'], w['y'], 'MAP_GRENALUX_MINE_1F' if i < 3 else 'MAP_GRENALUX_MINE_3F', w['dest_warp_id']) for i, w in enumerate(src_warps('MtMoon_B1F')[:7])] + [(45, 4, 'MAP_PALLET_TOWN', 9)]
w3 = [(w['x'], w['y'], 'MAP_GRENALUX_MINE_2F', w['dest_warp_id']) for w in src_warps('MtMoon_B2F')]
save(f'data/maps/{M1}/map.json', None) if False else None
os.makedirs(f'data/maps/{M1}', exist_ok=True); os.makedirs(f'data/maps/{M2}', exist_ok=True); os.makedirs(f'data/maps/{M3}', exist_ok=True)
save(f'data/maps/{M1}/map.json', mapjson(M1, '1F', w1, [npc('OBJ_EVENT_GFX_WORKER_M', 18, 34, M1 + '_EventScript_Miner')]))
save(f'data/maps/{M2}/map.json', mapjson(M2, '2F', w2, [ball(15, 17, M2 + '_EventScript_ItemCandy', 'FLAG_MINE_ITEM_2')]))
save(f'data/maps/{M3}/map.json', mapjson(M3, '3F', w3,
     [npc('OBJ_EVENT_GFX_MEW', 14, 9, '0x0', 'FLAG_HIDE_MINE_MEW', 'DOWN', 'LOCALID_MINE_MEW'), ball(24, 6, M3 + '_EventScript_ItemNugget', 'FLAG_MINE_ITEM_1')],
     [{"type": "trigger", "x": 14, "y": 11, "elevation": 3, "var": "VAR_TEMP_0", "var_value": "0", "script": M3 + '_EventScript_Truth'}]))

# ---- scripts / textes ----
wr(f'data/maps/{M1}/scripts.inc', f'''{M1}_MapScripts::
	.byte 0

{M1}_EventScript_Miner::
	msgbox {M1}_Text_Miner, MSGBOX_NPC
	end
''')
wr(f'data/maps/{M1}/text.inc', box(f'{M1}_Text_Miner', [
    ['MINER: I thought I knew every inch', 'of this mine.'],
    ['Lately the garnet in the walls', 'hums like a living thing.'],
    ['It gets louder the deeper you go.', 'Mind the dark down there.']]))
wr(f'data/maps/{M2}/scripts.inc', f'''{M2}_MapScripts::
	.byte 0

{M2}_EventScript_ItemCandy::
	finditem ITEM_RARE_CANDY
	end
''')
wr(f'data/maps/{M2}/text.inc', '')
scripts3 = f'''{M3}_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, {M3}_OnTransition
	.byte 0

{M3}_OnTransition::
	setflag FLAG_HIDE_MINE_MEW
	end

{M3}_EventScript_ItemNugget::
	finditem ITEM_NUGGET
	end

@ Topaze: the truth about the AURA (placeholder text), then MEW appears and bolts.
{M3}_EventScript_Truth::
	lockall
	goto_if_set FLAG_MEW_FLED, EventScript_ReleaseEnd
	msgbox {M3}_Text_PendantGlows
	closemessage
	fadescreen FADE_TO_WHITE
	delay 30
	fadescreen FADE_FROM_WHITE
	msgbox {M3}_Text_Vision1
	msgbox {M3}_Text_Vision2
	msgbox {M3}_Text_Vision3
	closemessage
	special ShakeScreen
	delay 30
	addobject LOCALID_MINE_MEW
	delay 20
	playmoncry SPECIES_MEW, CRY_MODE_NORMAL
	waitmoncry
	applymovement LOCALID_MINE_MEW, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox {M3}_Text_MewAppears
	closemessage
	applymovement LOCALID_MINE_MEW, {M3}_Movement_MewFlees
	waitmovement 0
	removeobject LOCALID_MINE_MEW
	setflag FLAG_MEW_FLED
	msgbox {M3}_Text_MewGone
	releaseall
	end

{M3}_Movement_MewFlees::
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	set_invisible
	step_end
'''
wr(f'data/maps/{M3}/scripts.inc', scripts3)
t = box(f'{M3}_Text_PendantGlows', [
    ['Your PENDANT glows warm and', 'bright.'],
    ['The whole cavern begins to hum.', 'The garnet answers it.']])
t += '\n' + box(f'{M3}_Text_Vision1', [
    ['A vision washes over you.'],
    ['Ten years ago, deep in this vein,', 'the miners broke into a hollow.'],
    ['Something very old was sleeping', 'there.']])
t += '\n' + box(f'{M3}_Text_Vision2', [
    ['It woke in terror. Its fear spilled', 'out of the rock as light.'],
    ['That light was the AURA.', 'It washed across the world.'],
    ['It rewrote the TYPES of every', 'POKéMON it touched.']])
t += '\n' + box(f'{M3}_Text_Vision3', [
    ['The AURA was never a weapon.', 'It was a cry for help.'],
    ['The stones of the ten towns are', 'where that cry settled.'],
    ['Your PENDANT is the first of them.', 'It did not choose to be taken.', 'It chose YOU.']])
t += '\n' + box(f'{M3}_Text_MewAppears', [
    ['A small pink shape drifts out of', 'the crystal.'],
    ['It is MEW, the oldest of all', 'POKéMON.'],
    ['It looks at your PENDANT, squeaks,', 'and bolts!']])
t += '\n' + box(f'{M3}_Text_MewGone', [
    ['MEW slipped through the rock and', 'vanished.'],
    ['Far away, you faintly hear a truck', 'engine near the docks of APATIA.']])
wr(f'data/maps/{M3}/text.inc', t)
for k in ('scripts', 'text'):
    pth = 'data/event_scripts.s'
    s = rd(pth)
    anchor = f'\t.include "data/maps/VictoryRoadLair_3F/{k}.inc"\n'
    assert anchor in s
    s = s.replace(anchor, anchor + ''.join(f'\t.include "data/maps/GrenaluxMine_{x}/{k}.inc"\n' for x in ('1F', '2F', '3F')), 1)
    wr(pth, s)

# ---- Grenalux : porte de la mine (coord event + warp 9) ----
pp = 'data/maps/PalletTown/map.json'; d = json.load(open(pp))
d['warp_events'].append({"x": 39, "y": 24, "elevation": 0, "dest_map": "MAP_GRENALUX_MINE_1F", "dest_warp_id": "3"})
d['coord_events'].append({"type": "trigger", "x": 39, "y": 24, "elevation": 0, "var": "VAR_TEMP_0", "var_value": "0", "script": "PalletTown_EventScript_MineGate"})
save(pp, d)
s = rd('data/maps/PalletTown/scripts.inc')
s = s.replace('PalletTown_EventScript_SceneryMine::\n\tmsgbox PalletTown_Text_SceneryMine, MSGBOX_SIGN\n\tend\n',
 '''PalletTown_EventScript_SceneryMine::
	goto_if_set FLAG_TOPAZE_POSTGAME, PalletTown_EventScript_SceneryMineOpen
	msgbox PalletTown_Text_SceneryMine, MSGBOX_SIGN
	end

PalletTown_EventScript_SceneryMineOpen::
	msgbox PalletTown_Text_SceneryMineOpen, MSGBOX_SIGN
	end

@ Topaze: the mine opens in the postgame (ending 1)
PalletTown_EventScript_MineGate::
	lockall
	goto_if_set FLAG_TOPAZE_POSTGAME, PalletTown_EventScript_MineEnter
	msgbox PalletTown_Text_SceneryMine
	closemessage
	applymovement LOCALID_PLAYER, PalletTown_Movement_MineBack
	waitmovement 0
	releaseall
	end

PalletTown_EventScript_MineEnter::
	warp MAP_GRENALUX_MINE_1F, 18, 37
	waitstate
	releaseall
	end
''', 1)
wr('data/maps/PalletTown/scripts.inc', s)
tx = rd('data/maps/PalletTown/text.inc').rstrip('\n') + '\n\n' + box('PalletTown_Text_SceneryMineOpen', [
    ['The old mine gate stands open.', 'The garnet hums inside.']])
wr('data/maps/PalletTown/text.inc', tx)

# ---- Apatia : Mew sous le camion ----
vp = 'data/maps/VermilionCity/map.json'; d = json.load(open(vp))
d['object_events'] += [npc('OBJ_EVENT_GFX_MG_DELIVERYMAN', 16, 19, 'VermilionCity_EventScript_TruckDriver', 'FLAG_HIDE_MEW_TRUCK', 'RIGHT'),
                       npc('OBJ_EVENT_GFX_MEW', 17, 19, 'VermilionCity_EventScript_MewTruck', 'FLAG_HIDE_MEW_TRUCK', 'LEFT')]
save(vp, d)
s = rd('data/maps/VermilionCity/scripts.inc')
s = s.replace('\tcall_if_set FLAG_GOT_HM01, VermilionCity_EventScript_EastPoliceLeave\n\tend\n',
 '''\tcall_if_set FLAG_GOT_HM01, VermilionCity_EventScript_EastPoliceLeave
	setflag FLAG_HIDE_MEW_TRUCK
	call_if_set FLAG_MEW_FLED, VermilionCity_EventScript_MaybeShowMew
	end

@ Topaze: MEW hides under the delivery truck once it fled the Grenalux mine
VermilionCity_EventScript_MaybeShowMew::
	goto_if_set FLAG_FOUGHT_MEW_TRUCK, EventScript_Return
	clearflag FLAG_HIDE_MEW_TRUCK
	return

VermilionCity_EventScript_TruckDriver::
	msgbox VermilionCity_Text_TruckDriver, MSGBOX_NPC
	end

VermilionCity_EventScript_MewTruck::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_MEW, 50
	waitse
	playmoncry SPECIES_MEW, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, VermilionCity_EventScript_DefeatedMew
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, VermilionCity_EventScript_RanFromMew
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, VermilionCity_EventScript_RanFromMew
	setflag FLAG_FOUGHT_MEW_TRUCK
	setflag FLAG_HIDE_MEW_TRUCK
	release
	end

VermilionCity_EventScript_DefeatedMew::
	setflag FLAG_FOUGHT_MEW_TRUCK
	goto EventScript_RemoveStaticMon
	end

VermilionCity_EventScript_RanFromMew::
	setvar VAR_0x8004, SPECIES_MEW
	goto EventScript_MonFlewAway
	end
''', 1)
wr('data/maps/VermilionCity/scripts.inc', s)
tx = rd('data/maps/VermilionCity/text.inc').rstrip('\n') + '\n\n' + box('VermilionCity_Text_TruckDriver', [
    ['DRIVER: Don\'t mind the truck!', 'I just park here.'],
    ['...Why does it keep shaking?', 'Is something under there?']])
wr('data/maps/VermilionCity/text.inc', tx)
print('mine ok')
# NB (patch manuel apres coup) : la case (39,24) de PalletTown (entree de la mine) etait en collision 1 ; on l'a rendue franchissable
# (metatile 0x072c -> 0x032c dans data/layouts/PalletTown/map.bin). Les generateurs grenalux_town.py ne doivent pas etre relances sans ce patch.
# NB : les cartes sont dans gMapGroup_IndoorPallet (pas Dungeons : un groupe ne peut pas depasser 127 cartes, mapNum est un s8).
