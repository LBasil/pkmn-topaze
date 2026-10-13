# Grenalux fix 2: rival escort to the ranch by the east path, seams, Route 1 connection. NOT re-runnable.
import re, json, struct, collections, glob
R = '/home/claude/pkmn-topaze/'
def rd(p): return open(R+p).read()
def wr(p, s): open(R+p, 'w').write(s)
def jw(p, j): open(R+p, 'w').write(json.dumps(j, indent=2) + '\n')

# ---- A. BFS path rival/player (Pallet)
b = open(R+'data/layouts/PalletTown/map.bin', 'rb').read(); v = struct.unpack('<%dH' % (len(b)//2), b); W = 44; H = 36
blk = lambda x, y: ((v[y*W+x] >> 10) & 3) != 0
pj = json.load(open(R+'data/maps/PalletTown/map.json'))
objs = {(o['x'], o['y']) for o in pj['object_events']}
def bfs(s, g):
    q = collections.deque([s]); p = {s: None}
    while q:
        c = q.popleft()
        if c == g: break
        for d, (dx, dy) in {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}.items():
            n = (c[0]+dx, c[1]+dy)
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in p and not blk(*n) and n not in objs: p[n] = (c, d); q.append(n)
    path = []; c = g
    while p[c]: pc, d = p[c]; path.append(d); c = pc
    return path[::-1]
def mv(name, steps): return name + '::\n' + ''.join('\twalk_%s\n' % d for d in steps) + '\tstep_end\n\n'
mvs = ''
for side, sx in (('Left', 22), ('Right', 23)):
    P = bfs((sx, 2), (43, 7))
    mvs += mv('PalletTown_Movement_RivalWalkToRanch' + side, P)
    mvs += mv('PalletTown_Movement_PlayerWalkToRanch' + side, ['down'] + P[:-1])

s = rd('data/maps/PalletTown/scripts.inc')
def cut(s, label):
    m = re.search(r'^%s::\n(?:\t.*\n)*\n?' % label, s, re.M); assert m, label
    return s[:m.start()] + s[m.end():]
for l in ('PalletTown_Movement_RivalWalkToRanchLeft', 'PalletTown_Movement_RivalWalkToRanchRight', 'PalletTown_Movement_PlayerWalkToRanchLeft', 'PalletTown_Movement_PlayerWalkToRanchRight', 'PalletTown_Movement_RivalEnterRanch', 'PalletTown_Movement_PlayerEnterRanch'):
    s = cut(s, l)
s = s.replace('PalletTown_Movement_OakEnterLeft::', mvs + 'PalletTown_Movement_OakEnterLeft::', 1)
old = s[s.index('\topendoor 36, 8\n'):s.index('\twaitstate\n', s.index('warp MAP_PALLET_TOWN_RIVALS_HOUSE'))]
new = '''\tremoveobject LOCALID_PALLET_RIVAL
\tsetflag FLAG_HIDE_PALLET_RIVAL
\tsetvar VAR_GRENALUX_OPENING, 1
\tsetflag FLAG_DONT_TRANSITION_MUSIC
\twarp MAP_PALLET_TOWN_RANCH, 0, 7
'''
s = s.replace(old, new)
wr('data/maps/PalletTown/scripts.inc', s)

# ---- B. seams (ground) + borders
def lay(d): 
    bb = open(R+'data/layouts/%s/map.bin' % d, 'rb').read(); return list(struct.unpack('<%dH' % (len(bb)//2), bb))
def put(d, a): open(R+'data/layouts/%s/map.bin' % d, 'wb').write(struct.pack('<%dH' % len(a), *a))
PT = lay('PalletTown'); RA = lay('PalletTownRanch')
for y, t in ((6, 0x119), (7, 0x129)):
    PT[y*44+43] = (PT[y*44+43] & ~0x3ff) | t
    RA[y*32+0] = (RA[y*32+0] & ~0x3ff) | t
put('PalletTown', PT); put('PalletTownRanch', RA)
open(R+'data/layouts/Route1/border.bin', 'wb').write(open(R+'data/layouts/PalletTown/border.bin', 'rb').read())

# (C: a Pallet<->Route 1 connection was tried and dropped: the two maps use different tilesets -> garbled tiles)
print('ok')
