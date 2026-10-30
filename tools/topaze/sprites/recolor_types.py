#!/usr/bin/env python3
"""Recolore les palettes des Pokemon dont le typage a change (vs pret vanilla) pour refleter leurs nouveaux types.
Usage: recolor_types.py vanilla_species_info.h [--apply] [--sheet out.png] [NAME ...]
Idempotent: part toujours de la palette d'origine stockee dans tools/topaze/sprites/orig_pal/<nom>/{normal,shiny}.pal (creee au 1er passage)."""
import re, sys, os, json, colorsys, shutil
from PIL import Image
R = os.path.dirname(os.path.abspath(__file__)) + '/../../..'
args = [a for a in sys.argv[1:] if not a.startswith('--')]
APPLY = '--apply' in sys.argv
SHEET = sys.argv[sys.argv.index('--sheet') + 1] if '--sheet' in sys.argv else None
orig_path = args[0]; only = [a.upper() for a in args[1:] if a != SHEET]
def parse(src):
    d = {}; ms = list(re.finditer(r'\[(SPECIES_\w+)\] =', src))
    for i, m in enumerate(ms):
        blk = src[m.end(): ms[i + 1].start() if i + 1 < len(ms) else len(src)]
        t = re.search(r'\.types = \{(\w+), (\w+)\}', blk)
        if t: d[m.group(1)] = (t.group(1)[5:], t.group(2)[5:])
    return d
A = parse(open(orig_path).read()); B = parse(open(R + '/src/data/pokemon/species_info.h').read())
CH = [(k, A[k], B[k]) for k in B if k in A and set(A[k]) != set(B[k])]
# type -> (hue, sat mult/target, val mult, light?)  mode: 'dark' | 'light' | 'mid'
TY = {'FIRE': (14, .80, 1.0, 'mid'), 'WATER': (212, .75, 1.0, 'mid'), 'GRASS': (112, .65, .95, 'mid'), 'ELECTRIC': (50, .85, 1.05, 'light'),
      'ICE': (188, .38, 1.1, 'light'), 'PSYCHIC': (322, .55, 1.05, 'light'), 'POISON': (285, .55, .85, 'dark'), 'GROUND': (32, .45, .78, 'dark'),
      'ROCK': (40, .30, .80, 'dark'), 'BUG': (78, .70, .95, 'mid'), 'GHOST': (268, .40, .62, 'dark'), 'DRAGON': (238, .60, .85, 'dark'),
      'DARK': (262, .18, .55, 'dark'), 'STEEL': (215, .13, 1.0, 'light'), 'FIGHTING': (6, .65, .8, 'dark'), 'FLYING': (200, .35, 1.1, 'light'),
      'NORMAL': (35, .15, 1.0, 'light'), 'FAIRY': (330, .35, 1.12, 'light')}
HUEC = {t: v[0] for t, v in TY.items()}
def hd(a, b): d = abs(a - b) % 360; return min(d, 360 - d)
def load_pal(p): L = open(p).read().split('\n'); return [tuple(map(int, l.split())) for l in L[3:19]]
def save_pal(p, pal): open(p, 'w').write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in pal))
def hsv(c): h, s, v = colorsys.rgb_to_hsv(*(x / 255 for x in c)); return h * 360, s, v
def rgb(h, s, v): return tuple(max(0, min(255, round(x * 255))) for x in colorsys.hsv_to_rgb((h % 360) / 360, max(0, min(1, s)), max(0, min(1, v))))
def dirname(k):
    n = k[8:].lower()
    return {'nidoran_f': 'nidoran_f', 'nidoran_m': 'nidoran_m'}.get(n, n)
def paint(c, ty, keep=1.0):
    """pousse la couleur c vers le type ty en conservant le shading."""
    h, s, v = hsv(c); th, ts, tv, mode = TY[ty]
    if ty in ('STEEL', 'NORMAL', 'DARK'):
        ns = s * 0.25 + ts * 0.75 if s > .12 else ts * .6; return rgb(th, ns, v * tv if ty == 'DARK' else v)
    ns = max(s * .5 + ts * .5, ts * .8) if s > .18 else ts * .75
    nv = min(1.0, v * tv) if v > .25 else v
    return rgb(th, ns, nv)
