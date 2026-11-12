import sys, time, re
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
SC = open('/home/claude/pkmn-topaze/data/maps/IndigoPlateau_PokemonCenter_1F/scripts.inc').read()
REB = {int(m.group(1)): (int(m.group(2)), m.group(3)) for m in re.finditer(r'EventScript_Rebel(\d)::\n\tsetvar VAR_TOPAZE_BOOST, (\d+)\n\ttrainerbattle_no_intro (TRAINER_\w+)', SC)}
def hub_round(t):
    """Un duel du hub de Flora (tour = VAR_REBELS_ROUND) : niveau exact du duel, bonbons, entrainement, jusqu'a 4 essais."""
    rd = t.getvar('VAR_REBELS_ROUND'); boost, tr = REB[rd]
    need = OPP.power(OPP.db()[tr])[0] + boost + 2
    log('  hub duel', rd, tr, 'niveau conseille', need)
    t.too_strong = max(getattr(t, 'too_strong', 0), need); t.use_candies(0, upto=need); t.ensure(need)
    for essai in range(4):
        if t.sync() != 'IndigoPlateau_PokemonCenter_1F': assert t.go('IndigoPlateau_PokemonCenter_1F'), 'Centre inaccessible'
        t.talk_script('Flora', 20); t.scene(maxn=300); t.press('A', 4, 20); t.scene(maxn=900)
        for _ in range(8):
            if not t.inbattle(): break
            t.finish_battle(maxn=900); t.scene(maxn=300)
        t.heal(); t.e.run(60, 0)
        if t.getvar('VAR_REBELS_ROUND') != rd: t.save('r3_hub%d' % rd); return True
        top = max(q['level'] for q in t.party()); t.too_strong = top + 8; log('  duel perdu : entrainement jusqu au niveau', top + 8); t.use_candies(0, upto=top + 8); t.ensure(top + 8)
    return False
assert t.go('IndigoPlateau_PokemonCenter_1F'), 'Centre inaccessible'
while t.getvar('VAR_REBELS_ROUND') < 8:
    if not hub_round(t): log('BLOCK hub fige', t.getvar('VAR_REBELS_ROUND')); break
log('=== hub round', t.getvar('VAR_REBELS_ROUND'))
if not t.getflag('FLAG_LORD_SEVEN'):
    RF.stage_pg_ferry(t)
LORDS = ['OneIsland', 'TwoIsland', 'ThreeIsland', 'FourIsland', 'FiveIsland', 'SixIsland', 'SevenIsland']
for i, mp in enumerate(LORDS, 1):
    fl = ['FLAG_LORD_ONE', 'FLAG_LORD_TWO', 'FLAG_LORD_THREE', 'FLAG_LORD_FOUR', 'FLAG_LORD_FIVE', 'FLAG_LORD_SIX', 'FLAG_LORD_SEVEN'][i - 1]
    if t.getflag(fl): continue
    for essai in range(3):
        try: RF.go_isle(t, i, mp); t.e.run(60, 0); C.fight_npc(t, 'Lord', 16)
        except AssertionError as ex: log('BLOCK seigneur', mp, ex); break
        if t.getflag(fl): break
        top = max(q['level'] for q in t.party()); t.too_strong = top + 8; log('  duel perdu : entrainement jusqu au niveau', top + 8); t.use_candies(0, upto=top + 8); t.ensure(top + 8)
    log('  seigneur', mp, t.getflag(fl)); t.save('r3_' + mp)
assert t.go('IndigoPlateau_PokemonCenter_1F'), 'Centre inaccessible'
while t.getvar('VAR_REBELS_ROUND') < 9:
    if not hub_round(t): log('BLOCK hub final fige', t.getvar('VAR_REBELS_ROUND')); break
log('RESULTAT fin 3 chaine : round', t.getvar('VAR_REBELS_ROUND'), 'arenes', [t.getflag(f) for _, f in C.GYMS], 'seigneurs', [t.getflag(f) for f in ('FLAG_LORD_ONE','FLAG_LORD_TWO','FLAG_LORD_THREE','FLAG_LORD_FOUR','FLAG_LORD_FIVE','FLAG_LORD_SIX','FLAG_LORD_SEVEN')], '%ds' % (time.time() - t0))
t.save('end3_chain_done')
