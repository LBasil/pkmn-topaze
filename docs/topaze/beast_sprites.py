"""Sprites overworld de Raikou/Entei/Suicune, a la maniere de Polished Crystal:
mini 16x16 (rangi42/polishedcrystal gfx/minis + masque) recolore avec la palette
du Pokedex. Pose en bas-centre du cadre 32x32."""
import sys
from PIL import Image
from collections import Counter
R = '/home/claude/pkmn-topaze/'; PC = '/tmp/pc/gfx/minis/'
TRANSP = (115, 197, 164)
def lum(c): return 0.3*c[0] + 0.59*c[1] + 0.11*c[2]
def build(name):
    fr = Image.open(R + f'graphics/pokemon/{name}/front.png'); p = fr.getpalette()
    from collections import Counter
    cnt = Counter(fr.getpixel((x, y)) for x in range(64) for y in range(64)); cnt.pop(0, None)
    rgb = lambda i: tuple(p[i*3:i*3+3])
    sat = lambda c: max(c) - min(c)
    mids = [i for i in cnt if 100 < lum(rgb(i)) < 215 and sat(rgb(i)) > 40]
    body = max(mids, key=lambda i: cnt[i]) if mids else max(cnt, key=cnt.get)
    light = max(cnt, key=lambda i: lum(rgb(i)))
    darks = [i for i in cnt if lum(rgb(i)) < 110 and i != body]
    outline = min(darks, key=lambda i: lum(rgb(i)))
    accent = max([i for i in darks if i != outline] or [outline], key=lambda i: (sat(rgb(i)), cnt[i]))
    pick = [rgb(outline), rgb(accent), rgb(light), rgb(body)]
    mini = Image.open(PC + f'{name}.png').convert('L').crop((0, 0, 16, 16))
    mask = Image.open(PC + f'{name}_mask.png').convert('L').crop((0, 0, 16, 16))
    lv = {0: 0, 85: 1, 170: 2, 255: 3}
    cols = [TRANSP] + pick + [(0, 0, 0)] * 11
    out = Image.new('P', (32, 32), 0)
    for y in range(16):
        for x in range(16):
            if mask.getpixel((x, y)) != 0: continue
            out.putpixel((8 + x, 15 + y), 1 + lv[mini.getpixel((x, y))])
    out.putpalette([v for c in cols for v in c] + [0] * (768 - 48)); return out, cols
FIT = 22      # meme encombrement que Sulfura (22 x 20 dans le cadre 32x32)

def lum_i(pal, i): return lum(tuple(pal[i*3:i*3+3]))

def build_dex(name):
    fr = Image.open(R + f'graphics/pokemon/{name}/front.png'); pal = fr.getpalette()
    bb = fr.convert('RGBA').getbbox(); x0, y0, x1, y1 = bb
    # transparence : indice 0 du Pokedex
    mask = fr.point(lambda v: 0 if v == 0 else 255)
    bb = mask.getbbox(); x0, y0, x1, y1 = bb; w, h = x1 - x0, y1 - y0
    sc = max(w, h) / FIT; nw, nh = max(1, round(w / sc)), max(1, round(h / sc))
    out = Image.new('P', (32, 32), 0); op = out.load()
    ox = (32 - nw) // 2; oy = 31 - nh
    for y in range(nh):
        for x in range(nw):
            sx0, sx1 = x0 + int(x * w / nw), x0 + max(int((x + 1) * w / nw), int(x * w / nw) + 1)
            sy0, sy1 = y0 + int(y * h / nh), y0 + max(int((y + 1) * h / nh), int(y * h / nh) + 1)
            px = [fr.getpixel((i, j)) for i in range(sx0, sx1) for j in range(sy0, sy1)]
            op_ = [c for c in px if c != 0]
            if len(op_) < 0.45 * len(px): continue
            cnt = Counter(op_); dk = [c for c in op_ if lum_i(pal, c) < 90]
            op[ox + x, oy + y] = Counter(dk).most_common(1)[0][0] if len(dk) >= 0.25 * len(op_) else cnt.most_common(1)[0][0]
    cols = [TRANSP] + [tuple(pal[i * 3:i * 3 + 3]) for i in range(1, 16)]
    out.putpalette([v for c in cols for v in c] + [0] * (768 - 48))
    return out, cols

if __name__ == '__main__':
    for n in ('raikou', 'entei', 'suicune', 'regirock', 'regice', 'registeel'):
        im, cols = (build_dex if n.startswith('regi') else build)(n)
        im.save(R + f'graphics/object_events/pics/pokemon/{n}.png')
        open(R + f'graphics/object_events/palettes/{n}.pal', 'w', newline='').write(
            'JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in cols))
