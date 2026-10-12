#!/usr/bin/env python3
"""Centrale electrique de Chrondrolia v2 : 4 etages (cartes PokemonMansion_1F/2F/3F/B1F reutilisees) construits avec le
tileset PowerPlant (machines, turbines, barils, consoles) a partir de pochoirs de la carte PowerPlant d'origine.
Squelette de rangees + decor aleatoire (graine fixe) verifie par connexite (aucune poche close)."""
import sys, random
sys.path.insert(0, 'tools/topaze/maps')
from mapkit import Layout
PP = Layout('LAYOUT_POWER_PLANT')
FLOOR = PP.get(5, 5)
RUB = PP.get(5, 3)
STAMPS = {'B9': (1, 1, 9, 3), 'B9b': (11, 1, 9, 3), 'B12': (21, 1, 12, 3), 'B14': (34, 1, 14, 3),
          'L24': (20, 19, 25, 3), 'L25': (20, 28, 26, 3), 'DOME': (7, 8, 3, 4), 'TURB': (27, 34, 5, 5),
          'BAR': (24, 21, 17, 4), 'BAR9': (24, 21, 9, 4), 'CONS': (26, 13, 5, 4), 'ENTRY': (3, 37, 5, 3), 'CAB': (21, 14, 2, 3)}
class Map:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.g = [[FLOOR] * w for _ in range(h)]
        self.used = [[False] * w for _ in range(h)]
        for x in range(w):
            self.g[0][x] = PP.get(5, 0)
            for y in (1, 2): self.g[y][x] = PP.get(5, 0)
            self.g[h - 1][x] = PP.get(12, 39)
        for y in range(3, h - 1): self.g[y][0] = PP.get(0, 20); self.g[y][w - 1] = PP.get(48, 20)
        for x in range(w):
            for y in (0, 1, 2, h - 1): self.used[y][x] = True
        for y in range(h): self.used[y][0] = self.used[y][w - 1] = True
        self.pads = []
    def stamp(self, name, x, y):
        sx, sy, w, h = STAMPS[name]
        for j in range(h):
            for i in range(w): self.g[y + j][x + i] = PP.get(sx + i, sy + j); self.used[y + j][x + i] = True
    def fits(self, name, x, y, margin=1):
        w, h = STAMPS[name][2:]
        if x - margin < 1 or y - margin < 3 or x + w + margin > self.w - 1 or y + h + margin > self.h - 1: return False
        return not any(self.used[j][i] for j in range(y - margin, y + h + margin) for i in range(x - margin, x + w + margin))
    def pad(self, x, y):
        self.g[y][x] = PP.get(3, 37); self.used[y][x] = True       # plaque d'acces 1x1 (une seule case de warp)
        self.pads.append((x, y))
    def rub(self, x, y): self.g[y][x] = RUB; self.used[y][x] = True
    def row(self, y, *items):
        x = 1
        for it in items:
            if isinstance(it, int): x += it
            else:
                if x + STAMPS[it][2] > self.w - 1: print('  (rangee y=%d : %s ignore)' % (y, it)); break
                self.stamp(it, x, y); x += STAMPS[it][2]
    def blocked(self, x, y): return bool(self.g[y][x] & 0xc00)
    def reach(self, sx, sy):
        seen = {(sx, sy)}; q = [(sx, sy)]
        while q:
            x, y = q.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = x + dx, y + dy
                if 0 <= a < self.w and 0 <= b < self.h and (a, b) not in seen and not self.blocked(a, b): seen.add((a, b)); q.append((a, b))
        return seen
    def decorate(self, rnd, n=900):
        kinds = ['CAB', 'CAB', 'CAB', 'DOME', 'CONS', 'TURB']
        for _ in range(n):
            k = rnd.choice(kinds); w, h = STAMPS[k][2:]
            x, y = rnd.randint(1, self.w - w - 1), rnd.randint(3, self.h - h - 1)
            if self.fits(k, x, y, 1):
                bak = [r[:] for r in self.g], [r[:] for r in self.used]
                self.stamp(k, x, y)
                free = [(i, j) for j in range(3, self.h - 1) for i in range(1, self.w - 1) if not self.blocked(i, j)]
                if len(self.reach(*free[0])) != len(free): self.g, self.used = bak
        for _ in range(60):
            x, y = rnd.randint(2, self.w - 3), rnd.randint(4, self.h - 3)
            if not any(self.used[y + j][x + i] for j in (-1, 0, 1) for i in (-1, 0, 1)): self.rub(x, y)
