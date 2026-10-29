#!/usr/bin/env python3
"""LOT 7 : 4 zones de capture (glace, feu, foret nocturne, cote) + passeur des saisons. Textes anglais PROVISOIRES. Idempotent."""
import sys; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'FuchsiaCity_EventScript_SeasonsFerryman' in rd('data/maps/FuchsiaCity/scripts.inc'): print('deja applique'); raise SystemExit
Z = [
 dict(map='FrostHollow', tpl='FourIsland_IcefallCave_Back', badge=6, lv=(38, 44), land=['SWINUB', 'SNEASEL', 'DELIBIRD', 'SNORUNT', 'SPHEAL', 'SMOOCHUM', 'JYNX', 'GLALIE', 'PILOSWINE', 'SEALEO', 'LAPRAS', 'DEWGONG'],
      ask='The FROST HOLLOW: ice, silence and cold POKeMON. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('OLD_MAN_1', 'It is always winter in here. The ice remembers everything.'), ('LASS', 'SNEASEL steal what they can. Keep your berries close.')], hidden=['ELIXIR', 'MAX_ETHER', 'REVIVE'],
      quests=[dict(g='SCIENTIST', want=('BURN_HEAL', 2), rew=('NEVER_MELT_ICE', 1), ask='I study how ice melts. Two BURN HEALs would help my tests.', done='Perfect data! Take this NEVER-MELT ICE.', after='The hollow stays frozen. Good.', miss='Two BURN HEALs, please.', j=('THE ICE STUDY', 'FROST HOLLOW: bring 2 BURN HEALS.'))]),
 dict(map='EmberRim', tpl='MtEmber_RubyPath_B3F', badge=6, lv=(38, 44), land=['SLUGMA', 'MAGCARGO', 'NUMEL', 'HOUNDOUR', 'MAGBY', 'TORKOAL', 'GROWLITHE', 'PONYTA', 'RAPIDASH', 'MAGMAR', 'CAMERUPT', 'HOUNDOOM'],
      ask='The EMBER RIM: lava glows below the rock. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('HIKER', 'Heat makes POKeMON bold. It makes me thirsty.'), ('CAMPER', 'MAGBY juggle sparks. I do not recommend catching them barehanded.')], hidden=['ELIXIR', 'MAX_ETHER', 'REVIVE'],
      quests=[dict(g='OLD_WOMAN', want=('ICE_HEAL', 2), rew=('CHARCOAL', 1), ask='Two ICE HEALs would cool my pot. I will pay in charcoal.', done='Cool as snow. Take this CHARCOAL.', after='The rim is warm and cozy.', miss='Two ICE HEALs, please.', j=('A COOL CHANGE', 'EMBER RIM: bring 2 ICE HEALS.'))]),
 dict(map='NocturneWood', tpl='ViridianForest', badge=3, lv=(18, 24), land=['HOOTHOOT', 'SPINARAK', 'LEDYBA', 'ZUBAT', 'GLOOM', 'VENONAT', 'PINECO', 'WURMPLE', 'SHROOMISH', 'SURSKIT', 'NINCADA', 'VOLBEAT'],
      ask='The NOCTURNE WOOD: the owls sing all day long. Visit?', gt='Come back with 3 BADGES.',
      npcs=[('BUG_CATCHER', 'The trees here never sleep. Neither do I.'), ('WOMAN_1', 'HOOTHOOT knows the time better than any clock.')], hidden=['SUPER_POTION', 'ANTIDOTE', 'ULTRA_BALL'],
      quests=[dict(g='OLD_MAN_1', want=('ANTIDOTE', 3), rew=('SILVER_POWDER', 1), ask='Three ANTIDOTEs, young one. The wood bites back.', done='Gratitude. Take this SILVER POWDER.', after='The wood is gentle today.', miss='Three ANTIDOTEs, please.', j=('THE WOOD BITES', 'NOCTURNE WOOD: bring 3 ANTIDOTES.'))]),
 dict(map='ShellCoast', tpl='TwoIsland_CapeBrink', badge=5, lv=(30, 36), land=['KRABBY', 'SHELLDER', 'STARYU', 'WINGULL', 'PELIPPER', 'TENTACOOL', 'HORSEA', 'CHINCHOU', 'CORSOLA', 'REMORAID', 'CLAMPERL', 'LUVDISC'],
      water=['TENTACOOL', 'WINGULL', 'PELIPPER', 'WAILMER', 'TENTACRUEL'], fish=['MAGIKARP', 'TENTACOOL', 'KRABBY', 'HORSEA', 'CORSOLA', 'KINGLER', 'WAILMER', 'LAPRAS', 'SEADRA', 'FEEBAS'],
      ask='The SHELL COAST: the tide leaves treasure behind. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('SAILOR', 'The shells sing at night. If you listen, you hear your name.'), ('FISHER', 'FEEBAS hides in plain water. Patience, always patience.')], hidden=['PEARL', 'HEART_SCALE', 'ELIXIR'],
      quests=[dict(g='WOMAN_3', want=('LEMONADE', 1), rew=('DEEP_SEA_TOOTH', 1), ask='A cold LEMONADE for my seashell stand. I will trade you a rare tooth.', done='Refreshing! Take this DEEP SEA TOOTH.', after='The coast is a lovely place.', miss='One LEMONADE, please.', j=('A COLD DRINK', 'SHELL COAST: bring a LEMONADE.'))]),
]
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = ['# ---- LOT 7 (zones saisons)']; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
ferry('SeasonsFerryman', 'FISHER', (17, 24), 'Each season has its own shore, {PLAYER}.', 'The seasons are frozen. Come back when the clocks make sense.', 'Another time, then.',
      [(z['map'], arr[z['map']], z['badge'], z['ask'], z['gt']) for z in Z])
journal_add(journal); flush_flags()
