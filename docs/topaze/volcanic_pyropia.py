# Ambiance volcanique de Pyropia : ajoute des tuiles/metatuiles (basalte, lave, roche, geyser) au tileset
# secondaire PewterCity et repeint la carte. A lancer UNE fois depuis un depot propre.
import struct, random, sys, os
from PIL import Image, ImageDraw
sys.path.insert(0, 'tools/topaze/maps')
from mapkit import Layout
D = 'data/tilesets/secondary/pewter_city/'
rnd = random.Random(7)
PAL = [(0,0,0),(58,46,46),(44,34,36),(74,60,58),(92,76,70),(28,22,26),(130,50,30),(200,70,24),
       (240,110,30),(255,170,50),(255,226,120),(140,130,130),(100,92,96),(170,40,30),(255,255,255),(10,8,10)]
mt = bytearray(open(D+'metatiles.bin','rb').read()); NMT = len(mt)//16
assert NMT == 79, 'deja applique ?'
att = bytearray(open(D+'metatile_attributes.bin','rb').read())
png = Image.open(D+'tiles.png'); assert png.size == (128,144)
ntiles0 = 16*18
tiles = []          # liste de tuiles 8x8 (tuple de 64 index)
def add_tile(t):
    t = tuple(t)
    if t in tiles: return tiles.index(t)
    tiles.append(t); return len(tiles)-1
def new_meta(img, top=None, collide=False):
    """img: Image 'P' 16x16 (couche basse). top: Image 'P' 16x16 couche haute (0 = transparent)."""
    ents = []
    for layer in (img, top):
        for q in range(4):
            if layer is None: ents.append(0); continue
            x, y = (q%2)*8, (q//2)*8
            t = layer.crop((x,y,x+8,y+8)); px = list(t.getdata())
            if layer is top and not any(px): ents.append(0); continue   # tuile 0 primaire = vide
            ents.append((640 + ntiles0 + add_tile(px)) | (12 << 12))
    mt.extend(struct.pack('<8H', *ents)); att.extend(struct.pack('<I', 0))
    return 640 + NMT + (len(mt)//16 - NMT - 1)
def canvas(w,h,fill=1):
    im = Image.new('P',(w,h),fill); im.putpalette([c for p in PAL for c in p]); return im
def basalt(im, box, dens=1.0):
    px = im.load(); x0,y0,x1,y1 = box
    for y in range(y0,y1):
        for x in range(x0,x1):
            r = rnd.random()
            px[x,y] = 2 if r < .10*dens else 3 if r < .16*dens else 4 if r < .175*dens else 1
def crack(im):
    d = ImageDraw.Draw(im); x,y = rnd.randint(2,5), 0; pts=[(x,y)]
    while y < 15:
        y += rnd.randint(2,4); x = max(1,min(14,x+rnd.randint(-3,3))); pts.append((x,min(y,15)))
    d.line(pts, fill=6, width=1)
    for (a,b) in pts[1:-1]: d.point((a,b), fill=8); d.point((a+1,b), fill=7)
    return im
# ---- metatuiles de sol (basalte) ----
BAS = []
for i in range(4):
    im = canvas(16,16); basalt(im,(0,0,16,16), 1.0 if i<3 else 1.6); BAS.append(new_meta(im))
CRK = []
for i in range(2):
    im = canvas(16,16); basalt(im,(0,0,16,16)); CRK.append(new_meta(crack(im)))
# ---- roche (murs / bordure) ----
ROCK = []
for i in range(3):
    im = canvas(16,16,5); px = im.load()
    for y in range(16):
        for x in range(16):
            r = rnd.random(); px[x,y] = 2 if r<.35 else 1 if r<.55 else 5
    d = ImageDraw.Draw(im)
    for _ in range(3):
        x,y = rnd.randint(0,10), rnd.randint(0,10); d.line([(x,y),(x+rnd.randint(2,5),y)], fill=4); d.line([(x,y),(x,y+rnd.randint(1,3))], fill=3)
    ROCK.append(new_meta(im))
# ---- bassin de lave 4x3 ----
PW,PH = 4,3
pool = canvas(PW*16,PH*16); basalt(pool,(0,0,PW*16,PH*16))
d = ImageDraw.Draw(pool); w,h = PW*16,PH*16
d.ellipse((3,3,w-4,h-4), fill=5)          # bord obsidienne
d.ellipse((5,5,w-6,h-6), fill=13)         # lueur rouge
d.ellipse((7,7,w-8,h-8), fill=7)          # lave
px = pool.load()
for y in range(9,h-9):
    for x in range(9,w-9):
        if (x*3+y*5+(x*y)%7)%9 < 2: px[x,y] = 8
        elif (x+2*y)%11 == 0: px[x,y] = 9
        elif (x*y)%23 == 0: px[x,y] = 10
POOL = {}
for ty in range(PH):
    for tx in range(PW):
        POOL[(tx,ty)] = new_meta(pool.crop((tx*16,ty*16,tx*16+16,ty*16+16)))
# ---- geyser : cratere + fumee (couche haute) ----
g = canvas(16,16); basalt(g,(0,0,16,16)); dg = ImageDraw.Draw(g)
dg.ellipse((3,7,12,14), fill=5); dg.ellipse((5,9,10,13), fill=2); dg.point((7,11), fill=13)
smoke = canvas(16,16,0); ds = ImageDraw.Draw(smoke)
for (x,y,r,c) in [(7,6,3,12),(9,3,3,11),(6,1,2,11),(10,7,2,12)]: ds.ellipse((x-r,y-r,x+r,y+r), fill=c)
VENT = new_meta(g, smoke)
open(D+'metatiles.bin','wb').write(mt); open(D+'metatile_attributes.bin','wb').write(att)
# ---- png des tuiles ----
rows = (ntiles0 + len(tiles) + 15)//16
assert ntiles0 + len(tiles) <= 384, 'trop de tuiles: %d' % (ntiles0+len(tiles))
out = Image.new('P',(128,rows*8),0); out.putpalette(png.getpalette()); out.paste(png,(0,0))
for i,t in enumerate(tiles):
    n = ntiles0 + i; tim = Image.new('P',(8,8)); tim.putdata(list(t)); out.paste(tim,((n%16)*8,(n//16)*8))
out.save(D+'tiles.png')
# ---- palette 12 ----
open(D+'palettes/12.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n'%c for c in PAL))
# ---- carte ----
L = Layout('LAYOUT_PEWTER_CITY'); w,h = L.w,L.h
GRASS = {1,8,9,16,17} | set(range(189,208)); TREES = {14,15,20,21,22,23,28,29,30,31,36,37}
def blk(x,y): return L.get(x,y)&0x3ff
use = [(4,2),(35,1)]
GEY = [(9,3),(34,3)]
for y in range(h):
    for x in range(w):
        v = L.get(x,y); m = v&0x3ff; rest = v & ~0x3ff
        if m in GRASS: L.set(x,y, rest | rnd.choice(BAS+BAS+CRK))
        elif m in TREES: L.set(x,y, rest | rnd.choice(ROCK))
for (sx,sy) in use:
    for ty in range(PH):
        for tx in range(PW):
            v = L.get(sx+tx,sy+ty); L.set(sx+tx,sy+ty,(v & ~0x3ff & ~0xc00) | 0x400 | POOL[(tx,ty)])
for (gx,gy) in GEY:
    v=L.get(gx,gy); L.set(gx,gy,(v&~0x3ff&~0xc00)|0x400|VENT)
L.save()
print('tuiles ajoutees',len(tiles),'metatuiles',len(mt)//16)
