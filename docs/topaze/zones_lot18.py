#!/usr/bin/env python3
"""LOT 18 : 6 zones avec quetes (pool FLAG_0x8xx). Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'PebbleBeach' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
def Q(g, w, r, ask, done, after, miss, j): return dict(g=g, want=w, rew=r, ask=ask, done=done, after=after, miss=miss, j=j)
Z = [
 dict(map='PebbleBeach', tpl='OneIsland_TreasureBeach', badge=1, lv=(6, 12), land=['WINGULL', 'KRABBY', 'SANDSHREW', 'SHELLDER', 'STARYU', 'SLOWPOKE', 'PSYDUCK', 'ZIGZAGOON', 'LOTAD', 'WURMPLE', 'RATTATA', 'PIDGEY'],
      water=['TENTACOOL', 'WINGULL', 'MAGIKARP', 'KRABBY', 'STARYU'], fish=['MAGIKARP', 'KRABBY', 'STARYU', 'SHELLDER', 'GOLDEEN', 'POLIWAG', 'PSYDUCK', 'LOTAD', 'BARBOACH', 'FEEBAS'],
      ask='The PEBBLE BEACH: smooth stones and tiny tides. Visit?', gt='Come back with 1 BADGE.', npcs=[('LITTLE_BOY', 'I collect round pebbles. Want one? No.'), ('LASS', 'The waves bring something new every day.')],
      hidden=['POTION', 'POKE_BALL', 'ANTIDOTE'], quests=[Q('LITTLE_BOY', ('POKE_BALL', 1), ('NET_BALL', 1), 'A POKé BALL for my bucket! I trade a NET BALL.', 'Cool! Take this NET BALL.', 'My bucket is full.', 'One POKé BALL, please.', ('A BUCKET OF BALLS', 'PEBBLE BEACH: bring a POKE BALL.'))]),
 dict(map='HoneyGrove', tpl='ThreeIsland_BerryForest', badge=3, lv=(16, 22), land=['BEEDRILL', 'BUTTERFREE', 'VENOMOTH', 'ILLUMISE', 'VOLBEAT', 'MASQUERAIN', 'DUSTOX', 'BEAUTIFLY', 'HERACROSS', 'PINSIR', 'LEDIAN', 'ARIADOS'],
      ask='The HONEY GROVE: sweet air and busy wings. Visit?', gt='Come back with 3 BADGES.', npcs=[('BUG_CATCHER', 'ILLUMISE and VOLBEAT dance together at night.'), ('WOMAN_1', 'Mind the stingers. The honey is worth it.')],
      hidden=['SILVER_POWDER', 'SUPER_POTION', 'ANTIDOTE'], quests=[Q('WOMAN_1', ('ANTIDOTE', 2), ('SILVER_POWDER', 1), 'I got stung twice. Two ANTIDOTEs for a SILVER POWDER?', 'Much better! Take this SILVER POWDER.', 'Sweet as honey.', 'Two ANTIDOTEs, please.', ('STUNG TWICE', 'HONEY GROVE: bring 2 ANTIDOTES.'))]),
 dict(map='CircusLawn', tpl='SafariZone_East', badge=4, lv=(24, 30), land=['MR_MIME', 'KADABRA', 'DROWZEE', 'HYPNO', 'WOBBUFFET', 'GIRAFARIG', 'MEDITITE', 'MEDICHAM', 'KIRLIA', 'RALTS', 'SPOINK', 'GRUMPIG'],
      ask='The CIRCUS LAWN: psychic acts and strange shows. Visit?', gt='Come back with 4 BADGES.', npcs=[('GENTLEMAN', 'MR. MIME builds invisible walls. It is quite the act.'), ('LASS', 'RALTS feels everything you feel.')],
      hidden=['TWISTED_SPOON', 'ELIXIR', 'GREAT_BALL'], quests=[Q('GENTLEMAN', ('GREAT_BALL', 2), ('TWISTED_SPOON', 1), 'Two GREAT BALLs for the show. A TWISTED_SPOON for you.', 'Splendid! Take this TWISTED_SPOON.', 'The show goes on.', 'Two GREAT BALLs, please.', ('BALLS FOR THE SHOW', 'CIRCUS LAWN: bring 2 GREAT BALLS.'))]),
 dict(map='CinderPlain', tpl='Route8', badge=6, lv=(38, 44), land=['RAPIDASH', 'MAGMAR', 'CAMERUPT', 'MAGCARGO', 'TORKOAL', 'HOUNDOOM', 'CHARMELEON', 'QUILAVA', 'ARCANINE', 'FLAREON'.replace('FLAREON', 'NUMEL'), 'SLUGMA', 'MAGBY'],
      ask='The CINDER PLAIN: burnt grass, hot winds. Visit?', gt='Come back with 6 BADGES.', npcs=[('HIKER', 'The ground glows at night. Do not sleep here.'), ('SCIENTIST', 'ARCANINE runs faster than my instruments.')],
      hidden=['FIRE_STONE', 'CHARCOAL', 'MAX_POTION'], quests=[Q('SCIENTIST', ('FIRE_STONE', 1), ('CHARCOAL', 1), 'A FIRE STONE for my study. A CHARCOAL in return.', 'Hot data! Take this CHARCOAL.', 'The plain simmers.', 'One FIRE STONE, please.', ('A STONE ON FIRE', 'CINDER PLAIN: bring a FIRE STONE.'))]),
 dict(map='FrozenMarsh', tpl='SafariZone_Center', badge=7, lv=(44, 50), land=['GLALIE', 'WALREIN', 'LAPRAS', 'DEWGONG', 'CLOYSTER', 'JYNX', 'PILOSWINE', 'SNEASEL', 'DELIBIRD', 'SEALEO', 'SNORUNT', 'SPHEAL'],
      water=['LAPRAS', 'DEWGONG', 'CLOYSTER', 'WALREIN', 'WAILMER'], fish=['MAGIKARP', 'DEWGONG', 'CLOYSTER', 'LAPRAS', 'WAILMER', 'CORSOLA', 'SEADRA', 'FEEBAS', 'RELICANTH', 'SHELLDER'],
      ask='The FROZEN MARSH: ice on the reeds. Visit?', gt='Come back with 7 BADGES.', npcs=[('OLD_MAN_1', 'The marsh froze twenty years ago. It never thawed.'), ('SAILOR', 'DEWGONG sleeps on the ice. Do not wake it.')],
      hidden=['NEVER_MELT_ICE', 'PEARL', 'MAX_ELIXIR'], quests=[Q('OLD_MAN_1', ('PEARL', 1), ('NEVER_MELT_ICE', 1), 'A PEARL for my wife. A NEVER-MELT ICE for you.', 'She will smile. Take this NEVER-MELT ICE.', 'The ice keeps its cold.', 'One PEARL, please.', ('A PEARL FOR HER', 'FROZEN MARSH: bring a PEARL.'))]),
 dict(map='ThornyTrail', tpl='Route4', badge=4, lv=(24, 30), land=['NIDORINA', 'NIDORINO', 'ARBOK', 'SANDSLASH', 'PERSIAN', 'FEAROW', 'RAICHU'.replace('RAICHU', 'PIKACHU'), 'DODUO', 'GOLBAT', 'MUK', 'LINOONE', 'ZANGOOSE'],
      ask='The THORNY TRAIL: a sharp path for sharp teeth. Visit?', gt='Come back with 4 BADGES.', npcs=[('HIKER', 'NIDORINO is nasty when it feels cornered.'), ('YOUNGSTER', 'Moon stone, moon stone... I have none.')],
      hidden=['MOON_STONE', 'POISON_BARB', 'REVIVE'], quests=[Q('YOUNGSTER', ('REVIVE', 1), ('POISON_BARB', 1), 'My buddy fainted! A REVIVE, and I give a POISON BARB.', 'He is up! Take this POISON BARB.', 'Back on the trail.', 'One REVIVE, please.', ('A FALLEN BUDDY', 'THORNY TRAIL: bring a REVIVE.'))]),
]
SPX = rd('include/constants/species.h')
bad = [(z['map'], n) for z in Z for n in z['land'] + z.get('water', []) + z.get('fish', []) if not re.search(r'#define SPECIES_%s\b' % n, SPX)]
badi = [i for z in Z for q in z['quests'] for i in (q['want'][0], q['rew'][0])] + [i for z in Z for i in z['hidden']]
badi = [i for i in badi if not re.search(r'#define ITEM_%s\b' % i, IT)]
EVO = rd('include/constants/event_objects.h'); badg = [g for z in Z for g in [x[0] for x in z['npcs']] + [q['g'] for q in z['quests']] if not re.search(r'OBJ_EVENT_GFX_%s\b' % g, EVO)]
if bad or badi or badg: print('INVALIDE', bad, badi, set(badg)); raise SystemExit(1)
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = ['# ---- LOT 18']; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman', 'ScribeFerryman', 'SeasonsFerryman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
journal_add(journal); flush_flags()
