#!/usr/bin/env python3
"""LOT 15 : DrowsyDown, BlossomCrest, ThunderRidge, FangValley, LuckyClover + SilentHollow. Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'DrowsyDown' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='DrowsyDown', tpl='Route11', badge=4, lv=(24, 30), land=['DROWZEE', 'HYPNO', 'SLAKOTH', 'VIGOROTH', 'SPOINK', 'SNUBBULL', 'GRANBULL', 'MEDITITE', 'WHISMUR', 'LOUDRED', 'TEDDIURSA', 'MUNCHLAX'.replace('MUNCHLAX', 'SKITTY')],
      ask='The DROWSY DOWN: sleepy hills full of dozing POKéMON. Visit?', gt='Come back with 4 BADGES.',
      npcs=[('FAT_MAN', 'Nap here and nothing bothers you. Almost nothing.'), ('OLD_MAN_1', 'DROWZEE eats dreams. Keep an eye on yours.')], hidden=['LEFTOVERS', 'CHESTO_BERRY', 'SUPER_POTION'],
      quests=[dict(g='FAT_MAN', want=('CHESTO_BERRY', 1), rew=('LEFTOVERS', 1), ask='A CHESTO BERRY keeps me awake. Trade for LEFTOVERS?', done='Wide awake! Take these LEFTOVERS.', after='Zzz... oh, hello.', miss='One CHESTO BERRY, please.', j=('STAY AWAKE', 'DROWSY DOWN: bring a CHESTO BERRY.'))]),
 dict(map='BlossomCrest', tpl='Route16', badge=3, lv=(18, 24), land=['ODDISH', 'GLOOM', 'BELLSPROUT', 'WEEPINBELL', 'HOPPIP', 'SKIPLOOM', 'SUNKERN', 'ROSELIA', 'BUDEW'.replace('BUDEW', 'SEEDOT'), 'NUZLEAF', 'SHROOMISH', 'CASCOON'.replace('CASCOON', 'CACNEA')],
      ask='The BLOSSOM CREST: a hill covered in flowers. Visit?', gt='Come back with 3 BADGES.',
      npcs=[('WOMAN_1', 'SUN STONE and LEAF STONE make these bloom. See the GREENHOUSE.'), ('LITTLE_GIRL', 'ROSELIA has a flower in each hand!')], hidden=['MIRACLE_SEED', 'LEAF_STONE', 'SUN_STONE'],
      quests=[dict(g='WOMAN_1', want=('LEAF_STONE', 1), rew=('MIRACLE_SEED', 1), ask='My garden needs a LEAF STONE. I will give a MIRACLE SEED.', done='Bloom time! Take this MIRACLE SEED.', after='Everything is in flower.', miss='One LEAF STONE, please.', j=('A GARDEN IN BLOOM', 'BLOSSOM CREST: bring a LEAF STONE.'))]),
 dict(map='ThunderRidge', tpl='Route24', badge=5, lv=(32, 38), land=['ELECTRIKE', 'MANECTRIC', 'PLUSLE', 'MINUN', 'MAREEP', 'FLAAFFY', 'VOLTORB', 'ELECTRODE', 'MAGNEMITE', 'MAGNETON', 'PICHU', 'PIKACHU'],
      water=['CHINCHOU', 'LANTURN', 'MAGIKARP', 'GOLDEEN', 'SEAKING'], fish=['MAGIKARP', 'CHINCHOU', 'LANTURN', 'GOLDEEN', 'SEAKING', 'BARBOACH', 'WHISCASH', 'CORPHISH', 'FEEBAS', 'WAILMER'],
      ask='The THUNDER RIDGE: static in the air, storms on the horizon. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('SCIENTIST', 'Thunder here is old and angry. PIKACHU love it.'), ('YOUNGSTER', 'My hair stands up every time I climb!')], hidden=['MAGNET', 'THUNDER_STONE', 'ELIXIR'],
      quests=[dict(g='SCIENTIST', want=('THUNDER_STONE', 1), rew=('MAGNET', 1), ask='A THUNDER STONE for my lab. A MAGNET for you.', done='Shocking! Take this MAGNET.', after='The ridge hums.', miss='One THUNDER STONE, please.', j=('A SHOCKING SWAP', 'THUNDER RIDGE: bring a THUNDER STONE.'))]),
 dict(map='FangValley', tpl='Route15', badge=6, lv=(38, 44), land=['HOUNDOUR', 'HOUNDOOM', 'POOCHYENA', 'MIGHTYENA', 'ZANGOOSE', 'SEVIPER', 'ARBOK', 'SKARMORY', 'MANKEY', 'PRIMEAPE', 'SNEASEL', 'ABSOL'],
      water=['CARVANHA', 'SHARPEDO', 'WAILMER', 'TENTACRUEL', 'MAGIKARP'], fish=['MAGIKARP', 'CARVANHA', 'SHARPEDO', 'WAILMER', 'TENTACOOL', 'TENTACRUEL', 'FEEBAS', 'REMORAID', 'OCTILLERY', 'CORSOLA'],
      ask='The FANG VALLEY: fierce hunters and sharp teeth. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('HIKER', 'HOUNDOUR hunts in packs. Never run alone.'), ('BLACK_BELT', 'ZANGOOSE and SEVIPER fight each other. Always.')], hidden=['BLACK_GLASSES', 'MAX_POTION', 'FULL_HEAL'],
      quests=[dict(g='HIKER', want=('FULL_HEAL', 2), rew=('BLACK_GLASSES', 1), ask='Poison is everywhere. Two FULL HEALs, and BLACK GLASSES are yours.', done='You are a lifesaver! Take these BLACK GLASSES.', after='The valley bites less now.', miss='Two FULL HEALs, please.', j=('CURE FOR THE HIKER', 'FANG VALLEY: bring 2 FULL HEALS.'))]),
 dict(map='LuckyClover', tpl='Route6', badge=2, lv=(12, 18), land=['SKITTY', 'ZIGZAGOON', 'AZURILL', 'WHISMUR', 'SLAKOTH', 'TEDDIURSA', 'SMEARGLE'.replace('SMEARGLE', 'MEOWTH'), 'RATTATA', 'SENTRET', 'LILLIPUP'.replace('LILLIPUP', 'FURRET'), 'PIDGEY', 'HOOTHOOT'],
      water=['PSYDUCK', 'MAGIKARP', 'MARILL', 'GOLDEEN', 'POLIWAG'], fish=['MAGIKARP', 'GOLDEEN', 'POLIWAG', 'MARILL', 'BARBOACH', 'CORPHISH', 'LOTAD', 'PSYDUCK', 'WOOPER', 'FEEBAS'],
      ask='The LUCKY CLOVER: normal types, big hearts. Visit?', gt='Come back with 2 BADGES.',
      npcs=[('LASS', 'SKITTY loves to chase its own tail.'), ('YOUNGSTER', 'MEOWTH and SENTRET never run from a fight.')], hidden=['POKE_BALL', 'GREAT_BALL', 'POTION'],
      quests=[dict(g='LASS', want=('POKE_BALL', 3), rew=('SILK_SCARF', 1), ask='Three POKé BALLs for my team, and a SILK SCARF for you!', done='Thanks! Take this SILK SCARF.', after='What a lovely day.', miss='Three POKé BALLs, please.', j=('A SCARF FOR BALLS', 'LUCKY CLOVER: bring 3 POKE BALLS.'))]),
 dict(map='SilentHollow', tpl='Route16', badge=7, lv=(44, 50), land=['MISDREAVUS', 'MURKROW', 'HOUNDOUR', 'SNEASEL', 'DUSKULL', 'DUSCLOPS', 'SHUPPET', 'BANETTE', 'SABLEYE', 'HAUNTER', 'GENGAR', 'SPIRITOMB'.replace('SPIRITOMB', 'WOBBUFFET')],
      ask='The SILENT HOLLOW: no wind, no sound. Visit?', gt='Come back with 7 BADGES.',
      npcs=[('OLD_WOMAN', 'Nothing makes noise here. Not even you.'), ('SCIENTIST', 'GENGAR evolves only through trade. Odd, no?')], hidden=['SPELL_TAG', 'BLACK_GLASSES', 'MAX_ELIXIR'],
      quests=[dict(g='OLD_WOMAN', want=('MAX_ELIXIR', 1), rew=('SPELL_TAG', 1), ask='A MAX ELIXIR will help me sleep. I trade a SPELL TAG.', done='Peace at last. Take this SPELL TAG.', after='Hush now.', miss='One MAX ELIXIR, please.', j=('A QUIET NIGHT', 'SILENT HOLLOW: bring a MAX ELIXIR.'))]),
]
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = ['# ---- LOT 15 (somnolence, fleurs, tonnerre, crocs, trefle, silence)']; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman', 'ScribeFerryman', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
journal_add(journal); flush_flags()
