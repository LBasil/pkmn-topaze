# CHEMINS v1 (01-11) : raccourcis ponctuels pour la navigation (idempotent ; a relancer apres tourmalia_copy.py / ville regeneree).
# Tourmalia : (20,25) corniche et (17,21) arbre isole -> herbe marchable (Centre-Arene 41 -> 27 pas).
# Amethiolite : (36,16) et (34,20) pieces du muret de la place -> sol (Centre-Arene 56 -> 40 pas).
import struct, json
L = json.load(open('data/layouts/layouts.json'))['layouts']
def lay(lid): return [x for x in L if x.get('id') == lid][0]
def edit(lid, fn):
    l = lay(lid); w, h = l['width'], l['height']; p = l['blockdata_filepath']
    g = list(struct.unpack('<%dH' % (w * h), open(p, 'rb').read()))
    for (x, y), v in fn(g, w).items(): g[y * w + x] = v
    open(p, 'wb').write(struct.pack('<%dH' % (w * h), *g))
edit('LAYOUT_CERULEAN_CITY', lambda g, w: {(20, 25): g[24 * w + 20], (17, 21): g[21 * w + 16]})
edit('LAYOUT_FUCHSIA_CITY', lambda g, w: {(36, 16): 0x32a1, (34, 20): 0x32a1})
