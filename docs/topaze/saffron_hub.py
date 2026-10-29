#!/usr/bin/env python3
"""HUB DU TEMPS (Safrania) : 7 maisons libres (SaffronCity_Home*) reecrites en batiments utiles. Textes anglais PROVISOIRES.
  HomeN musee du Temps | HomeM tour chronometree (5 combats) | HomeA auberge du Sablier | HomeE spa | HomeB bureau de poste (lettre du futur)
  HomeC objets perdus (3 objets caches sur les routes) | HomeD tournoi des routes (10 dresseurs -> ROI DES ROUTES)
Flags 0x210..0x214. Dresseurs reutilises : 86,87,88,176,257 -> TRAINER_TRIAL_1..5 ; 263 -> TRAINER_ROUTE_KING. Idempotent."""
import sys, os, re, json
sys.path.insert(0, 'docs/topaze'); sys.path.insert(0, 'tools/topaze/emu'); sys.path.insert(0, '/tmp/gx')
import newmap as N, route_test as R
rd, wr = N.rd, N.wr
if 'TRAINER_TRIAL_1' in rd('include/constants/opponents.h'): print('deja applique'); raise SystemExit
# ---------------- flags
fl = rd('include/constants/flags.h')
fl = fl.replace('\n#endif // GUARD_CONSTANTS_FLAGS_H', '\n// Topaze: hub du Temps\n' + '\n'.join('#define %s FLAG_0x%X' % (n, 0x210 + i) for i, n in enumerate(
    ['FLAG_TOPAZE_LETTER', 'FLAG_TOPAZE_LOST_1', 'FLAG_TOPAZE_LOST_2', 'FLAG_TOPAZE_LOST_3', 'FLAG_TOPAZE_LOST_DONE'])) + '\n\n#endif // GUARD_CONSTANTS_FLAGS_H')
