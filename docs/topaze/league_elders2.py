#!/usr/bin/env python3
"""Conseil des Anciens v2 : ajoute les 7 champions d'arene de Kanto (Koga est deja Ancien) en tete -> 20 combats.
Reutilise les ids des 7 chefs d'arene Hoenn inutilises (ROXANNE..WINONA) renommes TRAINER_ELDER_*. Regenere les blocs scripts/textes. Non rejouable."""
import re, sys
rd = lambda p: open(p).read(); wr = lambda p, s: open(p, 'w').write(s)
if 'TRAINER_ELDER_BROCK' in rd('include/constants/opponents.h'): print('already'); sys.exit(0)
src = rd('docs/topaze/league_elders.py')
ns = {}
exec(src[src.index('E = ['):src.index("\nP = ")], {'re': re}, ns); OLD = ns['E']
# (cle, nom, pic, gfx, ancien_id_hoenn, equipe, intro, defaite)
L = [
 ('BROCK','BROCK','LEADER_BROCK','BROCK','ROXANNE',[('GOLEM',66),('ONIX',66),('OMASTAR',67),('KABUTOPS',67),('RHYDON',68),('AERODACTYL',69)],
  'BROCK: My defense is rock solid.\\pShow me you can break it!','You cracked my defense...'),
 ('MISTY','MISTY','LEADER_MISTY','MISTY','BRAWLY',[('STARMIE',66),('GOLDUCK',66),('LAPRAS',67),('VAPOREON',67),('SLOWBRO',68),('GYARADOS',69)],
  'MISTY: Water POKéMON are not\\njust pretty!\\pDive in, CHAMPION!','Wow! You are a real CHAMPION!'),
 ('SURGE','LT. SURGE','LEADER_LT_SURGE','LT_SURGE','TATE_LIZA',[('RAICHU',66),('ELECTRODE',66),('MAGNETON',67),('ELECTABUZZ',67),('JOLTEON',68),('AMPHAROS',69)],
  'LT. SURGE: Hey, kid! I heard you\\nbecame CHAMPION!\\pLet me test that voltage!','Shocking! You are strong!'),
 ('ERIKA','ERIKA','LEADER_ERIKA','ERIKA','WATTSON',[('VILEPLUME',66),('VICTREEBEL',66),('TANGELA',67),('BELLOSSOM',67),('VENUSAUR',68),('EXEGGUTOR',69)],
  'ERIKA: Oh, hello. I was watering\\nthe flowers.\\pShall we have a gentle battle?','Oh my... You bloomed beautifully.'),
 ('SABRINA','SABRINA','LEADER_SABRINA','SABRINA','FLANNERY',[('ALAKAZAM',66),('MR_MIME',66),('ESPEON',67),('HYPNO',67),('SLOWKING',68),('GIRAFARIG',69)],
  'SABRINA: I foresaw this battle.\\pI did not foresee how it ends.','I did not foresee this...'),
 ('BLAINE','BLAINE','LEADER_BLAINE','BLAINE','NORMAN',[('ARCANINE',66),('RAPIDASH',66),('MAGMAR',67),('NINETALES',67),('FLAREON',68),('CHARIZARD',69)],
  'BLAINE: Hah! My fire is still\\nburning hot!\\pLet us see if you can take it!','I burned out... Well fought!'),
 ('GIOVANNI','GIOVANNI','LEADER_GIOVANNI','GIOVANNI','WINONA',[('NIDOKING',66),('NIDOQUEEN',66),('RHYDON',67),('DUGTRIO',67),('PERSIAN',68),('KANGASKHAN',69)],
  'GIOVANNI: ...The ground trembles\\nbefore a true CHAMPION.\\pI will not hold back.','Hmph. The earth bows to you.'),
]
for l in L:
    for ln in re.split(r'\\p|\\n', l[6]):
        if len(ln) > 35: raise SystemExit('LONG ' + ln)
E = [(l[0], l[1], l[2], l[3], None, l[5], l[6], l[7]) for l in L] + OLD
N = len(E); P = 'PokemonLeague_LoreleisRoom'
# --- opponents.h : renommage
s = rd('include/constants/opponents.h')
for l in L:
    s, n = re.subn(r'#define TRAINER_LEADER_%s(\s+)' % l[4], lambda m: '#define TRAINER_ELDER_%s%s' % (l[0], m.group(1)), s)
    assert n == 1, l[4]
wr('include/constants/opponents.h', s)
# --- trainers.h
tr = rd('src/data/trainers.h')
for k, name, pic, gfx, _, team, i_, d_ in [l[:5] + l[5:] for l in [(l[0], l[1], l[2], l[3], None, l[5], l[6], l[7]) for l in L]]:
    old = [l[4] for l in L if l[0] == k][0]
    blk = f'''    [TRAINER_ELDER_{k}] = {{
        .trainerClass = TRAINER_CLASS_PKMN_TRAINER,
        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,
        .trainerPic = TRAINER_PIC_{pic},
        .trainerName = _("{name}"),
        .items = {{ITEM_FULL_RESTORE, ITEM_FULL_RESTORE}},
        .doubleBattle = FALSE,
        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,
        .party = NO_ITEM_DEFAULT_MOVES(sParty_Elder{k.title()}),
    }},
'''
    tr, n = re.subn(r'    \[TRAINER_LEADER_%s\] = \{.*?\n    \},\n' % old, lambda m: blk, tr, count=1, flags=re.S)
    assert n == 1, old
