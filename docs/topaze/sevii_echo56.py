#!/usr/bin/env python3
"""Echos 5 et 6 (post-game). Echo 5 : Bill (stage 12->13->14->15) envoie au Meadow (ile 5), Registeel niv. 54 (6,32), Bill donne FEUFOREVE (Torchic).
Echo 6 : Celio (15->16->17->18) envoie a Ruin Valley (ile 6), Regirock niv. 56 (14,23), Celio donne GOBOU (Mudkip).
Flags 0x0C8-0x0CB. Sprite provisoire = rocher. Non rejouable."""
import json, sys
rd = lambda p: open(p).read(); wr = lambda p, s: open(p, 'w').write(s)
if 'FLAG_HIDE_ECHO_BEAST5' in rd('include/constants/flags.h'): print('already'); sys.exit(0)
s = rd('include/constants/flags.h')
for k, n, t in (('0C8', 'FLAG_HIDE_ECHO_BEAST5   ', ' // Topaze: Echo 5 (Registeel)'), ('0C9', 'FLAG_ECHO_BEAST5_DONE   ', ''),
                ('0CA', 'FLAG_HIDE_ECHO_BEAST6   ', ' // Topaze: Echo 6 (Regirock)'), ('0CB', 'FLAG_ECHO_BEAST6_DONE   ', '')):
    s = s.replace(f'#define FLAG_0x{k}               0x{k}', f'#define {n}  0x{k}{t}', 1)
