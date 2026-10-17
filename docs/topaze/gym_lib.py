"""Outils communs pour la refonte des arenes (decors d'Emeraude) - voir docs/topaze/gym_*.py"""
import sys, os, json, struct, collections
sys.path.insert(0, 'tools/topaze/maps')
import mapkit
from PIL import Image, ImageDraw
def load(lid):
    return mapkit.Layout(lid)
def grid_png(L, out, scale=2, marks=None):
    im = L.render().convert('RGB')
    im = im.resize((im.width * scale, im.height * scale), Image.NEAREST); d = ImageDraw.Draw(im)
    s = 16 * scale
    for x in range(L.w):
        for y in range(L.h):
            d.text((x * s + 2, y * s + 1), '%d,%d' % (x, y), fill=(255, 255, 0))
            if (L.get(x, y) >> 10) & 3: d.rectangle((x * s, y * s, x * s + s - 1, y * s + s - 1), outline=(255, 0, 0))
    for (x, y, t) in (marks or []): d.text((x * s + 4, y * s + 12), t, fill=(0, 255, 255))
    im.save(out)
def walkable(L, x, y): return 0 <= x < L.w and 0 <= y < L.h and ((L.get(x, y) >> 10) & 3) == 0
def bfs(L, start, blocked=()):
    seen = {start}; q = collections.deque([start]); blocked = set(blocked)
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in seen and n not in blocked and walkable(L, *n): seen.add(n); q.append(n)
    return seen
def sheet(key, out, scale=2):
    """planche de toutes les metatuiles d'un tileset d'arene (primaire + secondaire), avec id et comportement"""
    L = mapkit.Layout('LAYOUT_GYM_EM_%s' % key.upper())
    npri = len(L.prim.metatiles) // 16; nsec = len(L.sec.metatiles) // 16
    ids = list(range(npri)) + [640 + i for i in range(nsec)]
    def beh(ts, i):
        b = open(os.path.join(ts.d, 'metatile_attributes.bin'), 'rb').read(); return struct.unpack('<I', b[i * 4:i * 4 + 4])[0] & 0x1ff
    cols = 14; rows = (len(ids) + cols - 1) // cols; s = 16 * scale
    im = Image.new('RGB', (cols * (s + 4), rows * (s + 14)), (50, 50, 50)); d = ImageDraw.Draw(im)
    for n, mid in enumerate(ids):
        x, y = (n % cols) * (s + 4), (n // cols) * (s + 14)
        t = L.metatile_img(mid).convert('RGB').resize((s, s), Image.NEAREST); im.paste(t, (x, y + 12))
        b = beh(L.prim, mid) if mid < 640 else beh(L.sec, mid - 640)
        d.text((x, y), '%d%s' % (mid, ('/%x' % b) if b else ''), fill=(255, 255, 0))
    im.save(out)

import colorsys, shutil
EMD = '../pokeemerald/data/tilesets/'
EMSEC = {'lavaridge': 'lavaridge_gym', 'fortree': 'fortree_gym', 'sootopolis': 'sootopolis_gym', 'dewford': 'dewford_gym', 'mossdeep': 'mossdeep_gym', 'mauville': 'mauville_gym', 'rustboro': 'rustboro_gym'}
def _rd(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * i:6 + 3 * i]) for i in range(n)]
def _wr(p, cols):
    open(p, 'w').write('JASC-PAL\r\n0100\r\n%d\r\n' % len(cols) + ''.join('%d %d %d\r\n' % c for c in cols))
