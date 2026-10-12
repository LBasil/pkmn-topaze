# Art d'Amethiolite v7 : arene (monument de geode 128x96, moitie gauche dessinee, droite = miroir) + mobilier urbain (lampadaire-cristal, jardiniere, banc).
# Importe par amethiolite_town.py ; `python3 amethiolite_art.py apercu.png` produit un apercu.
import math, random
from PIL import Image, ImageDraw
AP = [(0, 0, 0), (28, 12, 48), (60, 34, 104), (92, 56, 152), (128, 88, 196), (170, 130, 232), (212, 180, 250), (246, 236, 255), (120, 110, 150), (160, 152, 184),
      (84, 76, 112), (255, 214, 110), (236, 90, 190), (255, 150, 226), (90, 226, 236), (40, 26, 70)]
# 1 contour | 2 violet profond | 3 violet | 4 violet clair | 5 amethyste | 6 amethyste pale | 7 reflet | 8 pierre | 9 pierre claire | 10 pierre sombre | 11 fenetre or | 12 neon magenta | 13 rose clair | 14 cyan | 15 interieur
def newimg(w, h): return Image.new('P', (w, h), 0)
def prism(d, x, base, w, h, core=True):
    half = max(2, w // 2); top = base - h; sh = top + max(4, half + 1)
    d.polygon([(x - half, base), (x - half, sh), (x, top), (x + half, sh), (x + half, base)], fill=5, outline=1)
    d.polygon([(x - half + 1, base - 1), (x - half + 1, sh + 1), (x, top + 2), (x, base - 1)], fill=6)          # face eclairee
    d.polygon([(x + 1, top + 2), (x + half - 1, sh + 1), (x + half - 1, base - 1), (x + 1, base - 1)], fill=4)   # face a l'ombre
    d.line([(x, top + 2), (x, base - 1)], fill=3)                                                                # arete
    if core and half >= 4 and h >= 14:
        hc = max(2, half // 2 - 1); ct = base - int(h * 0.55); cs = ct + hc + 1
        d.polygon([(x - hc, base - 3), (x - hc, cs), (x, ct), (x + hc, cs), (x + hc, base - 3)], fill=12, outline=2)          # coeur lumineux
        d.line([(x - 1, ct + 3), (x - 1, base - 5)], fill=13)
    d.point((x - half + 2, sh + 1), fill=7); d.point((x - 1, top + 3), fill=14)
def stone(d, x0, y0, x1, y1):
    """appareil de pierre sur grille de 8 px (periode 8 : les tuiles se repetent)"""
    d.rectangle((x0, y0, x1, y1), fill=8)
    for y in range(y0, y1 + 1):
        if (y - y0) % 8 == 7: d.line([(x0, y), (x1, y)], fill=10)
    for y in range(y0, y1 + 1, 8):
        off = 0 if ((y - y0) // 8) % 2 == 0 else 4
        for x in range(x0 + off, x1 + 1, 8): d.line([(x, y), (x, min(y + 6, y1))], fill=10)
    for y in range(y0, y1 + 1, 8): d.line([(x0, y), (x1, y)], fill=9)
def window(d, x, y, w=6, h=10, lit=11):
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=lit, outline=1)
    d.line([(x + w // 2, y + 1), (x + w // 2, y + h - 2)], fill=1)
    d.point((x + 1, y + 1), fill=7)
def slate(d, x0, y0, x1, y1):
    """toit d'ardoise violette : ecailles sur grille de 8 px"""
    d.rectangle((x0, y0, x1, y1), fill=3)
    for y in range(y0, y1 + 1, 4):
        for x in range(x0 + (0 if ((y - y0) // 4) % 2 == 0 else 4), x1 + 1, 8):
            d.line([(x, y + 3), (x + 7, y + 3)], fill=2); d.line([(x, y), (x, y + 3)], fill=2); d.point((x + 1, y), fill=4)
    d.line([(x0, y0), (x1, y0)], fill=5); d.line([(x0, y1), (x1, y1)], fill=1)
def left_half():
    im = newimg(64, 96); d = ImageDraw.Draw(im)
    d.ellipse((0, 88, 63, 96), fill=15)                                    # ombre au sol
    # --- hall bas : mur de pierre, toit d'ardoise, fenetres allumees
    stone(d, 2, 66, 63, 92); d.rectangle((2, 66, 63, 92), outline=1)
    slate(d, 0, 52, 63, 66); d.rectangle((0, 64, 63, 67), fill=2); d.line([(0, 67), (63, 67)], fill=1); d.line([(0, 64), (63, 64)], fill=5)
    for x in (12, 28): window(d, x, 72, 6, 10)
    d.rectangle((2, 88, 63, 92), fill=10); d.line([(2, 88), (63, 88)], fill=9)                                     # soubassement
    # --- tour laterale (gauche) : fut de pierre + toit-cristal
    stone(d, 5, 36, 26, 92); d.rectangle((5, 36, 26, 92), outline=1); d.rectangle((3, 34, 28, 38), fill=2, outline=1); d.line([(4, 35), (27, 35)], fill=5)
    window(d, 11, 44, 6, 10, 11); window(d, 11, 58, 6, 10, 13)
    prism(d, 16, 36, 24, 30)
    # --- tour centrale : fut + couronne de geode (le grand prisme est sur l'axe : on dessine sa moitie gauche, le miroir fait le reste)
    stone(d, 38, 30, 63, 92); d.rectangle((38, 30, 63, 92), outline=1); d.rectangle((36, 28, 63, 32), fill=2, outline=1); d.line([(37, 29), (63, 29)], fill=5)
    for k, y in enumerate((38, 52)): window(d, 42, y, 6, 10, 11 if k == 0 else 13); window(d, 54, y, 6, 10, 13 if k == 0 else 11)
    prism(d, 63, 30, 40, 29, core=True)               # grand cristal (axe)
    prism(d, 47, 30, 20, 22); prism(d, 36, 32, 11, 12)
    # --- porte : arche sombre, neon magenta, marches
    d.rectangle((50, 68, 63, 92), fill=15, outline=1); d.pieslice((50, 62, 78, 82), 180, 360, fill=15, outline=1)
    d.line([(51, 70), (51, 91)], fill=12); d.arc((51, 63, 77, 81), 180, 270, fill=12)
    for k in range(5): d.point((54 + k * 2, 90 - (k % 2)), fill=11)
    d.rectangle((46, 90, 63, 93), fill=9, outline=1); d.rectangle((44, 93, 63, 95), fill=8, outline=1)
    # --- cristaux-lanternes de part et d'autre des marches
    prism(d, 43, 90, 7, 12, core=False); d.point((43, 82), fill=11); d.point((42, 83), fill=13)
    return im
def full():
    L = left_half(); im = newimg(128, 96); im.paste(L, (0, 0)); im.paste(L.transpose(Image.FLIP_LEFT_RIGHT), (64, 0)); return im
def uniq_tiles(im):
    return len({tuple(im.crop((x, y, x + 8, y + 8)).getdata()) for y in range(0, im.height, 8) for x in range(0, im.width, 8)})

# ---- mobilier urbain (16x16, palette ART_PAL de la ville : 1 contour | 2 violet fonce | 3 violet | 4 amethyste claire | 5 lilas | 6 blanc | 11 ombre | 12 rose toxique | 13 pierre | 14 pierre sombre | 15 lueur)
def lamp():
    """lampadaire-cristal : pied de pierre, mat, lanterne d'amethyste a coeur rose lumineux"""
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    d.ellipse((3, 13, 13, 16), fill=11)
    d.rectangle((5, 13, 10, 15), fill=13, outline=1); d.line([(6, 13), (9, 13)], fill=6)
    d.rectangle((7, 7, 8, 13), fill=14, outline=1)
    d.polygon([(8, 0), (11, 3), (11, 7), (8, 10), (5, 7), (5, 3)], fill=5, outline=1)
    d.polygon([(8, 3), (10, 5), (10, 7), (8, 9), (6, 7), (6, 5)], fill=12)
    d.line([(8, 4), (8, 8)], fill=13); d.point((8, 6), fill=15)
    d.point((6, 3), fill=6)
    return im
def planter(var):
    """jardiniere de pierre : bourgeons de cristal (rose / lilas) a la place des fleurs"""
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    d.ellipse((0, 12, 15, 16), fill=11)
    d.rectangle((1, 9, 14, 14), fill=13, outline=1); d.line([(2, 10), (13, 10)], fill=6); d.rectangle((2, 13, 13, 13), fill=14)
    for k in range(2, 14, 4): d.line([(k, 11), (k, 12)], fill=14)
    cols = ((12, 5, 12), (4, 12, 5)) if var == 0 else ((5, 12, 4), (12, 4, 12))
    for (x, y, c) in ((3, 7, cols[0][0]), (7, 4, cols[0][1]), (11, 6, cols[0][2])):
        d.polygon([(x, y), (x + 2, y + 3), (x + 2, 9), (x - 2, 9), (x - 2, y + 3)], fill=c, outline=1); d.point((x - 1, y + 3), fill=6)
    return im
def bench(back_top):
    """banc de pierre vu de face ; dossier au nord (back_top) ou au sud"""
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    y0 = 3 if back_top else 7
    d.ellipse((0, 12, 15, 16), fill=11)
    if back_top:
        d.rectangle((1, y0, 14, y0 + 4), fill=14, outline=1); d.line([(2, y0 + 1), (13, y0 + 1)], fill=13)
        d.rectangle((0, 8, 15, 11), fill=13, outline=1); d.line([(1, 9), (14, 9)], fill=6)
    else:
        d.rectangle((0, 4, 15, 7), fill=13, outline=1); d.line([(1, 5), (14, 5)], fill=6)
        d.rectangle((1, 8, 14, 12), fill=14, outline=1); d.line([(2, 9), (13, 9)], fill=13)
    for x in (2, 12): d.rectangle((x, 12, x + 1, 14), fill=14, outline=1)
    d.point((3, 5 if not back_top else 9), fill=4); d.point((12, 5 if not back_top else 9), fill=4)
    return im

if __name__ == '__main__':
    import sys
    im = full(); im.putpalette([c for p in AP for c in p] + [0] * (768 - 48))
    print('tuiles uniques moitie gauche :', uniq_tiles(left_half()), '| image complete :', uniq_tiles(im))
    bg = Image.new('RGB', (128 + 16 * 5 + 40, 96), (186, 156, 228))
    rgba = im.convert('RGBA'); px = rgba.load(); src = im.load()
    for y in range(96):
        for x in range(128):
            if src[x, y] == 0: px[x, y] = (0, 0, 0, 0)
    bg.paste(rgba, (0, 0), rgba)
    PALT = [(0, 0, 0), (30, 10, 52), (94, 44, 142), (142, 84, 202), (188, 132, 236), (228, 200, 252), (252, 242, 255), (62, 30, 112), (104, 56, 170), (152, 100, 222), (214, 188, 252), (40, 30, 66), (214, 64, 152), (176, 168, 192), (96, 88, 118), (255, 246, 200)]
    for n, f in enumerate((lamp(), planter(0), planter(1), bench(True), bench(False))):
        f.putpalette([c for p in PALT for c in p] + [0] * (768 - 48)); r = f.convert('RGBA'); p2 = r.load(); s2 = f.load()
        for y in range(16):
            for x in range(16):
                if s2[x, y] == 0: p2[x, y] = (0, 0, 0, 0)
        bg.paste(r, (136 + n * 18, 4), r)
    bg.resize((bg.width * 5, bg.height * 5), Image.NEAREST).save(sys.argv[1])
