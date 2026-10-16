#!/usr/bin/env python3
"""partykit : donnees du hack (especes, attaques, tables de types, apprentissage) + ecriture d'une equipe de 6 en RAM.

Utilise par balance.py. Tout est lu dans les sources du depot (le hack modifie les types, les stats et les learnsets), donc l'equipe de
reference se comporte comme une vraie equipe du jeu : stats calculees avec les formules de la GBA (IV 15, EV 0, nature neutre),
attaques = les 4 dernieres apprises par niveau (comme GiveMonInitialMoveset)."""
import os, re, struct, functools
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..')
def rd(p): return open(os.path.join(ROOT, p)).read()

@functools.lru_cache(None)
def consts(path, prefix):
    out = {}
    for m in re.finditer(r'#define (%s\w+)\s+(0x[0-9A-Fa-f]+|\d+)\b' % prefix, rd(path)): out[m.group(1)] = int(m.group(2), 0)
    return out
SPECIES = lambda: consts('include/constants/species.h', 'SPECIES_')
MOVES = lambda: consts('include/constants/moves.h', 'MOVE_')
TYPES = lambda: consts('include/constants/pokemon.h', 'TYPE_')

@functools.lru_cache(None)
def species_info():
    s = rd('src/data/pokemon/species_info.h'); out = {}
    parts = re.split(r'\n    \[(SPECIES_\w+)\] =', s)
    for nm, b in zip(parts[1::2], parts[2::2]):
        if '.baseHP' not in b: continue
        class m_:  # compat avec l'ancien schema
            pass
        g = lambda k, b=b: int(re.search(r'\.%s = (\d+)' % k, b).group(1))
        t = re.search(r'\.types = \{(\w+), (\w+)\}', b); ab = re.search(r'\.abilities = \{(\w+), (\w+)\}', b)
        gr = re.search(r'\.growthRate = (\w+)', b)
        out[nm] = dict(hp=g('baseHP'), atk=g('baseAttack'), df=g('baseDefense'), spe=g('baseSpeed'), spa=g('baseSpAttack'), spd=g('baseSpDefense'),
                              types=(t.group(1), t.group(2)), growth=gr.group(1) if gr else 'GROWTH_MEDIUM_FAST', abil=ab.groups() if ab else ('ABILITY_NONE', 'ABILITY_NONE'))
    return out

@functools.lru_cache(None)
def moves_info():
    s = rd('src/data/battle_moves.h'); out = {}
    for m in re.finditer(r'\[(MOVE_\w+)\] =\s*\{(.*?)\n    \},', s, re.S):
        b = m.group(2); g = lambda k, d=0: (lambda r: r.group(1) if r else d)(re.search(r'\.%s = (\w+)' % k, b))
        out[m.group(1)] = dict(effect=g('effect'), power=int(g('power')), type=g('type', 'TYPE_NORMAL'), acc=int(g('accuracy')), pp=int(g('pp')), prio=int(g('priority')) if str(g('priority')).lstrip('-').isdigit() else 0)
    return out

@functools.lru_cache(None)
def type_chart():
    s = rd('src/battle_main.c'); i = s.index('const u8 gTypeEffectiveness'); j = s.index('};', i)
    mul = {'TYPE_MUL_NO_EFFECT': 0, 'TYPE_MUL_NOT_EFFECTIVE': 5, 'TYPE_MUL_SUPER_EFFECTIVE': 20, 'TYPE_MUL_NORMAL': 10}
    ch = {}
    for m in re.finditer(r'(TYPE_\w+), (TYPE_\w+), (TYPE_MUL_\w+)', s[i:j]): ch[(m.group(1), m.group(2))] = mul[m.group(3)] / 10.0
    return ch
def effectiveness(mtype, dtypes):
    ch = type_chart(); e = 1.0
    for d in set(dtypes):
        if d and d != 'TYPE_NONE': e *= ch.get((mtype, d), 1.0)
    return e

@functools.lru_cache(None)
def learnsets():
    s = rd('src/data/pokemon/level_up_learnsets.h'); ptr = rd('src/data/pokemon/level_up_learnset_pointers.h'); sets = {}
    for m in re.finditer(r'static const u16 (\w+)\[\] = \{(.*?)LEVEL_UP_END', s, re.S):
        sets[m.group(1)] = [(int(l), mv) for l, mv in re.findall(r'LEVEL_UP_MOVE\(\s*(\d+),\s*(MOVE_\w+)\)', m.group(2))]
    return {m.group(1): sets.get(m.group(2), []) for m in re.finditer(r'\[(SPECIES_\w+)\] = (\w+),', ptr)}

def initial_moves(species, level):
    mv = []
    for l, m in learnsets().get(species, []):
        if l > level or m in mv: continue
        mv.append(m)
        if len(mv) > 4: mv.pop(0)
    return mv

