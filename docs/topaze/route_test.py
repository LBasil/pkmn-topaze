# TEST EMULATEUR (mGBA, ROM de debug a gTopazeDbg) : marche le long d'un chemin calcule d'apres la collision de la carte, essaie de traverser chaque obstacle voisin du chemin, verifie les warps.
# Usage : python3 docs/topaze/route_test.py <ROM> <Carte> <x_depart> <y_depart> <x_but> <y_but> [<x_but2> <y_but2> ...]   (le dernier but doit etre une case de warp)
# Banc : /tmp/gx/harness (C, libmgba) + /tmp/gx/drive.py ; ROM de debug : voir docs/technique/EMULATEUR.md
import sys, json, struct, re, os, collections
sys.path.insert(0, '/tmp/gx'); sys.path.insert(0, 'tools/topaze/emu'); sys.path.insert(0, 'tools/topaze/maps')
from drive import *
import mapkit
ROOT = '.'
WATER = (0x10, 0x11, 0x12, 0x13, 0x15, 0x1b)
SURF = False     # vrai : l'eau est praticable (le joueur a la CS3 et l'insigne) ; utilise par l'autopilote tools/topaze/emu/bench/run_full.py
def mapid(name):
    for l in open('include/constants/map_groups.h'):
        m = re.match(r'#define MAP_%s\s+\((\d+)\s*\|\s*\((\d+)\s*<<\s*8\)' % name, l)
        if m: return int(m.group(2)), int(m.group(1))
    raise KeyError(name)
