#!/usr/bin/env python3
"""Centrale electrique de Chrondrolia v2 : 4 etages (cartes PokemonMansion_1F/2F/3F/B1F reutilisees) construits
avec le tileset PowerPlant (machines, turbines, barils, consoles) a partir de pochoirs de la carte PowerPlant d'origine.
Etape 1 : geometrie + rendu.  Etape 2 (--events) : warps, objets, scripts."""
import sys, json, os
sys.path.insert(0, 'tools/topaze/maps')
from mapkit import Layout, ROOT
PP = Layout('LAYOUT_POWER_PLANT')
W, H = 49, 36
FLOOR = PP.get(5, 5)            # sol
DARK = PP.get(5, 0)             # bande sombre (hors jeu)
STAMPS = {'BENCH9a': (1, 1, 9, 3), 'BENCH9b': (11, 1, 9, 3), 'BENCH12': (21, 1, 12, 3), 'BENCH14': (34, 1, 14, 3),
          'LONG24': (20, 19, 25, 3), 'LONG25': (20, 28, 26, 3), 'DOME': (7, 8, 3, 4), 'TURB2': (27, 34, 5, 5),
          'BARRELS': (24, 21, 17, 4), 'CONS': (26, 13, 5, 4), 'ENTRY': (3, 37, 5, 3), 'ROW9a': (1, 14, 9, 3), 'ROW9b': (11, 14, 9, 3), 'CAB': (21, 14, 2, 3)}
class Map:
    def __init__(self):
        self.g = [[FLOOR] * W for _ in range(H)]
        for x in range(W):                                     # haut : 3 rangees de la carte d'origine, bas : sa derniere
            for y in range(3): self.g[y][x] = PP.get(x, y)
            self.g[H - 1][x] = PP.get(12, 39)
        for y in range(3, H - 1):
            self.g[y][0] = PP.get(0, 20); self.g[y][W - 1] = PP.get(48, 20)
        self.pads = []
    def stamp(self, name, x, y, h=None):
        sx, sy, w, hh = STAMPS[name]
        for j in range(h or hh):
            for i in range(w): self.g[y + j][x + i] = PP.get(sx + i, sy + j)
    def pad(self, x, y):                                        # plateforme elevatrice 2x2 (tuiles du tapis d'entree)
        for j in range(2):
            for i in range(2): self.g[y + j][x + i] = PP.get(3, 37)
        self.pads.append((x, y))
    def blocked(self, x, y): return bool(self.g[y][x] & 0xc00)
RUB = PP.get(5, 3)
def rub(m, *pts):
    for x, y in pts: m.g[y][x] = RUB
def row(m, y, *segs):
    for name, x in segs: m.stamp(name, x, y)
def floor1():
    m = Map()
    row(m, 8, ('BENCH9a', 1), ('BENCH9b', 11), ('BENCH12', 21), ('BENCH14', 34))      # gaps x10, x20, x33
    row(m, 14, ('ROW9a', 1), ('LONG24', 12))                                          # ouvert x10..11 et x38..47
    m.stamp('CONS', 22, 3)
    m.stamp('BARRELS', 14, 21); m.stamp('DOME', 6, 21); m.stamp('DOME', 38, 21)
    row(m, 28, ('LONG25', 3), ('BENCH12', 35))
    m.stamp('ENTRY', 22, 33)
    m.stamp('CONS', 3, 4); m.stamp('CONS', 42, 4); m.stamp('DOME', 12, 3)
    m.stamp('DOME', 43, 15); m.stamp('TURB2', 40, 30); m.stamp('DOME', 2, 31); m.stamp('CAB', 8, 18); m.stamp('CAB', 30, 18)
    rub(m, (16, 6), (17, 6), (28, 5), (29, 5), (45, 19), (5, 20), (6, 20), (36, 26), (37, 26), (38, 27), (11, 26), (12, 26), (31, 32), (34, 32))
    m.pad(33, 4); m.pad(2, 18)
    return m
