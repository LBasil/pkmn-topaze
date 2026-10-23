#!/usr/bin/env python3
"""Refonte des 4 etages de la centrale (ex-Manoir). Idempotent: repart de centrale_orig/."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from centrale_lib import *
L = lambda n: os.path.join(ROOT, 'data/layouts/PokemonMansion_%s/map.bin' % n)

def f1():
    c = Cv(34, 26, '1F'); c.shell(doors=(5, 16, 28))
    for a, b in ((1, 9), (11, 19), (21, 32)): c.topwall(a, b)
    for x in (4, 5, 6, 7, 8, 14, 15, 16, 17, 18): c.set(x, 3, 693)
    for x in (1, 8, 15, 22): c.turbine(x, 5)
    c.stamp(28, 5, 5, 4, 28, 5)                    # annexe consoles
    # allee centrale en caillebotis: entree -> turbines
    c.fill(16, 13, 16, 22, 716); c.fill(5, 22, 28, 22, 716)
    c.fill(15, 10, 17, 12, 716)
    # transformateurs
    for x in (2, 6, 10): c.stamp_lit(MACH, x, 14)
    for x in (22, 26): c.stamp_lit(MACH, x, 14)
    c.stamp_lit(BENCH, 11, 18); c.stamp_lit(BENCH, 19, 18)
    c.stamp_lit(BENCH, 2, 18)
    # monte-charge vers la chaufferie (27,20)
    c.fill(26, 19, 28, 21, 716); c.set(27, 20, 710)
    for x, y in ((25, 19), (25, 20), (25, 21), (29, 19), (29, 20), (29, 21), (26, 18), (27, 18), (28, 18)): c.set(x, y, 693)
    c.fill(27, 21, 27, 21, 716)
    c.stamp_lit(MACH, 30, 14)
    return c
def f2():
    c = Cv(22, 14, '2F'); c.shell(doors=(11,))
    c.topwall(1, 9); c.topwall(11, 20)
    for x in (4, 5, 6, 7, 8, 14, 15, 16, 17, 18): c.set(x, 3, 693)
    c.stamp_lit(BENCH, 2, 5); c.stamp_lit(BENCH, 8, 5); c.turbine(14, 5)
    c.stamp_lit(SIDE, 2, 9); c.stamp_lit(SIDE, 17, 9)
    c.fill(10, 9, 12, 11, 716); c.fill(11, 4, 11, 9, 716)
    for x, y in ((9, 9), (13, 9), (9, 10), (13, 10)): c.set(x, y, 693)
    return c

def f3():
    c = Cv(26, 18, '3F'); c.shell(doors=(12,))
    c.topwall(1, 12); c.topwall(14, 22)
    for x in (17, 18, 19, 20, 21): c.set(x, 3, 693)
    c.stamp_lit(BENCH, 2, 5); c.stamp_lit(BENCH, 8, 5); c.turbine(14, 5)
    c.stamp_lit(SIDE, 21, 5); c.stamp_lit(SIDE, 21, 9)
    c.stamp_lit(MACH, 2, 11); c.stamp_lit(MACH, 16, 11)
    c.stamp_lit(MACH, 2, 13) if False else None
    c.fill(11, 10, 13, 15, 716); c.fill(23, 3, 23, 12, 716)
    c.set(23, 3, 710); c.fill(22, 3, 22, 3, 693)
    c.stamp_lit(MACH, 20, 13)
    return c

def fb():
    c = Cv(28, 20, 'B1F'); c.shell(doors=())
    c.topwall(1, 12); c.topwall(14, 25)
    for x in (4, 5, 6, 7, 8, 9, 16, 17, 18, 19, 20, 21): c.set(x, 3, 693)
    # chaudieres le long du mur nord
    for x in (2, 8, 16, 22): c.turbine(x, 4)
    c.fill(1, 9, 26, 9, 716)
    # racks de tuyaux (reprise du dessin d'origine, etages 10-12 et 14-16)
    c.stamp(4, 10, 12, 3, 4, 10); c.stamp(18, 10, 9, 3, 18, 10)
    c.stamp(1, 14, 9, 3, 1, 14); c.stamp(12, 14, 12, 3, 12, 14)
    c.set(5, 14, 784)
    for x, y in ((6, 13), (7, 13), (8, 13), (13, 13), (14, 13)): c.set(x, y, 693)
    # puits de la montee: plot rouge et caillebotis
    c.stamp_lit(MACH, 24, 14); c.set(23, 16, 710); c.fill(23, 17, 23, 18, 716)
    c.fill(14, 17, 23, 17, 716)
    return c
if __name__ == '__main__':
    for n, f in (('1F', f1), ('2F', f2), ('3F', f3), ('B1F', fb)):
        f().save(L(n))
