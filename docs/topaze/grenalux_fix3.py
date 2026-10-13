# Grenalux fix 3: smooth Grenalux <-> Route 1 connection (no warp, no black screen).
# A connection draws the neighbour's strip with the CURRENT map's tilesets -> the strip must only use tiles identical in both
# tilesets: primary metatiles with palettes 0,2,5 (identical in general_emerald / general_gradient).
# So Grenalux gets 4 extra forest rows at the top (everything shifts +4 in y) and Route 1's bottom rows are cleaned.
# NOT re-runnable (git checkout data src docs first).
import json, struct, re, glob
R = '/home/claude/pkmn-topaze/'
def rd(p): return open(R+p).read()
def wr(p, s): open(R+p, 'w').write(s)
def jr(p): return json.load(open(R+p))
def jw(p, j): wr(p, json.dumps(j, indent=2) + '\n')
SH = 4

# 1. layout: prepend SH rows (copies of old rows 0/1 alternately), clear the few secondary tiles of old row 2
b = open(R+'data/layouts/PalletTown/map.bin', 'rb').read(); v = list(struct.unpack('<%dH' % (len(b)//2), b)); W = 44
rows = [v[i:i+W] for i in range(0, len(v), W)]
assert len(rows) == 36
new = [list(rows[i % 2]) for i in range(SH)] + rows
for x in range(W):
    if (new[SH+2][x] & 0x3ff) >= 0x280: new[SH+2][x] = (new[SH+2][x] & ~0x3ff) | 0x4
flat = [t for r in new for t in r]
open(R+'data/layouts/PalletTown/map.bin', 'wb').write(struct.pack('<%dH' % len(flat), *flat))
s = rd('data/layouts/layouts.json')
i = s.index('"id": "LAYOUT_PALLET_TOWN"'); j = s.index('"height": 36', i)
s = s[:j] + '"height": %d' % (36+SH) + s[j+len('"height": 36'):]
wr('data/layouts/layouts.json', s)

# 2. Pallet map.json: events +SH, warps to Route 1 removed, connections
pj = jr('data/maps/PalletTown/map.json')
for k in ('object_events', 'coord_events', 'bg_events', 'warp_events'):
    for e in pj.get(k, []): e['y'] += SH
pj['warp_events'] = [w for w in pj['warp_events'] if w['dest_map'] != 'MAP_ROUTE1']
for c in pj['connections']:
    if c['map'] == 'MAP_PALLET_TOWN_RANCH': c['offset'] = SH
pj['connections'].append({'map': 'MAP_ROUTE1', 'offset': 10, 'direction': 'up'})
jw('data/maps/PalletTown/map.json', pj)
rj = jr('data/maps/PalletTown_Ranch/map.json')
for c in rj['connections']:
    if c['map'] == 'MAP_PALLET_TOWN': c['offset'] = -SH
jw('data/maps/PalletTown_Ranch/map.json', rj)

# 3. Route 1: connection down, warps removed, bottom cleaned of secondary metatiles
r1 = jr('data/maps/Route1/map.json')
r1['warp_events'] = [w for w in r1['warp_events'] if w['dest_map'] != 'MAP_PALLET_TOWN']
r1['connections'] = [{'map': 'MAP_PALLET_TOWN', 'offset': -10, 'direction': 'down'}]
jw('data/maps/Route1/map.json', r1)
b = open(R+'data/layouts/Route1/map.bin', 'rb').read(); v = list(struct.unpack('<%dH' % (len(b)//2), b)); W1 = 26
grass = next(t for t in v[35*W1:36*W1] if (t & 0x3ff) == 1 and ((t >> 10) & 3) == 0)
for y in range(33, 38):
    for x in range(W1):
        if (v[y*W1+x] & 0x3ff) >= 0x280: v[y*W1+x] = grass
open(R+'data/layouts/Route1/map.bin', 'wb').write(struct.pack('<%dH' % len(v), *v))
# warp ids: Pallet 6..9 -> 4..7 ; Route1 2..5 -> 0..3
for f in glob.glob(R+'data/maps/*/map.json'):
    j = json.load(open(f)); ch = False
    for w in j.get('warp_events', []):
        if w['dest_map'] == 'MAP_PALLET_TOWN' and int(w['dest_warp_id']) >= 6: w['dest_warp_id'] = str(int(w['dest_warp_id'])-2); ch = True
        if w['dest_map'] == 'MAP_ROUTE1' and int(w['dest_warp_id']) >= 2: w['dest_warp_id'] = str(int(w['dest_warp_id'])-2); ch = True
    if ch: jw(f[len(R):], j)

# 4. absolute Pallet coordinates in scripts / heal location
s = rd('data/maps/PalletTown/scripts.inc')
for a, b2 in (('LOCALID_PALLET_SIGN_LADY, 10, 16', 'LOCALID_PALLET_SIGN_LADY, 10, %d' % (16+SH)), ('LOCALID_PALLET_SIGN_LADY, 22, 2\n', 'LOCALID_PALLET_SIGN_LADY, 22, %d\n' % (2+SH)),
              ('LOCALID_PALLET_PROF_OAK, 22, 15', 'LOCALID_PALLET_PROF_OAK, 22, %d' % (15+SH)), ('opendoor 35, 21', 'opendoor 35, %d' % (21+SH)), ('closedoor 35, 21', 'closedoor 35, %d' % (21+SH))):
    assert a in s, a; s = s.replace(a, b2)
wr('data/maps/PalletTown/scripts.inc', s)
h = rd('src/data/heal_locations.json')
a = '"map": "MAP_PALLET_TOWN",\n      "x": 8,\n      "y": 10,'
assert a in h; wr('src/data/heal_locations.json', h.replace(a, '"map": "MAP_PALLET_TOWN",\n      "x": 8,\n      "y": %d,' % (10+SH)))
print('ok')
