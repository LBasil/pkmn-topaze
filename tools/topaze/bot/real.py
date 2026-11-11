#!/usr/bin/env python3
"""Cerveau de combat du pilote « joueur reel » (sans mode dieu) : lecture de l'etat en RAM, choix d'attaque par types, changement de Pokemon.

Tout est lu dans la ROM / la RAM de /tmp/gx/dbg2.elf (adresses via nm, jamais en dur)."""
import struct, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ELF = '/tmp/gx/dbg2.elf'
_S = {}
def sym(name):
    if not _S:
        for l in subprocess.run(['arm-none-eabi-nm', ELF], capture_output=True, text=True).stdout.splitlines():
            a = l.split()
            if len(a) == 3: _S.setdefault(a[2], int(a[0], 16))
    return _S[name]

_SORTED = []
def name_of(addr):
    import bisect
    if not _SORTED:
        for l in subprocess.run(['arm-none-eabi-nm', '-n', ELF], capture_output=True, text=True).stdout.splitlines():
            a = l.split()
            if len(a) == 3 and a[1] in 'tT': _SORTED.append((int(a[0], 16), a[2]))
    i = bisect.bisect_right(_SORTED, (addr & ~1, '\xff')) - 1
    return _SORTED[i][1] if i >= 0 else hex(addr)

# types (FireRed) : NORMAL 0 FIGHTING 1 FLYING 2 POISON 3 GROUND 4 ROCK 5 BUG 6 GHOST 7 STEEL 8 MYSTERY 9 FIRE 10 WATER 11 GRASS 12 ELECTRIC 13 PSYCHIC 14 ICE 15 DRAGON 16 DARK 17
ORDERS = ['GAEM', 'GAME', 'GEAM', 'GEMA', 'GMAE', 'GMEA', 'AGEM', 'AGME', 'AEGM', 'AEMG', 'AMGE', 'AMEG', 'EGAM', 'EGMA', 'EAGM', 'EAMG', 'EMGA', 'EMAG', 'MGAE', 'MGEA', 'MAGE', 'MAEG', 'MEGA', 'MEAG']
# attaques a ne jamais choisir automatiquement (auto-KO, charge sans benefice, effets sans interet)
BAD_EFFECTS = {7: 'dream eater', 8: 'mirror move', 36: 'razor wind', 38: 'selfdestruct', 39: 'skull bash', 75: 'solarbeam', 76: 'sky attack'}


class Brain:
    def __init__(s, emu):
        s.e = emu
        s.mv = emu.peek(sym('gBattleMoves'), 12 * 620)      # table des attaques (ROM)
        s.te = []                                            # table des types
        b = emu.peek(sym('gTypeEffectiveness'), 3 * 120); i = 0
        while i + 2 < len(b) and b[i] != 0xFF:
            if b[i] != 0xFE: s.te.append((b[i], b[i + 1], b[i + 2]))
            i += 3
        s.tab = {(a, d): m for a, d, m in s.te}

    # ---- lecture
    def move(s, mid):
        o = s.mv[mid * 12:(mid + 1) * 12]
        if len(o) < 12: o = bytes(12)
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
_TID = {}
def trainer_id(n):
    """Numero de dresseur -> constante TRAINER_xxx (include/constants/opponents.h)."""
    import re, os
    if not _TID:
        root = os.environ.get('TZ_ROOT', '/home/claude/pkmn-topaze')
        for m in re.finditer(r'#define (TRAINER_\w+)\s+(0x[0-9A-Fa-f]+|\d+)\s*$', open(root + '/include/constants/opponents.h').read(), re.M):
            _TID[int(m.group(2), 0)] = m.group(1)
    return _TID.get(n)

