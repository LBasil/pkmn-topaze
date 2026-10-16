#!/usr/bin/env python3
"""Fin 3 « Reconquete » : 7 chefs dans leur arene (hook Visit3), 7 Seigneurs des iles Sevii (PNJ fixes), hub Flora (Hepha, Ligue, Maitres, Steven). Genere flags, scripts, textes, objets de cartes. Idempotent NON (a lancer une fois)."""
import json, re, os, sys
sys.path.insert(0, 'tools/topaze/maps')
import place_npc
# ---- flags
FLAGS = {'REBEL_KAY':'100','REBEL_SYLVESTRE':'101','REBEL_HERA':'102','REBEL_GRIM':'103','REBEL_ACHLYS':'104','REBEL_NOX':'105','REBEL_EDDIE':'106',
 'LORD_ONE':'107','LORD_TWO':'108','LORD_THREE':'109','LORD_FOUR':'10A','LORD_FIVE':'10B','LORD_SIX':'10C','LORD_SEVEN':'10D'}
fl = open('include/constants/flags.h').read()
for n, idx in FLAGS.items():
    old = f'#define FLAG_0x{idx}               0x{idx}'
    assert old in fl, idx
    fl = fl.replace(old, f'#define FLAG_{n} 0x{idx} // Topaze: ending 3 conquest')
open('include/constants/flags.h', 'w').write(fl)

def appendf(p, s): open(p, 'a').write(s)
def lines(txt): return txt.split('\n')
def textblock(label, txt):
    parts = txt.split('\n'); out = f'\n{label}::\n'
    for i, l in enumerate(parts): out += '    .string "' + l + ('\\n"\n' if i < len(parts) - 1 else '$"\n')
    return out

# ---- 1) chefs dans leur arene : on remplace Visit3 par un duel de revanche (une seule fois, drapeau FLAG_REBEL_*)
GYMS = [ # map, label, trainer, flag, boost, name, intro, defeat, after, reward
 ('PewterCity_Gym','Brock','TRAINER_LEADER_BROCK','FLAG_REBEL_KAY',54,'KAY',
  "The Council is over, but my rocks\\nnever stopped training, CHAMPION.\\pYou hold the six legends. Let me see\\nif a mountain can hold you!",
  "Cracked...\\nbut not broken.",
  "KAY: The REBELS are not your enemies.\\nWe only wanted to be asked.\\pTake this. Go on, the others wait."),
 ('CeruleanCity_Gym','Misty','TRAINER_LEADER_MISTY','FLAG_REBEL_SYLVESTRE',50,'SYLVESTRE',
  "Bugs and leaves take years to grow\\nback. We have grown, CHAMPION.\\pShow me why they should follow you!",
  "Pressed like a flower\\nin a book...",
  "SYLVESTRE: I said we would bow to\\nno one. I did not say we would not\\llisten. Take this."),
 ('VermilionCity_Gym','LtSurge','TRAINER_LEADER_LT_SURGE','FLAG_REBEL_HERA',45,'HERA',
  "I fly where the wind says. And the\\nwind says you rule everything now.\\pI will test that wind myself!",
  "Grounded...\\nthe sky respects you.",
  "HERA: The sky is wide enough for\\nthe two of us. Take this and soar."),
 ('CeladonCity_Gym','Erika','TRAINER_LEADER_ERIKA','FLAG_REBEL_GRIM',41,'GRIM',
  "Ice keeps what it holds, CHAMPION.\\nCan you hold six legends without\\lfreezing the world around you?",
  "Thawed...\\nI see now.",
  "GRIM: Hold them gently. Ice cracks\\nwhen squeezed. Take this."),
 ('FuchsiaCity_Gym','Koga','TRAINER_LEADER_KOGA','FLAG_REBEL_ACHLYS',38,'ACHLYS',
  "My poison once served the shadows.\\nNow I serve the question: should\\lone trainer rule it all?",
  "A cure...\\nyou found it.",
  "ACHLYS: The answer is not yes or no.\\nIt is how. Take this antidote."),
 ('SaffronCity_Gym','Sabrina','TRAINER_LEADER_SABRINA','FLAG_REBEL_NOX',35,'NOX',
  "I saw you in a dream: a crown with\\nsix gems. I did not see how it ends.\\pLet us find out together.",
  "The dream breaks.\\nThe morning is yours.",
  "NOX: Dreams can lie. I do not think\\nyours does. Take this."),
 ('CinnabarIsland_Gym','Blaine','TRAINER_LEADER_BLAINE','FLAG_REBEL_EDDIE',32,'EDDIE',
  "Hot-blooded or cold-hearted, you\\ntook the throne. Let me taste the\\lfire of your six legends!",
  "Burnt to ash...\\nbut I am smiling.",
  "EDDIE: Hah! That's the spirit. The\\nflame is yours to guard. Take this."),
]
for m, lab, tc, F, boost, nm, intro, defeat, after in GYMS:
    p = f'data/maps/{m}/scripts.inc'; s = open(p).read()
    vis = f'{m}_EventScript_{lab}Visit3::'
    if vis in s:
        # remplace le corps de Visit3
        pat = re.compile(re.escape(vis) + r'\n.*?\n\treturn\n', re.S)
        assert pat.search(s), m
        body = f'''{vis}
	goto_if_set {F}, EventScript_Return
	msgbox {m}_Text_{lab}Rebel1
	setvar VAR_TOPAZE_BOOST, {boost}
	trainerbattle_no_intro {tc}, {m}_Text_{lab}Rebel2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	setflag {F}
	msgbox {m}_Text_{lab}Rebel3
	giveitem ITEM_RARE_CANDY, 5
	giveitem ITEM_PP_MAX, 2
	return
'''
        s = pat.sub(lambda _: body, s, 1)
        open(p, 'w').write(s)
    else:
        # carte non encore equipee (Tourmalia) : ajoute le trio complet
        pass
    t = f'data/maps/{m}/text.inc'
    appendf(t, textblock(f'{m}_Text_{lab}Rebel1', nm + ': ' + intro.split('\\n')[0] + '\n' + '\n'.join(intro.split('\\n')[1:])) if False else '')
    # texte : 'NOM: ' + intro (les \\p/\\l restent dans les lignes)
    ilines = (nm + ': ' + intro).split('\\n'); dl = defeat.split('\\n')
    appendf(t, textblock(f'{m}_Text_{lab}Rebel1', '\n'.join(ilines).replace('\\n', '\n')))
    appendf(t, textblock(f'{m}_Text_{lab}Rebel2', '\n'.join(dl)))
    appendf(t, textblock(f'{m}_Text_{lab}Rebel3', after.replace('\\n', '\n')))

