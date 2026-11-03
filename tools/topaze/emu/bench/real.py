#!/usr/bin/env python3
"""Cerveau de combat du pilote « joueur reel » (sans mode dieu) : lecture de l'etat en RAM, choix d'attaque par types, changement de Pokemon.

Tout est lu dans la ROM / la RAM de /tmp/gx/dbg2.elf (adresses via nm, jamais en dur)."""
import struct, subprocess

ELF = '/tmp/gx/dbg2.elf'
_S = {}
def sym(name):
    if not _S:
        for l in subprocess.run(['arm-none-eabi-nm', ELF], capture_output=True, text=True).stdout.splitlines():
            a = l.split()
            if len(a) == 3: _S.setdefault(a[2], int(a[0], 16))
    return _S[name]

# types (FireRed) : NORMAL 0 FIGHTING 1 FLYING 2 POISON 3 GROUND 4 ROCK 5 BUG 6 GHOST 7 STEEL 8 MYSTERY 9 FIRE 10 WATER 11 GRASS 12 ELECTRIC 13 PSYCHIC 14 ICE 15 DRAGON 16 DARK 17
ORDERS = ['GAEM', 'GAME', 'GEAM', 'GEMA', 'GMAE', 'GMEA', 'AGEM', 'AGME', 'AEGM', 'AEMG', 'AMGE', 'AMEG', 'EGAM', 'EGMA', 'EAGM', 'EAMG', 'EMGA', 'EMAG', 'MGAE', 'MGEA', 'MAGE', 'MAEG', 'MEGA', 'MEAG']
# attaques a ne jamais choisir automatiquement (auto-KO, charge sans benefice, effets sans interet)
BAD_EFFECTS = {7: 'dream eater', 8: 'mirror move', 36: 'razor wind', 38: 'selfdestruct', 39: 'skull bash', 75: 'solarbeam', 76: 'sky attack'}


class Brain:
    def __init__(s, emu):
        s.e = emu
        s.mv = emu.peek(sym('gBattleMoves'), 12 * 412)      # table des attaques (ROM)
        s.te = []                                            # table des types
        b = emu.peek(sym('gTypeEffectiveness'), 3 * 120); i = 0
        while i + 2 < len(b) and b[i] != 0xFF:
            if b[i] != 0xFE: s.te.append((b[i], b[i + 1], b[i + 2]))
            i += 3
        s.tab = {(a, d): m for a, d, m in s.te}

    # ---- lecture
    def move(s, mid):
        o = s.mv[mid * 12:(mid + 1) * 12]
        return dict(effect=o[0], power=o[1], type=o[2], acc=o[3], pp=o[4], prio=o[7] if o[7] < 128 else o[7] - 256)
    def bm(s, i):
        """Combattant i (0 = joueur, 1 = adversaire) : dict."""
        a = sym('gBattleMons') + 0x58 * i; b = s.e.peek(a, 0x58)
        return dict(species=struct.unpack_from('<H', b, 0)[0], atk=struct.unpack_from('<H', b, 2)[0], moves=list(struct.unpack_from('<4H', b, 0x0C)),
                    type1=b[0x21], type2=b[0x22], pp=list(b[0x24:0x28]), hp=struct.unpack_from('<H', b, 0x28)[0], level=b[0x2A],
                    maxhp=struct.unpack_from('<H', b, 0x2C)[0], status=struct.unpack_from('<I', b, 0x4C)[0])
    def party(s, enemy=False):
        base = sym('gEnemyParty') if enemy else sym('gPlayerParty')
        n = s.e.peek(sym('gEnemyPartyCount') if enemy else sym('gPlayerPartyCount'), 1)[0]
        out = []
        for i in range(min(n, 6)):
            b = s.e.peek(base + 100 * i, 100)
            pers, otid = struct.unpack_from('<II', b, 0); key = pers ^ otid
            sec = list(struct.unpack_from('<12I', b, 0x20)); sec = [w ^ key for w in sec]
            raw = b''.join(struct.pack('<I', w) for w in sec); order = ORDERS[pers % 24]
            sub = {c: raw[12 * k:12 * k + 12] for k, c in enumerate(order)}
            sp = struct.unpack_from('<H', sub['G'], 0)[0]
            moves = list(struct.unpack_from('<4H', sub['A'], 0)); pp = list(sub['A'][8:12])
            lvl = b[0x54]; hp, mhp = struct.unpack_from('<HH', b, 0x56)
            out.append(dict(i=i, species=sp, moves=moves, pp=pp, level=lvl, hp=hp, maxhp=mhp, status=struct.unpack_from('<I', b, 0x50)[0], egg=bool(struct.unpack_from('<I', sub['M'], 4)[0] >> 30 & 1)))
        return out
    def eff(s, atype, t1, t2):
        m = 10
        for d in {t1, t2}:
            m = m * s.tab.get((atype, d), 10) // 10
        return m      # 0, 2, 5, 10, 20, 40 (x10 pour 1.0)
    # ---- decisions
    def score(s, mid, user, foe):
        """Valeur attendue d'une attaque de `user` (dict bm) sur `foe` (dict bm)."""
        if mid == 0: return -1
        m = s.move(mid)
        if m['power'] <= 1 or m['effect'] in BAD_EFFECTS: return 0
        e = s.eff(m['type'], foe['type1'], foe['type2'])
        stab = 15 if m['type'] in (user['type1'], user['type2']) else 10
        v = m['power'] * stab * e * max(m['acc'], 70 if m['acc'] == 0 else m['acc']) / 100.0
        if m['effect'] in (27, 28, 31, 63): v *= 0.6        # attaques en 2 temps / recul lourd
        return v
    def pick_move(s):
        u, f = s.bm(0), s.bm(1)
        best, bi = -1, 0
        for i, mid in enumerate(u['moves']):
            if mid == 0 or u['pp'][i] == 0: continue
            v = s.score(mid, u, f)
            if v > best: best, bi = v, i
        if best <= 0:       # aucune attaque utile : prend la 1re avec des PP
            for i, mid in enumerate(u['moves']):
                if mid and u['pp'][i]: return i
        return bi
    def best_switch(s, avoid=()):
        """Meilleur remplacant vivant (indice dans l'equipe) face a l'adversaire courant, ou None."""
        f = s.bm(1); cand = []
        pm = s.party()
        for p in pm:
            if p['i'] in avoid or p['hp'] <= 0 or p['egg']: continue
            # note : type du remplacant approxime par ses attaques (pas de table d'especes)
            v = 0
            for k, mid in enumerate(p['moves']):
                if mid and p['pp'][k]:
                    mm = s.move(mid)
                    if mm['power'] > 1: v = max(v, mm['power'] * s.eff(mm['type'], f['type1'], f['type2']) * (p['level'] + 10))
            cand.append((v * p['hp'] / max(p['maxhp'], 1), p['i']))
        cand.sort(reverse=True)
        return cand[0][1] if cand else None


