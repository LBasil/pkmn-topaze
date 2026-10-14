#!/usr/bin/env python3
"""Éditeur de cartes Pokémon Topaze — serveur local (stdlib + Pillow).

Usage :  python3 tools/topaze/editor/server.py [port]    puis ouvrir http://localhost:8765
Lit et écrit directement data/maps/*/map.json et data/layouts/*/map.bin.
Tout est versionné par git : `git diff` / `git checkout` pour revenir en arrière.
"""
import io, json, os, re, struct, sys, glob, threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'topaze', 'maps'))
import mapkit                                  # noqa: E402
from PIL import Image                          # noqa: E402

LOCK = threading.Lock()
_sheet_cache = {}
_sprite_cache = {}


def rd(path):
    with open(os.path.join(ROOT, path), encoding='utf-8', errors='replace') as f:
        return f.read()


def define_names(path, prefix):
    return sorted(set(re.findall(r'#define\s+(%s\w+)' % prefix, rd(path))))


def lookups():
    return {
        'gfx': define_names('include/constants/event_objects.h', 'OBJ_EVENT_GFX_'),
        'movement': define_names('include/constants/event_object_movement.h', 'MOVEMENT_TYPE_'),
        'flags': define_names('include/constants/flags.h', 'FLAG_'),
        'vars': define_names('include/constants/vars.h', 'VAR_'),
        'trainer_types': ['TRAINER_TYPE_NONE', 'TRAINER_TYPE_NORMAL', 'TRAINER_TYPE_SEE_ALL_DIRECTIONS',
                          'TRAINER_TYPE_BURIED'],
        'bg_dirs': ['BG_EVENT_PLAYER_FACING_ANY', 'BG_EVENT_PLAYER_FACING_NORTH', 'BG_EVENT_PLAYER_FACING_SOUTH',
                    'BG_EVENT_PLAYER_FACING_EAST', 'BG_EVENT_PLAYER_FACING_WEST'],
    }


def map_names():
    return sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(ROOT, 'data/maps/*/map.json')))


def map_json_path(name):
    if not re.fullmatch(r'\w+', name):
        raise ValueError('nom de carte invalide')
    return os.path.join(ROOT, 'data/maps', name, 'map.json')


def map_id_index():
    out = {}
    for n in map_names():
        try:
            out[json.load(open(map_json_path(n)))['id']] = n
        except Exception:
            pass
    return out


