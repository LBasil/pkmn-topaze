#!/usr/bin/env python3
"""Mini Porymap : lecture/écriture de map.bin et rendu PNG d'une carte (tuiles + palettes).
Usage : python3 mapkit.py render <LAYOUT_ID> out.png [x0 y0 x1 y1]"""
import json, struct, sys, os
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
TS = {'gTileset_General': 'data/tilesets/primary/general', 'gTileset_GeneralEmerald': 'data/tilesets/primary/general_emerald', 'gTileset_GeneralOpal': 'data/tilesets/primary/general_opal', 'gTileset_GeneralGradient': 'data/tilesets/primary/general_gradient', 'gTileset_GeneralEmber': 'data/tilesets/primary/general_ember', 'gTileset_GeneralDusk': 'data/tilesets/primary/general_dusk', 'gTileset_GeneralCinder': 'data/tilesets/primary/general_cinder', 'gTileset_GeneralScoria': 'data/tilesets/primary/general_scoria', 'gTileset_GeneralMoon': 'data/tilesets/primary/general_moon', 'gTileset_GeneralTourmaline': 'data/tilesets/primary/general_tourmaline'}
def ts_dir(name):
    if name in TS: return os.path.join(ROOT, TS[name])
    # gTileset_PalletTown -> secondary/pallet_town
    import re
    snake = re.sub(r'(?<!^)(?=[A-Z0-9])', '_', name.replace('gTileset_', '')).lower()
    snake = re.sub(r'_(\d)_(\d)', r'_\1\2', snake)
    for base in ('data/tilesets/secondary', 'data/tilesets/primary'):
        p = os.path.join(ROOT, base, snake)
        if os.path.isdir(p): return p
    raise KeyError(name)
def layouts():
    return {l['id']: l for l in json.load(open(os.path.join(ROOT, 'data/layouts/layouts.json')))['layouts'] if 'id' in l}
def read_pal(path):
    L = open(path).read().split()
    n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * i:6 + 3 * i]) for i in range(n)]
class Tileset:
    def __init__(self, name):
        d = ts_dir(name); self.d = d
        self.metatiles = open(os.path.join(d, 'metatiles.bin'), 'rb').read()
        self.img = Image.open(os.path.join(d, 'tiles.png'))   # indexed
        self.pals = {}
        pd = os.path.join(d, 'palettes')
        for i in range(16):
            f = os.path.join(pd, '%02d.pal' % i)
            if os.path.exists(f): self.pals[i] = read_pal(f)
class Layout:
    def __init__(self, lid):
        self.l = layouts()[lid]; self.w = self.l['width']; self.h = self.l['height']
        self.path = os.path.join(ROOT, self.l['blockdata_filepath'])
        d = open(self.path, 'rb').read()
        self.g = list(struct.unpack('<%dH' % (self.w * self.h), d))
        self.prim = Tileset(self.l['primary_tileset']); self.sec = Tileset(self.l['secondary_tileset'])
    def save(self): open(self.path, 'wb').write(struct.pack('<%dH' % len(self.g), *self.g))
    def get(self, x, y): return self.g[y * self.w + x]
    def set(self, x, y, v): self.g[y * self.w + x] = v
    def metatile_img(self, mid, cache={}):
        key = (id(self), mid)
        if key in cache: return cache[key]
        ts, idx = (self.prim, mid) if mid < 640 else (self.sec, mid - 640)
        pal_all = {}
        for tsx in (self.prim, self.sec): pass
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        raw = ts.metatiles[idx * 16:(idx + 1) * 16]
        ents = struct.unpack('<8H', raw)
        for layer in range(2):
            for q in range(4):
                e = ents[layer * 4 + q]
                tid, hf, vf, pal = e & 0x3ff, (e >> 10) & 1, (e >> 11) & 1, e >> 12
                src = self.prim if tid < 640 else self.sec
                t = tid if tid < 640 else tid - 640
                tw = src.img.width // 8
                tile = src.img.crop(((t % tw) * 8, (t // tw) * 8, (t % tw) * 8 + 8, (t // tw) * 8 + 8))
                if hf: tile = tile.transpose(Image.FLIP_LEFT_RIGHT)
                if vf: tile = tile.transpose(Image.FLIP_TOP_BOTTOM)
                pals = self.prim.pals if pal < 7 else self.sec.pals
                p = pals.get(pal, [(255, 0, 255)] * 16)
                rgba = Image.new('RGBA', (8, 8))
                px = tile.load(); out = rgba.load()
                for yy in range(8):
                    for xx in range(8):
                        c = px[xx, yy]
                        if c == 0 and layer == 1: out[xx, yy] = (0, 0, 0, 0)
                        else: out[xx, yy] = p[c] + (255,)
                im.alpha_composite(rgba, ((q % 2) * 8, (q // 2) * 8))
        cache[key] = im
        return im
    def render(self, box=None):
        x0, y0, x1, y1 = box or (0, 0, self.w, self.h)
        out = Image.new('RGBA', ((x1 - x0) * 16, (y1 - y0) * 16))
        for y in range(y0, y1):
            for x in range(x0, x1):
                out.paste(self.metatile_img(self.get(x, y) & 0x3ff), ((x - x0) * 16, (y - y0) * 16))
        return out
if __name__ == '__main__':
    if sys.argv[1] == 'render':
        L = Layout(sys.argv[2]); box = tuple(int(v) for v in sys.argv[4:8]) if len(sys.argv) >= 8 else None
        im = L.render(box); im.convert('RGB').save(sys.argv[3]); print(im.size)
