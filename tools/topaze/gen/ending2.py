#!/usr/bin/env python3
"""Fin 2 « Le Refuge » : 16 postes de Gardes (PNJ fixes) dans les villes de Kanto et Sevii, enchaines par VAR_REFUGE_STAGE (VAR_0x402F), +3 grands defis finals chez le gardien du Safari. A lancer une fois."""
import json, re, sys
sys.path.insert(0, 'tools/topaze/maps')
import place_npc
fl = open('include/constants/flags.h').read()
def appendf(p, s): open(p, 'a').write(s)
def textblock(label, txt):
    parts = txt.split('\n'); out = f'\n{label}::\n'
    for i, l in enumerate(parts): out += '    .string "' + l + ('\\n"\n' if i < len(parts) - 1 else '$"\n')
    return out
vh = open('include/constants/vars.h').read()
if 'VAR_REFUGE_STAGE' not in vh:
    vh = vh.replace('#define VAR_ELDERS_ROUND VAR_0x402C', '#define VAR_REFUGE_STAGE VAR_0x402F // Topaze: ending 2, Refuge rangers chain 0-16 (19 = done)\n#define VAR_ELDERS_ROUND VAR_0x402C', 1)
    open('include/constants/vars.h', 'w').write(vh)
# niveaux des chasseurs
tr = open('src/data/trainers.h').read(); pa = open('src/data/trainer_parties.h').read()
def toplvl(t):
    m = re.search(r'\[TRAINER_' + t + r'\] = \{(.*?)\n    \},', tr, re.S); pm = re.search(r'\.party = \w+\((\w+)\)', m.group(1))
    return max(int(x) for x in re.findall(r'\.lvl = (\d+)', re.search(r'\b' + pm.group(1) + r'\[\] = \{(.*?)\n\};', pa, re.S).group(1)))
