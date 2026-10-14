# Route 1 <-> Viridian smooth connection (no warp). Strip tiles must exist in both tilesets -> primary trees (1d4/1d5/1dc/1dd) + grass.
# Route 1 gets 5 new rows on top (everything shifts +5 in y); Viridian's bottom rows 35..39 become a primary forest edge.
# NOT re-runnable (git checkout data first).
import json, struct, glob
R = '/home/claude/pkmn-topaze/'
SH = 5
def jr(p): return json.load(open(R+p))
def jw(p, j): open(R+p, 'w').write(json.dumps(j, indent=2) + '\n')
def rdbin(p, w):
    b = open(R+p, 'rb').read(); v = struct.unpack('<%dH' % (len(b)//2), b); return [list(v[i:i+w]) for i in range(0, len(v), w)]
def wrbin(p, rows): flat = [t for r in rows for t in r]; open(R+p, 'wb').write(struct.pack('<%dH' % len(flat), *flat))

vir = rdbin('data/layouts/ViridianCity/map.bin', 42)
r1 = rdbin('data/layouts/Route1/map.bin', 26)
T = [[vir[38][12], vir[38][13]], [vir[39][12], vir[39][13]]]   # tree pair (top row / bottom row), with collision bits
assert (T[0][0] & 0x3ff) == 0x1d4 and (T[1][1] & 0x3ff) == 0x1dd
grass = next(t for t in r1[35] if (t & 0x3ff) == 1 and ((t >> 10) & 3) == 0)
GAP1 = (14, 15)      # Route 1 opening
GAP2 = (20, 21)      # Viridian opening
# Viridian rows 35..39
ground = vir[34][0] if False else vir[34][12]
for x in range(42): vir[35][x] = vir[34][x] if (vir[34][x] & 0x3ff) >= 0x280 and ((vir[34][x] >> 10) & 3) == 0 else ground
for y in (36, 37, 38, 39):
    for x in range(42):
        vir[y][x] = T[(y - 36) % 2][x % 2]
    for x in GAP2: vir[y][x] = grass
wrbin('data/layouts/ViridianCity/map.bin', vir)
# Route 1: 5 new rows
new = []
for y in range(SH):
    row = []
    for x in range(26):
        if y < 2: t = T[y % 2][x % 2]
        elif y < 4 and (x < 2 or x > 23): t = T[(y - 2) % 2][x % 2]
        else: t = grass
        if y < 4 and x in GAP1: t = grass
        row.append(t)
    new.append(row)
wrbin('data/layouts/Route1/map.bin', new + r1)
s = open(R+'data/layouts/layouts.json').read()
i = s.index('"id": "LAYOUT_ROUTE1"'); j = s.index('"height": 38', i)
open(R+'data/layouts/layouts.json', 'w').write(s[:j] + '"height": %d' % (38 + SH) + s[j+len('"height": 38'):])
# Route1 map.json
m = jr('data/maps/Route1/map.json')
for k in ('object_events', 'coord_events', 'bg_events'):
    for e in m.get(k, []): e['y'] += SH
m['warp_events'] = []
m['connections'].append({'map': 'MAP_VIRIDIAN_CITY', 'offset': -6, 'direction': 'up'})
jw('data/maps/Route1/map.json', m)
# Viridian map.json : warps 8,9 removed, ids > 9 shift by 2
v = jr('data/maps/ViridianCity/map.json')
assert [w['dest_map'] for w in v['warp_events'][8:10]] == ['MAP_ROUTE1'] * 2
v['warp_events'] = v['warp_events'][:8] + v['warp_events'][10:]
v['connections'] = (v['connections'] or []) + [{'map': 'MAP_ROUTE1', 'offset': 6, 'direction': 'down'}]
jw('data/maps/ViridianCity/map.json', v)
for f in glob.glob(R+'data/maps/*/map.json'):
    j = json.load(open(f)); ch = False
    for w in j.get('warp_events', []):
        if w['dest_map'] == 'MAP_VIRIDIAN_CITY' and int(w['dest_warp_id']) >= 10: w['dest_warp_id'] = str(int(w['dest_warp_id']) - 2); ch = True
    if ch: jw(f[len(R):], j)
print('ok')
