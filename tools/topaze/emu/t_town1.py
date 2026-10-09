from townlib import *
L = []; cur = (8, 10)
STEPS = [((10, 10), 'UP', 'sgn_player'), ((9, 15), 'RIGHT', 'sgn_tips'), ((10, 17), 'UP', 'lady_sign'), ((11, 22), 'UP', 'sgn_museum'),
         ((21, 11), 'UP', 'sgn_town'), ((18, 22), 'RIGHT', 'oldman')]
for tgt, face, name in STEPS:
    m, cur = go(cur, tgt); L += m + ['readp 03005008 0 6'] + talk(face, name, 3)
fromstate('town1', L)
