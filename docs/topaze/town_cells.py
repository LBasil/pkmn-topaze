#!/usr/bin/env python3
"""Quetes annexes de ville : un temoin, une cellule Onybris (2 sbires dans une maison), un memo + recompense.
Idempotent. Usage: python3 docs/topaze/town_cells.py"""
import json, re, os
R = '/home/claude/pkmn-topaze'

def retrain(tid, name, pic, party, music='AQUA'):
    p = f'{R}/src/data/trainers.h'; t = open(p).read()
    m = re.search(r'    \[%s\] = \{\n.*?\n    \},\n' % tid, t, re.S); assert m, tid
    sym = 'sParty_Cell_' + tid[8:].title().replace('_', '')
    blk = f'''    [{tid}] = {{
        // Topaze: cellule Onybris (quete annexe de ville)
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_{music},
        .trainerPic = TRAINER_PIC_{pic},
        .trainerName = _("{name}"),
        .items = {{}},
        .doubleBattle = FALSE,
        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE,
        .party = NO_ITEM_DEFAULT_MOVES({sym}),
    }},
'''
    open(p, 'w').write(t.replace(m.group(0), blk))
    q = f'{R}/src/data/trainer_parties.h'; s = open(q).read()
    body = ''.join(f'    {{\n        .iv = 30,\n        .lvl = {lv},\n        .species = {sp},\n    }},\n' for sp, lv in party)
    arr = f'static const struct TrainerMonNoItemDefaultMoves {sym}[] = {{\n{body}}};\n'
    m2 = re.search(r'static const struct TrainerMonNoItemDefaultMoves %s\[\] = \{\n.*?\n\};\n' % sym, s, re.S)
    if m2: s = s.replace(m2.group(0), arr)
    else: s = s.rstrip('\n') + '\n' + arr
    open(q, 'w').write(s)

def addobj(mapname, obj):
    p = f'{R}/data/maps/{mapname}/map.json'; d = json.load(open(p))
    if any(o['script'] == obj['script'] for o in d['object_events']): return
    d['object_events'].append(obj); json.dump(d, open(p, 'w'), indent=2); open(p, 'a').write('\n')

def addbg(mapname, bg):
    p = f'{R}/data/maps/{mapname}/map.json'; d = json.load(open(p))
    if any(b.get('script') == bg['script'] for b in d['bg_events']): return
    d['bg_events'].append(bg); json.dump(d, open(p, 'w'), indent=2); open(p, 'a').write('\n')

def obj(gfx, x, y, mv, script, trainer=None, sight='0'):
    return {"graphics_id": "OBJ_EVENT_GFX_" + gfx, "x": x, "y": y, "elevation": 3, "movement_type": "MOVEMENT_TYPE_" + mv,
            "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": sight, "script": script, "flag": "0"}

def append(mapname, text, marker):
    p = f'{R}/data/maps/{mapname}/scripts.inc'; t = open(p).read()
    if marker in t: return
    open(p, 'w').write(t.rstrip('\n') + '\n\n' + text)

def S(*lines):  # lines of a .string block, '\\p' ends box
    out = []
    for i, l in enumerate(lines):
        assert len(l.replace('\\p', '')) <= 35, l
        out.append(f'\t.string "{l}' + ('$"' if i == len(lines) - 1 else '"'))
    return '\n'.join(out)

