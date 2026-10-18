#!/usr/bin/env python3
"""Banc d'equilibrage : une VRAIE equipe (pas de mode dieu) contre des dresseurs cles du hack, pilotee par une IA de choix d'attaque.

Prerequis : /tmp/gx (harnais, tz.py, drive.py), ROM /tmp/gx/dbg3.gba (mkdbg3.py : declencheur de dresseur `gTopazeBattleReq`).
  cd <racine du depot> && PYTHONDONTWRITEBYTECODE=1 python3 tools/topaze/emu/bench/balance.py TRAINER_LEADER_BROCK [...] [--delta N] [--lines A|B]

Pour chaque dresseur : equipe de 6 aux niveaux (niveau max du dresseur + delta) construite par partykit (stats GBA reelles, 4 dernieres attaques
apprises), combat joue au tour par tour : on choisit l'attaque au meilleur degat attendu (types du hack, STAB, precision, PP), changement force
au premier Pokemon vivant, aucun objet. Rapport : victoire/defaite, tours, Pokemon restants, PV restants.
"""
import sys, os, re, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/gx')
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
from tz import T, KEYS
import partykit as pk

ROM = '/tmp/gx/dbg3.gba'
import subprocess
def _syms(elf=ROM[:-4] + '.elf'):
    """Adresses des symboles lues dans l'ELF (elles changent a chaque recompilation)."""
    out = subprocess.run(['arm-none-eabi-nm', elf], capture_output=True, text=True).stdout
    d = {}
    for ln in out.splitlines():
        a, _, n = ln.split()[:3] if len(ln.split()) >= 3 else (0, 0, 0)
        if n: d.setdefault(n, []).append(int(a, 16))
    return d
_S = _syms()
BM = _S['gBattleMons'][0]; BM_SZ = 0x58; CTRL = _S['gBattlerControllerFuncs'][0]; OUT = _S['gBattleOutcome'][0]
MOVE_CUR = _S['gMoveSelectionCursor'][0]; ACT_CUR = _S['gActionSelectionCursor'][0]; REQ = _S['gTopazeBattleReq'][0]
_pc = [a for a in _S['HandleInputChooseAction'] if a < 0x08040000]
H_ACTION = _pc[0]; H_MOVE = _S['HandleInputChooseMove'][0]; H_TARGET = [a for a in _S['HandleInputChooseTarget'] if a < 0x08040000][0]
H_PARTY = [a for a in _S['WaitForMonSelection'] if a < 0x08040000][0]
PHYS = {'TYPE_NORMAL', 'TYPE_FIGHTING', 'TYPE_FLYING', 'TYPE_POISON', 'TYPE_GROUND', 'TYPE_ROCK', 'TYPE_BUG', 'TYPE_GHOST', 'TYPE_STEEL'}

def trainer_ids():
    return {m.group(1): int(m.group(2)) for m in re.finditer(r'#define (TRAINER_\w+)\s+(\d+)', open('include/constants/opponents.h').read())}

def trainer_levels(name):
    """[(espece, niveau)] de la fiche du dresseur (trainers.h -> trainer_parties.h)."""
    s = open('src/data/trainers.h').read()
    m = re.search(r'\[%s\] = \{(.*?)\n    \},' % name, s, re.S)
    p = re.search(r'ITEM_CUSTOM_MOVES\((\w+)\)|NO_ITEM_CUSTOM_MOVES\((\w+)\)|ITEM_DEFAULT_MOVES\((\w+)\)|NO_ITEM_DEFAULT_MOVES\((\w+)\)', m.group(1))
    arr = [g for g in p.groups() if g][0]
    t = open('src/data/trainer_parties.h').read()
    b = re.search(r'%s\[\] = \{(.*?)\n\};' % arr, t, re.S).group(1)
    return [(sp, int(l)) for l, sp in re.findall(r'\.lvl = (\d+),\s*\.species = (SPECIES_\w+)', b) if True] or \
           [(sp, int(l)) for sp, l in re.findall(r'\.species = (SPECIES_\w+).*?\.lvl = (\d+)', b, re.S)]

def mon(emu, side):
    b = emu.peek(BM + side * BM_SZ, BM_SZ)
    sp, atk, df, spe, spa, spd = struct.unpack('<6H', b[:12]); mv = struct.unpack('<4H', b[12:20])
    return dict(sp=sp, atk=atk, df=df, spe=spe, spa=spa, spd=spd, moves=mv, t1=b[0x21], t2=b[0x22], pp=list(b[0x24:0x28]),
                hp=struct.unpack('<H', b[0x28:0x2a])[0], lvl=b[0x2a], mhp=struct.unpack('<H', b[0x2c:0x2e])[0], st=struct.unpack('<I', b[0x4c:0x50])[0])

_REV = None
def name_of(table, v):
    return next((k for k, x in table.items() if x == v), '?')

def best_move(me, foe):
    M = pk.MOVES(); T_ = pk.TYPES(); mi = pk.moves_info(); inv = {v: k for k, v in M.items()}; ti = {v: k for k, v in T_.items() if k.startswith('TYPE_')}
    mytypes = {ti.get(me['t1']), ti.get(me['t2'])}; ftypes = (ti.get(foe['t1']), ti.get(foe['t2']))
    best = (-1, 0)
    for i, mv in enumerate(me['moves']):
        if mv == 0 or me['pp'][i] == 0: continue
        info = mi.get(inv.get(mv));
        if not info: continue
        sc = 0.0
        if info['power'] > 1:
            phys = info['type'] in PHYS
            a, d = (me['atk'], foe['df']) if phys else (me['spa'], foe['spd'])
            dmg = info['power'] * a / max(d, 1) * (1.5 if info['type'] in mytypes else 1.0) * pk.effectiveness(info['type'], ftypes)
            sc = dmg * min(info['acc'] or 100, 100) / 100.0
        elif info['power'] == 1: sc = 5      # degats fixes / etc. : faible priorite
        else: sc = 0.1
        if sc > best[0]: best = (sc, i)
    return best[1]

