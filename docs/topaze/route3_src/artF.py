# ---- art specifique a la foret
from PIL import ImageOps
def dead_img(st, var):
    im = ground_bg(32, 32, st); d = ImageDraw.Draw(im)
    d.ellipse((3, 25, 29, 31), fill=13)
    d.polygon([(12, 29), (13, 12), (17, 12), (19, 29)], fill=6, outline=5)
    for p, q in (((14, 14), (6, 5)), ((15, 12), (23, 3)), ((16, 19), (25, 11)), ((14, 21), (6, 15)), ((6, 5), (3, 7)), ((23, 3), (27, 4))):
        d.line([p, q], fill=5, width=3); d.line([p, q], fill=6, width=1)
    d.line([(14, 14), (14, 27)], fill=7); d.line([(16, 18), (16, 25)], fill=10)
    for p in ((6, 5), (23, 3), (25, 11), (6, 15)): d.point(p, fill=11)
    d.point((15, 13), fill=12)
    if var: im = ImageOps.mirror(im)
    return im
def log_img(st):
    im = ground_bg(32, 16, st); d = ImageDraw.Draw(im)
    d.ellipse((2, 11, 30, 15), fill=13)
    d.rounded_rectangle((1, 3, 30, 13), radius=4, fill=7, outline=5)
    d.line([(5, 5), (28, 5)], fill=8); d.line([(5, 12), (28, 12)], fill=6)
    for x in range(9, 28, 5): d.line([(x, 7), (x, 10)], fill=6)
    d.line([(14, 8), (20, 9)], fill=10); d.point((17, 8), fill=11)
    d.ellipse((0, 2, 7, 13), fill=14, outline=5); d.ellipse((2, 5, 5, 10), fill=6); d.point((3, 7), fill=10); d.point((3, 8), fill=11)
    return im
def crater_img(st):
    im = ground_bg(48, 48, st); d = ImageDraw.Draw(im)
    d.ellipse((1, 20, 47, 47), fill=13)
    d.ellipse((2, 6, 45, 42), fill=14, outline=5)
    d.ellipse((6, 11, 41, 37), fill=6, outline=5)
    d.ellipse((10, 15, 37, 33), fill=12)
    d.ellipse((14, 18, 33, 30), fill=10)
    d.ellipse((19, 21, 28, 27), fill=11)
    for p, q in (((24, 24), (8, 14)), ((24, 24), (40, 16)), ((24, 24), (36, 35)), ((24, 24), (12, 34))):
        d.line([p, q], fill=10)
    for p in ((6, 12), (42, 14), (38, 36), (10, 36), (24, 9)): d.point(p, fill=12)
    d.line([(6, 10), (16, 7)], fill=15); d.line([(30, 7), (40, 10)], fill=15)
    return im
def ash_img(st):
    im = ground_bg(16, 16, st); d = ImageDraw.Draw(im)
    d.ellipse((2, 10, 14, 15), fill=13); d.ellipse((1, 9, 14, 14), fill=7); d.ellipse((3, 8, 11, 12), fill=14)
    d.point((6, 10), fill=6); d.point((9, 11), fill=6)
    return im
def giant_img(st):
    im = ground_bg(48, 64, st); d = ImageDraw.Draw(im)
    d.ellipse((2, 52, 46, 63), fill=13)
    d.polygon([(4, 61), (13, 44), (15, 22), (33, 22), (35, 44), (44, 61), (30, 56), (18, 56)], fill=6, outline=5)
    for p, q in (((18, 28), (4, 10)), ((30, 24), (44, 4)), ((14, 38), (1, 32)), ((34, 36), (47, 26)), ((24, 22), (24, 2)), ((4, 10), (1, 14)), ((44, 4), (47, 8)), ((4, 10), (7, 1))):
        d.line([p, q], fill=5, width=6); d.line([p, q], fill=6, width=4)
    d.line([(19, 26), (17, 54)], fill=7); d.line([(27, 28), (28, 52)], fill=10); d.line([(24, 24), (24, 30)], fill=10)
    d.ellipse((20, 38, 28, 48), fill=5); d.ellipse((22, 40, 26, 46), fill=12); d.point((24, 43), fill=11)
    for p in ((6, 12), (40, 6), (4, 30), (45, 24), (22, 3), (8, 4)): d.point(p, fill=11)
    for p in ((15, 56), (33, 56), (19, 55)): d.point(p, fill=12)
    return im
def boulder_img(st):
    im = ground_bg(32, 32, st); d = ImageDraw.Draw(im)
    d.ellipse((1, 22, 31, 31), fill=13)
    d.polygon([(3, 27), (4, 13), (11, 5), (22, 4), (29, 12), (30, 27)], fill=14, outline=5)
    d.polygon([(17, 27), (18, 10), (22, 5), (29, 12), (30, 27)], fill=6)
    d.line([(6, 12), (12, 7), (20, 6)], fill=15); d.line([(10, 25), (14, 16), (21, 19)], fill=10); d.point((14, 17), fill=11); d.point((8, 20), fill=12)
    return im
