#!/usr/bin/env python3
"""Suite de non-regression emulateur (mGBA headless). Prerequis : /tmp/gx (harness, drive.py, tz.py, dbg2.gba via mkdbg2.py).
Usage : python3 tools/topaze/emu/regress.py   (code retour 1 si un test echoue). Ne pas oublier ensuite un `make` normal."""
import sys, traceback
sys.path.insert(0, '/tmp/gx')
from tz import *
R_ = []
def test(name):
    def deco(f):
        try: f(); R_.append((name, True, ''))
        except Exception as e: R_.append((name, False, repr(e)[:120]))
        return f
    return deco

SMOKE = ['PalletTown','Route1','Route2','ViridianCity','Route3','Route4','CeruladonCity' if False else 'CeruleanCity','VermilionCity','CeladonCity',
         'SaffronCity','FuchsiaCity','CinnabarIsland','Route11','Route12','Route18','Route25','CeladonCity_Hotel','VermilionCity_PokemonFanClub',
         'PalletTown_RivalsHouse','VermilionCity_House2','CeruleanCity_House3','Route18_EastEntrance_2F','UndergroundPath_NorthEntrance']
for m in SMOKE:
    def mk(m):
        @test('smoke ' + m)
        def _():
            t = T(m, 6, 6, nocombat=True, god=True)
            t.e.run(120, 0)
            p = t.pos(); assert p is not None, 'pas de position'
            assert (p[0], p[1]) == mid(m), 'carte differente %s' % (p,)
    mk(m)

@test('quete Dontae (niveau >= 45 -> LINK CABLE)')
def _():
    t = T('CeruleanCity_House3', 2, 3, nocombat=True, god=True)
    t.press('UP', 1, 20); t.press('A', 4, 60); t.mash(16, every=6, gap=40)
    assert t.getflag('FLAG_DID_ZYNX_TRADE'), 'flag non pose'

@test('Fan Club Carmin : brossage d equipe + cooldown')
def _():
    t = T('VermilionCity_PokemonFanClub', 6, 5, nocombat=True, god=True)
    t.press('UP', 1, 20)
    assert t.getvar('VAR_PETTING_COOLDOWN_STEP_COUNTER') >= 300
    t.press('A', 4, 60); t.mash(14, every=6, gap=40); t.press('A', 4, 60); t.mash(12, every=6, gap=40)
    assert t.getvar('VAR_PETTING_COOLDOWN_STEP_COUNTER') < 300, 'compteur non reinitialise'

bad = [r for r in R_ if not r[1]]
for n, ok, msg in R_: print(('OK   ' if ok else 'FAIL ') + n + ('' if ok else '  -> ' + msg))
print('%d/%d tests OK' % (len(R_) - len(bad), len(R_)))
sys.exit(1 if bad else 0)