# ---- 2) Seigneurs des iles
LORDS = [ # carte, local id, flag, trainer, boost, nom, gfx, intro, defeat, after, recompense
 ('OneIsland','LORD_ONE','FLAG_LORD_ONE','TRAINER_ELDER_WILL',17,'WILL','OBJ_EVENT_GFX_PSYCHIC_M',
  "I read your thoughts before you\\nspeak, CHAMPION. You hold six\\llegends and fear your own power.\\pLet me test that fear!",
  "I saw the wrong future.",
  "WILL: The mind is a door, not a wall.\\nKeep yours open. Take this.",
  'ITEM_RARE_CANDY, 4'),
 ('TwoIsland','LORD_TWO','FLAG_LORD_TWO','TRAINER_ELDER_KAREN',17,'KAREN',None,
  "Strong people, weak people... I\\ncare only about the Pokémon who\\lfollow you. Do they love you?",
  "They do. I can see it.",
  "KAREN: Then you may rule, as long as\\nthey keep following. Take this.",
  'ITEM_RARE_CANDY, 4'),
 ('ThreeIsland','LORD_THREE','FLAG_LORD_THREE','TRAINER_ELDER_SIDNEY',16,'SIDNEY',None,
  "Hah! I traveled the whole world to\\nfind someone worth fighting. Looks\\llike the world came to me!",
  "Awesome! I'm glad I waited!",
  "SIDNEY: Keep that fire. And try not\\nto get bored at the top. Take this.",
  'ITEM_PP_MAX, 4'),
 ('FourIsland','LORD_FOUR','FLAG_LORD_FOUR','TRAINER_ELDER_GLACIA',15,'GLACIA',None,
  "Frozen cities, frozen kings... it\\nhappened before. I will see how\\lyour crown holds against ice!",
  "Warm. You are warm.",
  "GLACIA: A ruler who can still feel\\nthe cold is a good ruler. Take this.",
  'ITEM_RARE_CANDY, 4'),
 ('FiveIsland','LORD_FIVE','FLAG_LORD_FIVE','TRAINER_ELDER_PHOEBE',14,'PHOEBE',None,
  "The spirits whisper that you hold\\nsix legends. They are not afraid.\\pThey are curious. So am I!",
  "The spirits are laughing.",
  "PHOEBE: They like you. That is rare.\\nTake this, from the other side.",
  'ITEM_MAX_ELIXIR, 5'),
 ('SixIsland','LORD_SIX','FLAG_LORD_SIX','TRAINER_ELDER_DRAKE',13,'DRAKE',None,
  "I sailed every sea to learn one\\nthing: respect is earned, never\\lgiven. So earn it, CHAMPION!",
  "Hah! The sea bows to you.",
  "DRAKE: Fair winds, ruler of the six.\\nTake this for the road.",
  'ITEM_PP_MAX, 4'),
 ('SevenIsland','LORD_SEVEN','FLAG_LORD_SEVEN','TRAINER_ELDER_WALLACE',12,'WALLACE',None,
  "Beauty and strength should rule\\ntogether. Shall we see if your\\lcrown is as beautiful as it is heavy?",
  "Splendid. Truly splendid.",
  "WALLACE: You are the finest ruler I\\nhave seen. Take this, with my thanks.",
  'ITEM_MAX_REVIVE, 5'),
]
GFX = ['OBJ_EVENT_GFX_WOMAN_1','OBJ_EVENT_GFX_BLACKBELT','OBJ_EVENT_GFX_COOLTRAINER_M','OBJ_EVENT_GFX_COOLTRAINER_F','OBJ_EVENT_GFX_HIKER','OBJ_EVENT_GFX_BEAUTY','OBJ_EVENT_GFX_COOLTRAINER_M']
for i, (m, lid, F, tc, boost, nm, gfx, intro, defeat, after, reward) in enumerate(LORDS):
    anchor, cell = place_npc.choose(m, 'PokemonCenter'); assert cell, m
    mj_p = f'data/maps/{m}/map.json'; j = json.load(open(mj_p))
    lab = f'{m}_EventScript_Lord'
    j['object_events'].append({'graphics_id': gfx or GFX[i], 'x': cell[0], 'y': cell[1], 'elevation': 3, 'movement_type': 'MOVEMENT_TYPE_FACE_DOWN',
        'movement_range_x': 0, 'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE', 'trainer_sight_or_berry_tree_id': '0', 'script': lab, 'flag': '0'})
    json.dump(j, open(mj_p, 'w'), indent=2)
    p = f'data/maps/{m}/scripts.inc'
    appendf(p, f'''
@ Topaze, fin 3 : Seigneur de l'ile (duel avec niveaux gonfles par VAR_TOPAZE_BOOST), apres les Maitres de la Ligue (VAR_REBELS_ROUND >= 8)
{lab}::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_ne VAR_TOPAZE_ENDING, 3, {lab}Idle
	goto_if_set {F}, {lab}Done
	goto_if_lt VAR_REBELS_ROUND, 8, {lab}Early
	msgbox {m}_Text_Lord1
	setvar VAR_TOPAZE_BOOST, {boost}
	trainerbattle_no_intro {tc}, {m}_Text_Lord2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	setflag {F}
	msgbox {m}_Text_Lord3
	giveitem {reward}
	release
	end

{lab}Early::
	msgbox {m}_Text_LordEarly
	release
	end

{lab}Done::
	msgbox {m}_Text_LordDone
	release
	end

{lab}Idle::
	msgbox {m}_Text_LordIdle
	release
	end
''')
    t = f'data/maps/{m}/text.inc'
    appendf(t, textblock(f'{m}_Text_Lord1', (nm + ': ' + intro).replace('\\n', '\n')))
    appendf(t, textblock(f'{m}_Text_Lord2', defeat.replace('\\n', '\n')))
    appendf(t, textblock(f'{m}_Text_Lord3', after.replace('\\n', '\n')))
    appendf(t, textblock(f'{m}_Text_LordEarly', nm + ': Not yet. The old LEAGUE\nand the MASTERS must fall first.\nFLORA will tell you the way.'))
    appendf(t, textblock(f'{m}_Text_LordDone', nm + ': A ruler worthy of the six.\nI will remember this day.'))
    appendf(t, textblock(f'{m}_Text_LordIdle', nm + ': The islands are quiet. I look\nafter them, as I always have.'))
    print(m, cell)