# ======================================================================================================================
# Pilote : mixin a ajouter a Auto (voir real_run.py)
KEYSEQ = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)}      # curseur 2x2 -> (colonne, ligne)
class BattleMixin:
    real = True
    def _brain(s):
        if not hasattr(s, '_b'): s._b = Brain(s.e)
        return s._b
    def _cursor(s, cur, tgt):
        """Deplace un curseur 2x2 de cur vers tgt (touches pressees une par une)."""
        cx, cy = KEYSEQ[cur]; tx, ty = KEYSEQ[tgt]
        if tx != cx: s.press('RIGHT' if tx > cx else 'LEFT', 4, 14)
        if ty != cy: s.press('DOWN' if ty > cy else 'UP', 4, 14)
    def ctl(s):
        return s.e.u32(sym('gBattlerControllerFuncs')) & ~1
    def cb2(s):
        return s.e.u32(0x030031f0 + 4) & ~1
    def hp_frac(s):
        b = s._brain().bm(0); return b['hp'] / max(b['maxhp'], 1)
    def battle_step(s):
        """Un pas de decision en combat : menu d'actions -> FIGHT/POKEMON ; menu d'attaques -> meilleure attaque ; menu equipe -> remplacant ; sinon A."""
        b = s._brain(); cb2 = s.cb2()
        k = (cb2, s.ctl())
        if k != getattr(s, '_lastk', None):
            s._lastk = k; print('   [bat] cb2=%x ctl=%x hp=%s/%s foe=%s/%s' % (k[0], k[1], b.bm(0)['hp'], b.bm(0)['maxhp'], b.bm(1)['hp'], b.bm(1)['maxhp']), flush=True)
        party_cb = sym('CB2_UpdatePartyMenu') & ~1
        if cb2 == party_cb: return s.party_step()
        if cb2 != (sym('BattleMainCB2') & ~1):      # sac, resume, etc. : on ressort
            s.press('B', 4, 30); return
        f = s.ctl()
        if f == (sym('HandleInputChooseAction') if False else 0x080308d8 & ~1):
            u = b.bm(0)
            sw = None
            if u['hp'] * 100 < u['maxhp'] * 30 and not s.is_last_alive():
                sw = b.best_switch(avoid=(s.active_slot(),))
            if sw is not None and not getattr(s, '_noswitch', False):
                s._want = sw; tgt = 2
            else:
                tgt = 0
            cur = s.e.peek(sym('gActionSelectionCursor'), 1)[0]
            if cur != tgt: s._cursor(cur, tgt)
            s.press('A', 4, 40); return
        if f == (sym('HandleInputChooseMove') & ~1):
            i = b.pick_move()
            cur = s.e.peek(sym('gMoveSelectionCursor'), 1)[0]
            if cur != i: s._cursor(cur, i)
            s.press('A', 4, 40); return
        s.press('A', 4, 30)
    def active_slot(s):
        return s.e.peek(sym('gBattlerPartyIndexes'), 1)[0]
    def is_last_alive(s):
        return sum(1 for p in s._brain().party() if p['hp'] > 0) <= 1
    def party_step(s):
        b = s._brain(); want = getattr(s, '_want', None); s._want = None
        if want is None:
            want = b.best_switch(avoid=(s.active_slot(),))
            if want is None:
                want = next((p['i'] for p in b.party() if p['hp'] > 0), 0)
        for _ in range(14):
            cur = s.e.peek(sym('gPartyMenu') + 9, 1)[0]
            if cur >= 128: cur -= 256
            if cur == want: break
            s.press('DOWN', 4, 14)
        s.press('A', 4, 40); s.press('A', 4, 60)
