import ast, sys, os, math, random, struct, collections, numpy as np
from PIL import Image, ImageDraw, ImageFilter
os.chdir('/home/claude/pkmn-topaze'); sys.path.insert(0, 'docs/topaze'); sys.path.insert(0, '/tmp/recopy')
import maprender as M, classify as C
# ---- elements du jeu (tilesets Tourmalia)
P = M.loadts('gTileset_GeneralTourmaline'); S = M.loadts('gTileset_FortreeTourmaline')
pals = [P[1][i] for i in range(7)] + [S[1][i] for i in range(7, 13)] + [S[1][13], S[1][14], S[1][15]]
def mt(m): return M.metatile(P, S, pals, m).convert('RGB')
GRASS_IM = mt(1); FLOW_IM = mt(4)
TREES = {k: mt(k) for k in (14, 15, 198, 199, 468, 469, 476, 477)}
SAND = {k: mt(k) for k in range(280, 299)}
# ---- fonctions de dessin du generateur
src = open('docs/topaze/tourmalia_river.py').read(); tree = ast.parse(src)
want = {'newimg', 'shadow', 'vnoise', 'water_img', 'plank_img', 'cliff_img', 'pave_img', 'palm_img', 'rock_img'}
G = dict(math=math, random=random, np=np, Image=Image, ImageDraw=ImageDraw, ImageFilter=ImageFilter)
for n in tree.body:
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'PAL': exec(compile(ast.Module([n], []), 'x', 'exec'), G)
    if isinstance(n, ast.FunctionDef) and n.name in want: exec(compile(ast.Module([n], []), 'x', 'exec'), G)
GR = tuple(int(np.asarray(GRASS_IM)[:, :, k].mean()) for k in range(3))
WPAL = [(0, 0, 0), (22, 78, 104), (44, 120, 190), (82, 162, 226), (130, 200, 246), (228, 246, 255), tuple(int(v * 0.70) for v in GR), tuple(int(v * 0.84) for v in GR),
        (70, 44, 24), (150, 104, 64), (206, 156, 96), (52, 36, 28), (30, 110, 70), (64, 164, 96), (255, 170, 200), (255, 232, 136)]
def topil(ix, pal):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load(); a = ix.load()
    for y in range(16):
        for x in range(16):
            if a[x, y]: px[x, y] = tuple(pal[a[x, y]]) + (255,)
    return im
def on_grass(ix, pal):
    b = GRASS_IM.convert('RGBA'); b.alpha_composite(topil(ix, pal)); return b.convert('RGB')
# ---- maisons d'Emeraude (Petalburg)
EM = '../pokeemerald/data/'
FT = struct.unpack('<900H', open(EM + 'layouts/PetalburgCity/map.bin', 'rb').read())
def chunk_im(x0, y0, cw, ch):
    im = Image.new('RGB', (cw * 16, ch * 16))
    for j in range(ch):
        for i in range(cw):
            m = FT[(y0 + j) * 30 + x0 + i] & 0x3ff
            im.paste(mt(m) if m < 640 else GRASS_IM, (i * 16, j * 16))
    return im
HOUSE_A = chunk_im(5, 2, 5, 4); HOUSE_B = chunk_im(9, 16, 4, 4); CENTER = chunk_im(19, 13, 4, 4); MART = chunk_im(24, 10, 4, 3); GYM = chunk_im(12, 4, 6, 5)
def render(name, path, box, outname):
    im, w, h, lab = C.classify(path, box, K=11) if False else (None, None, None, None)
