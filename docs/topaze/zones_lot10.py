#!/usr/bin/env python3
"""LOT 10 : BerryThicket (Evolutions par objet echange), KindleTrail (feu/combat), RuinHollow (psy/spectre/rares anciens), TideCave (eau/glace profonds). Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'ThornThicket' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='ThornThicket', tpl='ThreeIsland_BerryForest', badge=4, lv=(24, 30), land=['PINECO', 'SHUCKLE', 'HERACROSS', 'PINSIR', 'SCYTHER', 'BEEDRILL', 'BUTTERFREE', 'SCEPTILE'.replace('SCEPTILE', 'FORRETRESS'), 'YANMA', 'LEDIAN', 'ARIADOS', 'WURMPLE'],
      ask='The THORN THICKET: bugs of every kind hide here. Visit?', gt='Come back with 4 BADGES.',
      npcs=[('BUG_CATCHER', 'HERACROSS and PINSIR live here. Bring a good ball!'), ('LASS', 'SCYTHER and SHUCKLE are shy, but worth the wait.')], hidden=['SILVER_POWDER', 'GREAT_BALL', 'REPEL'],
      quests=[dict(g='BUG_CATCHER', want=('REPEL', 2), rew=('SILVER_POWDER', 1), ask='Bugs keep eating my lunch. Bring 2 REPELs and I pay you!', done='Peace at last! Take this SILVER POWDER.', after='No more bugs on my sandwich.', miss='Two REPELs, please.', j=('LUNCH THIEVES', 'THORN THICKET: bring 2 REPELS.'))]),
 dict(map='KindleTrail', tpl='OneIsland_KindleRoad', badge=5, lv=(32, 38), land=['MACHOP', 'MACHOKE', 'MAKUHITA', 'MEDITITE', 'HITMONLEE', 'HITMONCHAN', 'MANKEY', 'PRIMEAPE', 'TYROGUE', 'GROWLITHE', 'MAGBY', 'NUMEL'],
      water=['MAGIKARP', 'GOLDEEN', 'SEAKING', 'WAILMER', 'KRABBY'], fish=['MAGIKARP', 'GOLDEEN', 'SEAKING', 'KRABBY', 'KINGLER', 'WAILMER', 'CORSOLA', 'HORSEA', 'SEADRA', 'FEEBAS'],
      ask='The KINDLE TRAIL: a training path for fighters. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('BLACK_BELT', 'Hit hard, stay humble. That is the way.'), ('HIKER', 'TYROGUE grows into three forms. Train it well!')], hidden=['BLACK_BELT', 'PROTEIN', 'X_ATTACK'],
      quests=[dict(g='BLACK_BELT', want=('PROTEIN', 1), rew=('FOCUS_BAND', 1), ask='Strong body needs PROTEIN. Bring one, get a FOCUS BAND.', done='Hah! Wear this FOCUS BAND.', after='Train every day.', miss='One PROTEIN, please. The APOTHECARY sells it.', j=('A STRONG BODY', 'KINDLE TRAIL: bring a PROTEIN.'))]),
 dict(map='RuinHollow', tpl='SixIsland_RuinValley', badge=7, lv=(44, 50), land=['UNOWN', 'WOBBUFFET', 'CHIMECHO', 'SABLEYE', 'SHUPPET', 'BANETTE', 'DUSKULL', 'MISDREAVUS', 'GASTLY', 'HAUNTER', 'ABRA', 'KADABRA'],
      ask='The RUIN HOLLOW: old stones, older secrets. Visit?', gt='Come back with 7 BADGES.',
      npcs=[('SCIENTIST', 'UNOWN carved these walls. Nobody read them yet.'), ('OLD_WOMAN', 'Do not stare at the walls too long, dear.')], hidden=['SPELL_TAG', 'TM30', 'ULTRA_BALL'],
      quests=[dict(g='OLD_WOMAN', want=('ULTRA_BALL', 1), rew=('SPELL_TAG', 1), ask='Bring me an ULTRA BALL and I give you a SPELL TAG.', done='Thank you, dear. A SPELL TAG for you.', after='The hollow whispers.', miss='One ULTRA BALL, please.', j=('A GHOSTLY SWAP', 'RUIN HOLLOW: bring an ULTRA BALL.'))]),
 dict(map='TideCave', tpl='SixIsland_WaterPath', badge=6, lv=(40, 46), land=['TENTACOOL', 'TENTACRUEL', 'SEEL', 'DEWGONG', 'SLOWPOKE', 'SLOWBRO', 'SHELLDER', 'CLOYSTER', 'STARYU', 'CORSOLA', 'LAPRAS', 'KINGDRA'.replace('KINGDRA', 'HORSEA')],
      water=['TENTACOOL', 'TENTACRUEL', 'WAILMER', 'LAPRAS', 'KINGLER'], fish=['MAGIKARP', 'HORSEA', 'SEADRA', 'CHINCHOU', 'LANTURN', 'WAILMER', 'RELICANTH', 'FEEBAS', 'CORSOLA', 'LAPRAS'],
      ask='The TIDE CAVE: deep water, strange lights. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('FISHER', 'Rare fish hide in the deep. Bring a GOOD ROD.'), ('SWIMMER_M_LAND', 'SEADRA, RELICANTH... the sea keeps its treasures.')], hidden=['DEEP_SEA_TOOTH', 'DEEP_SEA_SCALE', 'PEARL'],
      quests=[dict(g='FISHER', want=('PEARL', 1), rew=('MYSTIC_WATER', 1), ask='A PEARL for my collection, a MYSTIC WATER for you.', done='Beautiful! Take this MYSTIC WATER.', after='The tide is calm.', miss='One PEARL, please.', j=('PEARL FOR A FISHER', 'TIDE CAVE: bring a PEARL.'))]),
]
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = ['# ---- LOT 10 (ronces, sentier, ruines, maree)']; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['ScribeFerryman', 'ScribeFerryman', 'DuskFerrywoman', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
journal_add(journal); flush_flags()