def counts(d):
    cnt = [0] * 16
    for f in ('front.png', 'back.png'):
        im = Image.open(d + '/' + f)
        if im.mode == 'P':
            for px in im.getdata(): cnt[px] += 1
    return cnt
def recolor(name, o, n, pal, cnt):
    pal = list(pal); tot = sum(cnt[1:]) or 1
    out = list(pal); used = set(); nd = list(dict.fromkeys(n))
    W = lambda i: cnt[i] / tot
    chrom = [(i, hsv(pal[i]), W(i)) for i in range(1, 16) if hsv(pal[i])[1] >= .2 and hsv(pal[i])[2] >= .3 and W(i) > .008]
    fam = []
    for i, c, w in sorted(chrom, key=lambda x: -x[2]):
        for f in fam:
            if hd(f['h'], c[0]) < 32: f['m'].append((i, c, w)); f['w'] += w; break
        else: fam.append({'h': c[0], 'm': [(i, c, w)], 'w': w})
    fam.sort(key=lambda f: -f['w'])
    body_t = nd[0] if nd[0] not in o else None
    acc_t = [t for t in nd[1:] if t not in o]
    if body_t:                       # le type principal change: le corps change de couleur
        ents = [(i, c, w) for f in fam[:1] for i, c, w in f['m']]
        ents += [(i, hsv(pal[i]), W(i)) for i in range(1, 16) if i not in [e[0] for e in ents] and hsv(pal[i])[1] < .2 and .3 < hsv(pal[i])[2] < .97 and W(i) > .02]
        for i, c, w in ents: out[i] = paint(pal[i], body_t); used.add(i)
    for A_ in acc_t:
        mode = TY[A_][3]; pick = []
        for f in fam:                # accent = famille de teinte secondaire assez presente
            if f is fam[0]: continue
            if f['w'] > .015 and all(i not in used for i, _, _ in f['m']):
                pick = [(i, c, w) for i, c, w in f['m']]; break
        if not pick:
            prot = {i for i, _, _ in sorted([(i, 0, W(i)) for i in range(1, 16) if hsv(pal[i])[2] > .26], key=lambda x: -x[2])[:2]}
            cand = [(i, hsv(pal[i]), W(i)) for i in range(1, 16) if i not in used and i not in prot and hsv(pal[i])[2] > .26 and W(i) > .008]
            cand.sort(key=lambda x: x[1][2])
            if not cand: cand = [(i, hsv(pal[i]), W(i)) for i in range(1, 16) if i not in used and hsv(pal[i])[2] > .26 and W(i) > .008]; cand.sort(key=lambda x: x[1][2])
            if not cand: continue
            m = len(cand); third = max(1, round(m / 2.5))
            pick = cand[:third] if mode == 'dark' else cand[-third:] if mode == 'light' else cand[max(0, (m - third) // 2):(m - third) // 2 + third]
        for i, c, w in pick: out[i] = paint(pal[i], A_); used.add(i)
        acc = [i for i, _, _ in pick]
        dist = lambda i: sum((x - y) ** 2 for x, y in zip(out[i], pal[i])) ** .5
        cov = lambda: sum(W(i) for i in acc if dist(i) > 48)      # couverture VISIBLE (la couleur a vraiment change)
        if cov() < .30:
            keptc = [HUEC[t] for t in nd if t in o and t not in ('NORMAL', 'STEEL', 'DARK', 'GHOST')]
            keepcol = {i for i in range(1, 16) if hsv(pal[i])[1] > .3 and hsv(pal[i])[2] > .3 and W(i) > .008 and any(hd(hsv(pal[i])[0], h) < 30 for h in keptc)}
            bodyp = keepcol | {i for i, _, _ in sorted([(i, 0, W(i)) for i in range(1, 16) if hsv(pal[i])[2] > .26 and hsv(pal[i])[1] > .2], key=lambda x: -x[2])[:2]} if not body_t else set()
            pool = [(i, hsv(pal[i]), W(i)) for i in range(1, 16) if i not in used and i not in bodyp and hsv(pal[i])[2] > .22 and W(i) > .003]
            pool.sort(key=lambda x: x[1][2], reverse=(mode == 'light'))
            if mode == 'mid': pool.sort(key=lambda x: x[2])
            for i, c, w in pool:
                if cov() >= .40: break
                out[i] = paint(pal[i], A_); used.add(i); acc.append(i)
            if cov() < .18:      # vraiment rien de visible : on entame le corps, par ordre de poids croissant
                for i in sorted(bodyp, key=lambda i: W(i)):
                    if i in used or cov() >= .25: continue
                    out[i] = paint(pal[i], A_); used.add(i); acc.append(i)
    return out
def main():
    base = R + '/graphics/pokemon'; cache = os.path.dirname(os.path.abspath(__file__)) + '/orig_pal'
    sheet = []; rep = []
    for k, o, n in CH:
        nm = k[8:]
        if only and nm not in only: continue
        d = base + '/' + dirname(k)
        if not os.path.isdir(d): rep.append('? ' + nm); continue
        cd = cache + '/' + dirname(k); os.makedirs(cd, exist_ok=True)
        for f in ('normal.pal', 'shiny.pal'):
            if not os.path.exists(cd + '/' + f): shutil.copy(d + '/' + f, cd + '/' + f)
        po, ps = load_pal(cd + '/normal.pal'), load_pal(cd + '/shiny.pal')
        cnt = counts(d); newp = recolor(nm, o, n, po, cnt)
        # shiny : meme transformation, applique par indice (decalage de teinte relatif)
        news = list(ps)
        for i in range(1, 16):
            if newp[i] != po[i]:
                h0, s0, v0 = hsv(po[i]); h1, s1, v1 = hsv(newp[i]); hs, ss, vs = hsv(ps[i])
                if ps[i] == po[i]: news[i] = newp[i]
                else: news[i] = rgb(hs + (h1 - h0) * 0.9 + (hs - h0) * 0.0, ss * (s1 / s0 if s0 > .05 else 1), vs * (v1 / v0 if v0 > .05 else 1)) if s0 > .05 else rgb(h1, s1, vs)
        rep.append('%s %s -> %s : %d entrees' % (nm, '/'.join(dict.fromkeys(o)), '/'.join(dict.fromkeys(n)), sum(1 for i in range(16) if newp[i] != po[i])))
        if APPLY:
            save_pal(d + '/normal.pal', newp); save_pal(d + '/shiny.pal', news)
            for f in ('front.png', 'back.png'):
                im = Image.open(d + '/' + f)
                if im.mode == 'P':
                    p = [c for t in newp for c in t] ; im.putpalette(p); im.save(d + '/' + f)
        if SHEET:
            fr = Image.open(d + '/front.png'); a = fr.copy(); a.putpalette([c for t in po for c in t]); b = fr.copy(); b.putpalette([c for t in newp for c in t])
            sheet.append((nm, '/'.join(dict.fromkeys(o)) + ' > ' + '/'.join(dict.fromkeys(n)), a.convert('RGBA'), b.convert('RGBA')))
    print('\n'.join(rep))
    if SHEET and sheet:
        from PIL import ImageDraw
        cols = 3; W, H = 64 * 2 + 8, 64 + 14; rows = (len(sheet) + cols - 1) // cols
        im = Image.new('RGB', (cols * (W + 14) * 2 // 2, rows * H), (60, 60, 70)); dr = ImageDraw.Draw(im)
        for j, (nm, ty, a, b) in enumerate(sheet):
            x, y = (j % cols) * (W + 14), (j // cols) * H
            im.paste(a, (x, y + 14), a); im.paste(b, (x + 68, y + 14), b); dr.text((x + 1, y + 1), nm[:9] + ' ' + ty, fill=(255, 255, 255))
        im = im.resize((im.width * 3, im.height * 3), Image.NEAREST); im.save(SHEET); print('sheet', SHEET, im.size)
main()
