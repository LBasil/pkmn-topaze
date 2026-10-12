# captures en jeu (mGBA) a des positions choisies : python3 docs/topaze/route_shots.py <ROM> out.png Route13:62:2 Route9:30:7 ...
import sys, re; sys.path.insert(0, '/tmp/gx'); sys.path.insert(0, 'tools/topaze/emu'); sys.path.insert(0, 'docs/topaze')
from drive import *
from route_test import mapid, Nav
from PIL import Image, ImageDraw
rom, out, specs = sys.argv[1], sys.argv[2], sys.argv[3:]; ims = []
for sp in specs:
    name, x, y = sp.split(':'); nav = Nav(name); g, n = mapid(nav.mj['id'][4:]); e = Emu(rom); a = 0x03007480
    for i, v in enumerate((1, g, n, int(x), int(y), 1)): e.cmd('pin %x %x' % (a + i, v))
    for i in range(700):
        e.run(15, KEYS['A'] if (i // 2) % 2 == 0 else KEYS['START'])
        p = e.pos()
        if p and p[:2] == (g, n): break
    e.cmd('pin %x 0' % a); e.cmd('pin %x 0' % (a + 1)); e.run(100, 0); e.shot('/tmp/gx/_x.png')
    im = Image.open('/tmp/gx/_x.png').convert('RGB').resize((480, 320), Image.NEAREST); ImageDraw.Draw(im).text((4, 4), sp, fill=(255, 255, 0)); ims.append(im); e.p.kill()
cols = 2; W = Image.new('RGB', (480 * cols, 320 * ((len(ims) + cols - 1) // cols)))
for k, im in enumerate(ims): W.paste(im, ((k % cols) * 480, (k // cols) * 320))
W.save(out)
