# PARC SAFARI sous occupation ONYBRIS (Amethiolite) : 8 sbires + cadre SELENE, texte, sans limite de pas/balles. Idempotent.
import json, re
IDS = {  # id recycle (trainers RS inutilises) -> (pic, nom, equipe)
 'TRAINER_AQUA_GRUNT_M':   ('ROCKET_GRUNT_M', 'GRUNT', [('KOFFING', 31), ('ZUBAT', 31), ('RATICATE', 32)]),
 'TRAINER_AQUA_GRUNT_F':   ('ROCKET_GRUNT_F', 'GRUNT', [('ARBOK', 31), ('GRIMER', 31), ('GOLBAT', 32)]),
 'TRAINER_MAGMA_GRUNT_M':  ('ROCKET_GRUNT_M', 'GRUNT', [('MACHOP', 31), ('MACHOKE', 32), ('MANKEY', 31)]),
 'TRAINER_MAMGA_GRUNT_F':  ('ROCKET_GRUNT_F', 'GRUNT', [('GLOOM', 32), ('WEEPINBELL', 32), ('VENONAT', 31)]),
 'TRAINER_RS_CAMPER':      ('ROCKET_GRUNT_M', 'GRUNT', [('NIDORINO', 32), ('NIDORINA', 32)]),
 'TRAINER_RS_YOUNGSTER':   ('ROCKET_GRUNT_M', 'GRUNT', [('DROWZEE', 32), ('HAUNTER', 32)]),
 'TRAINER_RS_BUG_CATCHER': ('ROCKET_GRUNT_F', 'GRUNT', [('WEEZING', 32), ('MUK', 32)]),
 'TRAINER_TEAM_ROCKET_GRUNT_21': ('ROCKET_GRUNT_M', 'GRUNT', [('GOLBAT', 32), ('RATICATE', 32), ('ARBOK', 33)]),
 'TRAINER_MAGMA_ADMIN_COURTNEY': ('MAGMA_ADMIN_F', 'SELENE', [('HYPNO', 35), ('MUK', 35), ('VENOMOTH', 36), ('TENTACRUEL', 37)]),
}
tr = open('src/data/trainers.h').read(); pa = open('src/data/trainer_parties.h').read()
for tid, (pic, name, team) in IDS.items():
    b = re.search(r'\[%s\] = \{.*?\n    \},' % tid, tr, re.S).group(0)
    nb = re.sub(r'trainerClass = \w+', 'trainerClass = TRAINER_CLASS_TEAM_ROCKET', b)
    nb = re.sub(r'encounterMusic_gender = [\w |]+', 'encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_AQUA', nb)
    nb = re.sub(r'trainerPic = \w+', 'trainerPic = TRAINER_PIC_%s' % pic, nb)
    nb = re.sub(r'trainerName = _\("[^"]*"\)', 'trainerName = _("%s")' % name, nb)
    if name == 'SELENE': nb = nb.replace('AI_SCRIPT_CHECK_BAD_MOVE,', 'AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT,')
    tr = tr.replace(b, nb)
    sym = re.search(r'NO_ITEM_(?:DEFAULT|CUSTOM)_MOVES\((\w+)\)', nb).group(1)
    m = re.search(r'static const struct TrainerMon\w+ %s\[\] = \{.*?\};' % sym, pa, re.S); assert m, sym
    iv = 60 if name == 'SELENE' else 30
    body = ''.join('    {\n        .iv = %d,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n' % (iv, lv, sp) for sp, lv in team)
    pa = pa.replace(m.group(0), 'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};' % (sym, body))
open('src/data/trainers.h', 'w').write(tr); open('src/data/trainer_parties.h', 'w').write(pa)