wr('include/constants/flags.h', s)
C = 'OneIsland_PokemonCenter_1F'
cf = f'data/maps/{C}/scripts.inc'; cs = rd(cf); ct = rd(f'data/maps/{C}/text.inc')
a = cs.index(f'{C}_EventScript_EchoGiftParty::'); b = cs.index(f'{C}_EventScript_EchoCelioDone::')
GIFT = cs[a:b]
E = [
 dict(n=5, giver='Bill', who='BILL', a=12, species='TORCHIC', nm='Torchic', bsp='REGISTEEL', lvl=54, mp='FiveIsland_Meadow', x=6, y=32,
      anchor=f'\tgoto_if_ge VAR_ECHO_STAGE, 1, {C}_EventScript_EchoBillAfter\n',
      announce=['BILL: The fifth ECHO is on FIVE', 'ISLAND, in the MEADOW.', '', 'A statue of steel stands there.', 'Please, calm it down.'],
      wait=['BILL: The MEADOW, on FIVE ISLAND.', 'Steel does not bend easily.'],
      gift=['BILL: The ECHO is closed!', '', 'A little POKéMON came through.', 'It will warm your journey.'],
      nxt=['BILL: Five ECHOES closed. Ask', 'CELIO about the next one.']),
 dict(n=6, giver='Celio', who='CELIO', a=15, species='MUDKIP', nm='Mudkip', bsp='REGIROCK', lvl=56, mp='SixIsland_RuinValley', x=14, y=23,
      anchor=f'\tgoto_if_ge VAR_ECHO_STAGE, 3, {C}_EventScript_EchoCelioDone\n',
      announce=['CELIO: The sixth ECHO is in', 'RUIN VALLEY, on SIX ISLAND.', '', 'A statue of stone guards it.', 'It has waited a long time.'],
      wait=['CELIO: RUIN VALLEY, SIX ISLAND.', 'Mind the old ruins.'],
      gift=['CELIO: The ECHO is closed!', '', 'This POKéMON came with the', 'tide. Take good care of it.'],
      nxt=['CELIO: Six ECHOES closed. Only', 'one remains.']),
]
for d in E:
    n, a0 = d['n'], d['a']
    g = d['giver']; pre = f'Echo{n}'
    txt = lambda ls: '\n'.join('    .string "%s%s"' % (l, '\\n' if i < len(ls) - 1 and l != '' else '') for i, l in enumerate(ls))
    def tx(ls):
        out = ''; cur = []
        for l in ls:
            if l == '': cur.append('\\p')
            else: cur.append(l)
        # build with \n / \p separators
        res = []; i = 0
        s_ = ''
        for l in ls:
            if l == '':
                s_ = s_[:-2] + '\\p'; continue
            s_ += l + '\\n'
        s_ = s_[:-2] + '$'
        return ''.join('    .string "%s"\n' % p for p in split35(s_))
    def split35(s_):
        # split string at \n / \p boundaries into lines for .string (keeps escapes at end of each piece)
        import re
        parts = re.findall(r'.*?(?:\\n|\\p|\$)', s_)
        return [p for p in parts if p]
    # center map : dispatch + scripts
    disp = (f'\tgoto_if_eq VAR_ECHO_STAGE, {a0 + 2}, {C}_EventScript_{pre}Gift\n\tgoto_if_eq VAR_ECHO_STAGE, {a0 + 1}, {C}_EventScript_{pre}Wait\n'
            f'\tgoto_if_eq VAR_ECHO_STAGE, {a0}, {C}_EventScript_{pre}Announce\n')
    assert d['anchor'] in cs
    cs = cs.replace(d['anchor'], disp + d['anchor'], 1)
    blk = (GIFT.replace('CHIKORITA', d['species']).replace('EchoGiftParty', f'EchoGift{n}Party').replace('EchoGiftPC', f'EchoGift{n}PC')
           .replace('EchoGiftToPC', f'EchoGift{n}ToPC').replace('EchoGiftEnd', f'EchoGift{n}End').replace('EchoGotChikorita', f'EchoGot{d["nm"]}')
           .replace('setvar VAR_ECHO_STAGE, 3', f'setvar VAR_ECHO_STAGE, {a0 + 3}').replace('EchoCelioNext', f'Echo{n}Next'))
    cs = cs.rstrip('\n') + f'''

@ Topaze: Echo {n}
{C}_EventScript_{pre}Announce::
	msgbox {C}_Text_{pre}Announce
	setvar VAR_ECHO_STAGE, {a0 + 1}
	clearflag FLAG_HIDE_ECHO_BEAST{n}
	release
	end

{C}_EventScript_{pre}Wait::
	msgbox {C}_Text_{pre}Wait
	release
	end

{C}_EventScript_{pre}Gift::
	msgbox {C}_Text_{pre}Gift
	setvar VAR_TEMP_1, SPECIES_{d['species']}
	givemon SPECIES_{d['species']}, 30
	goto_if_eq VAR_RESULT, 0, {C}_EventScript_EchoGift{n}Party
	goto_if_eq VAR_RESULT, 1, {C}_EventScript_EchoGift{n}PC
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	release
	end

{blk.rstrip()}
'''
    ct = ct.rstrip('\n') + f'''

{C}_Text_{pre}Announce::
{tx(d['announce'])}
{C}_Text_{pre}Wait::
{tx(d['wait'])}
{C}_Text_{pre}Gift::
{tx(d['gift'])}
{C}_Text_Echo{n}Next::
{tx(d['nxt'])}
{C}_Text_EchoGot{d['nm']}::
    .string "{{{{PLAYER}}}} received {d['nm'].upper()}!$"
'''.replace('{{PLAYER}}', '{PLAYER}')
    # carte de la bete
    P = d['mp']; f = f'data/maps/{P}/scripts.inc'; s = rd(f)
    bs = d['bsp'].title()
    hdr = f'{P}_MapScripts::\n'
    assert hdr in s
    s = s.replace(hdr, hdr + f'\tmap_script MAP_SCRIPT_ON_TRANSITION, {P}_OnTransition\n', 1)
    wr(f, s.rstrip('\n') + f'''

@ Topaze: Echo {n} beast (static, stays if fled)
{P}_OnTransition::
	setflag FLAG_HIDE_ECHO_BEAST{n}
	goto_if_set FLAG_ECHO_BEAST{n}_DONE, EventScript_Return
	goto_if_ne VAR_ECHO_STAGE, {a0 + 1}, EventScript_Return
	clearflag FLAG_HIDE_ECHO_BEAST{n}
	end

{P}_EventScript_{bs}::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_{d['bsp']}, {d['lvl']}
	waitse
	playmoncry SPECIES_{d['bsp']}, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}_EventScript_Defeated{bs}
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}_EventScript_RanFrom{bs}
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}_EventScript_RanFrom{bs}
	setflag FLAG_ECHO_BEAST{n}_DONE
	setflag FLAG_HIDE_ECHO_BEAST{n}
	setvar VAR_ECHO_STAGE, {a0 + 2}
	release
	end

{P}_EventScript_Defeated{bs}::
	setflag FLAG_ECHO_BEAST{n}_DONE
	setvar VAR_ECHO_STAGE, {a0 + 2}
	goto EventScript_RemoveStaticMon
	end

{P}_EventScript_RanFrom{bs}::
	setvar VAR_0x8004, SPECIES_{d['bsp']}
	goto EventScript_MonFlewAway
	end
''')
    j = json.load(open(f'data/maps/{P}/map.json'))
    j['object_events'].append({'graphics_id': 'OBJ_EVENT_GFX_PUSHABLE_BOULDER', 'x': d['x'], 'y': d['y'], 'elevation': 3,
      'movement_type': 'MOVEMENT_TYPE_FACE_DOWN', 'movement_range_x': 1, 'movement_range_y': 1, 'trainer_type': 'TRAINER_TYPE_NONE',
      'trainer_sight_or_berry_tree_id': '0', 'script': f'{P}_EventScript_{bs}', 'flag': f'FLAG_HIDE_ECHO_BEAST{n}'})
    json.dump(j, open(f'data/maps/{P}/map.json', 'w'), indent=2); open(f'data/maps/{P}/map.json', 'a').write('\n')
wr(cf, cs); wr(f'data/maps/{C}/text.inc', ct)
print('echo56 ok')
