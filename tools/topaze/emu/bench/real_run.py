#!/usr/bin/env python3
"""Pilote « joueur reel » : Auto (run_full.py) sans mode dieu + cerveau de combat (real.py)."""
import sys, os
sys.path.insert(0, '/tmp/gx')
from run_full import *
import real
from real import BattleMixin, sym

class Real(BattleMixin, Auto):
    def heal(s): pass                  # plus de soin magique : Centre Pokemon / objets
    def heal_battle(s): pass
    @classmethod
    def resume(cls, name, rom='/tmp/gx/dbg2.gba'):
        t = Auto.resume.__func__(cls, name, rom)
        t.e.cmd('poke8 %x 0' % 0x030075e8)      # gTopazeGod = 0
        t._b = real.Brain(t.e); return t
    def grass(s):
        n = s.nav(); return [(x, y) for y in range(n.h) for x in range(n.w) if (n.attr(x, y) & 0xff) == 2 and not n.blocked(x, y)]
    def party(s): return s._brain().party()
    def train(s, mapname, lvl, maxsteps=400):
        """Combat dans l'herbe de `mapname` jusqu'a ce que la tete d'equipe atteigne `lvl`."""
        assert s.go(mapname), 'carte inaccessible'
        for it in range(maxsteps):
            p = s.party()
            if p and p[0]['level'] >= lvl: return True
            gr = s.grass(); me = s.pos()[2:]
            if not gr: log('pas d\'herbe', mapname); return False
            tgt = min(gr, key=lambda c: abs(c[0] - me[0]) + abs(c[1] - me[1]))
            s.walk_fight(tgt, 6)
            for k in range(30):
                s.press('LEFT' if (k // 2) % 2 == 0 else 'RIGHT', 2, 2)
                if s.inbattle(): break
            if s.inbattle():
                s.scene(maxn=600); log('combat fini', [(q['level'], q['hp'], q['maxhp']) for q in s.party()])
        return False

if __name__ == '__main__':
    t = Real.resume(sys.argv[1] if len(sys.argv) > 1 else 'opan')
    print(t.train('Route22', 10))
