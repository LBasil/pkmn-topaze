# Rendu d'une carte Pokemon Emeraude (../pokeemerald) pour choisir des morceaux : python3 emrender.py <Layout> <w> <h> <primaire> <secondaire> out.png
import sys, struct
from PIL import Image
EM = '../pokeemerald/data/'
def pal(path):
    L = open(path).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def load(pri, sec):
    P = EM + 'tilesets/primary/%s/' % pri; S = EM + 'tilesets/secondary/%s/' % sec
    pt = Image.open(P + 'tiles.png'); st = Image.open(S + 'tiles.png')
    pals = [pal(P + 'palettes/%02d.pal' % i) for i in range(6)] + [pal(S + 'palettes/%02d.pal' % i) for i in range(6, 13)]
    mp = struct.unpack('<%dH' % (len(open(P + 'metatiles.bin', 'rb').read()) // 2), open(P + 'metatiles.bin', 'rb').read())
    ms = struct.unpack('<%dH' % (len(open(S + 'metatiles.bin', 'rb').read()) // 2), open(S + 'metatiles.bin', 'rb').read())
    return pt, st, pals, mp, ms
def tile(pt, st, pals, t, p, hf, vf):
    img, idx = (pt, t) if t < 512 else (st, t - 512)
    w = img.size[0] // 8
    c = img.crop(((idx % w) * 8, (idx // w) * 8, (idx % w) * 8 + 8, (idx // w) * 8 + 8)).convert('P')
    px = img.convert('P') if False else None
    raw = Image.open((EM + 'tilesets/primary/%s/tiles.png') if False else img.filename).crop(((idx % w) * 8, (idx // w) * 8, (idx % w) * 8 + 8, (idx // w) * 8 + 8))
    raw = raw.convert('P') if raw.mode != 'P' else raw
    out = Image.new('RGBA', (8, 8)); o = out.load(); r = raw.load()
    for y in range(8):
        for x in range(8):
            i = r[x, y]
            o[x, y] = (0, 0, 0, 0) if i == 0 else pals[p][i] + (255,)
    if hf: out = out.transpose(Image.FLIP_LEFT_RIGHT)
    if vf: out = out.transpose(Image.FLIP_TOP_BOTTOM)
    return out
def metatile(L, m):
    pt, st, pals, mp, ms = L
    e = mp[m * 8:m * 8 + 8] if m < 512 else ms[(m - 512) * 8:(m - 512) * 8 + 8]
    im = Image.new('RGBA', (16, 16), pals[0][0] + (255,))
    for layer in (0, 1):
        for k in range(4):
            v = e[layer * 4 + k]
            t = tile(pt, st, pals, v & 0x3ff, v >> 12, v & 0x400, v & 0x800)
            im.alpha_composite(t, ((k % 2) * 8, (k // 2) * 8))
    return im
if __name__ == '__main__':
    name, w, h, pri, sec, out = sys.argv[1:7]; w = int(w); h = int(h)
    L = load(pri, sec); d = open(EM + 'layouts/%s/map.bin' % name, 'rb').read()
    g = struct.unpack('<%dH' % (w * h), d)
    cache = {}; im = Image.new('RGBA', (w * 16, h * 16))
    for y in range(h):
        for x in range(w):
            m = g[y * w + x] & 0x3ff
            if m not in cache: cache[m] = metatile(L, m)
            im.paste(cache[m], (x * 16, y * 16))
    im.convert('RGB').save(out); print(im.size)
