"""Boite a outils pour dessiner une arene de A a Z (tuiles dessinees en code) :
Spr = sprite 16x16 en lettres, Pal = palette nommee, TS = tileset secondaire (tuiles dedoublonnees + metatuiles + attributs),
puis ecriture dans data/tilesets/secondary/<dir>/ et data/layouts/<dir>/map.bin. Idempotent."""
import os, struct, random, math
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MAGENTA = (255, 0, 255)
class Pal:
    def __init__(s, letters, colors):
        assert len(letters) == len(colors) <= 15
        s.l = letters; s.c = list(colors)
    def idx(s, ch): return s.l.index(ch) + 1
    def rgb(s): return [MAGENTA] + s.c + [(0, 0, 0)] * (15 - len(s.c))
class Spr:
    """16x16 de lettres ; '.' = vide"""
    def __init__(s, fill='.'): s.g = [[fill] * 16 for _ in range(16)]
    @staticmethod
    def parse(rows, w=16):
        s = Spr(); rows = rows[:16]
        for y, r in enumerate(rows):
            for x, ch in enumerate(r[:w]): s.g[y][x] = ch
        return s
    def px(s, x, y, c):
        if 0 <= x < 16 and 0 <= y < 16: s.g[y][x] = c
    def rect(s, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): s.px(x, y, c)
    def noise(s, cs, p, seed, only=None):
        r = random.Random(seed)
        for y in range(16):
            for x in range(16):
                if only and s.g[y][x] not in only: continue
                if r.random() < p: s.g[y][x] = r.choice(cs)
        return s
    def over(s, o, dx=0, dy=0):
        for y in range(16):
            for x in range(16):
                if o.g[y][x] != '.': s.px(x + dx, y + dy, o.g[y][x])
        return s
    def copy(s):
        n = Spr(); n.g = [r[:] for r in s.g]; return n
    def hflip(s):
        n = Spr(); n.g = [r[::-1] for r in s.g]; return n
class TS:
    def __init__(s, pals):
        s.pals = pals          # {numero 7..12: Pal}
        s.tiles = [tuple([0] * 64)]      # tuile 0 = vide
        s.tmap = {s.tiles[0]: 0}
        s.mts = []; s.attrs = []; s.names = {}
        s.add('black', Spr.parse(['k' * 16] * 16), 7, 0, letters_override={'k': 1})
    def _tile(s, px):
        """px : 64 indices ; renvoie (id, hflip, vflip)"""
        px = tuple(px)
        for hf in (0, 1):
            for vf in (0, 1):
                q = [px[(7 - y if vf else y) * 8 + (7 - x if hf else x)] for y in range(8) for x in range(8)]
                t = tuple(q)
                if t in s.tmap: return s.tmap[t], hf, vf
        s.tiles.append(px); s.tmap[px] = len(s.tiles) - 1
        return len(s.tiles) - 1, 0, 0
    def add(s, name, spr, pal, beh=0, letters_override=None):
        P = s.pals[pal]; ents = []
        for qy in range(2):
            for qx in range(2):
                px = []
                for y in range(8):
                    for x in range(8):
                        ch = spr.g[qy * 8 + y][qx * 8 + x]
                        if letters_override: v = letters_override[ch]
                        else:
                            assert ch != '.', (name, qx * 8 + x, qy * 8 + y)
                            v = P.idx(ch)
                        px.append(v)
                tid, hf, vf = s._tile(px)
                ents.append((tid, hf, vf, pal))
        s.mts.append(ents); s.attrs.append(beh); s.names[name] = len(s.mts) - 1
        return 640 + len(s.mts) - 1
    def id(s, name): return 640 + s.names[name]
    def preview(s, spr_pal):
        pass
    def write(s, sec_dir):
        assert len(s.tiles) <= 384 and len(s.mts) <= 384, (len(s.tiles), len(s.mts))
        D = os.path.join(ROOT, 'data/tilesets/secondary', sec_dir)
        mt = b''
        for ents in s.mts:
            e8 = [(640 + t) | (hf << 10) | (vf << 11) | (p << 12) for (t, hf, vf, p) in ents]
            e8 = e8 + [0, 0, 0, 0]
            mt += struct.pack('<8H', *e8)
        open(D + '/metatiles.bin', 'wb').write(mt)
        open(D + '/metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', a) for a in s.attrs))
        rows = max(1, (len(s.tiles) + 15) // 16)
        im = Image.new('P', (128, rows * 8), 0)
        pal = []
        for c in s.pals[7].rgb(): pal += list(c)
        im.putpalette(pal + [0] * (768 - len(pal)))
        for n, t in enumerate(s.tiles):
            ti = Image.new('P', (8, 8)); ti.putdata(list(t)); im.paste(ti, ((n % 16) * 8, (n // 16) * 8))
        im.save(D + '/tiles.png')
        for n in range(16):
            p = s.pals.get(n)
            cols = p.rgb() if p else [MAGENTA] + [(0, 0, 0)] * 15
            open(D + '/palettes/%02d.pal' % n, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in cols))
        print('tileset %s : %d metatuiles, %d tuiles' % (sec_dir, len(s.mts), len(s.tiles)))
    def img(s, name):
        """rendu RVB 16x16 d'une metatuile (pour l'apercu)"""
        ents = s.mts[s.names[name]]; im = Image.new('RGB', (16, 16))
        for q, (t, hf, vf, p) in enumerate(ents):
            px = s.tiles[t]; P = s.pals[p].rgb()
            for y in range(8):
                for x in range(8):
                    xx = 7 - x if hf else x; yy = 7 - y if vf else y
                    im.putpixel(((q % 2) * 8 + x, (q // 2) * 8 + y), P[px[yy * 8 + xx]])
        return im
def build_map(ts, rows, legend, blocked):
    """rows : liste de chaines ; legend : {car: nom de metatuile} ; blocked : ensemble de cars bloquants -> mots de map.bin"""
    out = []
    for r in rows:
        for ch in r:
            nm = legend[ch]; out.append(ts.id(nm) | ((1 << 10) if ch in blocked else 0))
    return out
def write_layout(lid_dir, w, h, words, border_id):
    D = os.path.join(ROOT, 'data/layouts', lid_dir)
    open(D + '/map.bin', 'wb').write(struct.pack('<%dH' % len(words), *words))
    open(D + '/border.bin', 'wb').write(struct.pack('<4H', *([border_id | 0x400] * 4)))
def preview(ts, rows, legend, out, scale=2):
    H = len(rows); W = len(rows[0]); im = Image.new('RGB', (W * 16, H * 16))
    cache = {}
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            nm = legend[ch]
            if nm not in cache: cache[nm] = ts.img(nm)
            im.paste(cache[nm], (x * 16, y * 16))
    im = im.resize((im.width * scale, im.height * scale), Image.NEAREST); im.save(out); return im