class BattleMixin:
    real = True
    def opponent(s):
        """Fiche de l'adversaire du combat en cours (None si sauvage) : equipe, niveaux, IA, double."""
        if not (s.e.u32(sym('gBattleTypeFlags')) & 8): return None
        import opponents
        n = s.e.peek(sym('gTrainerBattleOpponent_A'), 2); n = n[0] | n[1] << 8
        return opponents.db().get(trainer_id(n))
    def vet_opponent(s):
        """Premier tour d'un duel : compare l'equipe a la notre ; note les duels trop forts (s.too_strong) pour que l'entrainement vise plus haut."""
        import opponents
        o = s.opponent()
        if not o: return
        need = opponents.need_level(o); mine = max((q['level'] for q in s._brain().party() if q['hp'] > 0), default=0)
        s.last_opp = (o['name'], need, mine)
        if mine < need - 4:
            s.too_strong = max(getattr(s, 'too_strong', 0), need); print('   [opp] %s : niveau conseille %d, notre meilleur %d -> entrainement a prevoir' % (o['name'], need, mine), flush=True)
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
            s._lastk = k
            if getattr(s, 'dbg_save', False) and hasattr(s, 'save'): s.save('lastbat')
            print('   [bat] cb2=%s ctl=%s hp=%s/%s foe=%s/%s' % (name_of(k[0]), name_of(k[1]), b.bm(0)['hp'], b.bm(0)['maxhp'], b.bm(1)['hp'], b.bm(1)['maxhp']), flush=True)
        party_cb = sym('CB2_UpdatePartyMenu') & ~1
        if cb2 == party_cb: return s.party_step()
        if cb2 == (sym('CB2_NamingScreen') & ~1):      # surnom : START (curseur sur OK), A (nom par defaut)
            s.press('START', 4, 30); s.press('A', 4, 60); return
        nm = name_of(cb2)
        if 'Evolution' in nm:      # evolution : on laisse faire (B l'annulerait)
            s.e.run(20, 0); s.press('A', 4, 20) if False else None; return
        if 'SetUpPSS' in nm: s.e.run(20, 0); return      # chargement de l'ecran de resume : on attend (B l'annulerait en boucle)
        if 'Summary' in nm and s.cb2() != (sym('BattleMainCB2') & ~1):      # ecran de resume = choix de l'attaque a oublier : la moins puissante
            pm = b.party(); a = s.e.peek(s.e.u32(sym('gBattleStruct')) + 16, 1)[0]      # expGetterMonId : le Pokemon qui apprend (pas forcement celui au combat)
            if a < len(pm):
                HM = {15, 19, 57, 70, 127, 148, 249, 291}      # CS : le jeu refuse de les faire oublier (boucle infinie sur l'ecran de resume)
                pw = [((b.move(m)['power'] if m else -1) + (10000 if m in HM else 0), i) for i, m in enumerate(pm[a]['moves'])]
                weakest = min(pw)[1]
                s.e.run(90, 0)      # laisser l'ecran finir de s'afficher (touches ignorees sinon)
                for _ in range(weakest): s.press('DOWN', 4, 40)
                s.press('A', 4, 60); s.press('A', 4, 60); return
        if cb2 != (sym('BattleMainCB2') & ~1):      # sac, resume, etc.
            if getattr(s, '_act', None) == 'ball':      # sac de combat : pochette BALLS (3e), 1re balle, UTILISER
                s._act = None; s.e.run(30, 0)
                for _ in range(3): s.press('LEFT', 4, 14)
                for _ in range(2): s.press('RIGHT', 4, 24)
                s.press('A', 4, 40); s.press('A', 4, 60); return
            s.press('B', 4, 30); return
        f = s.ctl()
        if f == (sym('HandleInputChooseAction') if False else 0x080308d8 & ~1):
            u = b.bm(0)
            sw = None; s._pm_tries = 0
            if u['hp'] * 100 < u['maxhp'] * 30 and not s.is_last_alive():
                sw = b.best_switch(avoid=(s.active_slot(),))
            s._turns = getattr(s, '_turns', 0) + 1
            if s._turns == 1: s.vet_opponent()
            if s._turns == 1 and getattr(s, 'xp_swap', False) and not (s.e.u32(sym('gBattleTypeFlags')) & 8):
                pm = b.party(); top = max((q for q in pm if q['hp'] * 2 > q['maxhp'] and not q['egg']), key=lambda q: q['level'], default=None)
                if top and top['i'] != s.active_slot() and u['level'] + 3 <= top['level'] and sw is None: sw = top['i']
            if sw is not None and not getattr(s, '_noswitch', False):
                s._want = sw; tgt = 2
            elif s.want_catch():
                s._act = 'ball'; s._throws = getattr(s, '_throws', 0) + 1; tgt = 1
            else:
                tgt = 0
            cur = s.e.peek(sym('gActionSelectionCursor'), 1)[0]
            if cur != tgt: s._cursor(cur, tgt)
            s.press('A', 4, 40); return
        if f == (sym('HandleInputChooseMove') & ~1):
            i = b.pick_move()
            u0, f0 = b.bm(0), b.bm(1); sig = (f0['hp'], u0['hp'], tuple(u0['pp']))
            if sig == getattr(s, '_msig', None): s._mrep = getattr(s, '_mrep', 0) + 1
            else: s._msig = sig; s._mrep = 0; s._mtried = set()
            if s._mrep >= 2:      # meme situation, rien ne se passe : capacite entravee (Entrave...) -> on essaie une autre
                s._mtried.add(i)
                alt = [k for k in range(4) if u0['moves'][k] and u0['pp'][k] > 0 and k not in s._mtried]
                if alt: i = max(alt, key=lambda k: b.bm(0)['moves'][k] and (b.move(u0['moves'][k])['power'] or 0))
            if getattr(s, 'verbose', False):
                u, f = b.bm(0), b.bm(1)
                print('   TOUR nous %s n%d %d/%d | adv %s n%d %d/%d (types %d/%d) -> %s' % (u['species'], u['level'], u['hp'], u['maxhp'], f['species'], f['level'], f['hp'], f['maxhp'], f['type1'], f['type2'], u['moves'][i]), flush=True)
            cur = s.e.peek(sym('gMoveSelectionCursor'), 1)[0]
            if cur != i: s._cursor(cur, i)
            s.press('A', 4, 40); return
        s.press('A', 4, 30)
    def balls(s):
        sb = s.e.u32(0x03005108); sb2 = s.e.u32(0x0300510c); key = s.e.u32(sb2 + 0xF20) & 0xffff
        b = s.e.peek(sb + 0x430, 13 * 4); n = 0
        for i in range(13):
            it, q = struct.unpack_from('<HH', b, i * 4)
            if it: n += q ^ key
        return n
    def want_catch(s):
        """Combat sauvage, espece inconnue de l'equipe/boite, de la place et des balles : on lance une balle (5 tentatives max par combat)."""
        if not getattr(s, 'catch', True): return False
        f = s.e.u32(sym('gBattleTypeFlags'))
        if f & (8 | 0x80 | 0x1): return False      # dresseur, safari, double
        if getattr(s, '_throws', 0) >= 5: return False
        b = s._brain(); foe = b.bm(1); party = b.party()
        if len(party) >= 6 or s.balls() <= 0: return False
        only = getattr(s, 'catch_only', None)
        if only: return foe['species'] in only and not any(q['species'] in only for q in party)
        owned = getattr(s, 'owned', set())
        return foe['species'] not in owned
    def lead_swap(s, src):
        """Hors combat : echange le Pokemon de la case `src` avec la tete d'equipe (menu START > POKEMON > CHANGER)."""
        if src <= 0: return
        s.press('START', 4, 40)
        for _ in range(9):                        # le curseur du menu START est collant : on le place sur POKEMON (case 1)
            c = s.e.peek(0x02037428, 1)[0]
            if c == 1: break
            s.press('DOWN' if c < 1 else 'UP', 4, 14)
        s.press('A', 4, 90)
        def goto(n):
            for _ in range(10):
                cur = s.e.peek(sym('gPartyMenu') + 9, 1)[0]
                if cur >= 128: cur -= 256
                if cur == n: return
                s.press('DOWN' if cur < n else 'UP', 4, 14)
        goto(src); s.press('A', 4, 40); s.press('DOWN', 4, 14); s.press('A', 4, 60)
        goto(0); s.press('A', 4, 90)
        for _ in range(4): s.press('B', 4, 40)
    def active_slot(s):
        return s.e.peek(sym('gBattlerPartyIndexes'), 1)[0]
    def is_last_alive(s):
        return sum(1 for p in s._brain().party() if p['hp'] > 0) <= 1
    def party_step(s):
        b = s._brain(); want = getattr(s, '_want', None); s._want = None
        forced = b.bm(0)['hp'] <= 0
        s._pm_tries = getattr(s, '_pm_tries', 0) + 1
        if s._pm_tries > 5: forced = True      # B n'a rien change : le menu est obligatoire (U-turn et consorts) -> on choisit un remplacant
        if not forced and (getattr(s, '_noswitch', False) or s._pm_tries > 2):      # changement impossible (Piege, Ligotage...) : on renonce
            s._noswitch = True
            for _ in range(3): s.press('B', 4, 40)
            return
        if s._pm_tries >= 2 and forced: s.press('B', 4, 40)      # sous-menu ENVOYER/RESUME ouvert sur un Pokemon KO (inutilisable) : on le ferme avant de re-choisir
        if want is None:
            want = b.best_switch(avoid=(s.active_slot(),))
            if want is None:
                want = next((p['i'] for p in b.party() if p['hp'] > 0), 0)
        if s._pm_tries > 3:      # le choix precedent n'a rien donne (deja au combat, apte a rien...) : on essaie les autres Pokemon vivants un par un
            tried = getattr(s, '_slots_tried', set()); alive = [p['i'] for p in b.party() if p['hp'] > 0 and p['i'] not in tried]
            if not alive: tried = set(); alive = [p['i'] for p in b.party() if p['hp'] > 0]
            if alive: want = alive[0]; tried.add(want); s._slots_tried = tried
        for _ in range(14):
            cur = s.e.peek(sym('gPartyMenu') + 9, 1)[0]
            if cur >= 128: cur -= 256
            if cur == want: break
            s.press('DOWN', 4, 14)
        s.press('A', 4, 40); s.press('A', 4, 60)
