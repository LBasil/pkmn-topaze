#!/usr/bin/env python3
"""Open walls so areas formerly reachable only by teleport are walkable (7F rival room, 11F lobby)."""
import json,struct
dl=json.load(open('data/layouts/layouts.json'))['layouts']
def carve(floor,cells,src):
    L=[x for x in dl if x.get('id')==f'LAYOUT_SILPH_CO_{floor}F'][0]; W=L['width']
    p=L['blockdata_filepath']; b=bytearray(open(p,'rb').read())
    v=struct.unpack_from('<H',b,(src[1]*W+src[0])*2)[0]
    for x,y in cells: struct.pack_into('<H',b,(y*W+x)*2,v)
    open(p,'wb').write(b)
carve(7,[(6,7),(7,7)],(8,7))
carve(11,[(13,19),(14,19)],(12,19))
