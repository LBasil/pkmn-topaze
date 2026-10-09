SP = '/tmp/claude-0/-home-claude-pkmn-topaze/63e017b6-62b1-5272-9bc7-2dbea6438581/scratchpad/'
src = open('docs/topaze/route2_gradient.py').read()
i_head = src.index('# ---- portes : sud')
i_art = src.index('# ---- art : cristaux')
i_cut = src.index('for j in range(3):\n    for i in range(3): del OCC[(STONE[0]')
i_tail = src.index('# ------------------------------------------------------------------ ecriture')
head, mid, tail = src[:i_head], src[i_art:i_cut], src[i_tail:]
head = head.replace('''# ROUTE 2 « la route du crépuscule »''', '''# FORET CALCINEE (carte de l'ex Viridian Forest, 54x69), generee avec la meme machinerie que la Route 2 (etage 2 seulement). Lancer apres forest_cinder.py.
# (en-tete herite de) ROUTE 2 « la route du crépuscule »''', 1)
head = head.replace('W, H = 26, 56', 'W, H = 46, 48')
head = head.replace('general_dusk', 'general_cinder').replace('dusk_road', 'cinder_forest')
# teinte d'arrivee plus sombre et plus grise : cendre et charbon
head = head.replace('s = min(0.30, s * 0.45); l = l * 0.58', 's = min(0.10, s * 0.2); l = l * 0.42').replace('s = s * 0.8; l = l * 0.62', 's = s * 0.6; l = l * 0.5')
head = head.replace('PALS[ROCK_SLOT] = stage_pal(3, 0.5)', '''PALS[ROCK_SLOT] = stage_pal(3, 0.5)
def lighten(c):
    h, l, s = colorsys.rgb_to_hls(*[x / 255 for x in c]); r, g, b = colorsys.hls_to_rgb(0.07, min(0.5, l * 1.18 + 0.02), min(0.1, s * 0.3 + 0.015))
    return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
for _s in (1, 3, 4): PALS[_s] = [PALS[_s][0]] + [lighten(c) for c in PALS[_s][1:]]''', 1)
head = head.replace('def put(x, y, raw_flags', 'def stage_at(x, y): return 2\ndef stage_smooth(x, y): return 2\ndef put(x, y, raw_flags', 1)
mid = mid.replace('for st in range(3)', 'for st in (2,)')
mid = mid.replace('        for var in (range(4) if mask == 15 else range(2)): ROCK[(mask, st, var)] = meta(rock_img(mask, st, var), st)', '        pass')
mid = mid.replace('    for mask in range(16):', '    for mask in ():')
a = tail.index('def add(path, text):'); b = tail.index('g = [G[(x, y)]')
tail = tail[:a] + tail[b:]
tail = tail.replace('PALS[ART_SLOT[0]]', 'PALS[ART_SLOT[2]]')
tail = tail.replace('variant(_m, 1)', 'variant(_m, 2)')
tail = tail.replace("open('data/layouts/Route2/map.bin', 'wb')", "open('data/layouts/ViridianForest/map.bin', 'wb')")
tail = tail.replace("open('data/layouts/Route2/border.bin', 'wb').write(struct.pack('<4H', *[0x400 | variant(m, 1) for m in (468, 469, 476, 477)]))", "open('data/layouts/ViridianForest/border.bin', 'wb').write(struct.pack('<6H', *[0x400 | variant(m, 2) for m in (468, 469, 468, 476, 477, 476)]))")
tail = tail.replace("if l.get('id') == 'LAYOUT_ROUTE2': l.update(width=W, height=H, primary_tileset='gTileset_GeneralDusk', secondary_tileset='gTileset_DuskRoad')", "if l.get('id') == 'LAYOUT_VIRIDIAN_FOREST': l.update(width=W, height=H, primary_tileset='gTileset_GeneralCinder', secondary_tileset='gTileset_CinderForest')")
a = tail.index("json.dump({'signS'"); b = tail.index("blk = sorted")
tail = tail[:a] + "json.dump({'w': W, 'h': H, 'obj': OBJ, 'hid': HID, 'signs': SIGNS, 'face': FACE, 'sight': TRAINERS, 'sdoor': S_DOOR, 'ndoor': N_DOOR, 'tall': TALL, 'path': sorted(PATH)}, open('/tmp/forest_info.json', 'w'))\n" + tail[b:]
tail = tail.replace('/tmp/route2_col.json', '/tmp/forest_col.json').replace("print('route 2 :", "print('foret :")
open('docs/topaze/forest_map.py', 'w').write(head + open(SP + 'geomF.py').read() + '\n' + mid + '\n' + open(SP + 'blockF.py').read() + '\n' + tail)
print('ok')