def metatile_sheet(layout_id):
    """PNG 32x32 métatuiles (16 px) ; l'index dans la grille = identifiant du métatuile (0..1023)."""
    if layout_id in _sheet_cache:
        return _sheet_cache[layout_id]
    lay = mapkit.Layout(layout_id)
    sheet = Image.new('RGBA', (32 * 16, 32 * 16), (40, 40, 40, 255))
    for mid in range(1024):
        ts, idx = (lay.prim, mid) if mid < 640 else (lay.sec, mid - 640)
        if (idx + 1) * 16 > len(ts.metatiles):
            continue
        sheet.paste(lay.metatile_img(mid), ((mid % 32) * 16, (mid // 32) * 16))
    b = io.BytesIO()
    sheet.save(b, 'PNG')
    _sheet_cache[layout_id] = b.getvalue()
    return _sheet_cache[layout_id]


def sprite_png(gfx):
    """Première image (face sud) du sprite d'un OBJ_EVENT_GFX_*, ou None."""
    if gfx in _sprite_cache:
        return _sprite_cache[gfx]
    out = None
    try:
        ptrs = rd('src/data/object_events/object_event_graphics_info_pointers.h')
        m = re.search(r'\[%s\]\s*=\s*&(\w+)' % re.escape(gfx), ptrs)
        info = rd('src/data/object_events/object_event_graphics_info.h')
        blk = re.search(r'%s\s*=\s*\{(.*?)\n\};' % re.escape(m.group(1)), info, re.S).group(1)
        w = int(re.search(r'\.width\s*=\s*(\d+)', blk).group(1))
        h = int(re.search(r'\.height\s*=\s*(\d+)', blk).group(1))
        img_tab = re.search(r'\.images\s*=\s*(\w+)', blk).group(1)
        tabs = rd('src/data/object_events/object_event_pic_tables.h')
        pic = re.search(r'%s\[\]\s*=\s*\{\s*overworld_frame\((\w+)' % re.escape(img_tab), tabs).group(1)
        gr = rd('src/data/object_events/object_event_graphics.h')
        path = re.search(r'%s\[\]\s*=\s*INCBIN_U\d+\("([^"]+)\.4bpp"' % re.escape(pic), gr).group(1) + '.png'
        im = Image.open(os.path.join(ROOT, path))
        tr = im.info.get('transparency', 0) if False else 0
        frame = im.crop((0, 0, w, h)).convert('P') if im.mode == 'P' else im.crop((0, 0, w, h))
        rgba = Image.new('RGBA', (w, h))
        pal = im.getpalette() or []
        src, dst = frame.load(), rgba.load()
        for yy in range(h):
            for xx in range(w):
                c = src[xx, yy]
                if im.mode == 'P':
                    dst[xx, yy] = (0, 0, 0, 0) if c == tr else (pal[c * 3], pal[c * 3 + 1], pal[c * 3 + 2], 255)
                else:
                    dst[xx, yy] = c
        b = io.BytesIO()
        rgba.save(b, 'PNG')
        out = b.getvalue()
    except Exception:
        out = None
    _sprite_cache[gfx] = out
    return out


def load_map(name):
    mj = json.load(open(map_json_path(name), encoding='utf-8'))
    lay = mapkit.layouts()[mj['layout']]
    w, h = lay['width'], lay['height']
    raw = open(os.path.join(ROOT, lay['blockdata_filepath']), 'rb').read()
    blocks = list(struct.unpack('<%dH' % (w * h), raw))
    ids = map_id_index()
    return {'name': name, 'map': mj, 'w': w, 'h': h, 'blocks': blocks, 'layout': mj['layout'],
            'maps': ids, 'layout_shared_by': [n for n, i in ((n, json.load(open(map_json_path(n))).get('layout'))
                                                             for n in map_names()) if i == mj['layout'] and n != name]}


def save_map(name, payload):
    mj = payload['map']
    old = json.load(open(map_json_path(name), encoding='utf-8'))
    if mj.get('layout') != old.get('layout') or mj.get('id') != old.get('id'):
        raise ValueError("id/layout d'une carte : non modifiable depuis l'éditeur")
    with open(map_json_path(name), 'w', encoding='utf-8') as f:
        json.dump(mj, f, indent=2, ensure_ascii=False)
        f.write('\n')
    blocks = payload.get('blocks')
    if blocks is not None:
        lay = mapkit.layouts()[mj['layout']]
        if len(blocks) != lay['width'] * lay['height']:
            raise ValueError('taille de blocs incorrecte')
        with open(os.path.join(ROOT, lay['blockdata_filepath']), 'wb') as f:
            f.write(struct.pack('<%dH' % len(blocks), *[int(b) & 0xFFFF for b in blocks]))
    return {'ok': True,
            'reminder': 'Après modif de carte : rm -f build/firered/data/maps.o puis make -j8 firered'}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, ctype='application/json'):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode('utf-8')
        elif isinstance(body, str):
            body = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        try:
            if u.path in ('/', '/index.html'):
                return self.send(200, open(os.path.join(HERE, 'index.html'), 'rb').read(), 'text/html; charset=utf-8')
            if u.path == '/api/maps':
                return self.send(200, map_names())
            if u.path == '/api/lookups':
                return self.send(200, lookups())
            if u.path == '/api/map':
                with LOCK:
                    return self.send(200, load_map(q['name']))
            if u.path == '/api/metatiles':
                with LOCK:
                    return self.send(200, metatile_sheet(q['layout']), 'image/png')
            if u.path == '/api/sprite':
                with LOCK:
                    d = sprite_png(q['gfx'])
                return self.send(200 if d else 404, d or b'', 'image/png')
            self.send(404, {'error': 'not found'})
        except Exception as e:
            self.send(500, {'error': '%s: %s' % (type(e).__name__, e)})

    def do_POST(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        try:
            body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'{}')
            if u.path == '/api/save':
                with LOCK:
                    return self.send(200, save_map(q['name'], body))
            self.send(404, {'error': 'not found'})
        except Exception as e:
            self.send(500, {'error': '%s: %s' % (type(e).__name__, e)})


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print('Éditeur Topaze : http://localhost:%d  (racine du dépôt : %s)' % (port, ROOT))
    ThreadingHTTPServer(('127.0.0.1', port), H).serve_forever()
