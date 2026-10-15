# Bibliothèque de test scénarisé (mGBA headless + ROM de debug dbg2.gba : équipe forte, pas de combats auto)
import sys, os, re, struct, json
sys.path[:0] = ['/tmp/gx', '/home/claude/pkmn-topaze/docs/topaze', '/home/claude/pkmn-topaze/tools/topaze/maps']
os.chdir('/home/claude/pkmn-topaze')
from drive import Emu, KEYS, step
import route_test as R

FLB, VRB, SB = 0xEE0, 0x1000, 0x03005048
def _sym(name, elf='/tmp/gx/dbg2.elf'):
    import subprocess
    for l in subprocess.run(['arm-none-eabi-nm', elf], capture_output=True, text=True).stdout.splitlines():
        a = l.split()
        if len(a) == 3 and a[2] == name: return int(a[0], 16)
_BMD = _sym('gBackupMapData') or 0x02031e00
_CB2 = (_sym('CB2_Overworld') or 0x08057094) | 1   # lu dans dbg2.elf : l'adresse change a chaque build
_BTF = _sym('gBattleTypeFlags')
_PAV = _sym('gPlayerAvatar')
_defs = {}
def _load(path):
    for l in open(path):
        m = re.match(r'#define\s+(\w+)\s+(.+?)\s*(//.*)?$', l.rstrip())
        if m: _defs[m.group(1)] = m.group(2).strip()
for f in ('flags', 'vars', 'opponents', 'items', 'species', 'moves'): _load('include/constants/%s.h' % f)
def val(x):
    if isinstance(x, int): return x
    if x not in _defs and re.fullmatch(r'[A-Za-z_]\w*', x): raise KeyError(x)
    x = _defs.get(x, x).strip()
    if re.fullmatch(r'0x[0-9a-fA-F]+|\d+', x): return int(x, 0)
    ex = re.sub(r'(?<![\w])[A-Za-z_]\w*', lambda m: str(val(m.group(0))), x)
    if re.search(r'(?<![\w])[A-Za-z_]', ex): raise KeyError(x)
    return eval(ex, {'__builtins__': {}})

def mid(name):
    k = name.replace('_', '').lower()
    for l in open('include/constants/map_groups.h'):
        m = re.match(r'#define MAP_(\w+)\s+\((\d+)\s*\|\s*\((\d+)\s*<<\s*8\)', l)
        if m and m.group(1).replace('_', '').lower() == k: return int(m.group(3)), int(m.group(2))
    raise KeyError(name)

