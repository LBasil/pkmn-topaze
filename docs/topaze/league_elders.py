#!/usr/bin/env python3
"""CONSEIL DES ANCIENS (post-game, fin 1) : 13 anciens Champions / Conseil des 4 / Maitres de Gen 1-3, dans la 1re salle de la Ligue.
VAR_ELDERS_ROUND 0-12 (13 = termine). Kanto : rematchs vanilla (TRAINER_ELITE_FOUR_*_2) ; Johto/Hoenn : 9 nouveaux dresseurs (TRAINER_ELDER_*). Non rejouable."""
import re, sys
rd = lambda p: open(p).read(); wr = lambda p, s: open(p, 'w').write(s)
if 'VAR_ELDERS_ROUND' in rd('include/constants/vars.h'): print('already'); sys.exit(0)
# (cle, nom, pic, gfx, const_existant|None, equipe, intro, defaite)
E = [
 ('LORELEI','LORELEI',None,'LORELEI','TRAINER_ELITE_FOUR_LORELEI_2',None,
  'LORELEI: The ice has not melted\\nsince you last came.\\pShow me the CHAMPION\'s strength!','Still cold as ever...\\nYou win.'),
 ('BRUNO','BRUNO',None,'BRUNO','TRAINER_ELITE_FOUR_BRUNO_2',None,
  'BRUNO: Hoo! The CHAMPION returns!\\pLet us see whose will is stronger!','Hah! My training was not enough!'),
 ('AGATHA','AGATHA',None,'AGATHA','TRAINER_ELITE_FOUR_AGATHA_2',None,
  'AGATHA: Hee hee! Look at you, a\\nCHAMPION.\\pI have buried better TRAINERS!','Oh, you old rascal.\\nYou win again.'),
 ('LANCE','LANCE',None,'LANCE','TRAINER_ELITE_FOUR_LANCE_2',None,
  'LANCE: The dragons knew you would\\ncome back.\\pLet me see how far you have grown.','Magnificent. Truly.'),
 ('WILL','WILL','PSYCHIC_M','GENTLEMAN',None,[('XATU',66),('JYNX',66),('EXEGGUTOR',67),('SLOWBRO',67),('ALAKAZAM',69)],
  'WILL: I saw your victory in dreams.\\pLet me see if the dream was true.','The dream was true...'),
 ('KOGA','KOGA','LEADER_KOGA','KOGA',None,[('ARIADOS',66),('VENOMOTH',66),('FORRETRESS',67),('MUK',67),('CROBAT',68),('WEEZING',69)],
  'KOGA: A ninja never loses twice.\\pYet I will gladly lose to a\\nworthy foe.','Hmm. Admirable technique.'),
 ('KAREN','KAREN','LADY','BEAUTY',None,[('UMBREON',67),('VILEPLUME',67),('GENGAR',68),('MURKROW',67),('HOUNDOOM',69)],
  'KAREN: Strong POKéMON, weak\\nPOKéMON... I do not care.\\pOnly the bond matters.','Your bond is real. Good.'),
 ('SIDNEY','SIDNEY','ELITE_FOUR_SIDNEY','BLACK_BELT',None,[('MIGHTYENA',66),('CACTURNE',66),('SHIFTRY',67),('SHARPEDO',67),('ABSOL',69)],
  'SIDNEY: Ahahaha! A CHAMPION!\\pI came all this way for a good\\nfight. Do not disappoint me!','Ahaha! That was worth the trip!'),
 ('PHOEBE','PHOEBE','ELITE_FOUR_PHOEBE','BEAUTY',None,[('DUSCLOPS',66),('BANETTE',66),('SABLEYE',67),('BANETTE',67),('DUSCLOPS',69)],
  'PHOEBE: The spirits whisper your\\nname, CHAMPION.\\pLet us listen together.','The spirits are pleased.'),
 ('GLACIA','GLACIA','ELITE_FOUR_GLACIA','COOLTRAINER_F',None,[('GLALIE',66),('SEALEO',66),('WALREIN',67),('GLALIE',67),('WALREIN',69)],
  'GLACIA: I have waited a long time\\nfor a fight that burns.\\pMelt me, if you can.','Finally... a fight that burns.'),
 ('DRAKE','DRAKE','ELITE_FOUR_DRAKE','SAILOR',None,[('ALTARIA',66),('FLYGON',67),('KINGDRA',67),('SALAMENCE',69)],
  'DRAKE: A true TRAINER treats\\nPOKéMON as equals.\\pShow me that you do!','Well fought, TRAINER.'),
 ('STEVEN','STEVEN','CHAMPION_STEVEN','GENTLEMAN',None,[('SKARMORY',67),('CLAYDOL',67),('AGGRON',68),('CRADILY',68),('ARMALDO',68),('METAGROSS',70)],
  'STEVEN: I collect stones. And I\\ncollect strong TRAINERS.\\pYou belong in both collections.','A battle to remember!'),
 ('WALLACE','WALLACE','LEADER_WALLACE','GENTLEMAN',None,[('WAILORD',68),('TENTACRUEL',68),('LUDICOLO',69),('WHISCASH',69),('GYARADOS',69),('MILOTIC',71)],
  'WALLACE: Beauty and strength, both.\\pThe last of the old guard\\nstands before you.','Splendid! You are a true MASTER.'),
]

