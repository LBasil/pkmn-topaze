#!/usr/bin/env python3
"""Genere zones_lotN.py (zones sauvages sans drapeau) a partir de lignes (map,tpl,badge,lv,land,ask,npc1,npc2). Usage: mklot.py N rows.py"""
import sys
n=int(sys.argv[1]); rows=eval(open(sys.argv[2]).read())
s=open('docs/topaze/zones_lot20.py').read(); a=s.index('Z = ['); b=s.index(']\nSPX')
gt=lambda b:'Come back with %d BADGE%s.'%(b,'' if b==1 else 'S') if b<8 else 'Come back with all 8 BADGES.'
Z='Z = [\n'+''.join(" dict(map=%r, tpl=%r, badge=%d, lv=%r, land=%r,\n      ask=%r, gt=%r,\n      npcs=[%r, %r], hidden=[], quests=[]),\n"%(m,t,bd,lv,land,ask,gt(bd),n1,n2) for m,t,bd,lv,land,ask,n1,n2 in rows)
t=s[:a]+Z+s[b:]; t=t.replace('CrickPond',rows[0][0]).replace('LOT 20','LOT %d'%n)
open('docs/topaze/zones_lot%d.py'%n,'w').write(t)