def render_job(key, outname):
    im, w, h, lab = C.classify_rules(*C.JOBS[key])
    L = lambda x, y: lab[y, x] if 0 <= x < w and 0 <= y < h else 'tree'
    WATERS = {(x, y) for y in range(h) for x in range(w) if lab[y, x] == 'water'}
    # ponts : sable entre deux eaux
    BR = set()
    for y in range(h):
        for x in range(w):
            if lab[y, x] != 'sand': continue
            hz = any((x - a, y) in WATERS for a in (1, 2, 3)) and any((x + a, y) in WATERS for a in (1, 2, 3))
            vt = any((x, y - a) in WATERS for a in (1, 2, 3)) and any((x, y + a) in WATERS for a in (1, 2, 3))
            if hz or vt: BR.add((x, y))
    WAT = WATERS | BR
    CLIFFS = {(x, y) for y in range(h) for x in range(w) if lab[y, x] in ('cliff', 'rock')}
    SANDS = {(x, y) for y in range(h) for x in range(w) if lab[y, x] == 'sand'} - BR
    PAVES = {(x, y) for y in range(h) for x in range(w) if lab[y, x] == 'pave'}
    TREESS = {(x, y) for y in range(h) for x in range(w) if lab[y, x] == 'tree'}
    G.update(WAT=WAT, BRIDGEC=BR, CLIFF=CLIFFS, STAIRS=set())
    out = Image.new('RGB', (w * 16, h * 16)); rr = random.Random(7)
    done = set()
    # batiments : composantes de toits
    roofs = {(x, y) for y in range(h) for x in range(w) if lab[y, x] == 'roof'}
    seen = set(); comps = []
    for c in sorted(roofs):
        if c in seen: continue
        st = [c]; comp = []; seen.add(c)
        while st:
            u = st.pop(); comp.append(u)
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                n = (u[0] + d[0], u[1] + d[1])
                if n in roofs and n not in seen: seen.add(n); st.append(n)
        if len(comp) >= 3: comps.append(comp)
    blds = []
    for comp in comps:
        xs = [c[0] for c in comp]; ys = [c[1] for c in comp]; x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys); bw = x1 - x0 + 1
        img = CENTER if (len(comp) >= 12 and bw >= 4) else (HOUSE_A if bw >= 5 else HOUSE_B)
        bx = x0 + (bw - img.width // 16) // 2 if bw < 4 else x0
        blds.append((img, bx, y0))
        for j in range(img.height // 16):
            for i in range(img.width // 16): done.add((bx + i, y0 + j))
    for y in range(h):
        for x in range(w):
            c = (x, y)
            if c in done: continue
            l = lab[y, x]
            if c in BR:
                ix = G['plank_img'](c); tile = topil(ix, WPAL).convert('RGB')
            elif c in WATERS:
                ix = G['water_img'](c, WAT); tile = on_grass(ix, WPAL)
            elif c in CLIFFS:
                ix = G['cliff_img'](c); tile = on_grass(ix, WPAL)
            elif c in PAVES and any((x + a, y + b) in WATERS for a in (-1, 0, 1) for b in (-1, 0, 1)):
                b_ = on_grass(G['water_img'](c, WAT), WPAL).convert('RGBA'); b_.alpha_composite(topil(G['rock_img'](rr.randint(0, 1)), G['PAL'])); tile = b_.convert('RGB')
            elif c in PAVES:
                ix = G['pave_img']((x + y) % 2); tile = topil(ix, G['PAL']).convert('RGB')
            elif c in SANDS:
                f = lambda q: q in SANDS or q in BR or q in PAVES or not (0 <= q[0] < w and 0 <= q[1] < h)
                N = f((x, y - 1)); Sx = f((x, y + 1)); Wn = f((x - 1, y)); E_ = f((x + 1, y))
                if N and Sx and Wn and E_: i_ = 289
                elif not N and not Wn and Sx and E_: i_ = 280
                elif not N and not E_ and Sx and Wn: i_ = 282
                elif not Sx and not Wn and N and E_: i_ = 296
                elif not Sx and not E_ and N and Wn: i_ = 298
                elif not N and Sx and Wn and E_: i_ = 281
                elif not Sx and N and Wn and E_: i_ = 297
                elif not Wn and N and Sx and E_: i_ = 288
                elif not E_ and N and Sx and Wn: i_ = 290
                else: i_ = 289
                tile = SAND[i_]
            elif c in TREESS:
                bx, by = x - x % 2, y - y % 2
                blk = [(bx + i, by + j) for i in (0, 1) for j in (0, 1)]
                if all(q in TREESS for q in blk): tile = TREES[(468 if x % 2 == 0 else 469) if y % 2 == 0 else (476 if x % 2 == 0 else 477)]
                else: tile = TREES[rr.choice((14, 15, 198, 199))]
            else:
                tile = FLOW_IM if rr.random() < 0.07 else GRASS_IM
            out.paste(tile, (x * 16, y * 16))
    for img, bx, by in blds: out.paste(img, (bx * 16, by * 16))
    both = Image.new('RGB', (w * 32 + 16, h * 16), (30, 30, 30)); both.paste(im, (0, 0)); both.paste(out, (w * 16 + 16, 0))
    both.save('/tmp/recopy/%s_cmp.png' % outname); out.save('/tmp/recopy/%s.png' % outname)
    print(outname, w, h, 'eau', len(WATERS), 'ponts', len(BR), 'falaise', len(CLIFFS), 'maisons', len(blds))
if __name__ == '__main__':
    for k in sys.argv[1:]: render_job(k, 'recopie_' + k)