wr('src/data/trainers.h', tr)
pa = rd('src/data/trainer_parties.h'); body = ''
for l in L:
    body += f'static const struct TrainerMonNoItemDefaultMoves sParty_Elder{l[0].title()}[] = {{\n' + ''.join(
        f'    {{\n        .iv = 220,\n        .lvl = {lv},\n        .species = SPECIES_{sp},\n    }},\n' for sp, lv in l[5]) + '};\n\n'
i = pa.index('static const struct TrainerMonNoItemDefaultMoves sParty_LeagueBoss2[]'); j = pa.index('\n};\n', i) + 4
pa = pa[:j] + '\n' + body.rstrip('\n') + '\n' + pa[j:]; wr('src/data/trainer_parties.h', pa)
# --- scripts.inc : regenere
f = f'data/maps/{P}/scripts.inc'; s = rd(f)
a = s.index('\n@ Topaze: Council of Elders (post-game)\n'); s = s[:a].rstrip('\n') + '\n'
a = s.index('@ Topaze: post-game Council of Elders, opponent sprite per round'); b = s.index(f'{P}_OnWarp::')
eg = f'@ Topaze: post-game Council of Elders, opponent sprite per round\n{P}_EventScript_SetElderGfx::\n'
for i, e in enumerate(E):
    eg += f'\tsetvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_{e[3]}\n'
    if i < N - 1: eg += f'\tgoto_if_eq VAR_ELDERS_ROUND, {i}, {P}_EventScript_GfxDone\n'
eg += f'\tgoto {P}_EventScript_GfxDone\n\n'
s = s[:a] + eg + s[b:]
t = f'\n@ Topaze: Council of Elders (post-game)\n{P}_EventScript_ElderMatch::\n\tgoto_if_ge VAR_ELDERS_ROUND, {N}, {P}_EventScript_ElderDone\n\tswitch VAR_ELDERS_ROUND\n'
for i in range(N): t += f'\tcase {i}, {P}_EventScript_Elder{i}\n'
t += '\trelease\n\tend\n\n'
for i, e in enumerate(E):
    const = e[4] or f'TRAINER_ELDER_{e[0]}'
    t += f'{P}_EventScript_Elder{i}::\n\tmsgbox {P}_Text_Elder{i}Intro\n\ttrainerbattle_no_intro {const}, {P}_Text_Elder{i}Defeat\n\tsetvar VAR_ELDERS_ROUND, {i + 1}\n'
    t += f'\tgoto {P}_EventScript_' + ('ElderReward' if i == N - 1 else 'NextElder') + '\n\tend\n\n'
t += f'''{P}_EventScript_NextElder::
	msgbox {P}_Text_NextElder
	closemessage
	special HealPlayerParty
	fadescreen FADE_TO_BLACK
	warp MAP_POKEMON_LEAGUE_LORELEIS_ROOM, 6, 10
	waitstate
	end

{P}_EventScript_ElderReward::
	special HealPlayerParty
	msgbox {P}_Text_ElderReward
	giveitem ITEM_MASTER_BALL
	release
	end

{P}_EventScript_ElderDone::
	msgbox {P}_Text_ElderDone
	release
	end
'''
wr(f, s + t)
# --- text.inc
def lines(x):
    out = ''; ps = x.split('\\p')
    for i, p_ in enumerate(ps):
        ls = p_.split('\\n')
        for j, l in enumerate(ls):
            last = i == len(ps) - 1 and j == len(ls) - 1
            sep = '{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}$' if last else ('\\p' if j == len(ls) - 1 else '\\n')
            out += f'    .string "{l}{sep}"\n'
    return out
f = f'data/maps/{P}/text.inc'; s = rd(f)
s = s[:s.index(f'\n{P}_Text_Elder0Intro::')].rstrip('\n') + '\n'
tx = ''
for i, e in enumerate(E):
    tx += f'\n{P}_Text_Elder{i}Intro::\n    .string "COUNCIL OF ELDERS, {i + 1} OF {N}.\\p"\n' + lines(e[6])
    tx += f'\n{P}_Text_Elder{i}Defeat::\n    .string "{e[7]}$"\n'
tx += f'''
{P}_Text_NextElder::
    .string "Well fought!\\p"
    .string "The next veteran steps forward.\\n"
    .string "Recover your strength.$"

{P}_Text_ElderReward::
    .string "All {N} veterans bow to you.\\p"
    .string "You are the greatest of all\\n"
    .string "the CHAMPIONS!\\p"
    .string "Take this, as proof of their\\n"
    .string "respect.$"

{P}_Text_ElderDone::
    .string "The old guard has nothing more\\n"
    .string "to teach you, CHAMPION.$"
'''
wr(f, s + tx)
print('elders2 ok', N)