def pyropia():
    retrain('TRAINER_GUITARIST', 'GRUNT', 'ROCKET_GRUNT_M', [('SPECIES_EKANS', 14), ('SPECIES_ZUBAT', 14)])
    retrain('TRAINER_KINDLER', 'GRUNT', 'ROCKET_GRUNT_F', [('SPECIES_KOFFING', 15), ('SPECIES_GRIMER', 15)])
    addobj('PewterCity', obj('OLD_MAN_1', 13, 8, 'FACE_UP', 'PewterCity_EventScript_CellWitness'))
    addobj('PewterCity_House3', obj('ROCKET_M', 8, 3, 'FACE_LEFT', 'PewterCity_House3_EventScript_CellA', 'TRAINER_GUITARIST', '3'))
    addobj('PewterCity_House3', obj('ROCKET_F', 8, 5, 'FACE_LEFT', 'PewterCity_House3_EventScript_CellB', 'TRAINER_KINDLER', '3'))
    addbg('PewterCity_House3', {"type": "sign", "x": 9, "y": 1, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH", "script": "PewterCity_House3_EventScript_CellMemo"})
    append('PewterCity', '''PewterCity_EventScript_CellWitness::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_CELL_PEWTER, PewterCity_EventScript_CellWitnessDone
	goto_if_defeated TRAINER_GUITARIST, PewterCity_EventScript_CellWitnessHalf
	msgbox PewterCity_Text_CellWitness, MSGBOX_DEFAULT
	release
	end

PewterCity_EventScript_CellWitnessHalf::
	msgbox PewterCity_Text_CellWitnessHalf, MSGBOX_DEFAULT
	release
	end

PewterCity_EventScript_CellWitnessDone::
	msgbox PewterCity_Text_CellWitnessDone, MSGBOX_DEFAULT
	release
	end

PewterCity_Text_CellWitness::
''' + S('Do not stare at that house. Two', 'strangers in black moved in last', 'week.\\p', 'The shutters stay shut all day.', 'Crates go in. Nothing comes out.\\p', 'Police call it a private matter.', 'I call it the start of something.') + '''

PewterCity_Text_CellWitnessHalf::
''' + S('You went in? Then you saw it too.\\p', 'That house holds something worth', 'reading. Look near the back wall.') + '''

PewterCity_Text_CellWitnessDone::
''' + S('The shutters are open again.\\p', 'You know, those crates were labeled', 'BRANCH FOUR. Think about that.') + '\n', 'CellWitness::')
    append('PewterCity_House3', '''PewterCity_House3_EventScript_CellA::
	trainerbattle_single TRAINER_GUITARIST, PewterCity_House3_Text_CellAIntro, PewterCity_House3_Text_CellADefeat
	msgbox PewterCity_House3_Text_CellAPost, MSGBOX_AUTOCLOSE
	end

PewterCity_House3_EventScript_CellB::
	trainerbattle_single TRAINER_KINDLER, PewterCity_House3_Text_CellBIntro, PewterCity_House3_Text_CellBDefeat
	msgbox PewterCity_House3_Text_CellBPost, MSGBOX_AUTOCLOSE
	end

PewterCity_House3_EventScript_CellMemo::
	lockall
	goto_if_set FLAG_TOPAZE_CELL_PEWTER, PewterCity_House3_EventScript_CellMemoDone
	goto_if_not_defeated TRAINER_GUITARIST, PewterCity_House3_EventScript_CellMemoLocked
	goto_if_not_defeated TRAINER_KINDLER, PewterCity_House3_EventScript_CellMemoLocked
	msgbox PewterCity_House3_Text_CellMemo, MSGBOX_DEFAULT
	giveitem ITEM_RARE_CANDY, 2
	setflag FLAG_TOPAZE_CELL_PEWTER
	releaseall
	end

PewterCity_House3_EventScript_CellMemoLocked::
	msgbox PewterCity_House3_Text_CellMemoLocked, MSGBOX_DEFAULT
	releaseall
	end

PewterCity_House3_EventScript_CellMemoDone::
	msgbox PewterCity_House3_Text_CellMemoDone, MSGBOX_DEFAULT
	releaseall
	end

PewterCity_House3_Text_CellAIntro::
''' + S('Wrong house, kid. Nothing to see.', 'Nothing at all.') + '''

PewterCity_House3_Text_CellADefeat::
''' + S('Branch work is not supposed to', 'fail...') + '''

PewterCity_House3_Text_CellAPost::
''' + S('Read the memo if you like. It will', 'not change anything.') + '''

PewterCity_House3_Text_CellBIntro::
''' + S('The boss said to ignore tourists.', 'He did not say how.') + '''

PewterCity_House3_Text_CellBDefeat::
''' + S('...I only carry crates.') + '''

PewterCity_House3_Text_CellBPost::
''' + S('Nobody told me kids fight this', 'hard.') + '''

PewterCity_House3_Text_CellMemo::
''' + S('A delivery note lies in a crate.\\p', 'BRANCH 4 of 7. Eleven crates of', 'POKé BALLS, forty uniforms.\\p', 'Next pickup: after the school job.', 'Report to V.\\p', 'Under it, a black ring, a red dot.', 'Under the note, 2 RARE CANDY.') + '''

PewterCity_House3_Text_CellMemoLocked::
''' + S('Crates, stacked to the ceiling. The', 'guards will not let you look.') + '''

PewterCity_House3_Text_CellMemoDone::
''' + S('The crates are empty now. Only the', 'ring on the wall remains.') + '\n', 'CellMemo::')


import sys
sys.path.insert(0, f'{R}/docs/topaze')
import route_test as RT

def freecell(nav, x, y, used):
    return 0 <= x < nav.w and 0 <= y < nav.h and not nav.blocked(x, y) and (x, y) not in used

def cell(k):
    """k: dict(town, house, key, flag, tidA, tidB, partyA, partyB, reward, witness[3], intro[2], defeat[2], post[2], memo, reward_name)"""
    T, H, K = k['town'], k['house'], k['key']
    retrain(k['tidA'], 'GRUNT', 'ROCKET_GRUNT_M', k['partyA'])
    retrain(k['tidB'], 'GRUNT', 'ROCKET_GRUNT_F', k['partyB'])
    # temoin pres de la porte de la maison
    dt = json.load(open(f'{R}/data/maps/{T}/map.json')); nt = RT.Nav(T)
    dest = 'MAP_' + ''.join(('_' + c if c.isupper() and i else c) for i, c in enumerate(H)).upper().replace('__', '_')
    door = next(w for w in dt['warp_events'] if w['dest_map'].replace('_', '') == ('MAP' + H).upper().replace('_', ''))
    used = {(o['x'], o['y']) for o in dt['object_events']}
    wpos = k.get('wpos') or next((x, y) for x, y in [(door['x'] + 1, door['y'] + 2), (door['x'] - 1, door['y'] + 2), (door['x'], door['y'] + 2), (door['x'] + 2, door['y'] + 1), (door['x'] - 2, door['y'] + 1), (door['x'] + 1, door['y'] + 3)] if freecell(nt, x, y, used))
    addobj(T, obj('OLD_MAN_1', wpos[0], wpos[1], 'FACE_UP', f'{T}_EventScript_CellWitness'))
    dh = json.load(open(f'{R}/data/maps/{H}/map.json')); nh = RT.Nav(H)
    hused = {(o['x'], o['y']) for o in dh['object_events']} | {(w['x'], w['y']) for w in dh['warp_events']}
    gp = [c for c in [(8, 3), (8, 5), (9, 3), (9, 5), (7, 3), (7, 5), (8, 4), (9, 4), (6, 5), (2, 3), (2, 5)] if freecell(nh, c[0], c[1], hused)][:2]
    mp = next((x, 1) for x in (9, 8, 7, 6, 5, 4, 3) if nh.blocked(x, 1) and freecell(nh, x, 2, hused | set(gp)))
    addobj(H, obj('ROCKET_M', gp[0][0], gp[0][1], 'FACE_DOWN', f'{H}_EventScript_CellA', k['tidA'], '3'))
    addobj(H, obj('ROCKET_F', gp[1][0], gp[1][1], 'FACE_DOWN', f'{H}_EventScript_CellB', k['tidB'], '3'))
    addbg(H, {"type": "sign", "x": mp[0], "y": 1, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH", "script": f"{H}_EventScript_CellMemo"})
    f = k['flag']; a, b = k['tidA'], k['tidB']
    item, qty = k['reward']
    append(T, f'''{T}_EventScript_CellWitness::
	lock
	faceplayer
	goto_if_set {f}, {T}_EventScript_CellWitnessDone
	goto_if_defeated {a}, {T}_EventScript_CellWitnessHalf
	msgbox {T}_Text_CellWitness, MSGBOX_DEFAULT
	release
	end

{T}_EventScript_CellWitnessHalf::
	msgbox {T}_Text_CellWitnessHalf, MSGBOX_DEFAULT
	release
	end

{T}_EventScript_CellWitnessDone::
	msgbox {T}_Text_CellWitnessDone, MSGBOX_DEFAULT
	release
	end

{T}_Text_CellWitness::
''' + S(*k['witness'][0]) + f'''

{T}_Text_CellWitnessHalf::
''' + S(*k['witness'][1]) + f'''

{T}_Text_CellWitnessDone::
''' + S(*k['witness'][2]) + '\n', 'CellWitness::')
    append(H, f'''{H}_EventScript_CellA::
	trainerbattle_single {a}, {H}_Text_CellAIntro, {H}_Text_CellADefeat
	msgbox {H}_Text_CellAPost, MSGBOX_AUTOCLOSE
	end

{H}_EventScript_CellB::
	trainerbattle_single {b}, {H}_Text_CellBIntro, {H}_Text_CellBDefeat
	msgbox {H}_Text_CellBPost, MSGBOX_AUTOCLOSE
	end

{H}_EventScript_CellMemo::
	lockall
	goto_if_set {f}, {H}_EventScript_CellMemoDone
	goto_if_not_defeated {a}, {H}_EventScript_CellMemoLocked
	goto_if_not_defeated {b}, {H}_EventScript_CellMemoLocked
	msgbox {H}_Text_CellMemo, MSGBOX_DEFAULT
	giveitem {item}, {qty}
	setflag {f}
	releaseall
	end

{H}_EventScript_CellMemoLocked::
	msgbox {H}_Text_CellMemoLocked, MSGBOX_DEFAULT
	releaseall
	end

{H}_EventScript_CellMemoDone::
	msgbox {H}_Text_CellMemoDone, MSGBOX_DEFAULT
	releaseall
	end

{H}_Text_CellAIntro::
''' + S(*k['intro'][0]) + f'''

{H}_Text_CellADefeat::
''' + S(*k['defeat'][0]) + f'''

{H}_Text_CellAPost::
''' + S(*k['post'][0]) + f'''

{H}_Text_CellBIntro::
''' + S(*k['intro'][1]) + f'''

{H}_Text_CellBDefeat::
''' + S(*k['defeat'][1]) + f'''

{H}_Text_CellBPost::
''' + S(*k['post'][1]) + f'''

{H}_Text_CellMemo::
''' + S(*k['memo']) + f'''

{H}_Text_CellMemoLocked::
''' + S('Crates, stacked to the ceiling. The', 'guards will not let you look.') + f'''

{H}_Text_CellMemoDone::
''' + S('The crates are empty now. Only the', 'ring on the wall remains.') + '\n', 'CellMemo::')
    print(T, 'witness', wpos, 'grunts', gp, 'memo', mp)

TOWNS = [
 dict(town='CeruleanCity', house='CeruleanCity_House3', key='Cerulean', flag='FLAG_TOPAZE_CELL_CERULEAN',
  tidA='TRAINER_RICH_BOY', tidB='TRAINER_HEX_MANIAC',
  partyA=[('SPECIES_GRIMER', 20), ('SPECIES_ZUBAT', 20)], partyB=[('SPECIES_KOFFING', 21), ('SPECIES_EKANS', 21)],
  reward=('ITEM_PP_UP', 1),
  witness=[('The police watch the north road all', 'day. Nobody watches that house.\\p', 'Its lights burn at night and a new', 'lock appears on the door each week.'),
           ('You went in? Then look at the wall', 'behind them. They write it down.'),
           ('The lights are normal again.\\p', 'A pity. They paid for every lock', 'in cash. Who has that much cash?')],
  intro=[('Nothing to see. Move along, kid.',), ('The boss says no witnesses. No', 'children either.')],
  defeat=[('Branch two will hear about this...',), ('...Fine. Go ahead and read it.',)],
  post=[('It is only a list. Lists are not', 'crimes.',), ('We do not even hate you.',)],
  memo=('A ledger lies in a crate.\\p', 'BRANCH 2 of 7. Forty uniforms paid,', 'sixty POKé BALLS withdrawn.\\p', 'Next pickup: after the gym job.', 'Report to K.\\p', 'In the corner, a PP UP in a box.')),
 dict(town='VermilionCity', house='VermilionCity_House2', key='Vermilion', flag='FLAG_TOPAZE_CELL_VERMILION',
  tidA='TRAINER_BUG_MANIAC', tidB='TRAINER_INTERVIEWER',
  partyA=[('SPECIES_ARBOK', 26), ('SPECIES_GOLBAT', 26)], partyB=[('SPECIES_KOFFING', 27), ('SPECIES_MUK', 27)],
  reward=('ITEM_REVIVE', 3),
  witness=[('The harbor is busy, so nobody asks', 'who rents that house.\\p', 'But dockers talk. Crates arrive at', 'night and ship out before dawn.'),
           ('You got in. Good. The back wall', 'is where they keep their count.'),
           ('The night ships stopped.\\p', 'Funny. The captain looks relieved', 'and worried at once.')],
  intro=[('The harbor is ours. This too.',), ('Do not touch the crates, kid.',)],
  defeat=[('The harbor is... still ours.',), ('Tch. The count will be off.',)],
  post=[('Check the wall if you like. It', 'means nothing to you.',), ('Seven branches. You cannot stop', 'them all.',)],
  memo=('A slip is pinned to a crate.\\p', 'BRANCH 6 of 7. Harbor division.', 'Three ships a week, no markings.\\p', 'The stone from the SS ANNE job is', 'overdue. Report to V.\\p', 'Beside it, 3 REVIVE in a box.')),
 dict(town='LavenderTown', house='LavenderTown_House2', key='Lavender', flag='FLAG_TOPAZE_CELL_LAVENDER',
  tidA='TRAINER_SCHOOL_KID_M', tidB='TRAINER_SCHOOL_KID_F',
  partyA=[('SPECIES_HAUNTER', 29), ('SPECIES_GOLBAT', 29)], partyB=[('SPECIES_WEEZING', 30), ('SPECIES_ARBOK', 30)],
  reward=('ITEM_ELIXIR', 2),
  witness=[('The tower bell rang by itself last', 'night. Nobody climbed it.\\p', 'Since then, that house keeps its', 'curtains shut, even at noon.'),
           ('You went in? Then you saw the set.', 'Look behind the crates.'),
           ('The bell is quiet again.\\p', 'I think the dead are relieved. Or', 'they are listening to someone else.')],
  intro=[('The tower hides us well. Leave.',), ('The dead do not scare us anymore.',)],
  defeat=[('The tower did not warn us...',), ('...You are quite scary yourself.',)],
  post=[('The radio only talks to us. Do not', 'bother.',), ('One more wall to read. Then go.',)],
  memo=('A logbook sits among the crates.\\p', 'BRANCH 5 of 7. Tower relay, all', 'quiet. Fifty recruits this month.\\p', 'Next voice: the BOSS, at noon.', 'Report to S.\\p', 'In a drawer, 2 ELIXIR.')),
 dict(town='FuchsiaCity', house='FuchsiaCity_House3', key='Fuchsia', wpos=(34, 24), flag='FLAG_TOPAZE_CELL_FUCHSIA',
  tidA='TRAINER_POKEFAN_M', tidB='TRAINER_POKEFAN_F',
  partyA=[('SPECIES_ARBOK', 35), ('SPECIES_WEEZING', 35)], partyB=[('SPECIES_CROBAT', 36), ('SPECIES_MUK', 36)],
  reward=('ITEM_PP_UP', 2),
  witness=[('Strange. The keeper of that house', 'left town without a word.\\p', 'Now black coats walk in and out as', 'if they owned the street.'),
           ('You went in? Then read what they', 'left on the north wall.'),
           ('The street feels like ours again.\\p', 'Though I count them everywhere now.', 'In every town. Do you notice too?')],
  intro=[('This house is our supply room.', 'Out.',), ('You came a long way for a few', 'crates.',)],
  defeat=[('The supply line will be cut...',), ('...I will be reassigned.',)],
  post=[('Read it. The numbers will keep you', 'awake.',), ('Seven branches. Four towns are', 'already ours.',)],
  memo=('A thick ledger lies open.\\p', 'BRANCH 1 of 7. Supply and training.', 'Two hundred recruits, nine houses.\\p', 'Next shipment: HEMATEK tower.', 'Report to V.\\p', 'Tucked inside, 2 PP UP.')),
]

if __name__ == '__main__':
    pyropia()
    for k in TOWNS: cell(k)
    print('ok')