# (map, tid, x, y, dir, sight, label, intro, defeat, post)
G = [
 ('SafariZone_Center', 'TRAINER_AQUA_GRUNT_M', 26, 26, 'DOWN', 3, 'Grunt1', 'Free park, free POKéMON!\\nGet lost, this is ONYBRIS ground!', 'Free to lose, huh...', 'We opened every cage. POKéMON\\nbelong to nobody!'),
 ('SafariZone_Center', 'TRAINER_AQUA_GRUNT_F', 40, 16, 'LEFT', 4, 'Grunt2', 'Trainers are what is wrong with\\nthis world!', 'Lost to a trainer...', 'Our cadre SELENE is in the WEST\\nAREA. She is looking for something.'),
 ('SafariZone_East', 'TRAINER_MAGMA_GRUNT_M', 24, 15, 'LEFT', 4, 'Grunt1', 'This park is under ONYBRIS control!', 'Argh!', 'The old WARDEN hid something.\\nWe will find it!'),
 ('SafariZone_East', 'TRAINER_MAMGA_GRUNT_F', 30, 28, 'UP', 3, 'Grunt2', 'Halt! No visitors today!', 'Fine, fine!', 'The SAFARI staff ran away like\\nscared RATTATA.'),
 ('SafariZone_North', 'TRAINER_RS_CAMPER', 20, 12, 'DOWN', 3, 'Grunt1', 'Stay out of our sight, kid!', 'Spotted...', 'SELENE wants the real stone.\\nThe one on show was a fake!'),
 ('SafariZone_North', 'TRAINER_RS_YOUNGSTER', 38, 11, 'LEFT', 3, 'Grunt2', 'You are the one who beat my pals?', 'Impossible!', 'The WARDEN\'s gold teeth are the\\nkey. SELENE keeps them.'),
 ('SafariZone_West', 'TRAINER_RS_BUG_CATCHER', 13, 22, 'RIGHT', 4, 'Grunt1', 'No trespassers in the WEST AREA!', 'Overrun...', 'SELENE waits in the big clearing\\nto the east. Good luck!'),
 ('SafariZone_West', 'TRAINER_TEAM_ROCKET_GRUNT_21', 35, 24, 'LEFT', 3, 'Grunt2', 'Free POKéMON, free world, kid!', 'The boss will be furious.', 'ONYBRIS never loses...\\nusually.'),
]
BOSS = ('SafariZone_West', 'TRAINER_MAGMA_ADMIN_COURTNEY', 29, 16, 'UP', 3)
BT = {
 'Intro': 'SELENE: So the little hero arrives.\\p'
          'We opened the cages to free the\\nPOKéMON. They are happier now.\\p'
          'But the old WARDEN fooled us.\\nThe stone on display was a fake!\\p'
          'We kept his gold teeth, so he\\ncannot tell anyone where it is.\\p'
          'Enough talk. Step back, child!',
 'Defeat': 'How can a child do this?!',
 'Post': 'SELENE: Fine. Take the old man\'s\\nteeth. They are useless to us.\\p'
         'The more you guard the stones,\\nthe harder ONYBRIS hunts them.\\p'
         'We will free the POKéMON. All of\\nthem. Farewell, child!',
}
def chk(s):
    for part in re.split(r'\\n|\\p|\\l|\$', s): assert len(part) <= 35, (len(part), part)
def obj(tid, gfx, x, y, d, sight, script, flag='FLAG_TEMP_5'):
    return {"graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": "MOVEMENT_TYPE_FACE_" + d, "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NORMAL", "trainer_sight_or_berry_tree_id": str(sight), "script": script, "flag": flag}
