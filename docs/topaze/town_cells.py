#!/usr/bin/env python3
"""Quetes annexes de ville : un temoin, une cellule Onybris (2 sbires dans une maison), un memo + recompense.
Idempotent. Usage: python3 docs/topaze/town_cells.py"""
import json, re, os
R = '/home/claude/pkmn-topaze'

def retrain(tid, name, pic, party, music='AQUA'):
    p = f'{R}/src/data/trainers.h'; t = open(p).read()
    m = re.search(r'    \[%s\] = \{\n.*?\n    \},\n' % tid, t, re.S); assert m, tid
    sym = re.search(r'NO_ITEM_DEFAULT_MOVES\((\w+)\)', m.group(0)).group(1)
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
    m2 = re.search(r'static const struct TrainerMonNoItemDefaultMoves %s\[\] = \{(?:DUMMY_TRAINER_MON\};\n|\n.*?\n\};\n)' % sym, s, re.S); assert m2, sym
    body = ''.join(f'    {{\n        .iv = 30,\n        .lvl = {lv},\n        .species = {sp},\n    }},\n' for sp, lv in party)
    open(q, 'w').write(s.replace(m2.group(0), f'static const struct TrainerMonNoItemDefaultMoves {sym}[] = {{\n{body}}};\n'))

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
''' + S('Do not stare at that house. Two', 'strangers in black moved in last week.\\p', 'The shutters stay shut, day and night.', 'Crates go in. Nothing comes out.\\p', 'The police call it a private matter.', 'I call it the start of something.') + '''

PewterCity_Text_CellWitnessHalf::
''' + S('You went in? Then you saw it too.\\p', 'There is something in that house worth', 'reading. Look near the back wall.') + '''

PewterCity_Text_CellWitnessDone::
''' + S('The shutters are open again.\\p', 'You know, those crates were labeled', 'BRANCH FOUR. Four. Think about that.') + '\n', 'CellWitness::')
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
''' + S('A delivery note lies in a crate.\\p', 'BRANCH 4 of 7. Eleven crates of', 'POKé BALLS, forty uniforms.\\p', 'Next pickup: after the school job.', 'Report to V.\\p', 'Under it, a black ring with a red dot.', 'Under the note, 2 RARE CANDY.') + '''

PewterCity_House3_Text_CellMemoLocked::
''' + S('Crates, stacked to the ceiling. The', 'guards will not let you look.') + '''

PewterCity_House3_Text_CellMemoDone::
''' + S('The crates are empty now. Only the', 'ring on the wall remains.') + '\n', 'CellMemo::')

if __name__ == '__main__':
    pyropia()
    print('ok')
