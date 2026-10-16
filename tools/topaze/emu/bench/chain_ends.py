"""Bot des chaines post-game des fins 3 (Reconquete) et 2 (Refuge). Usage : chain_ends.py 3 | 2   (repart de la sauvegarde 'ending1' du harnais, fin re-posee)."""
import sys, re, time
sys.path.insert(0, '/tmp/gx')
import run_full as R
from run_full import *

GYMS = [('PewterCity', 'FLAG_REBEL_KAY'), ('CeruleanCity', 'FLAG_REBEL_SYLVESTRE'), ('VermilionCity', 'FLAG_REBEL_HERA'), ('CeladonCity', 'FLAG_REBEL_GRIM'),
        ('FuchsiaCity', 'FLAG_REBEL_ACHLYS'), ('SaffronCity', 'FLAG_REBEL_NOX'), ('CinnabarIsland', 'FLAG_REBEL_EDDIE')]

def leader_pat(mapname):
    s = open('/home/claude/pkmn-topaze/data/maps/%s_Gym/scripts.inc' % mapname).read()
    for blk in re.split(r'\n\n', s):
        if 'call_if_set FLAG_TOPAZE_COUNCIL' in blk:
            return re.match(r'(\w+)::', blk.strip()).group(1).split('EventScript_')[1]

def predefeat(t, mapname):
    """Le chef est deja battu (aventure principale) : drapeau de dresseur, DEFEATED_*, CT donnee."""
    s = open('/home/claude/pkmn-topaze/data/maps/%s_Gym/scripts.inc' % mapname).read()
    ids = dict(re.findall(r'#define (TRAINER_LEADER_\w+)\s+(\d+)', open('/home/claude/pkmn-topaze/include/constants/opponents.h').read()))
    for tr in set(re.findall(r'TRAINER_LEADER_\w+', s)):
        if tr in ids: t.flag(0x500 + int(ids[tr]))
    for f in set(re.findall(r'FLAG_GOT_TM\d+_FROM_\w+', s)) | set(re.findall(r'FLAG_DEFEATED_\w+', s)):
        try: t.flag(f)
        except KeyError: pass
    t.flag('FLAG_HEMATEK_BOSS_DONE')

def reset_ending(t, e):
    t.var('VAR_TOPAZE_ENDING', e); t.var('VAR_TOPAZE_BOOST', 0)
    for f in ('FLAG_TOPAZE_COUNCIL', 'FLAG_SYS_GAME_CLEAR', 'FLAG_DEFEATED_CHAMP'): t.flag(f)
    t.flag('FLAG_TOPAZE_POSTGAME', e == 1)

def fight_npc(t, pat, n=14, tries=3):
    for k in range(tries):
        ok = t.talk_script(pat, n); t.scene(maxn=900)
        for _ in range(8):
            if not t.inbattle(): break
            t.finish_battle(maxn=900); t.scene(maxn=300)
        t.heal(); t.scene(maxn=300)
        return ok

def ending3(t):
    t0 = time.time(); reset_ending(t, 3); t.buff()
    for mp, fl in GYMS:
        pat = leader_pat(mp); t1 = time.time()
        # champion deja battu ; le chef est deja battu en vrai : on repose son drapeau de dresseur est inutile (le script Visit3 fait trainerbattle_no_intro)
        if not t.go(mp + '_Gym'): log('BLOCK arene', mp); continue
        predefeat(t, mp); t.e.run(60, 0)
        try: fight_npc(t, pat, 16)
        except AssertionError as ex: log('BLOCK', mp, ex)
        log('  arene', mp, pat, fl, t.getflag(fl), 'boost', t.getvar('VAR_TOPAZE_BOOST'), '%ds' % (time.time() - t1)); t.save('e3_' + mp)
    log('=== arenes ok', [t.getflag(f) for _, f in GYMS], '%ds' % (time.time() - t0))
    # Flora : duels du hub
    assert t.go('IndigoPlateau_PokemonCenter_1F'), 'Centre inaccessible'
    for k in range(12):
        rd = t.getvar('VAR_REBELS_ROUND'); log('  hub duel', rd, t.sync())
        if rd >= 9: break
        t.walk_fight((0, 0), 0) if False else None
        try: t.talk_script('Flora', 20); t.scene(maxn=300); t.press('A', 4, 20)  # YESNO : A = OUI
        except AssertionError as ex: log('BLOCK', ex); break
        t.scene(maxn=900)
        for _ in range(8):
            if not t.inbattle(): break
            t.finish_battle(maxn=900); t.scene(maxn=300)
        t.heal(); t.e.run(60, 0)
        if t.getvar('VAR_REBELS_ROUND') == rd:
            # peut-etre bloque sur les Seigneurs : on les fait
            if rd == 8: break
            log('BLOCK hub fige', rd); break
        t.save('e3_hub%d' % rd)
    log('=== hub round', t.getvar('VAR_REBELS_ROUND'), '%ds' % (time.time() - t0))
    # Seigneurs
    for i, mp in enumerate(['OneIsland', 'TwoIsland', 'ThreeIsland', 'FourIsland', 'FiveIsland', 'SixIsland', 'SevenIsland'], 1):
        t1 = time.time()
        try:
            go_isle(t, i, mp); t.e.run(60, 0); fight_npc(t, 'Lord', 16)
        except AssertionError as ex: log('BLOCK seigneur', mp, ex); continue
        log('  seigneur', mp, [t.getflag(f) for f in ('FLAG_LORD_ONE', 'FLAG_LORD_TWO', 'FLAG_LORD_THREE', 'FLAG_LORD_FOUR', 'FLAG_LORD_FIVE', 'FLAG_LORD_SIX', 'FLAG_LORD_SEVEN')], '%ds' % (time.time() - t1)); t.save('e3_lord%d' % i)
    log('=== FIN fin 3 : %d s de jeu emule/bot' % (time.time() - t0))

def fresh():
    """Etats sauves perimes (ROM de test reconstruite) : on repart d'un etat reconstitue a Bourg-Palette (8 badges, CS, fin de jeu)."""
    t = Auto('PalletTown', 8, 14, party=True, nocombat=False, god=True, pre=['FLAG_BADGE%02d_GET' % i for i in range(1, 9)] + ['FLAG_SYS_GAME_CLEAR', 'FLAG_TOPAZE_COUNCIL', 'FLAG_DEFEATED_CHAMP'])
    t.e.cmd('unpin')
    for i in range(1, 9): t.flag('FLAG_BADGE%02d_GET' % i)
    for i in range(1, 7): t.flag('FLAG_GOT_HM%02d' % i)
    for f in ('FLAG_SYS_POKEDEX_GET', 'FLAG_SYS_POKEMON_GET', 'FLAG_OAK_RATED_POKEDEX', 'FLAG_GOT_POKEDEX', 'FLAG_SYS_CAN_LINK_WITH_RS', 'FLAG_DEFEATED_CHAMP', 'FLAG_SYS_GAME_CLEAR'):
        try: t.flag(f)
        except Exception as ex: log('flag?', f, ex)
    t.var('VAR_MAP_SCENE_PALLET_TOWN_OAK', 1); t.flag('FLAG_HIDE_PALLET_RIVAL'); t.flag('FLAG_HIDE_OAK_IN_PALLET_TOWN')
    R.SURF = True; t.buff(); give_hms(t); return t

def main():
    e = sys.argv[1]
    t = fresh(); log('reprise', t.sync(), t.pos()[2:])
    {'3': ending3}[e](t)

if __name__ == '__main__': main()