def floor2():
    m = Map()
    row(m, 6, ('BENCH9a', 1), ('BENCH9b', 11), ('BENCH12', 21))                      # ouvert x33..47
    row(m, 12, ('BENCH14', 34), ('LONG24', 8))                                         # ouvert x1..7 et x33
    row(m, 18, ('BENCH12', 1), ('BENCH9b', 14), ('BENCH12', 26), ('BENCH9a', 39))
    row(m, 25, ('LONG25', 20), ('ROW9a', 1))
    m.stamp('CONS', 3, 29); m.stamp('TURB2', 38, 28); m.stamp('DOME', 12, 30)
    m.stamp('CAB', 15, 3); m.stamp('CAB', 28, 3); m.stamp('CONS', 18, 8); m.stamp('DOME', 40, 8); m.stamp('CAB', 4, 9)
    m.stamp('CAB', 30, 22); m.stamp('CAB', 6, 22); m.stamp('DOME', 17, 28); m.stamp('CAB', 27, 31); m.stamp('CAB', 33, 28)
    rub(m, (10, 4), (11, 4), (36, 5), (37, 5), (24, 22), (25, 22), (2, 28), (3, 28), (46, 21), (23, 33), (24, 33), (45, 32))
    m.pad(2, 4); m.pad(43, 3)
    return m
def floor3():
    m = Map()
    m.stamp('BARRELS', 4, 8); m.stamp('BARRELS', 28, 8); m.stamp('BARRELS', 10, 17); m.stamp('BARRELS', 30, 17)
    m.stamp('DOME', 22, 12); m.stamp('DOME', 2, 13)
    row(m, 24, ('LONG24', 1), ('BENCH12', 34))
    row(m, 30, ('BENCH14', 8), ('BENCH9a', 30))
    m.stamp('CONS', 41, 12)
    m.stamp('CAB', 2, 4); m.stamp('CAB', 44, 4); m.stamp('CONS', 12, 4); m.stamp('CONS', 32, 4); m.stamp('DOME', 44, 17)
    m.stamp('DOME', 22, 27); m.stamp('CAB', 4, 28); m.stamp('CAB', 42, 28); m.stamp('CONS', 22, 20)
    rub(m, (20, 6), (21, 6), (26, 6), (8, 15), (9, 15), (38, 15), (39, 15), (30, 26), (31, 26), (6, 27), (14, 33), (15, 33), (33, 33))
    m.pad(24, 4); m.pad(44, 32)
    return m
def floor4():
    m = Map()
    row(m, 5, ('BENCH14', 1), ('BENCH12', 17), ('BENCH9b', 31))
    row(m, 11, ('BENCH12', 8), ('BENCH14', 22))
    row(m, 17, ('ROW9a', 1), ('LONG24', 14))
    row(m, 23, ('LONG25', 4), ('BENCH9a', 33))
    row(m, 29, ('BENCH12', 14), ('BENCH14', 30))
    m.stamp('TURB2', 40, 6); m.stamp('CONS', 3, 31)
    m.stamp('CAB', 12, 7); m.stamp('CAB', 35, 9); m.stamp('DOME', 3, 12); m.stamp('DOME', 44, 12); m.stamp('CONS', 22, 12)
    m.stamp('CAB', 10, 26); m.stamp('CAB', 28, 26); m.stamp('DOME', 3, 25); m.stamp('CAB', 40, 31); m.stamp('CONS', 24, 30)
    rub(m, (9, 3), (10, 3), (30, 3), (31, 3), (8, 20), (9, 20), (36, 20), (46, 27), (47, 27), (20, 32), (21, 32), (12, 22))
    m.pad(44, 24)
    return m
FLOORS = {'1F': floor1, '2F': floor2, '3F': floor3, 'B1F': floor4}
if __name__ == '__main__':
    for n, f in FLOORS.items():
        m = f(); L = Layout('LAYOUT_POKEMON_MANSION_1F'); L.w, L.h = W, H; L.g = [v for r in m.g for v in r]
        L.prim = PP.prim; L.sec = PP.sec
        L.render().convert('RGB').save('/tmp/cp/c_%s.png' % n)
