#!/usr/bin/env python3
"""LOT 9 : Bosquet d'Evoli (evolutions d'Evoli + bebes), Reserve du Professeur (postgame : departs), tableaux d'avis dans 10 villes (ou trouver quoi, genere depuis les tables sauvages). Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'EeveeGrove' in rd('data/maps/FuchsiaCity/scripts.inc') or 'EeveeGrove' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='EeveeGrove', tpl='SixIsland_PatternBush', badge=5, lv=(30, 36), land=['EEVEE', 'VAPOREON', 'JOLTEON', 'FLAREON', 'ESPEON', 'UMBREON', 'PIKACHU', 'PICHU', 'CLEFFA', 'IGGLYBUFF', 'TOGEPI', 'SMOOCHUM'],
      ask='The EEVEE GROVE: every shade of one family lives here. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('LASS', 'EEVEE can become many things. Stones, bonds, patience.'), ('LITTLE_GIRL', 'I saw all of the family under the same tree.')], hidden=['FIRE_STONE', 'WATER_STONE', 'THUNDER_STONE'],
      quests=[dict(g='WOMAN_1', want=('SODA_POP', 1), rew=('SOOTHE_BELL', 1), ask='A fizzy drink for my little one, and a bell for you.', done='Cheers! Take this SOOTHE BELL.', after='The grove is happy.', miss='One SODA POP, please. The cafe sells them.', j=('A FIZZY TREAT', 'EEVEE GROVE: bring a SODA POP.'))]),
 dict(map='ProfessorReserve', tpl='FiveIsland_Meadow', badge=8, lv=(52, 58), land=['BULBASAUR', 'CHARMANDER', 'SQUIRTLE', 'CHIKORITA', 'CYNDAQUIL', 'TOTODILE', 'TREECKO', 'TORCHIC', 'MUDKIP', 'IVYSAUR', 'CHARMELEON', 'WARTORTLE'],
      water=['SQUIRTLE', 'TOTODILE', 'MUDKIP', 'WARTORTLE', 'MARSHTOMP'], fish=['MAGIKARP', 'SQUIRTLE', 'TOTODILE', 'MUDKIP', 'WARTORTLE', 'CROCONAW', 'MARSHTOMP', 'BLASTOISE', 'FERALIGATR', 'SWAMPERT'],
      ask='The PROFESSOR\'S RESERVE: first partners run free here. Visit?', gt='Come back with all 8 BADGES.',
      npcs=[('SCIENTIST', 'Every trainer starts with one. Here they roam free.'), ('OLD_MAN_1', 'I come here to remember my first partner.')], hidden=['RARE_CANDY', 'MAX_REVIVE', 'PP_UP'],
      quests=[dict(g='SCIENTIST', want=('RARE_CANDY', 1), rew=('PP_MAX', 1), ask='A RARE CANDY for my research. I will give you a PP MAX.', done='Excellent! Here is a PP MAX.', after='The research goes on.', miss='One RARE CANDY, please.', j=('THE RESERVE STUDY', 'PROFESSOR RESERVE: bring a RARE CANDY.'))]),
]
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = ['# ---- LOT 9 (bosquet evoli, reserve, avis)']; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z in Z: ferry_add('SeasonsFerryman', z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
# ---- tableaux d'avis : ou trouver quoi (genere depuis les tables sauvages des zones ajoutees)
NAMES = {'ReflectionMarsh': 'REFLECTION MARSH', 'StoneGreenhouse': 'STONE GREENHOUSE', 'TradeDock': 'TRADE DOCK', 'FossilDig': 'FOSSIL DIG', 'CyclePond': 'CYCLE POND', 'HoennWestReserve': 'WEST RESERVE', 'HoennEastReserve': 'EAST RESERVE',
         'SunriseMeadow': 'SUNRISE MEADOW', 'AshenMine': 'ASHEN MINE', 'BerryOrchard': 'BERRY ORCHARD', 'WhisperGrove': 'WHISPER GROVE', 'SparkGlade': 'SPARK GLADE', 'DragonPerch': 'DRAGON PERCH', 'ZenGarden': 'ZEN GARDEN',
         'GiantsPlain': 'GIANTS PLAIN', 'DuneSea': 'DUNE SEA', 'FrostHollow': 'FROST HOLLOW', 'EmberRim': 'EMBER RIM', 'NocturneWood': 'NOCTURNE WOOD', 'ShellCoast': 'SHELL COAST', 'EeveeGrove': 'EEVEE GROVE', 'ProfessorReserve': 'PROF RESERVE'}
where = {}
for e in grp:
    mm = e['map']
    for nm, pretty in NAMES.items():
        if mm == N.mapid(nm):
            for kind in ('land_mons', 'water_mons', 'fishing_mons'):
                for mo in e.get(kind, {}).get('mons', []):
                    s = mo['species'][8:]; where.setdefault(s, [])
                    if pretty not in where[s]: where[s].append(pretty)
RARE = ['FEEBAS', 'ABSOL', 'LARVITAR', 'DRATINI', 'AERODACTYL', 'CHANSEY', 'KANGASKHAN', 'EEVEE', 'PORYGON', 'RELICANTH', 'ZANGOOSE', 'SEVIPER', 'HERACROSS', 'SKARMORY', 'LAPRAS', 'DITTO', 'SABLEYE', 'MAWILE', 'SHEDINJA', 'ELECTABUZZ', 'MAGMAR', 'MR_MIME', 'WOBBUFFET', 'CHIMECHO', 'LUNATONE', 'SOLROCK', 'SNEASEL', 'DRAGONAIR', 'PIKACHU', 'TOGEPI']
BOARDS = ['PalletTown', 'ViridianCity', 'PewterCity', 'VermilionCity', 'LavenderTown', 'CeladonCity', 'FuchsiaCity', 'CinnabarIsland', 'SaffronCity', 'IndigoPlateau_Exterior']
RARE = [r for r in RARE if r in where]; per = 3
for bi, m in enumerate(BOARDS):
    sel = RARE[bi * per:(bi + 1) * per] or RARE[:per]
    if not sel: continue
    nav = R.Nav(m); d = json.load(open('data/maps/%s/map.json' % m)); cells = comp(nav); taken = [(o['x'], o['y']) for o in d['object_events']] + [(b['x'], b['y']) for b in d['bg_events']] + list(nav.warps)
    c = near(nav, [x for x in cells if 2 <= x[0] < nav.w - 2 and 2 <= x[1] < nav.h - 2], (nav.w // 2 - 3, nav.h // 2 + 3), taken, margin=3)
    S = '%s_EventScript_NoticeBoard' % m; T = '%s_Text_NoticeBoard' % m
    d['bg_events'].append(N.sign(c[0], c[1], S, 0)); N.jdump(d, 'data/maps/%s/map.json' % m)
    sc = '\n@ Topaze: tableau d\'avis (ou trouver les rares)\n%s::\n\tmsgbox %s, MSGBOX_SIGN\n\tend\n' % (S, T); tx = ''
    lines = []
    for s in sel: lines.append('%s: %s.' % (s.replace('_', ' '), ', '.join(where[s][:2])))
    tx = N.text(T, 'WANTED: ' + ' '.join(lines))
    open('data/maps/%s/scripts.inc' % m, 'a').write(sc); open('data/maps/%s/text.inc' % m, 'a').write(tx)
    print(m, c, sel)
journal_add(journal); flush_flags()