def snake_const(n): return re.sub(r'(?<!^)(?=[A-Z0-9])', '_', n).upper().replace('_1_F', '_1F').replace('_2_F', '_2F')
NOWALK = ()     # comportements de case jamais franchissables (ex. (19,) = cascade sans CS07)
CURRENT_STOPPED = False
class Nav:
    def __init__(self, name):
        self.name = name; self.mj = json.load(open('data/maps/%s/map.json' % name)); lid = self.mj['layout']
        if CURRENT_STOPPED and name in ('SeafoamIslands_B3F', 'SeafoamIslands_B4F'): lid += '_CURRENT_STOPPED'      # disposition apres arret du courant de lave (vanille : setmaplayoutindex)
        L = mapkit.layouts()[lid]
        self.w, self.h = L['width'], L['height']; self.g = struct.unpack('<%dH' % (self.w * self.h), open(L['blockdata_filepath'], 'rb').read())
        rd = lambda ts: struct.unpack('<%dI' % (os.path.getsize(mapkit.ts_dir(ts) + '/metatile_attributes.bin') // 4), open(mapkit.ts_dir(ts) + '/metatile_attributes.bin', 'rb').read())
        self.pa, self.sa = rd(L['primary_tileset']), rd(L['secondary_tileset'])
        self.warps = {(w['x'], w['y']): w for w in self.mj['warp_events']}
        self.objs = {(o['x'], o['y']) for o in self.mj['object_events']}
    def attr(self, x, y): m = self.g[y * self.w + x] & 0x3ff; return self.pa[m] if m < 640 else self.sa[m - 640]
    def blocked(self, x, y):
        if not (0 <= x < self.w and 0 <= y < self.h): return True
        return (x, y) in self.objs or bool((self.g[y * self.w + x] >> 10) & 3) or (not SURF and (self.attr(x, y) & 0x1ff) in WATER) or (self.attr(x, y) & 0x1ff) in NOWALK
    def step_ok(self, c, n):
        """Regle d'altitude du moteur : on ne passe pas d'un niveau a un autre (sauf 0 et 15, qui relient tout)."""
        ea = self.g[c[1] * self.w + c[0]] >> 12; eb = self.g[n[1] * self.w + n[0]] >> 12
        wc = (self.attr(*c) & 0x1ff) in WATER; wn = (self.attr(*n) & 0x1ff) in WATER
        if SURF and wn: return wc or ea == 3      # navigation sur l'eau ; embarquement (terre -> eau) : IsPlayerFacingSurfableFishableWater exige que le joueur soit a l'altitude 3 (comme CanStopSurfing)
        # debarquement (eau -> terre) : CanStopSurfing du moteur = altitude 3 exactement ; sinon collision normale (ex. volcan Ecume B4F : lac a 1, terre a 4 = pas de sortie)
        if SURF and wc and eb == 3: return True
        return ea in (0, 15) or eb in (0, 15) or ea == eb
    def path(self, a, b):
        prev = {a: None}; q = collections.deque([a])
        while q:
            c = q.popleft()
            if c == b: break
            for d, (dx, dy) in (('UP', (0, -1)), ('DOWN', (0, 1)), ('LEFT', (-1, 0)), ('RIGHT', (1, 0))):
                n = (c[0] + dx, c[1] + dy)
                if n in prev or self.blocked(*n) or (n in self.warps and n != b) or not self.step_ok(c, n): continue
                prev[n] = (c, d); q.append(n)
        if b not in prev: return None
        out = []; c = b
        while prev[c]: c, d = prev[c][0], prev[c][1]; out.append(d); 
        # recalcul propre des directions
        cells = []; c = b
        while c: cells.append(c); c = prev[c][0] if prev[c] else None
        cells.reverse(); return cells
DIR = {(0, -1): 'UP', (0, 1): 'DOWN', (-1, 0): 'LEFT', (1, 0): 'RIGHT'}
def walk(e, nav, cells, shots, label):
    bad = []; n = 0
    for i, (c, d) in enumerate(zip(cells, cells[1:])):
        dd = DIR[(d[0] - c[0], d[1] - c[1])]
        # sondes : chaque voisin bloque (hors warp) ne doit pas se laisser traverser
        for (dx, dy), pd in DIR.items():
            nb = (c[0] + dx, c[1] + dy)
            if nb == d or nb in nav.warps or not (0 <= nb[0] < nav.w and 0 <= nb[1] < nav.h) or not nav.blocked(*nb): continue
            p0 = e.pos(); e.run(22, KEYS[pd]); e.run(10, 0); p1 = e.pos(); n += 1
            if p1 != p0: bad.append(('traverse', c, nb, p0, p1)); return bad, n   # le joueur a bouge : on arrete (position perdue)
        p = step(e, dd)
        if i == 0 and p is not None and (p[2], p[3]) == c: p = step(e, dd)      # 1er pas : le joueur doit d'abord se tourner
        if i % 14 == 0: shots.append((e.pos(), e))
        if p is None or p[:2] != e.pos()[:2]: break
        if (p[2], p[3]) != d and e.pos()[:2] == p[:2] and p[:2] == mapid(nav.mj['id'][4:]): bad.append(('pas', c, d, p)); return bad, n
    return bad, n
if __name__ == '__main__':
    rom, name, sx, sy = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); goals = [int(v) for v in sys.argv[5:]]
    e = Emu(rom); a = 0x03007480
    e.cmd('pin %x 1' % (a + 5 * 0))
    nav = Nav(name); g, nn = mapid(nav.mj['id'][4:])
    for i, v in enumerate((1, g, nn, sx, sy, 1)): e.cmd('pin %x %x' % (a + i, v))
    for i in range(700):
        e.run(15, KEYS['A'] if (i // 2) % 2 == 0 else KEYS['START'])
        p = e.pos()
        if p and p[:2] == (g, nn): break
    e.cmd('pin %x 0' % a); e.cmd('pin %x 0' % (a + 1)); e.run(90, 0)       # plus de warp force ; on garde dbg[5] = 1 (pas de combats)
    print('depart', e.pos()); shots = []; os.makedirs('/tmp/gx/rt', exist_ok=True); k = 0
    for gi in range(0, len(goals), 2):
        goal = (goals[gi], goals[gi + 1]); p = e.pos(); cells = nav.path((p[2], p[3]), goal)
        if not cells: print('PAS DE CHEMIN', p, goal); break
        bad, n = walk(e, nav, cells, shots, name); print('trajet', p[2:], '->', goal, len(cells) - 1, 'pas,', n, 'sondes ; anomalies :', bad or 'aucune')
        e.run(90, 0); print('arrivee', e.pos())
        for (pp, _) in shots: pass
        e.shot('/tmp/gx/rt/%s_%d.png' % (name, gi // 2))
        if e.pos()[:2] != (g, nn): break
