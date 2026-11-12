import sys, time
sys.path.insert(0, '/tmp/gx'); sys.path.append('/home/claude/pkmn-topaze/tools/topaze/emu/bench')
from play import *
import chain_ends as C
sys.path.append('/home/claude/pkmn-topaze/tools/topaze/bot')
import opponents as OPP
BOOST = {'Brock': 54, 'Misty': 50, 'LtSurge': 45, 'Erika': 41, 'Koga': 38, 'Sabrina': 35, 'Blaine': 32}
TRAINER = {'Brock': 'BROCK', 'Misty': 'MISTY', 'LtSurge': 'LT_SURGE', 'Erika': 'ERIKA', 'Koga': 'KOGA', 'Sabrina': 'SABRINA', 'Blaine': 'BLAINE'}
t = Player.resume(sys.argv[1] if len(sys.argv) > 1 else 'end3_done'); RF.R.SURF = True
log('=== FIN 3 reprise', t.sync(), t.pos()[2:], 'fin', t.getvar('VAR_TOPAZE_ENDING'), [(q['level'], q['hp']) for q in t.party()])
t.var('VAR_TOPAZE_BOOST', 0)
t0 = time.time()
for mp, fl in C.GYMS:
    pat = C.leader_pat(mp); t1 = time.time()
    objs = RF.mj(mp + '_Gym')['object_events']
    if not any(pat in o.get('script', '') for o in objs):      # le label du hook n'est pas celui de l'objet (Sabrina...) : on prend le script du chef
        ld = [o for o in objs if pat.replace('Fight', '').upper() in o['graphics_id']]
        if ld: pat = ld[0]['script'].split('EventScript_')[1]
        log('  motif du chef :', pat)
    if t.getflag(fl): continue
    ld = [k for k in BOOST if k.lower() in pat.lower()]
    if ld:      # niveau exact du duel (niveau de base + bonus de la Reconquete) : on s'entraine AVANT le premier essai
        need = OPP.power(OPP.db()['TRAINER_LEADER_' + TRAINER[ld[0]]])[0] + BOOST[ld[0]] + 2
        t.too_strong = max(getattr(t, 'too_strong', 0), need); log('  niveau conseille', mp, need); t.use_candies(0, upto=need); t.ensure(need)
    for essai in range(4):
        if not t.go(mp + '_Gym'): log('BLOCK arene', mp); break
        C.fight_npc(t, pat, 16)
        if t.getflag(fl): break
        top = max(q['level'] for q in t.party()); t.too_strong = top + 8; log('  duel perdu : entrainement jusqu au niveau', top + 8); t.use_candies(0, upto=top + 8); t.ensure(top + 8)
    log('  arene', mp, fl, t.getflag(fl), '%ds' % (time.time() - t1)); t.save('r3_' + mp)
log('=== arenes', [t.getflag(f) for _, f in C.GYMS])
assert t.go('IndigoPlateau_PokemonCenter_1F'), 'Centre inaccessible'
for k in range(14):
    rd = t.getvar('VAR_REBELS_ROUND'); log('  hub duel', rd, t.sync())
    if rd >= 9: break
    if rd == 8: break
    t.talk_script('Flora', 20); t.scene(maxn=300); t.press('A', 4, 20); t.scene(maxn=900)
    for _ in range(8):
        if not t.inbattle(): break
        t.finish_battle(maxn=900); t.scene(maxn=300)
    t.heal(); t.e.run(60, 0)
    if t.getvar('VAR_REBELS_ROUND') == rd: log('BLOCK hub fige', rd); break
    t.save('r3_hub%d' % rd)
for i, mp in enumerate(['OneIsland', 'TwoIsland', 'ThreeIsland', 'FourIsland', 'FiveIsland', 'SixIsland', 'SevenIsland'], 1):
    try: C.go_isle(t, i, mp); t.e.run(60, 0); C.fight_npc(t, 'Lord', 16)
    except AssertionError as ex: log('BLOCK seigneur', mp, ex); continue
    log('  seigneur', mp, [t.getflag(f) for f in ('FLAG_LORD_ONE', 'FLAG_LORD_TWO', 'FLAG_LORD_THREE', 'FLAG_LORD_FOUR', 'FLAG_LORD_FIVE', 'FLAG_LORD_SIX', 'FLAG_LORD_SEVEN')]); t.save('r3_' + mp)
assert t.go('IndigoPlateau_PokemonCenter_1F'), 'Centre inaccessible'
for k in range(4):
    rd = t.getvar('VAR_REBELS_ROUND'); log('  hub final', rd)
    if rd >= 9: break
    t.talk_script('Flora', 20); t.scene(maxn=300); t.press('A', 4, 20); t.scene(maxn=900)
    for _ in range(8):
        if not t.inbattle(): break
        t.finish_battle(maxn=900); t.scene(maxn=300)
    t.heal(); t.e.run(60, 0)
log('RESULTAT fin 3 chaine : round', t.getvar('VAR_REBELS_ROUND'), 'arenes', [t.getflag(f) for _, f in C.GYMS], 'seigneurs', [t.getflag(f) for f in ('FLAG_LORD_ONE','FLAG_LORD_TWO','FLAG_LORD_THREE','FLAG_LORD_FOUR','FLAG_LORD_FIVE','FLAG_LORD_SIX','FLAG_LORD_SEVEN')], '%ds' % (time.time() - t0))
t.save('end3_chain_done')
