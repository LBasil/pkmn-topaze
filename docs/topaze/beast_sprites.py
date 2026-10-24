#!/usr/bin/env python3
"""Sprites overworld 32x32 de Raikou / Entei / Suicune, DESSINES A LA MAIN (pixel art, de face, aplats + contour), dans le style de Sulfura/Artikodin.
Chaque bete : moitie gauche en texte (12 colonnes), miroir automatique ; extras = pixels asymetriques (queue de Raikou). Ecrit le PNG indexe (index 0 = transparent) et la palette .pal."""
import os
from PIL import Image
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + '/'
TRANSP = (115, 197, 164)
def render(rows_half, pal, extra=None, out=None, scale=10, name='x'):
    rows=[]
    for r in rows_half:
        assert len(r)==len(rows_half[0]),(len(r),r)
        rows.append(r+r[::-1])
    pad=4 if extra else 0
    h=len(rows); w=len(rows[0])+pad; g=[list(r)+['.']*pad for r in rows]
    if extra:
        for (x,y,c) in extra: g[y][x]=c
    return g,pal
# ---------- RAIKOU ----------
P_R={'K':(40,28,48),'Y':(248,208,56),'y':(214,158,28),'P':(120,80,190),'p':(168,130,226),'Q':(76,44,124),
     'W':(250,250,250),'g':(188,190,206),'B':(48,36,64),'R':(226,56,56),'N':(60,40,40)}
H_R=[
".KK...KK....",
"KPPK.KYYK...",
"KPpPKKYQYK..",
"KPpPPKYYYYK.",
"KpPPPPKYYYYY",
"KpPPPPPKYYBB",
"KPpPPPPQKYYY",
".KPpPPPQKRKY",
".KPPPPQQKYYY",
"..KPPQKKWWYY",
"..KPPQKWWWWN",
"..KpPQKWWWWW",
"...KPQKWWWKK",
"....KQKKWWWW",
"...KPPQKgWWW",
"..KPPQKYYgWW",
".KPPQKYYyYgW",
".KQQKYYBYyYg",
"..KKKYyYBYyY",
"....KYYyYB..",
"....KYyYYB..",
"....KBBBBB..",
"....KYYYYY..",
"....KWWWWW..",
".....KKKKK..",
]
BOLT_R=[(24,14,'g'),(25,14,'g'),(24,15,'g'),(25,15,'W'),(25,16,'g'),(26,16,'W'),(27,16,'g'),(26,17,'W'),(27,17,'g'),(25,18,'W'),(26,18,'g'),(24,19,'g'),(25,19,'W'),(24,20,'g')]
# ---------- ENTEI ----------
P_E={'K':(46,28,22),'B':(176,116,52),'b':(122,76,34),'T':(236,200,146),'W':(250,250,250),'R':(214,52,40),'r':(150,30,28),'G':(206,206,218),'g':(150,150,168),'N':(30,20,20),'E':(255,208,64)}
H_E=[
"....K.K.KK..",
"...KBKBKBBKK",
"..KBBBBBBBRR",
".KBBbBBBBRWW",
".KBbBBBBBRWR",
"KBBBBBBBTTRR",
"KBbBBBBTTTTT",
"KBBbBBTTENTT",
"KBBBBBTTTTTT",
".KBbBBKTTTNN",
".KBBBBKTTWWW",
"..KBbBKKTWWW",
"..KKBBBKKKKK",
".KGKKBBBBTTT",
"KGGKBbBBBTTT",
"KgGKBBBBBbbB",
".KgKBbBBBBbB",
"..KKBBBBbBBB",
"....KBbBBBbB",
"....KBBBBBBB",
".....KbbbbN.",
".....KBBBBN.",
".....KTTTTN.",
"......KKKK..",
]
# ---------- SUICUNE ----------
P_S={'K':(28,36,70),'B':(110,170,235),'b':(70,120,200),'L':(186,224,250),'W':(250,250,250),'P':(130,84,190),'p':(176,138,226),'Q':(86,50,140),'C':(236,90,150),'N':(30,30,60)}
H_S=[
"..........KK",
".........KLL",
"....KK..KBLL",
"...KPPKKBBLB",
"..KPpPPKBBBB",
".KPpPQKBBBBB",
"KPpPPQKBCKBB",
"KPPpPQKBBBBB",
"KPpPQKBBLLLL",
"KPpPQKBLLLLN",
".KPpQKBLLLLL",
".KPpQKKLLLKK",
".KPPQKBBLLLL",
"..KPQKBBWWWW",
"..KPQKBBLWWW",
"..KPQKBbBLWW",
"..KPpQKBbBLW",
"...KPQKBbBBL",
"...KPQKBBbBB",
".....KBbBB..",
".....KBbBB..",
".....KBBBb..",
".....KLLLL..",
".....KKKKK..",
]

def export(name, half, pal, extra=None):
    g, _ = render(half, pal, extra)
    h, w = len(g), len(g[0])
    if extra:      # contour sombre autour des pixels asymetriques
        ex = {(x, y) for x, y, _ in extra}
        for (x, y) in ex:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                X, Y = x + dx, y + dy
                if 0 <= X < w and 0 <= Y < h and g[Y][X] == '.': g[Y][X] = 'K'
    letters = []
    for row in g:
        for c in row:
            if c != '.' and c not in letters: letters.append(c)
    letters.sort(key=lambda c: (c != 'K', c))
    assert len(letters) <= 15, letters
    idx = {c: i + 1 for i, c in enumerate(letters)}
    img = Image.new('P', (32, 32), 0); ip = img.load()
    ox = (32 - w) // 2; oy = 31 - h
    for y in range(h):
        for x in range(w):
            if g[y][x] != '.': ip[ox + x, oy + y] = idx[g[y][x]]
    full = [TRANSP] + [pal[c] for c in letters]; full += [(0, 0, 0)] * (16 - len(full))
    img.putpalette([v for c in full for v in c] + [0] * (768 - 48))
    img.save(R + f'graphics/object_events/pics/pokemon/{name}.png')
    with open(R + f'graphics/object_events/palettes/{name}.pal', 'w') as f:
        f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in full))
    print(name, w, h, len(letters), 'couleurs')

if __name__ == '__main__':
    export('raikou', H_R, P_R, BOLT_R)
    export('entei', H_E, P_E)
    export('suicune', H_S, P_S)