GENT = ['GENTLEMAN_THOMAS','GENTLEMAN_ARTHUR','GENTLEMAN_TUCKER','GENTLEMAN_NORTON','GENTLEMAN_WALTER','GENTLEMAN_BROOKS','GENTLEMAN_LAMAR','GENTLEMAN_CLIFFORD']
JUGG = ['JUGGLER_DALTON','JUGGLER_NELSON','JUGGLER_KIRK','JUGGLER_SHAWN','JUGGLER_GREGORY','JUGGLER_EDWARD','JUGGLER_KAYDEN','JUGGLER_NATE']
# poste: carte, nom, type, ...
POSTS = [
 ('PalletTown','AYA','I',('ITEM_POTION',5),'SPECIES_EEVEE','Eevee',
   "I run the first REFUGE post. Our\nfirst rule: nobody goes hungry.\nPOKéMON hurt in the wild have\nnowhere to go but here.\pI need five POTIONS for the new\narrivals. Can you spare them?"),
 ('ViridianCity','BRUN','D',None,'SPECIES_LARVITAR','Larvitar',
   "Hunters came last night, looking\nfor rare POKéMON to sell. They\nwant them back in cages.\pI cannot fight them alone."),
 ('PewterCity','CLEO','I',('ITEM_FULL_HEAL',3),'SPECIES_DRATINI','Dratini',
   "A DRATINI came down from the\nmountain, sick and scared. I need\nthree FULL HEALS to cure it."),
 ('CeruleanCity','DANTE','D',None,'SPECIES_BAGON','Bagon',
   "The river is quiet. Too quiet.\nHunters set traps near the bridge\nand I saw them with nets."),
 ('VermilionCity','ELISE','I',('ITEM_REVIVE',2),'SPECIES_BELDUM','Beldum',
   "A BELDUM was found half-buried\nafter the storm. It barely moves.\pTwo REVIVES, please. It deserves a\nchance."),
 ('LavenderTown','FINN','D',None,'SPECIES_PORYGON','Porygon',
   "The old tower is full of lost\nPOKéMON. Hunters know it, and they\ncome at dusk with lanterns."),
 ('CeladonCity','GWEN','I',('ITEM_LEMONADE',3),'SPECIES_LAPRAS','Lapras',
   "My LAPRAS hasn't spoken in days.\nShe misses the sea. Three\nLEMONADES might cheer her up."),
 ('SaffronCity','HUGO','D',None,'SPECIES_SNORLAX','Snorlax',
   "A big sleeper blocks the road and\nthe hunters want it. They came\nwith ropes and a truck."),
 ('CinnabarIsland','IRIS','I',('ITEM_MAX_POTION',2),'SPECIES_AERODACTYL','Aerodactyl',
   "The old lab revived a creature\nfrom the amber. It needs two MAX\nPOTIONS to get through the week."),
 ('OneIsland','JONAH','D',None,'SPECIES_KANGASKHAN','Kangaskhan',
   "Poachers took a baby from its\nmother on the shore. Bring them\nto justice, please."),
 ('TwoIsland','KIRA','I',('ITEM_HYPER_POTION',3),'SPECIES_HERACLES','Heracross',
   "The forest beetles are hurt by\ndrought. Three HYPER POTIONS will\nkeep the elders alive."),
 ('ThreeIsland','LEON','D',None,'SPECIES_ABSOL','Absol',
   "An ABSOL warned me of danger for\nweeks. Now I know why: hunters\nare on the island."),
 ('FourIsland','MAYA','I',('ITEM_ICE_HEAL',3),'SPECIES_FEEBAS','Feebas',
   "A strange fish lives in a cold\npond. It is ill and nobody can\nsee it. Three ICE HEALS, please."),
 ('FiveIsland','NOEL','D',None,'SPECIES_TAUROS','Tauros',
   "The herd is spooked. Hunters burn\nthe meadow to drive them into\ntheir nets."),
 ('SixIsland','OLGA','I',('ITEM_FULL_RESTORE',2),'SPECIES_PINSIR','Pinsir',
   "A PINSIR was caught in a trap and\nit is badly hurt. Two FULL\nRESTORES, please."),
 ('SevenIsland','PAXTON','D',None,'SPECIES_SKARMORY','Skarmory',
   "This is the last post. The hunters'\nleader is somewhere near. Beat his\ntwo henchmen and he will show up."),
]
POSTS[10] = POSTS[10][:4] + ('SPECIES_HERACROSS', 'Heracross') + POSTS[10][6:]
for k, (m, nm, ty, item, sp, spn, ask) in enumerate(POSTS):
    anchor, cell = place_npc.choose(m, 'PokemonCenter'); 
    # evite un PNJ deja pose (Seigneur de la fin 3) : on prend la case suivante la plus proche
    j = json.load(open(f'data/maps/{m}/map.json')); taken = {(o['x'], o['y']) for o in j['object_events']}
    if cell in taken or any(abs(cell[0] - t[0]) + abs(cell[1] - t[1]) < 2 for t in taken if t != cell and (t == cell)):
        nav = place_npc.R.Nav(m); best = None
        for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (-2, 2), (2, -2), (-2, -2), (3, 0), (-3, 0)):
            c = (cell[0] + dx, cell[1] + dy)
            if not (0 <= c[0] < nav.w and 0 <= c[1] < nav.h) or nav.blocked(*c) or c in nav.warps or c in taken: continue
            if sum(1 for ddx, ddy in ((0, 1), (0, -1), (1, 0), (-1, 0)) if not nav.blocked(c[0] + ddx, c[1] + ddy)) < 3: continue
            best = c; break
        cell = best or cell
    j['object_events'].append({'graphics_id': ['OBJ_EVENT_GFX_BEAUTY','OBJ_EVENT_GFX_HIKER','OBJ_EVENT_GFX_WOMAN_1','OBJ_EVENT_GFX_CAMPER'][k % 4], 'x': cell[0], 'y': cell[1], 'elevation': 3,
        'movement_type': 'MOVEMENT_TYPE_FACE_DOWN', 'movement_range_x': 0, 'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE', 'trainer_sight_or_berry_tree_id': '0',
        'script': f'{m}_EventScript_Refuge', 'flag': '0'})
    json.dump(j, open(f'data/maps/{m}/map.json', 'w'), indent=2)
    lab = f'{m}_EventScript_Refuge'; T = f'{m}_Text_Ref'
    s = f'''
@ Topaze, fin 2 « Le Refuge » : poste {k+1}/16 ({nm}) — {"duel contre 2 chasseurs" if ty == "D" else "livraison d'objets"}, recompense : {spn}
{lab}::
	lock
	faceplayer
	goto_if_ne VAR_TOPAZE_ENDING, 2, {lab}Idle
	goto_if_gt VAR_REFUGE_STAGE, {k}, {lab}Done
	goto_if_lt VAR_REFUGE_STAGE, {k}, {lab}Early
'''
    if ty == 'I':
        s += f'''	checkitem {item[0]}, {item[1]}
	goto_if_eq VAR_RESULT, TRUE, {lab}Offer
	msgbox {T}Ask
	release
	end

{lab}Offer::
	msgbox {T}Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, {lab}Refuse
	removeitem {item[0]}, {item[1]}
	goto {lab}Reward
	end

{lab}Refuse::
	msgbox {T}No
	release
	end
'''
    else:
        g, ju = GENT[k // 2], JUGG[k // 2]; tgt = 62 + 2 * (k // 2) * 1 + 4
        bg = max(0, tgt - toplvl(g)); bj = max(0, tgt + 2 - toplvl(ju))
        s += f'''	msgbox {T}Ask
	setvar VAR_TOPAZE_BOOST, {bg}
	trainerbattle_no_intro TRAINER_{g}, {T}Hunter1
	setvar VAR_TOPAZE_BOOST, {bj}
	trainerbattle_no_intro TRAINER_{ju}, {T}Hunter2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	goto {lab}Reward
	end
'''
    s += f'''
{lab}Reward::
	msgbox {T}Gives
	givemon {sp}, 0
	addvar VAR_REFUGE_STAGE, 1
	msgbox {T}After
	release
	end

{lab}Early::
	msgbox {T}Early
	release
	end

{lab}Done::
	msgbox {T}Done
	release
	end

{lab}Idle::
	msgbox {T}Idle
	release
	end
'''
    appendf(f'data/maps/{m}/scripts.inc', s)
    t = f'data/maps/{m}/text.inc'
    appendf(t, textblock(f'{T}Ask', f'{nm}: ' + ask.replace('\\n', '\n').replace('\n\\p', '\n\\p') if False else nm + ': ' + ask))
    if ty == 'I':
        appendf(t, textblock(f'{T}Offer', f'{nm}: You have them! May I take\n{item[1]} of them for the post?'))
        appendf(t, textblock(f'{T}No', f'{nm}: I understand. It is a lot to\nask. The offer stands.'))
    else:
        appendf(t, textblock(f'{T}Hunter1', 'HUNTER: Rare ones fetch a fortune!\nStay out of this, child!'))
        appendf(t, textblock(f'{T}Hunter2', 'HUNTER: You beat my partner? Fine,\nI am not afraid of a ranger!'))
    appendf(t, textblock(f'{T}Gives', f'{nm}: You saved the day. The post\nhas a gift for you: {spn.upper()}!'))
    appendf(t, textblock(f'{T}After', f'{nm}: Take good care of it. The\nnext REFUGE post is waiting.'))
    appendf(t, textblock(f'{T}Early', f'{nm}: Not yet. Finish the earlier\nposts first. The KEEPER at the\nSAFARI ZONE knows the order.'))
    appendf(t, textblock(f'{T}Done', f'{nm}: Thank you again. The REFUGE\nis safer because of you.'))
    appendf(t, textblock(f'{T}Idle', f'{nm}: I watch over the animals here.\nThe world is quieter now.'))
    print(k, m, cell)
