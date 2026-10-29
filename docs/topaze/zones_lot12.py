#!/usr/bin/env python3
"""LOT 12 : CottonField, QuarryHeights, PondOfSong, CenterMeadow. Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'CottonField' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='CottonField', tpl='Route6', badge=3, lv=(18, 24), land=['MAREEP', 'FLAAFFY', 'SPOINK', 'SPINDA', 'SLAKOTH', 'ZIGZAGOON', 'LINOONE', 'NINCADA', 'TAILLOW', 'SWABLU', 'SHROOMISH', 'SKIPLOOM'],
      water=['PSYDUCK', 'GOLDEEN', 'MAGIKARP', 'POLIWAG', 'MARILL'], fish=['MAGIKARP', 'GOLDEEN', 'POLIWAG', 'MARILL', 'BARBOACH', 'CORPHISH', 'LOTAD', 'PSYDUCK', 'SEAKING', 'WHISCASH'],
      ask='The COTTON FIELD: soft grass, sleepy POKéMON. Visit?', gt='Come back with 3 BADGES.',
      npcs=[('FARMER', 'MAREEP is warm and gentle. Great for starters!'), ('LITTLE_GIRL', 'SLAKOTH naps all day. Me too!')], hidden=['SUPER_POTION', 'ELIXIR', 'LEFTOVERS'],
      quests=[dict(g='FARMER', want=('SUPER_POTION', 1), rew=('LEFTOVERS', 1), ask='A SUPER POTION for my tired flock. LEFTOVERS for you!', done='Thank you! Take these LEFTOVERS.', after='The flock sleeps well.', miss='One SUPER POTION, please.', j=('A TIRED FLOCK', 'COTTON FIELD: bring a SUPER POTION.'))]),
 dict(map='QuarryHeights', tpl='Route4', badge=4, lv=(24, 30), land=['GEODUDE', 'GRAVELER', 'ONIX', 'SANDSHREW', 'NOSEPASS', 'ARON', 'LAIRON', 'RHYHORN', 'MACHOP', 'MAGNEMITE', 'SKARMORY', 'MEDITITE'],
      ask='The QUARRY HEIGHTS: rock, steel and hard heads. Visit?', gt='Come back with 4 BADGES.',
      npcs=[('HIKER', 'ARON eats the rails. The workers hate it.'), ('WORKER', 'METAL COAT is somewhere in the pit, they say.')], hidden=['METAL_COAT', 'HARD_STONE', 'IRON'],
      quests=[dict(g='HIKER', want=('IRON', 1), rew=('METAL_COAT', 1), ask='Bring me some IRON and I give you a METAL COAT.', done='Solid! Take this METAL COAT.', after='Rock on!', miss='One IRON, please. The APOTHECARY sells it.', j=('IRON FOR THE HIKER', 'QUARRY HEIGHTS: bring an IRON.'))]),
 dict(map='PondOfSong', tpl='Route25', badge=3, lv=(18, 24), land=['PSYDUCK', 'MARILL', 'POLIWAG', 'LOTAD', 'SURSKIT', 'BARBOACH', 'CORPHISH', 'SLOWPOKE', 'CHINCHOU', 'BELLSPROUT', 'ODDISH', 'WOOPER'],
      water=['PSYDUCK', 'MARILL', 'POLIWHIRL', 'LOTAD', 'CHINCHOU'], fish=['MAGIKARP', 'POLIWAG', 'MARILL', 'BARBOACH', 'CORPHISH', 'CHINCHOU', 'WOOPER', 'FEEBAS', 'LOTAD', 'WHISCASH'],
      ask='The POND OF SONG: frogs, ducks and gentle ripples. Visit?', gt='Come back with 3 BADGES.',
      npcs=[('FISHER', 'MARILL sings on the lily pads at dawn.'), ('LASS', 'POLIWAG, POLIWHIRL... one needs a KING\'S ROCK!')], hidden=['KINGS_ROCK', 'MYSTIC_WATER', 'NET_BALL'],
      quests=[dict(g='LASS', want=('NET_BALL', 1), rew=('KINGS_ROCK', 1), ask='A NET BALL for my collection, a KING\'S ROCK for you.', done='Lovely! Take this KING\'S ROCK.', after='The pond is peaceful.', miss='One NET BALL, please.', j=('A BALL FOR A ROCK', 'POND OF SONG: bring a NET BALL.'))]),
 dict(map='CenterMeadow', tpl='SafariZone_Center', badge=5, lv=(30, 36), land=['CHANSEY', 'KANGASKHAN', 'TAUROS', 'PINSIR', 'SCYTHER', 'EXEGGCUTE', 'TANGELA', 'DODUO', 'RHYHORN', 'PARAS', 'VENONAT', 'GIRAFARIG'],
      water=['PSYDUCK', 'SLOWPOKE', 'MAGIKARP', 'GOLDEEN', 'DRATINI'], fish=['MAGIKARP', 'GOLDEEN', 'DRATINI', 'SLOWPOKE', 'PSYDUCK', 'SEAKING', 'DRAGONAIR', 'POLIWAG', 'BARBOACH', 'WHISCASH'],
      ask='The CENTER MEADOW: the old safari grounds. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('SCIENTIST', 'Safari stock still roams the center fields.'), ('GENTLEMAN', 'CHANSEY, KANGASKHAN... a collector\'s dream.')], hidden=['LUCKY_EGG', 'ULTRA_BALL', 'REVIVE'],
      quests=[dict(g='GENTLEMAN', want=('ULTRA_BALL', 2), rew=('LUCKY_EGG', 1), ask='Two ULTRA BALLs for my collection. LUCKY EGG for you!', done='Wonderful! Take this LUCKY EGG.', after='What a fine meadow.', miss='Two ULTRA BALLs, please.', j=('A COLLECTOR\'S WISH', 'CENTER MEADOW: bring 2 ULTRA BALLS.'))]),
]
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = ['# ---- LOT 12 (coton, carriere, etang, prairie)']; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman']):
    ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
journal_add(journal); flush_flags()