def run_battle(t, trainer, maxturns=150, log=None):
    """Lance le combat contre `trainer` (id numerique) ; renvoie dict(issue, tours, vivants, pv%)."""
    e = t.e; e.cmd('poke8 %x 0' % OUT)
    e.cmd('poke8 %x %x' % (REQ, trainer & 255)); e.cmd('poke8 %x %x' % (REQ + 1, trainer >> 8))
    seen = []; turns = 0; moved = False; idle = 0
    for it in range(6000):
        e.run(12, 0)
        out = e.peek(OUT, 1)[0]
        f = struct.unpack('<I', e.peek(CTRL, 4))[0] & ~1
        if os.environ.get('BAL_V') and it % 10 == 0: m0 = mon(e, 0); m1 = mon(e, 1); print(it, hex(f), 'me', m0['sp'], m0['hp'], 'foe', m1['sp'], m1['hp'], 'out', out, 'turns', turns, flush=True)
        if out and it > 20:
            e.run(120, 0); break
        if f == H_ACTION:
            m0 = mon(e, 0); m1 = mon(e, 1)
            if (m1['sp'], m1['lvl']) not in seen: seen.append((m1['sp'], m1['lvl']))
            e.cmd('poke8 %x 0' % ACT_CUR); e.run(4, KEYS['A']); e.run(30, 0); turns += 1
            if turns > maxturns: return dict(issue='TIMEOUT', turns=turns, seen=seen)
        elif f == H_MOVE:
            m0 = mon(e, 0); m1 = mon(e, 1); i = best_move(m0, m1)
            e.cmd('poke8 %x %x' % (MOVE_CUR, i)); e.run(4, KEYS['A']); e.run(30, 0)
            if e.peek(CTRL, 4) and (struct.unpack('<I', e.peek(CTRL, 4))[0] & ~1) == H_TARGET: e.run(4, KEYS['A']); e.run(30, 0)
        elif f in (H_TARGET,): e.run(4, KEYS['A']); e.run(30, 0)
        else:
            m0 = mon(e, 0)
            if f == H_PARTY:      # menu des Pokemon apres un K.O. : on se place sur le premier Pokemon vivant et on l'envoie
                e.run(60, 0)
                hp = [struct.unpack('<H', e.peek(0x02024288 + 100 * k + 0x56, 2))[0] for k in range(6)]
                tgt = next((k for k in range(6) if hp[k] > 0 and k < e.peek(0x0202402d, 1)[0]), None)
                if tgt is None: e.run(4, KEYS['A']); e.run(20, 0); continue
                for _ in range(tgt): e.run(4, KEYS['DOWN']); e.run(14, 0)
                e.run(4, KEYS['A']); e.run(30, 0); e.run(4, KEYS['A']); e.run(60, 0)
                if (struct.unpack('<I', e.peek(CTRL, 4))[0] & ~1) == f:
                    for _ in range(3): e.run(4, KEYS['B']); e.run(20, 0)      # echec : on annule et on recommence
                    for _ in range(tgt): e.run(4, KEYS['UP']); e.run(14, 0)
            else: e.run(4, KEYS['A']); e.run(20, 0)      # texte
    out = e.peek(OUT, 1)[0]
    alive = 0; tot = 0; mx = 0
    n = e.peek(0x0202402d, 1)[0]
    for i in range(n):
        d = e.peek(0x02024288 + 100 * i + 0x56, 4); hp, mh = struct.unpack('<HH', d)
        alive += hp > 0; tot += hp; mx += mh
    return dict(issue={1: 'WIN', 2: 'LOSS'}.get(out, 'OUT%d' % out), turns=turns, alive=alive, n=n, hp=round(100 * tot / max(mx, 1)), seen=seen)

def main():
    args = sys.argv[1:]; delta = 0; lines = pk.LINES_A
    if '--delta' in args: i = args.index('--delta'); delta = int(args[i + 1]); del args[i:i + 2]
    if '--lines' in args: i = args.index('--lines'); lines = {'A': pk.LINES_A, 'B': pk.LINES_B}[args[i + 1]]; del args[i:i + 2]
    ids = trainer_ids(); inv = {v: k for k, v in pk.SPECIES().items()}
    t = T('PalletTown', 12, 12, rom=ROM, party=True, nocombat=True, badges=8, god=False)
    t.e.run(60, 0); base = '/tmp/gx/st/bal_base.ss'; t.e.cmd('ss ' + base)
    for name in args:
        foe = trainer_levels(name); lv = max(l for _, l in foe) + delta
        t.e.cmd('ls ' + base); t.e.run(10, 0)
        team = pk.team(lines, lv); pk.write_team(t.e, team)
        r = run_battle(t, ids[name])
        es = ', '.join('%s%d' % (inv.get(sp, sp).replace('SPECIES_', '')[:9], l) for sp, l in foe)
        print('%-34s niv equipe %3d | %-7s tours %3s  restants %s/%s PV %s%% | ennemis: %s' % (name, lv, r['issue'], r['turns'], r.get('alive', '-'), r.get('n', '-'), r.get('hp', '-'), es), flush=True)

if __name__ == '__main__':
    main()
