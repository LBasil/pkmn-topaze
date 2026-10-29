#!/usr/bin/env python3
"""LOT 11 : SunkenBeach, SoulPillar, MirrorLabyrinth, MeadowPath, OutcastShore. Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'MeadowPath' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='SunkenBeach', tpl='OneIsland_TreasureBeach', badge=2, lv=(14, 20), land=['WINGULL', 'KRABBY', 'SANDSHREW', 'SHELLDER', 'STARYU', 'CORSOLA', 'SLOWPOKE', 'PSYDUCK', 'MARILL', 'WOOPER', 'SURSKIT', 'LOTAD'],
      water=['TENTACOOL', 'WINGULL', 'MAGIKARP', 'KRABBY', 'STARYU'], fish=['MAGIKARP', 'KRABBY', 'STARYU', 'SHELLDER', 'CORSOLA', 'HORSEA', 'GOLDEEN', 'POLIWAG', 'BARBOACH', 'MARILL'],
      ask='The SUNKEN BEACH: shells, sand and early water types. Visit?', gt='Come back with 2 BADGES.',
      npcs=[('FISHER', 'Easy waters. Perfect for a first rod.'), ('LITTLE_GIRL', 'I found a pretty shell here yesterday!')], hidden=['PEARL', 'HEART_SCALE', 'SUPER_POTION'],
      quests=[dict(g='LITTLE_GIRL', want=('HEART_SCALE', 1), rew=('SHELL_BELL', 1), ask='I love shiny things. Bring a HEART SCALE, get a SHELL BELL!', done='So pretty! Take this SHELL BELL.', after='Shells everywhere!', miss='One HEART SCALE, please.', j=('SHINY SHELLS', 'SUNKEN BEACH: bring a HEART SCALE.'))]),
 dict(map='SoulPillar', tpl='FiveIsland_MemorialPillar', badge=6, lv=(36, 42), land=['GASTLY', 'HAUNTER', 'MISDREAVUS', 'SHUPPET', 'DUSKULL', 'CUBONE', 'MAROWAK', 'SABLEYE', 'MURKROW', 'SNEASEL', 'HOUNDOUR', 'BANETTE'],
      ask='The SOUL PILLAR: the quiet place of remembrance. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('OLD_MAN_1', 'Speak softly here. Many rest beneath.'), ('OLD_WOMAN', 'CUBONE carries its mother\'s memory.')], hidden=['SPELL_TAG', 'ZINC', 'ULTRA_BALL'],
      quests=[dict(g='OLD_WOMAN', want=('ZINC', 1), rew=('LUCKY_EGG', 1), ask='Bring me a ZINC and I give you a LUCKY EGG.', done='Bless you. Take this LUCKY EGG.', after='Rest in peace.', miss='One ZINC, please. The APOTHECARY sells it.', j=('A TOKEN OF ZINC', 'SOUL PILLAR: bring a ZINC.'))]),
 dict(map='MirrorLabyrinth', tpl='ThreeIsland_BondBridge', badge=5, lv=(30, 36), land=['WOBBUFFET', 'WYNAUT', 'SMOOCHUM', 'SNORUNT', 'LAPRAS', 'SEEL', 'DEWGONG', 'STARYU', 'MR_MIME', 'CORSOLA', 'SLOWPOKE', 'LUVDISC'],
      water=['LAPRAS', 'LUVDISC', 'TENTACOOL', 'WAILMER', 'STARYU'], fish=['MAGIKARP', 'LUVDISC', 'CORSOLA', 'HORSEA', 'SEADRA', 'FEEBAS', 'LAPRAS', 'WAILMER', 'RELICANTH', 'SHELLDER'],
      ask='The MIRROR BRIDGE: calm water, calm reflections. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('SCIENTIST', 'WYNAUT never attacks first. It waits.'), ('LASS', 'LUVDISC means love in the sea!')], hidden=['MYSTIC_WATER', 'WATER_STONE', 'HEART_SCALE'],
      quests=[dict(g='LASS', want=('WATER_STONE', 1), rew=('MIRACLE_SEED', 1), ask='A WATER STONE shines like a mirror. Trade for a MIRACLE SEED?', done='Sparkly! Take this MIRACLE SEED.', after='So pretty!', miss='One WATER STONE, please.', j=('MIRROR TRADE', 'MIRROR BRIDGE: bring a WATER STONE.'))]),
 dict(map='MeadowPath', tpl='SixIsland_PatternBush', badge=1, lv=(8, 14), land=['RATTATA', 'PIDGEY', 'CATERPIE', 'WEEDLE', 'NIDORAN_M', 'NIDORAN_F', 'ODDISH', 'BELLSPROUT', 'ZIGZAGOON', 'POOCHYENA', 'SENTRET', 'HOPPIP'],
      ask='The MEADOW PATH: a calm start for new collectors. Visit?', gt='Come back with 1 BADGE.',
      npcs=[('YOUNGSTER', 'Good spot to meet every early POKéMON.'), ('LASS', 'Both NIDORAN live here. Catch a pair!')], hidden=['POTION', 'ANTIDOTE', 'POKE_BALL'],
      quests=[dict(g='YOUNGSTER', want=('POTION', 2), rew=('EXP_SHARE', 1), ask='My POKéMON are hurt. Two POTIONs for an EXP SHARE?', done='You saved us! Take this EXP SHARE.', after='We are training again.', miss='Two POTIONs, please.', j=('HURT FRIENDS', 'MEADOW PATH: bring 2 POTIONS.'))]),
 dict(map='OutcastShore', tpl='SixIsland_WaterPath', badge=7, lv=(44, 50), land=['KINGLER', 'CRAWDAUNT', 'GOLDUCK', 'SEAKING', 'BARBOACH', 'WHISCASH', 'CARVANHA', 'SHARPEDO', 'REMORAID', 'OCTILLERY', 'MANTINE', 'LANTURN'],
      water=['SHARPEDO', 'MANTINE', 'WAILMER', 'WAILORD', 'TENTACRUEL'], fish=['MAGIKARP', 'CARVANHA', 'SHARPEDO', 'WAILMER', 'REMORAID', 'OCTILLERY', 'MANTINE', 'LANTURN', 'FEEBAS', 'LAPRAS'],
      ask='The OUTCAST SHORE: wild waters, wild POKéMON. Visit?', gt='Come back with 7 BADGES.',
      npcs=[('FISHER', 'SHARPEDO bites hard. Bring a strong team.'), ('HIKER', 'MANTINE glides above the waves here.')], hidden=['SOUL_DEW', 'MAX_REPEL', 'MAX_ELIXIR'],
      quests=[dict(g='HIKER', want=('MAX_REPEL', 1), rew=('SOUL_DEW', 1), ask='Bring me a MAX REPEL and I give you a SOUL DEW.', done='Safe at last! Take this SOUL DEW.', after='Quiet shore.', miss='One MAX REPEL, please.', j=('A QUIET SHORE', 'OUTCAST SHORE: bring a MAX REPEL.'))]),
]
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = ['# ---- LOT 11 (plage, pilier, pont, prairie, rivage)']; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['SeasonsFerryman', 'DuskFerrywoman', 'ScribeFerryman', 'Apprentice', 'DuskFerrywoman']):
    ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
journal_add(journal); flush_flags()