for _e in E:
    for _l in re.split(r'\\p|\\n', _e[6]):
        if len(re.sub(r'\{[^}]*\}', 'X', _l)) > 35: raise SystemExit('LONG '+_l)
P = 'PokemonLeague_LoreleisRoom'
new = [e for e in E if e[4] is None]
# ---- vars
sub = lambda p, o, n: (lambda s: (lambda: wr(p, s.replace(o, n, 1)))() if o in s else (_ for _ in ()).throw(AssertionError((p, o[:50]))))(rd(p))
sub('include/constants/vars.h', '#define VAR_TOURNAMENT_ROUND VAR_0x402B', '#define VAR_ELDERS_ROUND VAR_0x402C // post-game Council of Elders, 0-12 (13 = done)\n#define VAR_TOURNAMENT_ROUND VAR_0x402B')
# ---- trainers
s = rd('include/constants/opponents.h')
base = int(re.search(r'#define NUM_TRAINERS\s+(\d+)', s).group(1))
defs = ''.join('#define TRAINER_ELDER_%-22s %d\n' % (e[0], base + i) for i, e in enumerate(new))
s = s.replace('\n// NOTE: Because each Trainer', '\n' + defs + '\n// NOTE: Because each Trainer', 1) if '// NOTE: Because each Trainer' in s else s
s = re.sub(r'#define NUM_TRAINERS\s+\d+', '#define NUM_TRAINERS                             %d' % (base + len(new)), s)
wr('include/constants/opponents.h', s)
tr = rd('src/data/trainers.h'); blk = ''
for k, name, pic, gfx, const, team, intro, dfn in new:
    blk += f'''    [TRAINER_ELDER_{k}] = {{
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
i = tr.index('    [TRAINER_LEAGUE_BOSS_2] = {'); j = tr.index('    },\n', i) + 7
tr = tr[:j] + blk + tr[j:]; wr('src/data/trainers.h', tr)
pa = rd('src/data/trainer_parties.h'); body = ''
for k, name, pic, gfx, const, team, intro, dfn in new:
    body += f'static const struct TrainerMonNoItemDefaultMoves sParty_Elder{k.title()}[] = {{\n' + ''.join(
        f'    {{\n        .iv = 220,\n        .lvl = {lv},\n        .species = SPECIES_{sp},\n    }},\n' for sp, lv in team) + '};\n\n'
i = pa.index('static const struct TrainerMonNoItemDefaultMoves sParty_LeagueBoss2[]'); j = pa.index('\n};\n', i) + 4
pa = pa[:j] + '\n' + body.rstrip('\n') + '\n' + pa[j:]; wr('src/data/trainer_parties.h', pa)
# ---- scripts
f = f'data/maps/{P}/scripts.inc'; s = rd(f)
g = f'{P}_EventScript_SetOpponentGfx::\n\tgoto_if_set FLAG_TOPAZE_POSTGAME, {P}_EventScript_SetElderGfx\n'
assert f'{P}_EventScript_SetOpponentGfx::\n' in s
s = s.replace(f'{P}_EventScript_SetOpponentGfx::\n', g, 1)
eg = f'\n@ Topaze: post-game Council of Elders, opponent sprite per round\n{P}_EventScript_SetElderGfx::\n'
for i, e in enumerate(E):
    eg += f'\tsetvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_{e[3]}\n'
    if i < len(E) - 1: eg += f'\tgoto_if_eq VAR_ELDERS_ROUND, {i}, {P}_EventScript_GfxDone\n'
eg += f'\tgoto {P}_EventScript_GfxDone\n\n'
s = s.replace(f'{P}_OnWarp::', eg.lstrip('\n') + f'{P}_OnWarp::', 1)
old = '\tfamechecker FAMECHECKER_LORELEI, FCPICKSTATE_COLORED, UpdatePickStateFromSpecialVar8005\n\tgoto_if_set FLAG_DEFEATED_LORELEI, '
assert old in s
s = s.replace(old, '\tgoto_if_set FLAG_TOPAZE_POSTGAME, ' + P + '_EventScript_ElderMatch\n' + old, 1)
t = f'\n@ Topaze: Council of Elders (post-game)\n{P}_EventScript_ElderMatch::\n\tgoto_if_ge VAR_ELDERS_ROUND, 13, {P}_EventScript_ElderDone\n\tswitch VAR_ELDERS_ROUND\n'
for i in range(13): t += f'\tcase {i}, {P}_EventScript_Elder{i}\n'
t += '\trelease\n\tend\n\n'
for i, e in enumerate(E):
    const = e[4] or f'TRAINER_ELDER_{e[0]}'
    last = i == 12
    t += f'{P}_EventScript_Elder{i}::\n\tmsgbox {P}_Text_Elder{i}Intro\n\ttrainerbattle_no_intro {const}, {P}_Text_Elder{i}Defeat\n\tsetvar VAR_ELDERS_ROUND, {i + 1}\n'
    t += f'\tgoto {P}_EventScript_' + ('ElderReward' if last else 'NextElder') + '\n\tend\n\n'
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
wr(f, s.rstrip('\n') + '\n' + t)
# ---- textes
def lines(x):
    out = ''; ps = x.split('\\p')
    for i, p_ in enumerate(ps):
        ls = p_.split('\\n')
        for j, l in enumerate(ls):
            assert len(re.sub(r'\{[^}]*\}', 'X', l)) <= 35, l
            last = i == len(ps) - 1 and j == len(ls) - 1
            sep = '{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}$' if last else ('\\p' if j == len(ls) - 1 else '\\n')
            out += f'    .string "{l}{sep}"\n'
    return out
tx = ''
for i, e in enumerate(E):
    tx += f'\n{P}_Text_Elder{i}Intro::\n    .string "COUNCIL OF ELDERS, {i + 1} OF 13.\\p"\n' + lines(e[6])
    tx += f'\n{P}_Text_Elder{i}Defeat::\n    .string "{e[7]}$"\n'
tx += f'''
{P}_Text_NextElder::
    .string "Well fought!\\p"
    .string "The next veteran steps forward.\\n"
    .string "Recover your strength.$"

{P}_Text_ElderReward::
    .string "All thirteen veterans bow to you.\\p"
    .string "You are the greatest of all\\n"
    .string "the CHAMPIONS!\\p"
    .string "Take this, as proof of their\\n"
    .string "respect.$"

{P}_Text_ElderDone::
    .string "The old guard has nothing more\\n"
    .string "to teach you, CHAMPION.$"
'''
wr(f'data/maps/{P}/text.inc', rd(f'data/maps/{P}/text.inc').rstrip('\n') + '\n' + tx)
print('elders ok', base, '->', base + len(new))
