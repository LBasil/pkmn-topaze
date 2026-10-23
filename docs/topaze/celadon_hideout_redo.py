#!/usr/bin/env python3
"""Repaire de Bourg Quartz (ex-Rocket) : histoire Onybris coherente (23/10). Idempotent.
Branche n°3 du reseau : la branche de l'argent (le casino blanchit le butin). Scene d'entree a la B1F, livre de comptes a la B3F."""
import json, re
R = 'data/maps/RocketHideout_%s/'
def S(*lines): return '    .string "' + '"\n    .string "'.join(lines) + '$"' if False else None
def txt(label, *lines):
    return label + '::\n' + '\n'.join('    .string "%s"' % l for l in lines[:-1]) + ('\n' if len(lines) > 1 else '') + '    .string "%s$"\n' % lines[-1] if len(lines) > 1 else label + '::\n    .string "%s$"\n' % lines[0]
def P(*paras): return paras
def body(label, text):      # text avec \n et \p deja ecrits : decoupe en lignes .string
    parts = re.split(r'(?<=\\n)|(?<=\\p)|(?<=\\l)', text)
    return label + '::\n' + '\n'.join('    .string "%s%s"' % (p, '$' if i == len(parts) - 1 else '') for i, p in enumerate(parts)) + '\n\n'
T = {
'B1F': [
 ('Grunt1Intro', r"Hold it. ROCKET left this lift to\nrot. ONYBRIS keeps it running."),
 ('Grunt1Defeat', r"Oww!\nBeaten!"),
 ('Grunt1PostBattle', r"ROCKET vanished years ago and left\nthe whole base behind.\pONYBRIS moved in, scrubbed three\nrooms blue, and called it a bank.\pOur boss never calls. Orders just\nappear in our heads. Creepy, huh?"),
 ('Grunt2Intro', r"A customer in the new reception?\nManagement does not allow that."),
 ('Grunt2Defeat', r"Boom!"),
 ('Grunt2PostBattle', r"ONYBRIS paid for the paint. The\nrest of the floor is still ROCKET's\lold mess. Watch your step.\pThis branch pays for the whole\nnetwork. Touch it and you answer\lto VESPER."),
 ('Grunt3Intro', r"Intruder alert!"),
 ('Grunt3Defeat', r"I can't do it!"),
 ('Grunt3PostBattle', r"ROCKET left crates of junk down\nhere. We sell whatever we find.\pRusty, dusty... but the cash\nspends just the same."),
 ('Grunt4Intro', r"Why did you come here?"),
 ('Grunt4Defeat', r"This won't do!"),
 ('Grunt4PostBattle', r"Okay, I'll talk...\nThese were ROCKET's bunks. Nobody\lcleaned them. Nobody dares.\pTake the elevator to see VESPER.\nBut the LIFT KEY went missing.\lAsk the guards on the lower floors."),
 ('Grunt5Intro', r"Are you lost, you little mouse?\nThe old bunks are off limits!"),
 ('Grunt5Defeat', r"Why…?"),
 ('Grunt5PostBattle', r"Uh-oh, that ruckus somehow opened\nthe door!"),
 ('Entry1', r"Fresh blue paint, new lights, a new\ndesk. But under the paint, a faded\lred R still shows through.\p"),
 ('Entry2', r"ROCKET abandoned this base long\nago. Now somebody has taken it\lback, one blue room at a time."),
],
'B2F': [
 ('GruntIntro', r"ROCKET's old maze still works.\nThey fled, but the traps stayed!"),
 ('GruntDefeat', r"I surrender!"),
 ('GruntPostBattle', r"ONYBRIS never fixed the arrows.\nCheaper to let intruders get lost.\pThe more the town plays upstairs,\nthe more we launder. Think you can\lreach VESPER?"),
],
'B3F': [
 ('Grunt1Intro', r"Stop meddling in TEAM ONYBRIS's\naffairs or else!"),
 ('Grunt1Defeat', r"Oof!\nTaken down!"),
 ('Grunt1PostBattle', r"The LIFT KEY? One of the guards\nbelow keeps it on him.\pRead the ledger in the office if\nyou want to know what you are up\lagainst."),
 ('Grunt2Intro', r"We got word from upstairs that you\nwere coming!"),
 ('Grunt2Defeat', r"What?\nI lost? No!"),
 ('Grunt2PostBattle', r"Go ahead and go!\pBut you can't run the elevator\nwithout the LIFT KEY."),
 ('Ledger', r"A ledger lies open on the new desk.\p“BRANCH 3 of 7: the money branch.\nCasino takings: sorted, counted,\lsent up to V.”\p“Old ROCKET base: 4 rooms cleaned,\nthe rest is junk. Do not bother.”\p“Quartz is in V.'s pocket. The\nboss wants ten stones, not one.”\pYou keep one page: a cash voucher."),
 ('LedgerDone', r"Only dull numbers and a stamp:\n“BRANCH 3 of 7”."),
],
'B4F': [
 ('GiovanniIntro', r"VESPER: So you are the brat who\nkeeps wrecking my plans.\pROCKET left this base to rot. I\nonly took what was worth taking:\lthe vault, and this office.\pNow, scram!"),
 ('GiovanniDefeat', r"Impossible...!"),
 ('GiovanniPostBattle', r"VESPER: Hmph. You beat me...\nin a fight. Fights are for fools.\pI have the QUARTZ in my pocket.\nThe boss wants ten stones. Ten!\pDo not ask me why. I only collect.\pLet us settle it like adults: at my\ntable in the GAME CORNER, upstairs.\pWin, and you keep it. Lose, and it\nis mine. Come, if you dare!"),
 ('Grunt2Intro', r"I know you!\nYou have been all over our network!"),
 ('Grunt2Defeat', r"Burned again!"),
 ('Grunt2PostBattle', r"Do you have something against TEAM\nONYBRIS?"),
 ('Grunt3Intro', r"How can you not see the beauty of\nour business?"),
 ('Grunt3Defeat', r"Ayaya!"),
 ('Grunt3PostBattle', r"BOSS!\nI'm sorry I failed you!"),
 ('Grunt1Intro', r"The elevator doesn't work?\nROCKET's old key has vanished!"),
 ('Grunt1Defeat', r"No!"),
 ('Grunt1PostBattle', r"Oh, no!\nI dropped the LIFT KEY!"),
 ('FoundRocketLedger', r"{PLAYER} searched VESPER's desk.\pUnder a stack of vouchers lay a\nbattered case: the POKé FLUTE,\lstolen from MR. FUJI!"),
 ('ReceivedPokeFlute', r"{PLAYER} received the POKé FLUTE.\pIt wakes sleeping POKéMON."),
],
}
def lines_ok(t):
    for l in re.split(r'\\n|\\p|\\l', t): assert len(l.replace('{PLAYER}', 'PLAYERNAME')) <= 35, ('trop long', l)