def thorns_img(st):
    im = ground_bg(32, 32, st); d = ImageDraw.Draw(im)
    d.ellipse((2, 24, 30, 31), fill=13); d.ellipse((6, 21, 26, 29), fill=6, outline=5)
    for k, (x, tx, ty) in enumerate(((8, 3, 6), (12, 9, 3), (16, 16, 1), (20, 24, 4), (24, 29, 9), (14, 5, 14), (19, 27, 15))):
        d.line([(x, 24), (tx, ty)], fill=5, width=3); d.line([(x, 24), (tx, ty)], fill=6, width=1)
        d.point((tx, ty), fill=11 if k % 2 else 10)
    return im
def spire_img(st):
    im = ground_bg(32, 32, st); d = ImageDraw.Draw(im)
    d.ellipse((1, 24, 31, 31), fill=13)
    shape(d, st, 10, 28, 6, 22, -1); shape(d, st, 22, 29, 7, 26, 1); shape(d, st, 16, 30, 5, 13)
    return im
def lake_tile(x, y, st, var):
    im = ground_bg(16, 16, st); d = ImageDraw.Draw(im)
    n = (x, y - 1) in LAKE; so = (x, y + 1) in LAKE; w = (x - 1, y) in LAKE; e = (x + 1, y) in LAKE
    x0, y0, x1, y1 = (0 if w else 0), (0 if n else 0), 15, 15
    d.rectangle((0, 0, 15, 15), fill=14)
    L = 3 if not w else 0; R = 12 if not e else 15; T = 3 if not n else 0; B = 12 if not so else 15
    # rebord de roche : tout est roche, puis on creuse le bassin de lave
    d.rectangle((L, T, R, B), fill=6)
    ix0, iy0, ix1, iy1 = L + (1 if not w else 0), T + (1 if not n else 0), R - (1 if not e else 0), B - (1 if not so else 0)
    d.rectangle((ix0, iy0, ix1, iy1), fill=12)
    # coins rentrants : roche dans l'angle si les deux voisins existent mais pas la diagonale
    for (dx, dy, cx, cy) in ((-1, -1, 0, 0), (1, -1, 12, 0), (-1, 1, 0, 12), (1, 1, 12, 12)):
        if (x + dx, y) in LAKE and (x, y + dy) in LAKE and (x + dx, y + dy) not in LAKE: d.rectangle((cx, cy, cx + 3, cy + 3), fill=14); d.rectangle((cx + (0 if dx < 0 else 1), cy + (0 if dy < 0 else 1), cx + (2 if dx < 0 else 3), cy + (2 if dy < 0 else 3)), fill=6)
    if var == 2: d.polygon([(ix0 + 3, iy0 + 4), (ix0 + 8, iy0 + 3), (ix0 + 10, iy0 + 7), (ix0 + 5, iy0 + 8)], fill=6); d.point((ix0 + 6, iy0 + 5), fill=10); d.point((ix1 - 3, iy1 - 3), fill=11)
    elif var == 0: d.ellipse((ix0 + 2, iy0 + 3, ix0 + 7, iy0 + 6), fill=10); d.point((ix0 + 4, iy0 + 4), fill=11); d.ellipse((ix1 - 6, iy1 - 4, ix1 - 2, iy1 - 2), fill=10)
    else: d.ellipse((ix1 - 7, iy0 + 2, ix1 - 2, iy0 + 5), fill=10); d.point((ix1 - 4, iy0 + 3), fill=11); d.ellipse((ix0 + 2, iy1 - 5, ix0 + 6, iy1 - 2), fill=10); d.point((ix0 + 4, iy1 - 4), fill=11)
    # contour exterieur de la roche
    for (cond, line) in ((not n, (0, 0, 15, 0)), (not so, (0, 15, 15, 15)), (not w, (0, 0, 0, 15)), (not e, (15, 0, 15, 15))):
        if cond: d.line(line, fill=5)
    # ombre cote sud / roche claire cote nord
    if not n: d.line((1, 1, 14, 1), fill=15)
    return im
for st in (2,):
    b = giant_img(st); ART[('giant', st)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(4) for i in range(3)}
    for var in (0, 1):
        b = dead_img(st, var); ART[('dead', st, var)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(2) for i in range(2)}
    b = log_img(st); ART[('log', st)] = [meta(b.crop((0, 0, 16, 16)), st), meta(b.crop((16, 0, 32, 16)), st)]
    b = crater_img(st); ART[('crater', st)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(3) for i in range(3)}
    ART[('ash', st)] = meta(ash_img(st), st)
    for nm, fn in (('boulder', boulder_img), ('thorns', thorns_img), ('spire', spire_img)):
        b = fn(st); ART[(nm, st)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(2) for i in range(2)}
    ART[('volcano', st)] = {c: meta(lake_tile(c[0], c[1], st, (c[0] * 3 + c[1] * 5) % 3), st) for c in LAKE}
