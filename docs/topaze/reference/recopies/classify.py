import numpy as np, colorsys
from PIL import Image
A = '/mnt/user-data/attachments/130674eb-51d3-5ba1-b7eb-0f75394f02c9/'
JOBS = {
 'f0bb32e8': (A + 'f0bb32e8-image.png', None),
 'ac5bb76b': (A + 'ac5bb76b-image.png', None),
 '14b9926a': (A + '14b9926a-image.jpg', None),
 'e8110426n': (A + 'e8110426-image.jpg', (770, 95, 1487, 978)),
 'e8110426s': (A + 'e8110426-image.jpg', (67, 398, 783, 1133)),
 'd998c33d': (A + 'd998c33d-image.png', None),
}
CLS = ['grass', 'tree', 'water', 'sand', 'cliff', 'roof', 'wood', 'pave', 'rock', 'crop']
COL = {'grass': (150, 230, 120), 'tree': (20, 90, 30), 'water': (40, 120, 255), 'sand': (240, 210, 120), 'cliff': (140, 90, 40), 'roof': (230, 40, 40), 'wood': (200, 150, 90), 'pave': (170, 170, 180), 'rock': (90, 90, 90), 'crop': (230, 160, 30)}
def load(path, box):
    im = Image.open(path).convert('RGB')
    if box: im = im.crop(box)
    w, h = max(1, round(im.width / 16)), max(1, round(im.height / 16))
    return im.resize((w * 16, h * 16), Image.LANCZOS), w, h
def feats(im, w, h):
    a = np.asarray(im, dtype=np.float32) / 255
    c = a.reshape(h, 16, w, 16, 3).transpose(0, 2, 1, 3, 4).reshape(h, w, 256, 3)
    return c
def hsv(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx = rgb.max(-1); mn = rgb.min(-1); d = mx - mn + 1e-6
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return h, d / (mx + 1e-6), mx
def classify(path, box, K=11):
    im, w, h = load(path, box); c = feats(im, w, h)
    mean = c.mean(2); std = c.std(2).mean(-1, keepdims=True)
    X = np.concatenate([mean, std * 2.0], -1).reshape(h * w, 4)
    rng = np.random.RandomState(3); cen = X[rng.choice(len(X), K, replace=False)]
    for _ in range(40):
        d = ((X[:, None, :] - cen[None]) ** 2).sum(-1); a = d.argmin(1)
        for k in range(K):
            if (a == k).any(): cen[k] = X[a == k].mean(0)
    names = []
    for k in range(K):
        r, g, b, sd = cen[k]; Hh, Ss, Vv = [float(v[0]) for v in hsv(np.array([[r, g, b]]))]
        if 160 < Hh < 250 and Ss > 0.2: n = 'water'
        elif (Hh < 18 or Hh > 340) and Ss > 0.45: n = 'roof'
        elif Ss < 0.2 and Vv > 0.58: n = 'pave'
        elif Ss < 0.28 and 0.25 < Vv <= 0.58 and not (70 < Hh < 160 and Ss > 0.2): n = 'rock'
        elif 15 < Hh < 55 and Ss > 0.2 and Vv > 0.68: n = 'sand'
        elif 15 < Hh < 55 and Ss > 0.2: n = 'cliff'
        elif Vv < 0.40 or (sd / 2 > 0.16 and Vv < 0.55): n = 'tree'
        else: n = 'grass'
        names.append(n)
    lab = np.empty((h, w), object)
    for y in range(h):
        for x in range(w): lab[y, x] = names[a[y * w + x]]
    return im, w, h, lab
def overlay(im, w, h, lab, out):
    o = Image.new('RGB', (w * 16, h * 16))
    px = o.load()
    for y in range(h):
        for x in range(w):
            col = COL[lab[y, x]]
            for j in range(16):
                for i in range(16): px[x * 16 + i, y * 16 + j] = col
    b = Image.new('RGB', (w * 32 + 16, h * 16), (30, 30, 30)); b.paste(im, (0, 0)); b.paste(o, (w * 16 + 16, 0)); b.save(out)
if __name__ == '__main__':
    import sys
    for k in sys.argv[1:]:
        im, w, h, lab = classify(*JOBS[k]); overlay(im, w, h, lab, '/tmp/recopy/cls_%s.png' % k)

TD, TS = 0.30, 0.17
def classify_rules(path, box):
    im, w, h = load(path, box); c = feats(im, w, h)
    H, S, V = hsv(c)
    frac = lambda m: m.mean(-1)
    water = (H > 165) & (H < 235) & (S > 0.30) & (V > 0.28)
    roof = ((H < 18) | (H > 345)) & (S > 0.55) & (V > 0.45)
    sand = (H > 28) & (H < 58) & (S > 0.18) & (S < 0.6) & (V > 0.70)
    wood = (H > 18) & (H < 45) & (S > 0.30) & (V > 0.40) & (V < 0.85)
    gray = (S < 0.14) & (V > 0.25)
    green = (H > 70) & (H < 165) & (S > 0.22)
    dark = V < 0.42
    lab = np.empty((h, w), object)
    FW, FR, FS, FO, FG, FGR, FD = [frac(m) for m in (water, roof, sand, wood, gray, green, dark)]
    for y in range(h):
        for x in range(w):
            vm = V[y, x].mean()
            if FW[y, x] > 0.45: l = 'water'
            elif FR[y, x] > 0.30: l = 'roof'
            elif FG[y, x] > 0.5: l = 'pave' if vm > 0.52 else 'rock'
            elif FS[y, x] > 0.45: l = 'sand'
            elif FO[y, x] > 0.45: l = 'cliff'
            elif FGR[y, x] > 0.4 and (FD[y, x] > TD or V[y, x].std() > TS): l = 'tree'
            elif FGR[y, x] > 0.3: l = 'grass'
            elif FW[y, x] > 0.2: l = 'water'
            elif FO[y, x] > 0.25: l = 'cliff'
            elif FS[y, x] > 0.2: l = 'sand'
            else: l = 'grass' if vm > 0.5 else 'tree'
            lab[y, x] = l
    return im, w, h, lab