for f, items in T.items():
    out = ''
    for k, t in items:
        lines_ok(t)
        lab = 'RocketHideout_%s_Text_%s' % (f, k)
        out += body(lab, t)
    open((R % f) + 'text.inc', 'w').write(out)
# ---- B1F : scene d'entree
m = json.load(open(R % 'B1F' + 'map.json'))
m['coord_events'] = m.get('coord_events') or []
if not any(c['script'] == 'RocketHideout_B1F_EventScript_Entry' for c in m['coord_events']):
    for x in (12, 13): m['coord_events'].append({'type': 'trigger', 'x': x, 'y': 3, 'elevation': 3, 'var': 'VAR_TEMP_0', 'var_value': '0', 'script': 'RocketHideout_B1F_EventScript_Entry'})
json.dump(m, open(R % 'B1F' + 'map.json', 'w'), indent=2); open(R % 'B1F' + 'map.json', 'a').write('\n')
s = open(R % 'B1F' + 'scripts.inc').read()
if 'Entry::' not in s:
    s += '''
@ Topaze: scene d'entree du repaire de Bourg Quartz (premiere fois)
RocketHideout_B1F_EventScript_Entry::
	lockall
	setvar VAR_TEMP_0, 1
	goto_if_set FLAG_TOPAZE_VAULT_ENTERED, RocketHideout_B1F_EventScript_EntryEnd
	setflag FLAG_TOPAZE_VAULT_ENTERED
	msgbox RocketHideout_B1F_Text_Entry1
	msgbox RocketHideout_B1F_Text_Entry2
RocketHideout_B1F_EventScript_EntryEnd::
	releaseall
	end
'''
open(R % 'B1F' + 'scripts.inc', 'w').write(s)
# ---- B3F : livre de comptes
m = json.load(open(R % 'B3F' + 'map.json'))
if not any(b.get('script') == 'RocketHideout_B3F_EventScript_Ledger' for b in m['bg_events']):
    m['bg_events'].append({'type': 'sign', 'x': 15, 'y': 7, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY', 'script': 'RocketHideout_B3F_EventScript_Ledger'})
json.dump(m, open(R % 'B3F' + 'map.json', 'w'), indent=2); open(R % 'B3F' + 'map.json', 'a').write('\n')
s = open(R % 'B3F' + 'scripts.inc').read()
if 'Ledger::' not in s:
    s += '''
RocketHideout_B3F_EventScript_Ledger::
	lockall
	goto_if_set FLAG_TOPAZE_LEDGER_CELADON, RocketHideout_B3F_EventScript_LedgerDone
	msgbox RocketHideout_B3F_Text_Ledger, MSGBOX_DEFAULT
	giveitem ITEM_PP_MAX, 1
	setflag FLAG_TOPAZE_LEDGER_CELADON
	releaseall
	end

RocketHideout_B3F_EventScript_LedgerDone::
	msgbox RocketHideout_B3F_Text_LedgerDone, MSGBOX_DEFAULT
	releaseall
	end
'''
open(R % 'B3F' + 'scripts.inc', 'w').write(s)
f = open('include/constants/flags.h').read()
if 'TOPAZE_LEDGER_CELADON' not in f:
    f = f.replace('#define FLAG_0x11D               0x11D\n', '#define FLAG_0x11D               0x11D\n#define FLAG_TOPAZE_LEDGER_CELADON FLAG_0x11D // livre de comptes du repaire de Bourg Quartz (branche 3)\n#define FLAG_TOPAZE_VAULT_ENTERED FLAG_0x11E // premiere entree dans le repaire de Bourg Quartz\n')
    f = f.replace('#define FLAG_0x11E               0x11E\n', '#define FLAG_0x11E               0x11E\n', 1)
open('include/constants/flags.h', 'w').write(f)
print('ok')