class T:
    def __init__(s, mapname, x, y, rom='/tmp/gx/dbg2.gba', party=True, nocombat=True, pre=(), prevars=None, badges=0, god=True):
        s.e = Emu(rom); s.mapname = mapname; g, n = mid(mapname)
        a = 0x03007520; e = s.e
        for i, v in enumerate((1, g, n, x, y, 1 if nocombat else 0, 0, 9 if party else 0)): e.cmd('pin %x %x' % (a + i, v))
        e.run(60, 0)
        e.cmd('poke8 %x %x' % (0x03007528, 1 if god else 0))
        fl = list(pre) + ['FLAG_BADGE%02d_GET' % i for i in range(1, badges + 1)]
        assert len(fl) <= 24 and len(prevars or {}) <= 8
        for i, f in enumerate(fl):
            k = val(f)
            e.cmd('poke8 %x %x' % (0x030074f0 + 2 * i, k & 255)); e.cmd('poke8 %x %x' % (0x030074f0 + 2 * i + 1, k >> 8))
        for i, (vn, vv) in enumerate((prevars or {}).items()):
            k = val(vn)
            for j, w in enumerate((k, vv)):
                e.cmd('poke8 %x %x' % (0x030074d0 + 4 * i + 2 * j, w & 255)); e.cmd('poke8 %x %x' % (0x030074d0 + 4 * i + 2 * j + 1, w >> 8))
        for i in range(900):
            e.run(15, KEYS['A'] if (i // 2) % 2 == 0 else KEYS['START'])
            p = e.pos()
            if p and p[:2] == (g, n): break
        e.cmd('unpin')
        if nocombat: e.cmd('pin %x 1' % (a + 5))
        e.run(90, 0)
        sb2 = e.u32(0x0300504c); b = e.peek(sb2 + 0x15, 1)[0]; e.cmd('poke8 %x %x' % (sb2 + 0x15, b | 6))   # style SET + animations off
        s.shots = []
    # --- état du jeu
    def sb(s): return s.e.u32(SB)
    def flag(s, f, on=True):
        n = val(f); a = s.sb() + FLB + n // 8; b = s.e.peek(a, 1)[0]
        s.e.cmd('poke8 %x %x' % (a, (b | (1 << (n % 8))) if on else (b & ~(1 << (n % 8)))))
    def flags(s, *fs):
        for f in fs: s.flag(f)
    def getflag(s, f):
        n = val(f); return bool(s.e.peek(s.sb() + FLB + n // 8, 1)[0] >> (n % 8) & 1)
    def var(s, v, x):
        a = s.sb() + VRB + 2 * (val(v) - 0x4000)
        s.e.cmd('poke8 %x %x' % (a, x & 255)); s.e.cmd('poke8 %x %x' % (a + 1, x >> 8))
    def getvar(s, v):
        a = s.sb() + VRB + 2 * (val(v) - 0x4000); return struct.unpack('<H', s.e.peek(a, 2))[0]
    def badges(s, n):
        for i in range(1, n + 1): s.flag('FLAG_BADGE%02d_GET' % i)
    # --- observation
    def pos(s): return s.e.pos()
    def where(s):
        p = s.pos(); return p
    def shot(s, name):
        os.makedirs('/tmp/gx/out', exist_ok=True); f = '/tmp/gx/out/%s.png' % name; s.e.shot(f); return f
    # --- actions
    def press(s, k, n=4, wait=20): s.e.run(n, KEYS[k]); s.e.run(wait, 0)
    def hold(s, k, n): s.e.run(n, KEYS[k]); s.e.run(10, 0)
    def mash(s, n=30, name=None, every=6, gap=40):
        """A en rafale (dialogues). Retourne la liste des captures prises."""
        out = []
        for i in range(n):
            s.press('A', 4, gap)
            if name and i % every == every - 1: out.append(s.shot('%s_%02d' % (name, i // every)))
        return out
    def live_grid(s, nav):
        """Remplace la grille statique de `nav` par la carte VIVANTE (RAM) : portes/barrieres ouvertes par des scripts, etc."""
        import struct as _st
        stride = nav.w + 15; g = []
        for y in range(nav.h):
            row = s.e.peek(_BMD + ((y + 7) * stride + 7) * 2, nav.w * 2)
            g.extend(_st.unpack('<%dH' % nav.w, row))
        if all((v & 0x3ff) < 640 + len(nav.sa) for v in g): nav.g = tuple(g)   # sinon (carte en cours de chargement) : grille statique
        return nav
    def live_objs(s):
        b = s.e.peek(0x02036e3c, 0x24 * 16); out = set()
        for i in range(16):
            o = b[i * 0x24:(i + 1) * 0x24]
            if o[0] & 1 and not (o[2] & 1) and not (o[1] >> 5) & 1:   # actif, pas le joueur, visible
                x, y = struct.unpack_from('<hh', o, 0x10); out.add((x - 7, y - 7))
        return out
    def plan_objs(s):
        """Objets pris en compte par le planificateur (par defaut : les objets vivants)."""
        return s.live_objs()
    def settle(s):
        last = None
        for _ in range(40):
            s.e.run(8, 0); p = s.pos()
            if p == last: return p
            last = p
        return last
    def surfing(s): return bool(_PAV and s.e.peek(_PAV, 1)[0] & 0x08)      # PLAYER_AVATAR_FLAG_SURFING
    def embark(s, nav, cur, d):
        """Si le pas `d` entre dans l'eau depuis la terre : lance SURF (face a l'eau, A, OUI). True si on est maintenant sur l'eau."""
        dx, dy = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}[d]; n = (cur[0] + dx, cur[1] + dy)
        if s.surfing() or (nav.attr(*n) & 0x1ff) not in R.WATER or (nav.attr(*cur) & 0x1ff) in R.WATER: return False
        s.e.run(2, KEYS[d]); s.e.run(10, 0)
        for _ in range(10):      # A jusqu'a la question (texte lent), puis A = OUI
            s.press('A', 4, 50)
            if s.surfing(): break
        for _ in range(8):
            if s.surfing() and s.idle(): break
            s.e.run(30, 0)
        s.e.run(20, 0); return s.surfing()
    def walk_to(s, goal, name=None, tries=200):
        """Marche vers goal (BFS qui connait les cases-flèches, objets lus en direct) ; True / False / 'warped'."""
        from spin import spin_bfs
        nav = R.Nav(name or s.sync()); s.live_grid(nav); stuck = 0
        for _ in range(tries):
            nav.objs = s.plan_objs()
            p = s.pos(); cur = (p[2], p[3])
            if cur == goal: return True
            dirs = spin_bfs(nav, cur, goal)
            if not dirs: s.why = ('nopath', cur, sorted(nav.objs)); return False
            if R.SURF and s.embark(nav, cur, dirs[0]): continue
            q = step(s.e, dirs[0])
            if q is None or q[:2] != p[:2]: return 'warped'
            q = s.settle()
            if q[:2] != p[:2]: return 'warped'
            if (q[2], q[3]) == cur:
                stuck += 1
                if stuck >= 3: s.why = ('stuck', cur, dirs[:3]); return False
            else: stuck = 0
        p = s.pos(); return (p[2], p[3]) == goal
    def face(s, d):
        s.e.run(2, KEYS[d]); s.e.run(8, 0)
    def talk(s, d, n=12, name=None):
        s.face(d); return s.mash(n, name)
    def battle_win(s, maxn=60):
        """Rafale de A pour enchaîner combat (1re attaque) jusqu'à la fin ; renvoie le nb d'itérations."""
        for i in range(maxn): s.press('A', 4, 45)
        return maxn

    def until(s, cond, maxn=500, name=None, every=25, gap=30):
        """Appuie sur A jusqu'à cond() vrai ; renvoie (ok, nb_iterations)."""
        for i in range(maxn):
            s.press('A', 4, gap)
            if name and i % every == every - 1: s.shot('%s_%03d' % (name, i))
            if cond(): return True, i
        return False, maxn

    def take_warp(s, dest, nth=0, nudge=('UP', 'RIGHT', 'LEFT', 'DOWN')):
        """Marche jusqu'à un warp menant à `dest` et le franchit (pousse vers le bord si la case ne se déclenche pas seule)."""
        nav = R.Nav(s.mapname)
        key = dest.replace('_', '').lower()
        ws = [w for w in nav.mj['warp_events'] if w['dest_map'].replace('MAP_', '').replace('_', '').lower() == key]
        w = ws[nth]; goal = (w['x'], w['y']); p0 = s.pos()
        r = s.walk_to(goal)
        if r == 'warped' or s.pos()[:2] != p0[:2]: s.e.run(70, 0); s.mapname = dest; return True
        for d in nudge:
            s.e.run(14, KEYS[d]); s.e.run(70, 0)
            if s.pos()[:2] != p0[:2]: s.mapname = dest; return True
        return False

    def inbattle(s): return bool(s.e.peek(0x03003130 + 0x439, 1)[0] & 3)      # bit1 = gMain.inBattle (bit0 = oamLoadDisabled)
    def idle(s):
        e = s.e
        return e.u32(0x03003130 + 4) == _CB2 and not (e.peek(0x03003130 + 0x439, 1)[0] & 3) and e.peek(0x03000f9c, 1)[0] == 0
    def scene(s, maxn=600, key='A', shot=None):
        """Fait avancer une scène/un combat (A en combat, `key` sinon) jusqu'à ce que le jeu soit redevenu libre ; renvoie le nb d'appuis."""
        n = 0; calm = 0
        while n < maxn:
            if s.idle():
                calm += 1
                if calm >= 3: return n
                s.e.run(20, 0); continue
            calm = 0
            if s.inbattle() and _BTF and s.e.u32(_BTF) & 0x80:      # combat du Parc Safari (BALL/APPAT/CAILLOU/FUITE) : on fuit
                s.press('DOWN', 4, 10); s.press('RIGHT', 4, 10); s.press('A', 4, 30); n += 1; continue
            if s.inbattle() and n % 60 == 59:       # attaque « entravee » (Entrave) ou menu bloque : on change de capacite (B, FIGHT, droite, A)
                mv = ('RIGHT', 'DOWN', 'LEFT', 'UP')[(n // 60) % 4]
                for k in ('B', 'B', 'B', 'UP', 'LEFT', 'A', mv, 'A'): s.press(k, 4, 40)      # retour au menu d'actions (curseur sur COMBAT), puis autre capacite
            if s.inbattle() and hasattr(s, 'heal_battle'): s.heal_battle()
            s.press('A' if s.inbattle() else key, 4, 30); n += 1
            if shot and n % 25 == 0: s.shot('%s_%03d' % (shot, n))
            if n == 150 and hasattr(s, 'save'): s.save('scenelong_%s' % s.sync())      # scene anormalement longue : etat conserve pour diagnostic
        return n
    def finish_battle(s, maxn=400):
        """A en rafale tant qu'un combat est en cours, puis B pour fermer les textes de fin."""
        n = 0
        while s.inbattle() and n < maxn: s.press('A', 4, 40); n += 1
        for _ in range(6): s.press('B', 4, 25)
        return n
    def walk_fight(s, goal, rounds=14, name=None, abat=130):
        """Marche vers goal ; si interrompu (dresseur, scène), joue la scène jusqu'au retour du contrôle puis reprend."""
        for r in range(rounds):
            if hasattr(s, 'heal'): s.heal()
            if not s.idle(): s.scene(key='B' if False else 'A', shot=name)
            res = s.walk_to(goal)
            if res is True or res == 'warped': return res
            p0 = s.pos()
            s.e.run(30, 0)
            if not s.idle(): s.scene(shot=name)
            if name: s.shot('%s_wf%02d' % (name, r))
            if s.pos()[:2] != p0[:2]: return 'warped'
        return False

_REV = {}
def _build_rev():
    import json
    for l in open('include/constants/map_groups.h'):
        m = re.match(r'#define MAP_(\w+)\s+\((\d+)\s*\|\s*\((\d+)\s*<<\s*8\)', l)
        if m: _REV[(int(m.group(3)), int(m.group(2)))] = m.group(1)
_build_rev()
_NAMES = {}
def _build_names():
    import glob, os
    for d in glob.glob('data/maps/*/'):
        n = os.path.basename(d.rstrip('/')); _NAMES[n.replace('_', '').lower()] = n
_build_names()
def mapname_of(g, n):
    return _NAMES[_REV[(g, n)].replace('_', '').lower()]

def _sync(s):
    p = s.pos(); s.mapname = mapname_of(p[0], p[1]); return s.mapname
T.sync = _sync

def _chain(s, steps, rounds=14, name=None):
    """steps : liste de (x, y) à atteindre dans la carte courante ; un pas peut être ('warp', 'Dest') pour franchir le warp vers Dest.
    Passe combats/textes. Renvoie la liste (carte, pos) après chaque pas."""
    out = []
    for st in steps:
        s.sync()
        if st[0] == 'warp':
            nav = R.Nav(s.mapname); key = st[1].replace('_', '').lower()
            ws = [w for w in nav.mj['warp_events'] if w['dest_map'].replace('MAP_', '').replace('_', '').lower() == key]
            nths = [st[2]] if len(st) > 2 else list(range(len(ws)))
            for nth in nths:
                m0 = s.pos()[:2]
                r = s._warp_try(nav, ws[nth], rounds, name)
                if s.pos()[:2] != m0: break
            out.append((s.sync(), s.pos()[2:], r)); continue
        else:
            r = s.walk_fight(st, rounds, name)
        out.append((s.sync(), s.pos()[2:], r))
    return out
T.chain = _chain

def _combat(s, on):
    s.e.cmd('unpin'); s.e.cmd('pin %x %x' % (0x03007525, 0 if on else 1))
T.combat = _combat


def _warp_try(s, nav, w, rounds, name):
    goal = (w['x'], w['y']); p0 = s.pos()
    if nav.blocked(*goal):      # porte à collision : on vise la case voisine puis on pousse vers la porte
        for d, (dx, dy) in (('DOWN', (0, -1)), ('UP', (0, 1)), ('RIGHT', (-1, 0)), ('LEFT', (1, 0))):   # d = touche à presser depuis la case voisine
            a = (goal[0] + dx, goal[1] + dy)
            if not nav.blocked(*a) and nav.path((s.pos()[2], s.pos()[3]), a):
                r = s.walk_fight(a, rounds, name)
                s.e.run(20, KEYS[d]); s.e.run(70, 0)
                break
        else: r = s.walk_fight(goal, rounds, name)
    else: r = s.walk_fight(goal, rounds, name)
    if s.pos()[:2] == p0[:2]:
        b = nav.attr(*goal) & 0x1ff
        order = {0x6c: ('RIGHT',), 0x6d: ('LEFT',), 0x6e: ('RIGHT',), 0x6f: ('LEFT',),
                 0x62: ('RIGHT',), 0x63: ('LEFT',), 0x64: ('UP',), 0x65: ('DOWN',)}.get(b, ())
        if goal[1] == nav.h - 1: order += ('DOWN',)
        if goal[1] == 0: order += ('UP',)
        if goal[0] == 0: order += ('LEFT',)
        if goal[0] == nav.w - 1: order += ('RIGHT',)
        order += ('DOWN', 'UP', 'LEFT', 'RIGHT')
        for d in order:
            if s.pos()[:2] != p0[:2]: break
            s.e.run(14, KEYS[d]); s.e.run(70, 0)
            if s.pos()[:2] != p0[:2]: break
            if (s.pos()[2], s.pos()[3]) != goal: s.walk_to(goal)   # la touche nous a decale : on revient sur la case de warp
    s.e.run(40, 0)

    return r
T._warp_try = _warp_try