by = {}
for g in G: by.setdefault(g[0], []).append(g)
for mp in ('SafariZone_Center', 'SafariZone_East', 'SafariZone_North', 'SafariZone_West'):
    f = 'data/maps/%s/map.json' % mp; m = json.load(open(f))
    m['object_events'] = [o for o in m['object_events'] if 'Onybris' not in o['script']]
    sc = open('data/maps/%s/scripts.inc' % mp).read(); tx = open('data/maps/%s/text.inc' % mp).read()
    sc = re.sub(r'\n%s_EventScript_Onybris.*?(?=\n%s_EventScript_\w+::|\Z)' % (mp, mp), '', sc, flags=re.S) if '_EventScript_Onybris' in sc else sc
    add_sc = ''; add_tx = ''
    for g in by[mp]:
        _, tid, x, y, d, sight, lab, intro, defeat, post = g
        for s in (intro, defeat, post): chk(s)
        script = '%s_EventScript_Onybris%s' % (mp, lab)
        m['object_events'].append(obj(tid, 'OBJ_EVENT_GFX_ROCKET_M' if 'M' in IDS[tid][0][-1] else 'OBJ_EVENT_GFX_ROCKET_F', x, y, d, sight, script))
        add_sc += '\n%s::\n\ttrainerbattle_single %s, %s_Text_Onybris%sIntro, %s_Text_Onybris%sDefeat\n\tmsgbox %s_Text_Onybris%sPost, MSGBOX_AUTOCLOSE\n\tend\n' % (script, tid, mp, lab, mp, lab, mp, lab)
        add_tx += '\n%s_Text_Onybris%sIntro::\n    .string "%s$"\n\n%s_Text_Onybris%sDefeat::\n    .string "%s$"\n\n%s_Text_Onybris%sPost::\n    .string "%s$"\n' % (mp, lab, intro, mp, lab, defeat, mp, lab, post)
    hide = 'call_if_set FLAG_AMETHYST_STONE_GIVEN, %s_EventScript_HideOnybris\n\tcall_if_unset FLAG_AMETHYST_RAID_STARTED, %s_EventScript_HideOnybris' % (mp, mp)
    if mp == 'SafariZone_West':
        for s in BT.values(): chk(s)
        tid, x, y, d, sight = BOSS[1], BOSS[2], BOSS[3], BOSS[4], BOSS[5]
        o = obj(tid, 'OBJ_EVENT_GFX_ROCKET_F', x, y, d, sight, 'SafariZone_West_EventScript_OnybrisSelene', 'FLAG_TEMP_6'); o = {'local_id': 'LOCALID_SAFARI_SELENE', **o}; m['object_events'].append(o)
        add_sc += ('\nSafariZone_West_EventScript_OnybrisSelene::\n\ttrainerbattle_single TRAINER_MAGMA_ADMIN_COURTNEY, SafariZone_West_Text_SeleneIntro, SafariZone_West_Text_SeleneDefeat, SafariZone_West_EventScript_SeleneLeaves\n'
                   '\tmsgbox SafariZone_West_Text_SelenePost, MSGBOX_AUTOCLOSE\n\tend\n\nSafariZone_West_EventScript_SeleneLeaves::\n\tmsgbox SafariZone_West_Text_SelenePost\n\tclosemessage\n\tfadescreen FADE_TO_BLACK\n'
                   '\tremoveobject LOCALID_SAFARI_SELENE\n\tdelay 20\n\tfadescreen FADE_FROM_BLACK\n\trelease\n\tend\n'
                   '\nSafariZone_West_EventScript_HideSelene::\n\tsetflag FLAG_TEMP_6\n\treturn\n')
        add_tx += '\nSafariZone_West_Text_SeleneIntro::\n    .string "%s$"\n\nSafariZone_West_Text_SeleneDefeat::\n    .string "%s$"\n\nSafariZone_West_Text_SelenePost::\n    .string "%s$"\n' % (BT['Intro'], BT['Defeat'], BT['Post'])
        hide += '\n\tcall_if_defeated TRAINER_MAGMA_ADMIN_COURTNEY, SafariZone_West_EventScript_HideSelene'
    add_sc += '\n%s_EventScript_HideOnybris::\n\tsetflag FLAG_TEMP_5\n\tsetflag FLAG_TEMP_6\n\treturn\n' % mp
    if '_OnTransition::' in sc and mp == 'SafariZone_Center':
        sc = re.sub(r'(%s_OnTransition::\n(?:\t.*\n)*?)\tend\n' % mp, lambda mm: mm.group(1) + '\t' + hide + '\n\tend\n', sc, 1) if 'HideOnybris' not in sc else sc
    elif 'HideOnybris' not in sc:
        sc = sc.replace('%s_MapScripts::\n\t.byte 0\n' % mp, '%s_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, %s_OnTransition\n\t.byte 0\n\n%s_OnTransition::\n\t%s\n\tend\n' % (mp, mp, mp, hide), 1)
    if 'HideOnybris::' not in sc: sc += add_sc
    else:   # regenerer : retirer l'ancien bloc
        pass
    if 'OnybrisGrunt1Intro' not in tx and 'SeleneIntro' not in tx: tx += add_tx
    json.dump(m, open(f, 'w'), indent=2); open('data/maps/%s/scripts.inc' % mp, 'w').write(sc); open('data/maps/%s/text.inc' % mp, 'w').write(tx)
