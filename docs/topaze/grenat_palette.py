# Habille Grenalux aux couleurs du GRENAT : recolore les palettes des tilesets d'Emeraude importes
# (idempotent : repart toujours des palettes d'origine de ../pokeemerald). A lancer apres import_emerald_tiles.py.
import colorsys, os, sys
EM = '../pokeemerald/data/tilesets/'
OUT = {'primary/general': 'data/tilesets/primary/general_emerald/palettes/',
       'secondary/petalburg': 'data/tilesets/secondary/petalburg_emerald/palettes/'}
MODE = sys.argv[1] if len(sys.argv) > 1 else 'A'
def tint(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    h *= 360
    if s < 0.08: return r, g, b                       # gris / blanc : inchanges
    if 60 <= h <= 180:                                # vegetation -> vin / bordeaux
        h = 352 + (h - 120) * 0.12; s = min(1, s * 0.9); l = l * 0.8
    elif 25 <= h < 60:                                # sable / paille -> terre rose cuivree
        h = 14 + (h - 40) * 0.2; s *= 0.75
    elif 180 < h <= 260:                              # eau -> violet nuit
        h = 262 + (h - 215) * 0.2; s *= 0.4; l = l * 0.5
    else:                                             # rouges / oranges (toits) -> grenat profond
        h = 350; s = min(1, s * 1.05); l = l * 0.78
    r, g, b = colorsys.hls_to_rgb(h / 360, max(0, min(1, l)), max(0, min(1, s)))
    return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
for src, dst in OUT.items():
    for i in range(16):
        L = open(EM + src + '/palettes/%02d.pal' % i).read().split()
        n = int(L[2]); cols = [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
        new = [cols[0]] + [tint(*c) for c in cols[1:]]     # couleur 0 = transparence : inchangee
        txt = 'JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in new)
        open(dst + '%02d.pal' % i, 'w').write(txt)
        if src.endswith('petalburg') and i == 6:
            open(OUT['primary/general'] + '06.pal', 'w').write(txt)
print('palettes grenat ecrites')
