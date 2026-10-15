import subprocess, sys, struct
from PIL import Image
KEYS = dict(A=1, B=2, SELECT=4, START=8, RIGHT=16, LEFT=32, UP=64, DOWN=128, R=256, L=512)
class Emu:
    def __init__(self, rom, dbg=None):
        self.p = subprocess.Popen(['/tmp/gx/harness', rom], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
        self.dbg = dbg
    def cmd(self, s):
        self.p.stdin.write(s + '\n'); self.p.stdin.flush(); return self.p.stdout.readline().strip()
    def run(self, n, keys=0): return self.cmd('run %d %x' % (n, keys))
    def peek(self, a, n): return bytes.fromhex(self.cmd('peek %x %d' % (a, n)))
    def shot(self, f, scale=2):
        self.cmd('shot /tmp/gx/_s.ppm'); im = Image.open('/tmp/gx/_s.ppm'); im.save(f)
    def u32(self, a): return struct.unpack('<I', self.peek(a, 4))[0]
    def pos(self):
        sb = self.u32(0x03005048)
        if not (0x02000000 <= sb < 0x02040000): return None
        x, y = struct.unpack('<hh', self.peek(sb, 4)); g, n = struct.unpack('<bb', self.peek(sb + 4, 2)); return (g, n, x, y)
    def start(self, g, n, x, y):
        a = 0x030074d0
        for i, v in enumerate((1, g, n, x, y)): self.cmd('pin %x %x' % (a + i, v))
        # titre -> nouvelle partie : appuyer sur A / START par salves jusqu'a avoir une position
        for i in range(600):
            self.run(10, KEYS['A'] if (i // 2) % 2 == 0 else KEYS['START'])
            p = self.pos()
            if p and p[:2] == (g, n) : break
        self.cmd('unpin'); self.run(120, 0)
        return self.pos()

def goto(e, g, n, x, y, maxi=700):
    a = 0x030074d0
    for i, v in enumerate((1, g, n, x, y)): e.cmd('pin %x %x' % (a + i, v))
    for i in range(maxi):
        e.run(15, KEYS['A'] if (i // 2) % 2 == 0 else KEYS['START'])
        p = e.pos()
        if p and p[:2] == (g, n): break
    e.cmd('unpin'); e.run(90, 0); return e.pos()
def step(e, d, tries=40):
    """un pas dans la direction d ('UP','DOWN','LEFT','RIGHT') ; renvoie la position finale ; les touches sont tenues jusqu'a un changement."""
    p0 = e.pos()
    for _ in range(tries):
        e.run(2, KEYS[d]); p = e.pos()
        if p != p0 and p is not None and p[:2] == p0[:2]:
            e.run(14, KEYS[d]) if False else e.run(12, 0); return e.pos()
        if p and p[:2] != p0[:2]: e.run(60, 0); return e.pos()
    return e.pos()