def recolor(key, fn, pri_idx=range(0, 7), sec_idx=range(7, 13)):
    """repart des palettes d'origine d'Emeraude et applique fn(h,s,v,pal_index,color_index)->(h,s,v) (h en degres, s/v 0..1)"""
    sec = EMSEC[key]; P = 'data/tilesets/primary/gym_%s_pri/palettes/' % key; S = 'data/tilesets/secondary/gym_%s_sec/palettes/' % key
    def go(src, dst, i):
        cols = _rd(src); out = [cols[0]]
        for ci, c in enumerate(cols[1:], 1):
            h, s, v = colorsys.rgb_to_hsv(*[x / 255 for x in c]); h *= 360
            h, s, v = fn(h, s, v, i, ci)
            r, g, b = colorsys.hsv_to_rgb((h % 360) / 360, max(0, min(1, s)), max(0, min(1, v)))
            out.append((round(r * 255), round(g * 255), round(b * 255)))
        _wr(dst, out)
    for i in pri_idx:
        src = EMD + ('primary/building/palettes/%02d.pal' % i if i < 6 else 'secondary/%s/palettes/06.pal' % sec)
        go(src, P + '%02d.pal' % i, i)
    for i in sec_idx:
        # palette secondaire Emeraude n'existe qu'a partir de 7 pour i>=7 (6 est dans le primaire cote FR)
        go(EMD + 'secondary/%s/palettes/%02d.pal' % (sec, i), S + '%02d.pal' % i, i)

def apply_gym(mapname, layout_id, objs=None, warps=None, bg=None, coords=None, drop_objects=(), drop_bg_from=None):
    """met a jour data/maps/<mapname>/map.json : nouveau layout, positions d'objets {index: (x, y[, mouvement[, vue]])},
    warps [(x, y)...] (on garde les champs dest_*), bg_events [(x, y)...] dans l'ordre existant."""
    p = 'data/maps/%s/map.json' % mapname; d = json.load(open(p))
    d['layout'] = layout_id
    for i, v in (objs or {}).items():
        o = d['object_events'][i]; o['x'], o['y'] = v[0], v[1]
        if len(v) > 2 and v[2]: o['movement_type'] = 'MOVEMENT_TYPE_' + v[2]
        if len(v) > 3 and v[3] is not None: o['trainer_sight_or_berry_tree_id'] = str(v[3])
    if drop_objects: d['object_events'] = [o for i, o in enumerate(d['object_events']) if i not in set(drop_objects)]
    if warps is not None:
        w0 = d['warp_events']; new = []
        for k, (x, y) in enumerate(warps):
            t = dict(w0[min(k, len(w0) - 1)]); t['x'], t['y'] = x, y; new.append(t)
        d['warp_events'] = new
    if bg is not None:
        b0 = d.get('bg_events', []); new = []
        for k, (x, y) in enumerate(bg):
            t = dict(b0[min(k, len(b0) - 1)]); t['x'], t['y'] = x, y; new.append(t)
        d['bg_events'] = new
    if drop_bg_from is not None: d['bg_events'] = d['bg_events'][:drop_bg_from]
    if coords is not None: d['coord_events'] = coords
    open(p, 'w').write(json.dumps(d, indent=2) + '\n')
def show_events(mapname):
    d = json.load(open('data/maps/%s/map.json' % mapname))
    for i, o in enumerate(d['object_events']): print(i, o['graphics_id'][12:], o['x'], o['y'], o['movement_type'][14:], o['trainer_type'][13:], o['trainer_sight_or_berry_tree_id'], o['script'])
    print('warps', [(w['x'], w['y'], w['dest_map'], w['dest_warp_id']) for w in d['warp_events']])
    print('bg', [(b['x'], b['y'], b.get('player_facing_dir'), b.get('script')) for b in d.get('bg_events', [])])

def edit_layout(key, fn):
    """recharge la carte Emeraude convertie (gym_src/<key>.bin), applique fn(L) puis ecrit data/layouts/GymEm<Key>/map.bin (idempotent)"""
    lid = 'LAYOUT_GYM_EM_%s' % key.upper(); L = mapkit.Layout(lid)
    src = open('docs/topaze/gym_src/%s.bin' % key, 'rb').read()
    L.g = list(struct.unpack('<%dH' % (L.w * L.h), src))
    fn(L); L.save(); return L
def replace_ids(L, mapping, collision=None):
    """remplace des metatuiles par id (mapping {ancien: nouveau}); collision=0/1 force le bit de collision"""
    for i, v in enumerate(L.g):
        m = v & 0x3ff
        if m in mapping:
            nv = (v & ~0x3ff) | mapping[m]
            if collision is not None: nv = (nv & ~(3 << 10)) | (collision << 10)
            L.g[i] = nv
