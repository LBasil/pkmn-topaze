#!/usr/bin/env python3
"""LOT 13 : 3 boutiques sans drapeau (BallBoutique, BattleStall, BerryStand), accessibles par le passeur des Saisons. Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'BallBoutique' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
B = [
 dict(map='BallBoutique', tpl='SaffronCity_HomeA', ask='The BALL BOUTIQUE: rare balls for keen collectors. Visit?', who='WOMAN_3', hi='Every ball has a story. Choose yours.',
      stock=['NET_BALL', 'NEST_BALL', 'DIVE_BALL', 'REPEAT_BALL', 'TIMER_BALL', 'LUXURY_BALL', 'PREMIER_BALL'], npcs=[('MAN', 'NET for bugs and water, DIVE for the deep, NEST for the weak.')]),
 dict(map='BattleStall', tpl='SaffronCity_HomeB', ask='The BATTLE STALL: small boosts for hard fights. Visit?', who='MAN', hi='Win before the fight begins.',
      stock=['X_ATTACK', 'X_DEFEND', 'X_SPEED', 'X_SPECIAL', 'X_ACCURACY', 'GUARD_SPEC', 'DIRE_HIT'], npcs=[('SAILOR', 'Items last one battle. Use them on the boss, not on rats.')]),
 dict(map='BerryStand', tpl='SaffronCity_HomeC', ask='The BERRY STAND: fresh berries for every need. Visit?', who='OLD_WOMAN', hi='Picked this morning. Take your pick.',
      stock=['CHERI_BERRY', 'CHESTO_BERRY', 'PECHA_BERRY', 'RAWST_BERRY', 'ASPEAR_BERRY', 'ORAN_BERRY', 'PERSIM_BERRY', 'LUM_BERRY', 'SITRUS_BERRY'], npcs=[('LASS', 'A berry in the right hand beats a potion.')]),
]
arr = {}
for z in B:
    mn = z['map']; N.clone(mn, z['tpl'], objects=[], warps=[], scripts='', txt=''); nav = R.Nav(mn); cells = comp(nav)
    a = near(nav, cells, (nav.w // 2, int(nav.h * .75)), [], margin=0); arr[mn] = a; taken = [a]; objs = []; sc = ''; tx = ''
    def place(gfx, pref, script, margin=2):
        c = near(nav, cells, pref, taken, margin); taken.append(c); objs.append(N.obj(gfx, c[0], c[1], script, el=EL(nav, c)))
    place('SAILOR', (a[0] + 2, a[1]), mn + '_EventScript_ReturnFerry', 1)
    sc += ('%s_EventScript_ReturnFerry::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_ReturnAsk, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s_EventScript_Stay\n\twarp MAP_FUCHSIA_CITY, 255, 24, 27\n\twaitstate\n\tend\n\n%s_EventScript_Stay::\n\tmsgbox %s_Text_Stay\n\trelease\n\tend\n\n') % (mn, mn, mn, mn, mn)
    tx += N.text(mn + '_Text_ReturnAsk', 'Ready to go back to the dock?') + N.text(mn + '_Text_Stay', 'Take your time. The tide can wait.')
    place(z['who'], (a[0], a[1] - 3), mn + '_EventScript_Shop')
    sc += '%s_EventScript_Shop::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_ShopHi\n\tpokemart %s_Stock\n\tmsgbox %s_Text_ShopBye\n\trelease\n\tend\n\n\t.align 2\n%s_Stock::\n' % (mn, mn, mn, mn, mn) + ''.join('\t.2byte %s\n' % it(i) for i in z['stock']) + '\t.2byte ITEM_NONE\n\n'
    tx += N.text(mn + '_Text_ShopHi', z['hi']) + N.text(mn + '_Text_ShopBye', 'Come back any time.')
    for j, (gfx, line) in enumerate(z['npcs']):
        S_, T_ = '%s_EventScript_Npc%d' % (mn, j), '%s_Text_Npc%d' % (mn, j)
        place(gfx, (a[0] - 2, a[1] - 2 - j * 2), S_); sc += '%s::\n\tmsgbox %s, MSGBOX_NPC\n\tend\n\n' % (S_, T_); tx += N.text(T_, line)
    N.rewrite(mn, objs, sc, tx, bgs=[]); print(mn, a, len(cells))
for z, f in zip(B, ['SeasonsFerryman', 'ScribeFerryman', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], 0, z['ask'])
