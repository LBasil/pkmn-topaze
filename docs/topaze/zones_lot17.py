#!/usr/bin/env python3
"""LOT 17 : 12 zones avec quetes + 3 objets caches, grace aux drapeaux permanents FLAG_0x82A+ (jamais utilises). Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'FoxField' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
def Q(g, w, r, ask, done, after, miss, j): return dict(g=g, want=w, rew=r, ask=ask, done=done, after=after, miss=miss, j=j)
Z = [
 dict(map='FoxField', tpl='Route8', badge=2, lv=(14, 20), land=['VULPIX', 'GROWLITHE', 'PONYTA', 'MEOWTH', 'SPEAROW', 'RATTATA', 'PIDGEOTTO', 'NIDORINO', 'NIDORINA', 'MANKEY', 'ABRA', 'DITTO'],
      ask='The FOX FIELD: sly hunters in golden grass. Visit?', gt='Come back with 2 BADGES.', npcs=[('LASS', 'VULPIX hides its tails. Nobody has counted them all.'), ('YOUNGSTER', 'DITTO copies whatever it sees. Even me!')],
      hidden=['FIRE_STONE', 'POTION', 'ANTIDOTE'], quests=[Q('YOUNGSTER', ('POTION', 2), ('CHARCOAL', 1), 'Two POTIONs for my hurt foxes. CHARCOAL for you!', 'Thanks! Take this CHARCOAL.', 'The foxes are fine.', 'Two POTIONs, please.', ('A FOX NEEDS HELP', 'FOX FIELD: bring 2 POTIONS.'))]),
 dict(map='MossyDell', tpl='ViridianForest', badge=2, lv=(10, 16), land=['CATERPIE', 'METAPOD', 'WEEDLE', 'KAKUNA', 'PIDGEY', 'PIKACHU', 'NIDORAN_M', 'NIDORAN_F', 'ODDISH', 'BELLSPROUT', 'PARAS', 'ZIGZAGOON'],
      ask='The MOSSY DELL: old trees and Pikachu. Visit?', gt='Come back with 2 BADGES.', npcs=[('BUG_CATCHER', 'PIKACHU likes the thick moss here.'), ('LASS', 'It never gets dry in the dell.')],
      hidden=['ANTIDOTE', 'POKE_BALL', 'POTION'], quests=[Q('BUG_CATCHER', ('ANTIDOTE', 2), ('SILVER_POWDER', 1), 'Poison everywhere! Two ANTIDOTEs, a SILVER POWDER for you.', 'Safe now! Take this SILVER POWDER.', 'No more stings.', 'Two ANTIDOTEs, please.', ('STINGS AND SALVE', 'MOSSY DELL: bring 2 ANTIDOTES.'))]),
 dict(map='BrightShallows', tpl='Route12', badge=3, lv=(18, 24), land=['PSYDUCK', 'POLIWAG', 'GOLDEEN', 'LOTAD', 'MARILL', 'SURSKIT', 'WOOPER', 'SLOWPOKE', 'KRABBY', 'STARYU', 'SHELLDER', 'MAGIKARP'],
      water=['PSYDUCK', 'GOLDEEN', 'POLIWHIRL', 'LOTAD', 'KRABBY'], fish=['MAGIKARP', 'GOLDEEN', 'POLIWAG', 'KRABBY', 'STARYU', 'CORPHISH', 'BARBOACH', 'FEEBAS', 'SHELLDER', 'WAILMER'],
      ask='The BRIGHT SHALLOWS: warm water, easy fishing. Visit?', gt='Come back with 3 BADGES.', npcs=[('FISHER', 'A GOOD ROD brings the best fish here.'), ('SWIMMER_F_LAND', 'The water is so clear! I can see the fish.')],
      hidden=['SUPER_POTION', 'PEARL', 'HEART_SCALE'], quests=[Q('FISHER', ('SUPER_POTION', 1), ('MYSTIC_WATER', 1), 'A SUPER POTION for a tired fisherman. MYSTIC WATER for you.', 'Good as new! Take this MYSTIC WATER.', 'The fish are biting.', 'One SUPER POTION, please.', ('A TIRED FISHERMAN', 'BRIGHT SHALLOWS: bring a SUPER POTION.'))]),
 dict(map='AshenHeights', tpl='Route24', badge=4, lv=(24, 30), land=['SLUGMA', 'NUMEL', 'TORKOAL', 'GROWLITHE', 'PONYTA', 'GEODUDE', 'GRAVELER', 'ONIX', 'RHYHORN', 'MAGBY', 'CYNDAQUIL', 'MACHOP'],
      water=['MAGIKARP', 'GOLDEEN', 'KRABBY', 'SEAKING', 'CORSOLA'], fish=['MAGIKARP', 'GOLDEEN', 'KRABBY', 'SEAKING', 'CORSOLA', 'HORSEA', 'SEADRA', 'BARBOACH', 'WHISCASH', 'FEEBAS'],
      ask='The ASHEN HEIGHTS: warm rock and smoking cracks. Visit?', gt='Come back with 4 BADGES.', npcs=[('HIKER', 'The ground is warm even in winter.'), ('SCIENTIST', 'TORKOAL carries coal on its back. Real coal!')],
      hidden=['FIRE_STONE', 'HARD_STONE', 'BURN_HEAL'], quests=[Q('HIKER', ('BURN_HEAL', 2), ('CHARCOAL', 1), 'I keep getting burned. Two BURN HEALs, a CHARCOAL for you.', 'Phew! Take this CHARCOAL.', 'Cool as a cucumber.', 'Two BURN HEALs, please.', ('BURNING HANDS', 'ASHEN HEIGHTS: bring 2 BURN HEALS.'))]),
 dict(map='HushedBog', tpl='SafariZone_North', badge=4, lv=(24, 30), land=['GRIMER', 'MUK', 'KOFFING', 'WEEZING', 'ODDISH', 'GLOOM', 'VENONAT', 'EKANS', 'ARBOK', 'TANGELA', 'SKUNKTANK'.replace('SKUNKTANK', 'SEVIPER'), 'SHROOMISH'],
      ask='The HUSHED BOG: slime, mist and poison types. Visit?', gt='Come back with 4 BADGES.', npcs=[('SCIENTIST', 'GRIMER thrives here. I do not.'), ('OLD_MAN_1', 'Do not breathe too deep, son.')],
      hidden=['POISON_BARB', 'ANTIDOTE', 'FULL_HEAL'], quests=[Q('SCIENTIST', ('FULL_HEAL', 1), ('POISON_BARB', 1), 'A FULL HEAL for my research. A POISON BARB in return.', 'Splendid! Take this POISON BARB.', 'Research continues.', 'One FULL HEAL, please.', ('BOG RESEARCH', 'HUSHED BOG: bring a FULL HEAL.'))]),
 dict(map='GaleCliff', tpl='Route16', badge=5, lv=(30, 36), land=['PIDGEOTTO', 'FEAROW', 'FARFETCHD', 'SKARMORY', 'DODUO', 'MURKROW', 'NATU', 'XATU', 'TAILLOW', 'SWABLU', 'DELIBIRD', 'ALTARIA'],
      ask='The GALE CLIFF: wind-whipped rocks. Visit?', gt='Come back with 5 BADGES.', npcs=[('HIKER', 'FARFETCH\'D carries a leek. A rare sight.'), ('OLD_WOMAN', 'The wind has stories. Listen.')],
      hidden=['SHARP_BEAK', 'GREAT_BALL', 'REVIVE'], quests=[Q('OLD_WOMAN', ('GREAT_BALL', 2), ('SHARP_BEAK', 1), 'Two GREAT BALLs for my grandson. SHARP BEAK for you.', 'Bless you! Take this SHARP BEAK.', 'The wind is kind today.', 'Two GREAT BALLs, please.', ('GRANNY AND BALLS', 'GALE CLIFF: bring 2 GREAT BALLS.'))]),
 dict(map='SoundMeadow', tpl='FiveIsland_Meadow', badge=5, lv=(30, 36), land=['JIGGLYPUFF', 'WIGGLYTUFF', 'LOUDRED', 'EXPLOUD'.replace('EXPLOUD', 'WHISMUR'), 'CHIMECHO', 'MARACTUS'.replace('MARACTUS', 'CACNEA'), 'SPINDA', 'SKITTY', 'DELCATTY', 'PLUSLE', 'MINUN', 'IGGLYBUFF'],
      ask='The SOUND MEADOW: songs, echoes and Normal types. Visit?', gt='Come back with 5 BADGES.', npcs=[('LASS', 'JIGGLYPUFF sings until you fall asleep.'), ('GENTLEMAN', 'SPINDA never walks the same path twice.')],
      hidden=['MOON_STONE', 'LEPPA_BERRY', 'ELIXIR'], quests=[Q('GENTLEMAN', ('LEPPA_BERRY', 1), ('SOFT_SAND', 1), 'A LEPPA BERRY for my concert. A SOFT SAND for you.', 'Marvelous! Take this SOFT SAND.', 'Bravo!', 'One LEPPA BERRY, please.', ('A BERRY FOR A SONG', 'SOUND MEADOW: bring a LEPPA BERRY.'))]),
 dict(map='ObsidianPass', tpl='MtEmber_RubyPath_B3F', badge=6, lv=(38, 44), land=['ROCKRUFF'.replace('ROCKRUFF', 'GEODUDE'), 'GRAVELER', 'GOLEM', 'ONIX', 'STEELIX', 'RHYHORN', 'RHYDON', 'ARON', 'LAIRON', 'NOSEPASS', 'SANDSLASH', 'SKARMORY'],
      ask='The OBSIDIAN PASS: black rock and heavy hitters. Visit?', gt='Come back with 6 BADGES.', npcs=[('HIKER', 'STEELIX digs through this like butter.'), ('BLACK_BELT', 'Rock hard. My head too.')],
      hidden=['HARD_STONE', 'METAL_COAT', 'MAX_REPEL'], quests=[Q('BLACK_BELT', ('MAX_REPEL', 1), ('HARD_STONE', 1), 'A MAX REPEL for the walk home. HARD STONE for you.', 'Thanks! Take this HARD STONE.', 'Stay strong.', 'One MAX REPEL, please.', ('A LONG WALK HOME', 'OBSIDIAN PASS: bring a MAX REPEL.'))]),
 dict(map='MirrorPond', tpl='Route10', badge=6, lv=(38, 44), land=['LAPRAS', 'SLOWKING'.replace('SLOWKING', 'SLOWBRO'), 'STARMIE', 'SEAKING', 'GOLDUCK', 'POLIWRATH', 'POLITOED'.replace('POLITOED', 'POLIWHIRL'), 'AZUMARILL', 'WHISCASH', 'CRAWDAUNT', 'LUDICOLO'.replace('LUDICOLO', 'LOMBRE'), 'LANTURN'],
      water=['LAPRAS', 'STARMIE', 'GOLDUCK', 'AZUMARILL', 'LANTURN'], fish=['MAGIKARP', 'SEAKING', 'GOLDUCK', 'AZUMARILL', 'WHISCASH', 'LANTURN', 'LAPRAS', 'FEEBAS', 'STARMIE', 'CRAWDAUNT'],
      ask='The MIRROR POND: still water, strong swimmers. Visit?', gt='Come back with 6 BADGES.', npcs=[('FISHER', 'LAPRAS crosses the pond at dusk.'), ('OLD_MAN_1', 'See your face in the water? It looks tired.')],
      hidden=['WATER_STONE', 'MYSTIC_WATER', 'MAX_POTION'], quests=[Q('OLD_MAN_1', ('WATER_STONE', 1), ('MYSTIC_WATER', 1), 'A WATER STONE for the pond. MYSTIC WATER for you.', 'Thank you. Take this MYSTIC WATER.', 'The pond shines.', 'One WATER STONE, please.', ('A STONE FOR THE POND', 'MIRROR POND: bring a WATER STONE.'))]),
 dict(map='PhantomLane', tpl='Route11', badge=7, lv=(44, 50), land=['GENGAR', 'HAUNTER', 'DUSCLOPS', 'BANETTE', 'MISMAGIUS'.replace('MISMAGIUS', 'MISDREAVUS'), 'MURKROW', 'UMBREON', 'SABLEYE', 'ABSOL', 'SNEASEL', 'HOUNDOOM', 'MIGHTYENA'],
      ask='The PHANTOM LANE: a road for ghosts and shadows. Visit?', gt='Come back with 7 BADGES.', npcs=[('OLD_WOMAN', 'Walk fast. Do not look behind.'), ('SCIENTIST', 'DUSCLOPS is a gate between two worlds.')],
      hidden=['SPELL_TAG', 'BLACK_GLASSES', 'MAX_REVIVE'], quests=[Q('OLD_WOMAN', ('MAX_REVIVE', 1), ('SPELL_TAG', 1), 'A MAX REVIVE for my old friend. A SPELL TAG for you.', 'He lives! Take this SPELL TAG.', 'Rest well, friend.', 'One MAX REVIVE, please.', ('AN OLD FRIEND', 'PHANTOM LANE: bring a MAX REVIVE.'))]),
 dict(map='CrownField', tpl='Route22', badge=8, lv=(54, 60), land=['TYRANITAR', 'DRAGONITE', 'SALAMENCE', 'METAGROSS', 'GARCHOMP'.replace('GARCHOMP', 'FLYGON'), 'SCIZOR', 'HERACROSS', 'SNORLAX', 'BLISSEY', 'KANGASKHAN', 'LAPRAS', 'MILTANK'],
      ask='The CROWN FIELD: the strongest wild POKéMON gather here. Visit?', gt='Come back with all 8 BADGES.', npcs=[('GENTLEMAN', 'Only champions walk this field. And their luck.'), ('BLACK_BELT', 'Everything here hits hard. Everything.')],
      hidden=['RARE_CANDY', 'MAX_REVIVE', 'PP_UP'], quests=[Q('GENTLEMAN', ('RARE_CANDY', 1), ('PP_MAX', 1), 'A RARE CANDY for my prize. A PP MAX for you.', 'Magnificent! Take this PP MAX.', 'Fit for a champion.', 'One RARE CANDY, please.', ('A CHAMPION\'S PRIZE', 'CROWN FIELD: bring a RARE CANDY.'))]),
]
SPX = rd('include/constants/species.h')
bad = [(z['map'], n) for z in Z for n in z['land'] + z.get('water', []) + z.get('fish', []) if not re.search(r'#define SPECIES_%s\b' % n, SPX)]
badi = [i for z in Z for q in z['quests'] for i in (q['want'][0], q['rew'][0])] + [i for z in Z for i in z['hidden']]
badi = [i for i in badi if not re.search(r'#define ITEM_%s\b' % i, IT)]
EVO = rd('include/constants/event_objects.h'); badg = [g for z in Z for g in [x[0] for x in z['npcs']] + [q['g'] for q in z['quests']] if not re.search(r'OBJ_EVENT_GFX_%s\b' % g, EVO)]
if bad or badi or badg: print('INVALIDE', bad, badi, set(badg)); raise SystemExit(1)
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = ['# ---- LOT 17']; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman', 'ScribeFerryman', 'DuskFerrywoman', 'SeasonsFerryman', 'ScribeFerryman', 'DuskFerrywoman', 'SeasonsFerryman', 'Apprentice', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
journal_add(journal); flush_flags()
