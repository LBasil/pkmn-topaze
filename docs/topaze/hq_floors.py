"""Plans des etages du repaire de Bourg Quartz. Chaque fonction renvoie (Cv, ancres)."""
from hq_lib import *
def b1f():
    c = Cv(28, 30); A = {}
    c.room(9, 2, 20, 8, z=1)          # A : accueil Onybris (zone reprise)
    c.room(1, 12, 26, 13, z=0)        # C : couloir
    c.room(1, 17, 8, 25, z=0)         # W : dortoir (deux escaliers vers B2F, derriere la barriere)
    c.room(11, 17, 16, 28, z=0)       # S : reserve
    c.room(19, 17, 26, 24, z=1)       # E : securite + ascenseur (zone reprise)
    c.vdoor(14, 9, 2); c.vdoor(4, 14, 2); c.vdoor(13, 14, 2); c.vdoor(20, 14, 2)
    c.zone(14, 9, 15, 11, 1); c.zone(13, 12, 22, 14, 1)     # la voie bleue : accueil -> couloir -> securite
    c.zone(20, 14, 21, 16, 1)
    A['casino'] = c.stair_up(10, 2)
    A['down1'] = c.stair_dn(1, 17); A['down2'] = c.stair_dn(6, 17)
    c.put(ELEV, 23, 15); A['lift'] = [(23, 16), (24, 16), (25, 16)]
    # A : accueil Onybris
    c.put(RACK, 15, 1); c.put(TERM, 18, 1); c.put(DESK, 11, 5); c.put(PLANT_A, 10, 6); c.put(PLANT_B, 19, 6)
    # C : couloir ancien (tableau d'affichage, caisses entassees aux deux bouts)
    c.put(BOARD, 6, 11); c.put(CRATE, 1, 12); c.put(CRATE, 1, 13); c.put(CRATE, 2, 13); c.put(CRATE, 26, 12); c.put(CRATE, 26, 13)
    c.put(MAT, 9, 13)
    # W : dortoir
    c.put(DESK, 1, 20); c.put(CRATE, 8, 22); c.put(CRATE, 8, 23); c.put(CRATE, 7, 23); c.put(PAPERS, 5, 21); c.put(MAT, 3, 24); c.put(LOCKER, 7, 24)
    # S : reserve
    c.put(SHELF, 11, 20); c.put(SHELF, 14, 23); c.put(SHELF, 11, 26)
    c.put(CRATE, 16, 20); c.put(CRATE, 16, 21); c.put(CRATE, 12, 24); c.put(PAPERS, 13, 21)
    # E : securite
    c.put(DESK2, 20, 19); c.put(PLANT_A, 26, 20); c.put(PLANT_B, 19, 22)
    return c, A

def b4f():
    c = Cv(24, 26); A = {}
    c.room(13, 2, 22, 8, z=1)         # bureau du boss (repris)
    c.room(1, 2, 9, 8, z=0)           # ancienne remise (cle de l'ascenseur)
    c.room(1, 12, 22, 16, z=0)        # grand hall
    c.room(1, 20, 9, 23, z=0)         # remise sud (escalier)
    c.room(14, 20, 22, 23, z=1)       # sas de l'ascenseur (repris)
    c.vdoor(17, 9, 2); c.vdoor(4, 9, 2); c.vdoor(5, 17, 2); c.vdoor(15, 17, 2)
    c.zone(17, 9, 18, 11, 1)
    A['up'] = c.stair_up(2, 20)
    c.put(ELEV, 19, 18); A['lift'] = [(19, 19), (20, 19), (21, 19)]
    # bureau du boss
    c.put(RACK, 14, 1); c.put(TERM, 21, 1); c.put(DESK, 18, 3); c.put(PLANT_A, 13, 7); c.put(PLANT_B, 22, 7); c.put(PLANT_A, 13, 3)
    # remise (rouille)
    c.put(SHELF, 1, 3); c.put(CRATE, 9, 2); c.put(CRATE, 9, 3); c.put(LOCKER, 7, 1); c.put(MAT, 3, 7); c.put(PAPERS, 6, 6); c.put(CRATE, 1, 8)
    # hall
    c.put(BOARD, 8, 11); c.put(CRATE, 1, 12); c.put(CRATE, 1, 13); c.put(CRATE, 22, 13); c.put(CRATE, 22, 12); c.put(MAT, 10, 14); c.put(PAPERS, 5, 15)
    c.put(SHELF, 12, 12)
    # remise sud
    c.put(CRATE, 1, 22); c.put(CRATE, 1, 23); c.put(CRATE, 2, 23); c.put(SHELF, 6, 21); c.put(PAPERS, 7, 23); c.put(MAT, 4, 23)
    # sas
    c.put(TERM, 17, 18); c.put(PLANT_A, 14, 22); c.put(PLANT_B, 22, 22)
    return c, A

def load(name, w, h, blue):
    """mazes d'origine : zone reprise = rectangles 'blue' [(x0,y0,x1,y1)]"""
    c = Cv(w, h); g = orig(name)
    c.g = list(g)
    for r in blue: c.zone(*r, 1)
    return c

def b2f():
    c = load('B2F', 32, 22, [(17, 0, 31, 21)]); return c, {}

def b3f():
    c = load('B3F', 22, 27, [(15, 4, 21, 26), (0, 0, 21, 3)]); return c, {}
if __name__ == '__main__':
    import sys; sys.path.insert(0, '/home/claude/pkmn-topaze/tools/topaze/maps'); import mapkit
    which = sys.argv[1] if len(sys.argv) > 1 else 'b1f'
    c, A = globals()[which](); print(A); print(c.ascii())
    L = mapkit.Layout('LAYOUT_ROCKET_HIDEOUT_B1F'); L.w, L.h, L.g = c.w, c.h, c.g
    L.render().convert('RGB').save('/tmp/gx/n%s.png' % which)