wr('include/constants/flags.h', fl)
# ---------------- dresseurs
OLD = {86: 'LEADER_WALLACE', 87: 'ELITE_FOUR_GLACIA', 88: 'ELITE_FOUR_DRAKE', 176: 'SUPER_NERD_3', 257: 'CUE_BALL_CHASE', 263: 'GAMER_1'}
NEW = {86: 'TRIAL_1', 87: 'TRIAL_2', 88: 'TRIAL_3', 176: 'TRIAL_4', 257: 'TRIAL_5', 263: 'ROUTE_KING'}
PIC = {86: 'ELITE_FOUR_PHOEBE', 87: 'ELITE_FOUR_GLACIA', 88: 'ELITE_FOUR_LORELEI', 176: 'ELITE_FOUR_AGATHA', 257: 'ELITE_FOUR_LANCE', 263: 'RIVAL_LATE'}
NAME = {86: 'SECOND', 87: 'MINUTE', 88: 'HOUR', 176: 'DAY', 257: 'YEAR', 263: 'KING'}
TEAM = {
 86: (60, 255, [('ALAKAZAM', 'PSYCHIC SHADOW_BALL FOCUS_BLAST RECOVER'), ('JOLTEON', 'THUNDER SHADOW_BALL VOLT_SWITCH ENERGY_BALL'), ('ELECTRODE', 'THUNDERBOLT VOLT_SWITCH THUNDER_WAVE ENERGY_BALL'), ('AERODACTYL', 'STONE_EDGE EARTHQUAKE FLY ROOST')]),
 87: (65, 255, [('STARMIE', 'HYDRO_PUMP ICE_BEAM PSYCHIC RECOVER'), ('LAPRAS', 'SURF ICE_BEAM THUNDERBOLT REST'), ('GYARADOS', 'WATERFALL CRUNCH EARTHQUAKE DRAGON_DANCE'), ('VAPOREON', 'SURF ICE_BEAM SHADOW_BALL PROTECT')]),
 88: (70, 255, [('SNORLAX', 'BODY_SLAM EARTHQUAKE REST SLEEP_TALK'), ('TAUROS', 'DOUBLE_EDGE EARTHQUAKE ZEN_HEADBUTT ROCK_SLIDE'), ('KANGASKHAN', 'DOUBLE_EDGE EARTHQUAKE CRUNCH FIRE_PUNCH'), ('PORYGON', 'TRI_ATTACK ICE_BEAM THUNDERBOLT RECOVER')]),
 176: (75, 255, [('ARCANINE', 'FLARE_BLITZ EXTREME_SPEED CRUNCH CLOSE_COMBAT'), ('GENGAR', 'SHADOW_BALL SLUDGE_BOMB FOCUS_BLAST THUNDERBOLT'), ('MACHAMP', 'CLOSE_COMBAT STONE_EDGE EARTHQUAKE BULLET_PUNCH'), ('VENUSAUR', 'GIGA_DRAIN SLUDGE_BOMB SLEEP_POWDER EARTHQUAKE')]),
 257: (80, 255, [('BLASTOISE', 'SCALD ICE_BEAM FLASH_CANNON ROAR'), ('CHARIZARD', 'FLAMETHROWER AIR_SLASH DRAGON_PULSE ROOST'), ('ZAPDOS', 'THUNDER HURRICANE HEAT_WAVE ROOST'), ('DRAGONITE', 'OUTRAGE EXTREME_SPEED EARTHQUAKE DRAGON_DANCE')]),
 263: (46, 230, [('PIDGEOT', 'BRAVE_BIRD HURRICANE ROOST U_TURN'), ('RAICHU', 'THUNDERBOLT FOCUS_BLAST SURF NASTY_PLOT'), ('FEAROW', 'DRILL_PECK DOUBLE_EDGE U_TURN ROOST'), ('NIDOKING', 'EARTH_POWER SLUDGE_WAVE ICE_BEAM THUNDERBOLT'), ('NIDOQUEEN', 'EARTH_POWER SLUDGE_WAVE ICE_BEAM THUNDERBOLT'), ('SNORLAX', 'BODY_SLAM EARTHQUAKE REST SLEEP_TALK')]),
}
op, tr, tp = rd('include/constants/opponents.h'), rd('src/data/trainers.h'), rd('src/data/trainer_parties.h')
consts = rd('include/constants/moves.h') + rd('include/constants/species.h')
for i, old in OLD.items():
    op, k = re.subn(r'(#define )TRAINER_%s(\s+)' % old, r'\1TRAINER_%s\2' % NEW[i], op); assert k == 1, old
    m = re.search(r'    \[TRAINER_%s\] = \{.*?\n    \},\n' % old, tr, re.S); assert m, old
    pn = 'sParty_' + ''.join(w.capitalize() for w in NEW[i].split('_'))
    ent = ('    [TRAINER_%s] = {\n        .trainerClass = TRAINER_CLASS_PKMN_TRAINER,\n        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_%s,\n        .trainerPic = TRAINER_PIC_%s,\n        .trainerName = _("%s"),\n'
           '        .items = {ITEM_FULL_RESTORE, ITEM_FULL_RESTORE},\n        .doubleBattle = FALSE,\n        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,\n        .party = ITEM_CUSTOM_MOVES(%s),\n    },\n') % (
        NEW[i], 'FEMALE' if PIC[i] in ('ELITE_FOUR_PHOEBE', 'ELITE_FOUR_GLACIA', 'ELITE_FOUR_LORELEI', 'ELITE_FOUR_AGATHA') else 'MALE', PIC[i], NAME[i], pn)
    tr = tr[:m.start()] + ent + tr[m.end():]
    lvl, iv, team = TEAM[i]; mons = ''
    for k2, (sp, mv) in enumerate(team):
        assert re.search(r'#define SPECIES_%s\b' % sp, consts), sp
        for x in mv.split(): assert re.search(r'#define MOVE_%s\b' % x, consts), x
        mons += '    {\n        .iv = %d,\n        .lvl = %d,\n        .species = SPECIES_%s,\n        .heldItem = %s,\n        .moves = {%s},\n    },\n' % (iv, lvl + (k2 if i != 263 else k2 // 2), sp, ['ITEM_LEFTOVERS', 'ITEM_SCOPE_LENS', 'ITEM_FOCUS_BAND', 'ITEM_QUICK_CLAW', 'ITEM_KINGS_ROCK'][k2 % 5], ', '.join('MOVE_' + x for x in mv.split()))
    cap = ''.join(w.capitalize() for w in OLD[i].split('_')); mm = re.search(r'static const struct TrainerMonNoItemDefaultMoves sParty_%s\[\] = \{DUMMY_TRAINER_MON\};\n' % re.escape(cap), tp)
    if not mm: mm = re.search(r'static const struct \w+ sParty_%s\[\] = \{.*?\};\n' % re.escape(cap), tp, re.S)
    assert mm, cap
    tp = tp[:mm.start()] + '// Topaze: %s (hub du Temps)\nstatic const struct TrainerMonItemCustomMoves %s[] = {\n%s};\n' % (NAME[i], pn, mons) + tp[mm.end():]
wr('include/constants/opponents.h', op); wr('src/data/trainers.h', tr); wr('src/data/trainer_parties.h', tp)
# ---------------- batiments
ECHOES = [('FLAG_ECHO_BEAST_DONE', 'RAIKOU', 'It crossed KINDLE ROAD once. The ground still remembers its thunder.'),
          ('FLAG_ECHO_BEAST2_DONE', 'ENTEI', 'It burned a path across CAPE BRINK. The ash never settled.'),
          ('FLAG_ECHO_BEAST3_DONE', 'SUICUNE', 'The BOND BRIDGE rings when it passes. The water clears for it.'),
          ('FLAG_ECHO_BEAST4_DONE', 'REGICE', 'Cold older than the island. It waits at the end of ICEFALL CAVE.'),
          ('FLAG_ECHO_BEAST5_DONE', 'REGISTEEL', 'Iron that was never forged. The MEADOW grows around it.'),
          ('FLAG_ECHO_BEAST6_DONE', 'REGIROCK', 'Stone that remembers every footstep in RUIN VALLEY.'),
          ('FLAG_DONE_ECHO_CELEBI', 'CELEBI', 'It showed the way through time. The moss still glows where it slept.')]
def room_signs(name, n, xs):
    nav = R.Nav(name); out = []
    for x in xs:
        y = next(y for y in range(nav.h) if not nav.blocked(x, y))
        out.append((x, y - 1))
    return out
S = 'SaffronCity_'
# --- Musee
H = S + 'HomeN'; sc = ''; tx = ''
objs = [N.obj('GENTLEMAN', 5, 3, H + '_EventScript_Guide')]
sc += '%s_EventScript_Guide::\n\tmsgbox %s_Text_Guide, MSGBOX_NPC\n\tend\n\n' % (H, H)
tx += N.text(H + '_Text_Guide', 'Welcome to the MUSEUM OF TIME. One plate for each ECHO. Read them in the order you met them.')
bgs = []
for k, ((fl_, nm, t), (x, y)) in enumerate(zip(ECHOES, room_signs(H, 7, [0 + 2, 3, 4, 6, 7, 8, 9][:7]))):
    # 7 plaques : x distincts sur le mur du fond
    sc += '%s_EventScript_Plate%d::\n\tgoto_if_unset %s, %s_EventScript_Blank\n\tmsgbox %s_Text_Plate%d, MSGBOX_SIGN\n\tend\n\n' % (H, k, fl_, H, H, k)
    tx += N.text('%s_Text_Plate%d' % (H, k), nm + ': ' + t); bgs.append(N.sign(x, y, '%s_EventScript_Plate%d' % (H, k)))
sc += '%s_EventScript_Blank::\n\tmsgbox %s_Text_Blank, MSGBOX_SIGN\n\tend\n' % (H, H); tx += N.text(H + '_Text_Blank', 'The plate is blank. Nothing has been written here yet.')
N.rewrite(H, objs, sc, tx, bgs=bgs)
# --- Tour chronometree
H = S + 'HomeM'; sc = '''%(H)s_EventScript_Master::
	lock
	faceplayer
	goto_if_unset FLAG_BADGE08_GET, %(H)s_EventScript_Early
	msgbox %(H)s_Text_Intro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, %(H)s_EventScript_Decline
	special HealPlayerParty
	msgbox %(H)s_Text_Go
	closemessage
''' % {'H': H}
for k, tn in enumerate(['TRIAL_1', 'TRIAL_2', 'TRIAL_3', 'TRIAL_4', 'TRIAL_5'], 1):
    sc += '\ttrainerbattle_no_intro TRAINER_%s, %s_Text_Beat%d\n' % (tn, H, k)
sc += '''	goto_if_defeated TRAINER_TRIAL_5, %(H)s_EventScript_Repeat
	release
	end
%(H)s_EventScript_Repeat::
	msgbox %(H)s_Text_Clear
	checkitemspace ITEM_RARE_CANDY, 5
	goto_if_eq VAR_RESULT, FALSE, %(H)s_EventScript_NoRoom
	giveitem ITEM_RARE_CANDY, 5
	release
	end
%(H)s_EventScript_Early::
	msgbox %(H)s_Text_Early
	release
	end
%(H)s_EventScript_Decline::
	msgbox %(H)s_Text_Decline
	release
	end
%(H)s_EventScript_NoRoom::
	msgbox %(H)s_Text_NoRoom
	release
	end
''' % {'H': H}
tx = ''.join(N.text(H + '_Text_' + k, v) for k, v in dict(
    Intro='This is the TRIAL TOWER. Five rivals, back to back, no healing between rounds. Ready to race the clock?', Go='Then begin. SECOND is first.',
    Beat1='Too slow...', Beat2='A minute is not enough.', Beat3='An hour well spent... for you.', Beat4='The day is yours.', Beat5='A whole year lost to you...',
    Clear='All five down! Time itself bows to you. Take these as proof.', Early='Not yet. Come back with all 8 BADGES.', Decline='Time waits for no one. But I will.', NoRoom='Your BAG is full. Make room, then come back.').items())
N.rewrite(H, [N.obj('BLACK_BELT', 5, 3, H + '_EventScript_Master')], sc, tx)
# --- Auberge du Sablier
H = S + 'HomeA'
sc = '''%(H)s_EventScript_Keeper::
	lock
	faceplayer
	msgbox %(H)s_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, %(H)s_EventScript_No
	fadescreen FADE_TO_BLACK
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox %(H)s_Text_Rested
	release
	end
%(H)s_EventScript_No::
	msgbox %(H)s_Text_No
	release
	end
%(H)s_EventScript_Guest::
	msgbox %(H)s_Text_Guest, MSGBOX_NPC
	end
''' % {'H': H}
tx = ''.join(N.text(H + '_Text_' + k, v) for k, v in dict(Offer='Welcome to the HOURGLASS INN. A bed, free of charge. Sleep a while?', Rested='You slept... for an hour? A day? Your team feels brand new.',
                                                     No='The sand keeps falling. Come back when you are tired.', Guest='I checked in at noon. The sun has set three times since.').items())
N.rewrite(H, [N.obj('BEAUTY', 5, 3, H + '_EventScript_Keeper'), N.obj('HIKER', 8, 5, H + '_EventScript_Guest', mv='MOVEMENT_TYPE_FACE_LEFT')], sc, tx)
# --- Spa
H = S + 'HomeE'
sc = '''%(H)s_EventScript_Attendant::
	lock
	faceplayer
	msgbox %(H)s_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, %(H)s_EventScript_No
	fadescreen FADE_TO_BLACK
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox %(H)s_Text_Done
	release
	end
%(H)s_EventScript_No::
	msgbox %(H)s_Text_No
	release
	end
''' % {'H': H}
tx = ''.join(N.text(H + '_Text_' + k, v) for k, v in dict(Offer='Welcome to the SPA. A warm bath for you and your team. Care to enjoy it?', Done='Ahh... Everyone is refreshed. Come back anytime.', No='Of course. The water is always warm here.').items())
N.rewrite(H, [N.obj('WOMAN_1', 5, 3, H + '_EventScript_Attendant')], sc, tx)
# --- Poste : la lettre du futur
H = S + 'HomeB'
sc = '''%(H)s_EventScript_Clerk::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_LETTER, %(H)s_EventScript_Done
	goto_if_unset FLAG_TOPAZE_CLOCK_1, %(H)s_EventScript_None
	goto_if_unset FLAG_TOPAZE_CLOCK_2, %(H)s_EventScript_None
	goto_if_unset FLAG_TOPAZE_CLOCK_3, %(H)s_EventScript_None
	checkitemspace ITEM_MAX_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, %(H)s_EventScript_NoRoom
	msgbox %(H)s_Text_Letter
	setflag FLAG_TOPAZE_LETTER
	giveitem ITEM_MAX_ELIXIR, 1
	msgbox %(H)s_Text_Read
	release
	end
%(H)s_EventScript_None::
	msgbox %(H)s_Text_None
	release
	end
%(H)s_EventScript_Done::
	msgbox %(H)s_Text_Done
	release
	end
%(H)s_EventScript_NoRoom::
	msgbox %(H)s_Text_NoRoom
	release
	end
''' % {'H': H}
tx = ''.join(N.text(H + '_Text_' + k, v) for k, v in dict(
    None_='x', Letter='A letter just arrived for you, {PLAYER}. It is dated... tomorrow. The handwriting is yours.', Read='It reads: THE FERRYMAN AT AMETHIOLITE KNOWS WHERE TIME RUNS ELSEWHERE. ASK HIM. Signed: you.',
    Done='No more letters today. Or yesterday. Or tomorrow.', NoRoom='Your BAG is full. Make room, then come back.').items() if k != 'None_')
tx += N.text(H + '_Text_None', 'No mail for you yet. Odd. The postman says letters are arriving before they are written.')
N.rewrite(H, [N.obj('WORKER_M', 5, 3, H + '_EventScript_Clerk')], sc, tx)
# --- Objets perdus
H = S + 'HomeC'; LOST = [('SCOPE_LENS', 'Route4'), ('KINGS_ROCK', 'Route10'), ('BLACK_GLASSES', 'Route14')]
sc = '%s_EventScript_Clerk::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_TOPAZE_LOST_DONE, %s_EventScript_Done\n' % (H, H)
for it, _ in LOST: sc += '\tcheckitem ITEM_%s, 1\n\tgoto_if_eq VAR_RESULT, FALSE, %s_EventScript_Ask\n' % (it, H)
sc += '\tcheckitemspace ITEM_MAX_ELIXIR, 3\n\tgoto_if_eq VAR_RESULT, FALSE, %s_EventScript_NoRoom\n' % H
for it, _ in LOST: sc += '\tremoveitem ITEM_%s, 1\n' % it
sc += '\tsetflag FLAG_TOPAZE_LOST_DONE\n\tmsgbox %s_Text_Thanks\n\tgiveitem ITEM_MAX_ELIXIR, 3\n\trelease\n\tend\n' % H
for k in ('Ask', 'Done', 'NoRoom'): sc += '%s_EventScript_%s::\n\tmsgbox %s_Text_%s\n\trelease\n\tend\n' % (H, k, H, k)
tx = ''.join(N.text(H + '_Text_' + k, v) for k, v in dict(Ask='LOST AND FOUND. Three things were lost on the routes: SCOPE LENS (ROUTE 4), KINGS ROCK (ROUTE 10), BLACK GLASSES (ROUTE 14). Bring them back.',
                                                     Thanks='All three! Their owners will be so happy. Here, a reward.', Done='Nothing left to find. The routes feel a bit lighter now.', NoRoom='Your BAG is full. Make room, then come back.').items())
N.rewrite(H, [N.obj('OLD_MAN_1', 5, 3, H + '_EventScript_Clerk')], sc, tx)
for k, (it, m) in enumerate(LOST, 1):
    mp = 'data/maps/%s/map.json' % m; d = json.load(open(mp)); nav = R.Nav(m)
    occ = {(o['x'], o['y']) for o in d['object_events']} | {(b['x'], b['y']) for b in d['bg_events'] if 'x' in b}
    cells = [(x, y) for y in range(2, nav.h - 2) for x in range(2, nav.w - 2) if not nav.blocked(x, y) and (x, y) not in nav.warps and (x, y) not in occ and all(not nav.blocked(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1))]
    cells.sort(key=lambda c: abs(c[0] - nav.w // 2 + 3) + abs(c[1] - nav.h // 2 - 2)); x, y = cells[0]
    d['bg_events'].append({"type": "hidden_item", "x": x, "y": y, "elevation": nav.g[y * nav.w + x] >> 12 or 3, "item": "ITEM_" + it, "flag": "FLAG_TOPAZE_LOST_%d" % k, "quantity": 1, "underfoot": False})
    N.jdump(d, mp); print('objet perdu', it, m, (x, y))
# --- Tournoi des routes
H = S + 'HomeD'
src = rd('data/scripts/trainers.inc'); seen = []; routes = []
for m_, t_ in re.findall(r'^(Route\d+)_EventScript_\w+::\n\ttrainerbattle_single (TRAINER_\w+)', src, re.M):
    if m_ not in routes: routes.append(m_); seen.append(t_)
ten = seen[:10]
sc = '%s_EventScript_Registrar::\n\tlock\n\tfaceplayer\n\tgoto_if_defeated TRAINER_ROUTE_KING, %s_EventScript_Done\n' % (H, H)
for t_ in ten: sc += '\tgoto_if_not_defeated %s, %s_EventScript_Ask\n' % (t_, H)
sc += '\tmsgbox %s_Text_Ready\n\ttrainerbattle_no_intro TRAINER_ROUTE_KING, %s_Text_Beaten\n\tcheckitemspace ITEM_RARE_CANDY, 3\n\tgoto_if_eq VAR_RESULT, FALSE, %s_EventScript_NoRoom\n\tmsgbox %s_Text_Prize\n\tgiveitem ITEM_RARE_CANDY, 3\n\trelease\n\tend\n' % (H, H, H, H)
for k in ('Ask', 'Done', 'NoRoom'): sc += '%s_EventScript_%s::\n\tmsgbox %s_Text_%s\n\trelease\n\tend\n' % (H, k, H, k)
tx = ''.join(N.text(H + '_Text_' + k, v) for k, v in dict(
    Ask='ROUTE TOURNAMENT. Beat one trainer on each of ten routes: ' + ', '.join(r.replace('Route', 'R') for r in routes[:10]) + '. Then face the ROUTE KING.',
    Ready='Ten routes, ten victories. The KING is waiting. Ready?', Beaten='The crown is yours... for now.', Prize='A new KING of the routes! Here, your prize.',
    Done='You are the ROUTE KING. The routes will remember.', NoRoom='Your BAG is full. Make room, then come back.').items())
N.rewrite(H, [N.obj('GENTLEMAN', 5, 3, H + '_EventScript_Registrar')], sc, tx)
print('routes tournoi', routes[:10])
# ---------------- journal
g = rd('docs/topaze/journal_gen.py')
if 'TRAINER_TRIAL_5' not in g:
    i = g.index('assert len(SECTIONS) <= 12')
    g = g[:i] + '\n'.join([
        '# ---- HUB DU TEMPS (Safrania)',
        'add("SIDE QUESTS", T, "TRAINER_TRIAL_5", 0, "THE TRIAL TOWER", "SAFFRON: beat 5 rivals in a row,\\\\nno healing. Needs 8 BADGES.", B(8))',
        'add("SIDE QUESTS", F, "FLAG_TOPAZE_LETTER", 0, "A LETTER FROM TOMORROW", "SAFFRON POST OFFICE: read the 3\\\\nclocks, then ask for your mail.", B(2))',
        'add("SIDE QUESTS", F, "FLAG_TOPAZE_LOST_DONE", 0, "LOST AND FOUND", "SAFFRON: find 3 lost items hidden\\\\non ROUTES 4, 10 and 14.", B(2))',
        'add("SIDE QUESTS", T, "TRAINER_ROUTE_KING", 0, "THE ROUTE TOURNAMENT", "SAFFRON: beat a trainer on 10\\\\nroutes, then face the KING.", B(3))', '']) + g[i:]
    wr('docs/topaze/journal_gen.py', g)
