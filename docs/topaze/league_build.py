#!/usr/bin/env python3
"""Génère le tournoi de la Ligue (11 combats) : dresseurs, équipes, constantes.
Idempotent : regénère les blocs entre les marqueurs / remplace les anciens blocs.
Les scripts et textes de la salle sont écrits à la main (voir LoreleisRoom/ChampionsRoom)."""
import re

# (const, nom, pic, double, items, [(espèce, niveau), ...])
T = [
 ('SEKO',   'SEKO',    'SCIENTIST',      0, 1, [('SWELLOW',50),('LINOONE',50),('VIGOROTH',51),('DELCATTY',51),('SCEPTILE',52)]),
 ('MAY',    'MAY',     'RS_MAY_1',       0, 1, [('ROSELIA',51),('MANECTRIC',51),('ALTARIA',52),('WAILORD',52),('BLAZIKEN',53)]),
 ('BRENDAN','BRENDAN', 'RS_BRENDAN_1',   0, 1, [('ABSOL',52),('EXPLOUD',52),('FLYGON',53),('GARDEVOIR',53),('SWAMPERT',54)]),
 ('GOLD',   'GOLD',    'COOLTRAINER_M',  0, 1, [('UMBREON',53),('ESPEON',53),('AMPHAROS',54),('STEELIX',54),('TYPHLOSION',55)]),
 ('CRYSTAL','CRYSTAL', 'COOLTRAINER_F',  1, 1, [('TOGETIC',54),('XATU',54),('AZUMARILL',55),('QUAGSIRE',55),('MEGANIUM',56)]),
 ('LEAF',   'LEAF',    'LEAF',           0, 2, [('CLEFABLE',55),('VAPOREON',55),('DUGTRIO',56),('ALAKAZAM',56),('SNORLAX',57),('VENUSAUR',58)]),
 ('ZEPHYR', 'ZEPHYR',  'RIVAL_LATE',     0, 2, [('JOLTEON',56),('GENGAR',56),('MACHAMP',57),('EXEGGUTOR',57),('BLASTOISE',58),('CHARIZARD',59)]),
 ('BLUE',   'BLUE',    'CHAMPION_RIVAL', 1, 2, [('PIDGEOT',58),('ALAKAZAM',58),('RHYDON',59),('GYARADOS',59),('ARCANINE',60),('EXEGGUTOR',61)]),
 ('N',      'N',       'PSYCHIC_M',      0, 2, [('ALTARIA',59),('BANETTE',59),('WALREIN',60),('LUDICOLO',60),('MILOTIC',61),('ABSOL',62)]),
 ('CHEN',   'OAK',     'PROFESSOR_OAK',  0, 3, [('TAUROS',61),('EXEGGUTOR',61),('GYARADOS',62),('ARCANINE',62),('SNORLAX',63),('DRAGONITE',64)]),
 ('BOSS',   'ONYBRIS', 'MAGMA_LEADER_MAXIE', 1, 3, [('CROBAT',64),('HOUNDOOM',64),('GENGAR',65),('TYRANITAR',65),('SALAMENCE',66),('METAGROSS',67)]),
]

def read(f): return open(f).read()
def write(f, s): open(f, 'w').write(s)

# --- opponents.h
f = 'include/constants/opponents.h'; s = read(f)
s = re.sub(r'#define TRAINER_LEAGUE_\w+\s+\d+\n', '', s)
defs = ''.join('#define TRAINER_LEAGUE_%-22s %d\n' % (t[0], 743 + i) for i, t in enumerate(T))
s = s.replace('#define TRAINER_CUE_BALL_PAXTON                  742\n',
              '#define TRAINER_CUE_BALL_PAXTON                  742\n' + defs)
s = re.sub(r'#define NUM_TRAINERS\s+\d+', '#define NUM_TRAINERS                             %d' % (743 + len(T)), s)
write(f, s)

# --- trainers.h
f = 'src/data/trainers.h'; s = read(f)
a = s.index('    [TRAINER_LEAGUE_POOL_1] = {')
b = s.index('\n};', a)
blk = ''
for c, name, pic, dbl, items, party in T:
    its = ', '.join(['ITEM_FULL_RESTORE'] * items)
    blk += f'''    [TRAINER_LEAGUE_{c}] = {{
        .trainerClass = TRAINER_CLASS_PKMN_TRAINER,
        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,
        .trainerPic = TRAINER_PIC_{pic},
        .trainerName = _("{name}"),
        .items = {{{its}}},
        .doubleBattle = {'TRUE' if dbl else 'FALSE'},
        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,
        .party = NO_ITEM_DEFAULT_MOVES(sParty_League{c.title()}),
    }},
'''
s = s[:a] + blk.rstrip('\n') + s[b:]
write(f, s)

# --- trainer_parties.h
f = 'src/data/trainer_parties.h'; s = read(f)
a = s.index('static const struct TrainerMonNoItemDefaultMoves sParty_LeaguePool1[]')
b = s.index('sParty_LeagueSemi[]')
b = s.index('\n};\n', b) + 4
blk = ''
for c, name, pic, dbl, items, party in T:
    blk += f'static const struct TrainerMonNoItemDefaultMoves sParty_League{c.title()}[] = {{\n'
    for sp, lv in party:
        blk += f'    {{\n        .iv = 200,\n        .lvl = {lv},\n        .species = SPECIES_{sp},\n    }},\n'
    blk += '};\n\n'
s = s[:a] + blk.rstrip('\n') + '\n' + s[b:]
write(f, s)
print('ok', len(T), 'dresseurs ->', 743 + len(T))