WALK = PP.get(1, 13)                       # passerelle (bande grise)
def walk(m, y, x0, x1):
    for x in range(x0, x1 + 1): m.g[y][x] = WALK
def top_wall(m, *items):
    """mur du haut : bancs poses des la rangee 1"""
    m.row(1, *items)
def door(m, x):
    m.stamp('ENTRY', x, m.h - 3)
def f1():                                   # HALLE DES TURBINES (carte principale), 34x26
    m = Map(34, 26); top_wall(m, 'B9', 1, 'B9b', 1, 'B12')
    door(m, 3); door(m, 14); door(m, 26)    # portes : transformateurs / sortie / salle de commande
    for x in (1, 8, 15, 22): m.stamp('TURB', x, 5)
    m.stamp('CONS', 28, 5); m.stamp('CAB', 29, 10)
    for y in (11, 12): walk(m, y, 1, 32)
    m.stamp('BAR', 1, 14); m.stamp('BAR9', 19, 14); m.stamp('DOME', 30, 14)
    m.stamp('BAR9', 1, 19); m.stamp('CAB', 11, 19); m.stamp('CAB', 20, 19)
    m.pad(27, 20)
    return m
def f2():                                   # SALLE DE COMMANDE, 22x14
    m = Map(22, 14); top_wall(m, 'B9', 1, 'B9b')
    door(m, 9)
    m.stamp('CONS', 2, 5); m.stamp('CONS', 8, 5); m.stamp('CONS', 14, 5)
    m.stamp('CAB', 2, 9); m.stamp('CAB', 17, 9)
    return m
def f3():                                   # PARC DES TRANSFORMATEURS, 26x18
    m = Map(26, 18); top_wall(m, 'B12', 1, 'B9b')
    door(m, 10)
    m.stamp('BAR9', 1, 5); m.stamp('BAR9', 11, 5); m.stamp('CAB', 21, 5)
    m.stamp('BAR9', 1, 9); m.stamp('BAR9', 11, 9); m.stamp('CAB', 21, 9)
    m.stamp('DOME', 2, 13); m.stamp('DOME', 20, 13)
    return m
def f4():                                   # GALERIE TECHNIQUE (cle secrete), 28x20
    m = Map(28, 20); top_wall(m, 'B12', 1, 'B12')
    m.row(6, 'B14', 2, 'B9'); m.row(10, 3, 'B12', 2, 'B9'); m.row(14, 'B9', 2, 'B12')
    m.pad(23, 16)
    return m
FLOORS = {'1F': (f1, 1), '2F': (f2, 2), '3F': (f3, 3), 'B1F': (f4, 4)}
def build_all():
    out = {}
    for n, (f, seed) in FLOORS.items():
        m = f()
        pass
        out[n] = m
    return out
if __name__ == '__main__':
    for n, m in build_all().items():
        L = Layout('LAYOUT_POKEMON_MANSION_1F'); L.w, L.h = m.w, m.h; L.g = [v for r in m.g for v in r]
        L.prim = PP.prim; L.sec = PP.sec
        L.render().convert('RGB').save('/tmp/cp/c_%s.png' % n)
        free = [(i, j) for j in range(3, m.h - 1) for i in range(1, m.w - 1) if not m.blocked(i, j)]
        r = m.reach(*free[0]); print(n, 'libres', len(free), 'atteignables', len(r), 'pads', all((x, y) in r for x, y in m.pads))