def exp_for(growth, n):
    c = n ** 3
    if growth == 'GROWTH_MEDIUM_FAST': return c
    if growth == 'GROWTH_FAST': return 4 * c // 5
    if growth == 'GROWTH_SLOW': return 5 * c // 4
    if growth == 'GROWTH_MEDIUM_SLOW': return 6 * c // 5 - 15 * n * n + 100 * n - 140
    if growth == 'GROWTH_ERRATIC':
        return (100 - n) * c // 50 if n <= 50 else (150 - n) * c // 100 if n <= 68 else ((1911 - 10 * n) // 3) * c // 500 if n <= 98 else (160 - n) * c // 100
    if n <= 15: return c * ((n + 1) // 3 + 24) // 50      # FLUCTUATING
    if n <= 35: return c * (n + 14) // 50
    return c * (n // 2 + 32) // 50

def stats(species, level, iv=15):
    b = species_info()[species]
    hp = (2 * b['hp'] + iv) * level // 100 + level + 10
    f = lambda k: (2 * b[k] + iv) * level // 100 + 5
    return hp, f('atk'), f('df'), f('spe'), f('spa'), f('spd')

ORDER = ['GAEM', 'GAME', 'GEAM', 'GEMA', 'GMAE', 'GMEA', 'AGEM', 'AGME', 'AEGM', 'AEMG', 'AMGE', 'AMEG', 'EGAM', 'EGMA', 'EAGM', 'EAMG', 'EMGA', 'EMAG', 'MGAE', 'MGEA', 'MAGE', 'MAEG', 'MEGA', 'MEAG']
def build_mon(template, species, level, moves=None, iv=15):
    """100 octets d'un Pokemon d'equipe, a partir d'un Pokemon valide existant (`template`, 100 octets) : on garde nom/OT/drapeaux."""
    b = bytearray(template)
    pid = 600 * 7919                    # multiple de 24 (ordre GAEM) et de 25 (nature neutre)
    otid = struct.unpack('<I', b[4:8])[0]; key = pid ^ otid
    info = species_info()[species]
    moves = list(moves) if moves else initial_moves(species, level)
    mi = moves_info(); M = MOVES(); S = SPECIES()
    g = struct.pack('<HHIBBH', S[species], 0, exp_for(info['growth'], level), 0, 70, 0)
    a = b''.join(struct.pack('<H', M[m]) for m in moves) + b'\0\0' * (4 - len(moves)) + bytes(mi[m]['pp'] for m in moves) + b'\0' * (4 - len(moves))
    e = bytes(12)
    ivw = iv | iv << 5 | iv << 10 | iv << 15 | iv << 20 | iv << 25     # abilityNum = 0, pas un oeuf
    m_ = struct.pack('<BBHII', 0, 0, 0, ivw, 0)
    sub = {'G': g, 'A': a, 'E': e, 'M': m_}
    data = b''.join(sub[c] for c in ORDER[pid % 24])
    ck = sum(struct.unpack('<24H', data)) & 0xffff
    enc = bytearray()
    for i in range(0, 48, 4): enc += struct.pack('<I', struct.unpack('<I', data[i:i + 4])[0] ^ key)
    b[0:4] = struct.pack('<I', pid); b[28:30] = struct.pack('<H', ck); b[32:80] = enc
    hp, atk, df, spe, spa, spd = stats(species, level, iv)
    b[80:84] = bytes(4); b[84] = level; b[85] = 0
    b[86:100] = struct.pack('<HHHHHHH', hp, hp, atk, df, spe, spa, spd)
    return bytes(b)

# lignees de reference : (espece, niveau minimal d'evolution)
LINES_A = [[('SPECIES_CHARMANDER', 1), ('SPECIES_CHARMELEON', 16), ('SPECIES_CHARIZARD', 36)],
           [('SPECIES_SQUIRTLE', 1), ('SPECIES_WARTORTLE', 16), ('SPECIES_BLASTOISE', 36)],
           [('SPECIES_BULBASAUR', 1), ('SPECIES_IVYSAUR', 16), ('SPECIES_VENUSAUR', 32)],
           [('SPECIES_PIDGEY', 1), ('SPECIES_PIDGEOTTO', 18), ('SPECIES_PIDGEOT', 36)],
           [('SPECIES_PIKACHU', 1), ('SPECIES_RAICHU', 30)],
           [('SPECIES_ABRA', 1), ('SPECIES_KADABRA', 16), ('SPECIES_ALAKAZAM', 36)]]
LINES_B = [[('SPECIES_MACHOP', 1), ('SPECIES_MACHOKE', 28), ('SPECIES_MACHAMP', 40)],
           [('SPECIES_GASTLY', 1), ('SPECIES_HAUNTER', 25), ('SPECIES_GENGAR', 38)],
           [('SPECIES_MAGIKARP', 1), ('SPECIES_GYARADOS', 20)],
           [('SPECIES_DRATINI', 1), ('SPECIES_DRAGONAIR', 30), ('SPECIES_DRAGONITE', 55)],
           [('SPECIES_GROWLITHE', 1), ('SPECIES_ARCANINE', 36)],
           [('SPECIES_RHYHORN', 1), ('SPECIES_RHYDON', 42)]]
def line_species(line, level):
    sp = line[0][0]
    for s, l in line:
        if level >= l: sp = s
    return sp
def team(lines, level):
    return [(line_species(l, level), level) for l in lines]

# --- RAM ------------------------------------------------------------------------------------------------------------------------------
PARTY = 0x02024288; PARTY_COUNT = 0x0202402d
def write_team(emu, members, template=None):
    """Remplace l'equipe du joueur par `members` = [(espece, niveau), ...] (6 max)."""
    tpl = template or emu.peek(PARTY, 100)
    blob = b''.join(build_mon(tpl, s, l) for s, l in members) + bytes(100 * (6 - len(members)))
    for i, x in enumerate(blob): emu.cmd('poke8 %x %x' % (PARTY + i, x))
    emu.cmd('poke8 %x %x' % (PARTY_COUNT, len(members)))

if __name__ == '__main__':
    import sys
    print(species_info()['SPECIES_CHARIZARD'], initial_moves('SPECIES_CHARIZARD', 50), stats('SPECIES_CHARIZARD', 50), exp_for('GROWTH_MEDIUM_SLOW', 50))
    print(team(LINES_A, 40)); print(len(type_chart()), effectiveness('TYPE_FIRE', ('TYPE_GRASS', 'TYPE_ICE')), len(learnsets()), len(moves_info()))
