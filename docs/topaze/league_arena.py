#!/usr/bin/env python3
"""Réécrit le tournoi dans la 1re salle de la Ligue (PokemonLeague_LoreleisRoom) :
9 matchs (VAR_TOURNAMENT_ROUND 0-8). Chen (9) et le boss (10) sont dans ChampionsRoom."""
import re

P = 'PokemonLeague_LoreleisRoom'
# (gfx, const, étape, intro, défaite)
R = [
 ('SCIENTIST',     'SEKO',    'POOL STAGE, MATCH 1 OF 5.',
  'PROF. SEKO: Even a professor enters\\nthe LEAGUE!\\pLet me see what you have learned\\nfrom your journey!',
  'Remarkable! Your POKéMON have\\ngrown so much!'),
 ('RS_MAY',        'MAY',     'POOL STAGE, MATCH 2 OF 5.',
  'MAY: Hi! I trained all the way from\\nHOENN for this!\\pI will not go easy on you!',
  'Wow, you are strong!\\nI will train even harder!'),
 ('RS_BRENDAN',    'BRENDAN', 'POOL STAGE, MATCH 3 OF 5.',
  'BRENDAN: So you are the one\\neveryone is talking about.\\pLet us see if the rumors are true!',
  'Not bad at all.\\nYou earned that win.'),
 ('COOLTRAINER_M', 'GOLD',    'POOL STAGE, MATCH 4 OF 5.',
  'GOLD: Finally, a worthy opponent!\\pMy partners and I have been\\nwaiting for this.',
  'Ha! That was a good one!'),
 ('COOLTRAINER_F', 'CRYSTAL', 'POOL STAGE, MATCH 5 OF 5.',
  'CRYSTAL: Last match of the pool!\\pI am not here to lose.\\nLet us fight with two POKéMON\\lat once!',
  'You are through.\\nGood luck in the bracket!'),
 ('BEAUTY',        'LEAF',    'ROUND OF 16.',
  'LEAF: The bracket starts here.\\pI have faced many TRAINERS, but\\nI keep getting stronger.',
  'I have no regrets.\\nGo on ahead!'),
 ('BLUE',          'ZEPHYR',  'QUARTER-FINAL.',
  '{RIVAL}: Well, well. You made it\\nthis far.\\pI will not let my rival beat me\\nin front of this crowd!',
  'Tch... You really have\\ngotten strong.'),
 ('BLUE',          'BLUE',    'SEMI-FINAL.',
  'BLUE: Smell that? The air of the\\nreal thing.\\pI was CHAMPION once. Show me\\nyou deserve more than that!\\pTwo POKéMON each. Ready?',
  'Hmph. Fine. You win this one.'),
 ('GENTLEMAN',     'N',       'THE FINAL.',
  'N: I can hear your POKéMON.\\pThey trust you. Yet are you\\nsure they are truly happy?\\pLet me hear their answer!',
  'Their voices... they chose you.\\nI understand now.'),
]

# --- scripts.inc
f = f'data/maps/{P}/scripts.inc'; s = open(f).read()
# gfx
a = s.index('@ Topaze: the first hall')
b = s.index(f'{P}_OnWarp::')
g = '@ Topaze: the first hall is the tournament arena (9 matches, VAR_TOURNAMENT_ROUND 0-8)\n'
g += f'{P}_EventScript_SetOpponentGfx::\n'
for i, r in enumerate(R):
    g += f'\tsetvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_{r[0]}\n'
    if i < len(R) - 1:
        g += f'\tgoto_if_eq VAR_TOURNAMENT_ROUND, {i}, {P}_EventScript_GfxDone\n'
g += f'{P}_EventScript_GfxDone::\n\treturn\n\n'
s = s[:a] + g + s[b:]
# lorelei entry: tournament all the way
s = s.replace('\tgoto_if_lt VAR_TOURNAMENT_ROUND, 5, ', '\tgoto_if_lt VAR_TOURNAMENT_ROUND, 9, ')
# replace everything from the tournament match switch to the end
a = s.index(f'{P}_EventScript_TournamentMatch::')
t = f'{P}_EventScript_TournamentMatch::\n\tswitch VAR_TOURNAMENT_ROUND\n'
for i in range(len(R)):
    t += f'\tcase {i}, {P}_EventScript_Round{i}\n'
t += '\trelease\n\tend\n\n'
for i, r in enumerate(R):
    last = i == len(R) - 1
    t += f'{P}_EventScript_Round{i}::\n'
    t += f'\tmsgbox {P}_Text_Round{i}Intro\n'
    t += f'\ttrainerbattle_no_intro TRAINER_LEAGUE_{r[1]}, {P}_Text_Round{i}Defeat\n'
    t += f'\tsetvar VAR_TOURNAMENT_ROUND, {i + 1}\n'
    t += f'\tgoto {P}_EventScript_' + ('TournamentWon' if last else 'NextMatch') + '\n\tend\n\n'
t += f'''{P}_EventScript_NextMatch::
	msgbox {P}_Text_NextMatch
	closemessage
	special HealPlayerParty
	fadescreen FADE_TO_BLACK
	warp MAP_POKEMON_LEAGUE_LORELEIS_ROOM, 6, 10
	waitstate
	end

@ Topaze: end of the bracket. The way to the CHAMPION's room opens.
{P}_EventScript_TournamentWon::
	setflag FLAG_DEFEATED_LORELEI
	call PokemonLeague_EventScript_OpenDoor
	special HealPlayerParty
	msgbox {P}_Text_TournamentWon
	release
	end
'''
s = s[:a] + t
open(f, 'w').write(s)

# --- text.inc
f = f'data/maps/{P}/text.inc'; s = open(f).read()
a = s.index(f'{P}_Text_Round0Intro::')
x = ''
for i, r in enumerate(R):
    x += f'{P}_Text_Round{i}Intro::\n    .string "{r[2]}\\p"\n'
    parts = r[3].split('\\p')
    for j, p in enumerate(parts):
        end = '' if j == len(parts) - 1 else '\\p'
        lines = p.split('\\n')
        for k, ln in enumerate(lines):
            last = (j == len(parts) - 1 and k == len(lines) - 1)
            if last:
                x += f'    .string "{ln}{{PLAY_BGM}}{{MUS_ENCOUNTER_GYM_LEADER}}$"\n'
            else:
                sep = end if k == len(lines) - 1 else '\\n'
                x += f'    .string "{ln}{sep}"\n'
    x += f'\n{P}_Text_Round{i}Defeat::\n    .string "{r[4]}$"\n\n'
x += f'''{P}_Text_NextMatch::
    .string "Well fought!\\p"
    .string "The next match begins shortly.\\n"
    .string "Recover your strength.$"

{P}_Text_TournamentWon::
    .string "The crowd roars!\\p"
    .string "You are the winner of the\\n"
    .string "POKéMON LEAGUE tournament!\\p"
    .string "Now, the CHAMPION is waiting\\n"
    .string "beyond the door.$"
'''
open(f, 'w').write(s[:a] + x)
print('arena ok')
