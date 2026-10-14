#!/usr/bin/env python3
"""NPC immobiles en extérieur -> petite errance (QOL). Ne touche pas : dresseurs, objets/Pokémon, NPC référencés par des scripts de mouvement,
NPC collés à un warp/événement. 2 NPC sur 3 bougent (déterministe). Rejouable : ne convertit que les FACE_*. Usage : npc_wander.py [--apply]"""
import json, glob, re, sys
APPLY = '--apply' in sys.argv
HUMAN = ('MAN', 'WOMAN', 'BOY', 'GIRL', 'LASS', 'CAMPER', 'PICNICKER', 'BEAUTY', 'WORKER', 'SAILOR', 'FISHER', 'GENTLEMAN', 'SCIENTIST', 'BALDING', 'BLACK_BELT',
         'SUPER_NERD', 'BIKER', 'CUE_BALL', 'JUGGLER', 'ROCKER', 'BURGLAR', 'TUBER', 'SWIMMER', 'HIKER', 'COOLTRAINER', 'PSYCHIC', 'TEACHER', 'MOTHER', 'FARMER',
         'HIKER', 'OLD_', 'EXPERT', 'GUITARIST', 'SCHOOL', 'KID', 'MAN_', 'CHILD', 'MINER', 'GARDENER', 'DAISY', 'BIRD_KEEPER', 'ENGINEER', 'POKEFAN')
BAD = ('ITEM_BALL', 'CUT_TREE', 'ROCK', 'BOULDER', 'SNORLAX', 'FOSSIL', 'SIGN', 'POKE_BALL', 'TRUCK', 'BERRY', 'ROCKET', 'GRUNT', 'GUARD', 'POLICE', 'OFFICER')
ok = 0; skip = {}; tot = 0; changed = []
for d in sorted(glob.glob('data/maps/*/map.json')):
    name = d.split('/')[2]; j = json.load(open(d))
    outdoor = j.get('map_type') in ('MAP_TYPE_TOWN', 'MAP_TYPE_CITY', 'MAP_TYPE_ROUTE')
    house = j.get('map_type') == 'MAP_TYPE_INDOOR' and ('House' in name or 'Home' in name) and 'Mart' not in name
    if not (outdoor or house): continue
    try: sc = open('data/maps/%s/scripts.inc' % name).read()
    except Exception: sc = ''
    near = [(w['x'], w['y']) for w in j.get('warp_events', [])] + [(c['x'], c['y']) for c in j.get('coord_events', [])] + [(b['x'], b['y']) for b in j.get('bg_events', [])]
    n = 0
    for o in j['object_events']:
        if o.get('trainer_type') != 'TRAINER_TYPE_NONE' or not (o['movement_type'].startswith('MOVEMENT_TYPE_FACE_') or o['movement_type'] == 'MOVEMENT_TYPE_LOOK_AROUND'): continue
        g = o['graphics_id'].replace('OBJ_EVENT_GFX_', ''); tot += 1
        why = None
        if any(b in g for b in BAD) or not any(h in g for h in HUMAN): why = 'gfx'
        elif o.get('local_id') and len(re.findall(r'\b%s\b' % o['local_id'], sc)) > 0: why = 'scripted'
        elif any(abs(o['x'] - x) <= (1 if outdoor else 2) and abs(o['y'] - y) <= (1 if outdoor else 2) for x, y in near): why = 'near'
        elif (o['x'] * 7 + o['y'] * 13 + n) % 4 == 0: why = 'stay'
        n += 1
        if why: skip[why] = skip.get(why, 0) + 1; continue
        r = 2 if outdoor else 1
        if APPLY: o['movement_type'] = 'MOVEMENT_TYPE_WANDER_AROUND'; o['movement_range_x'] = r; o['movement_range_y'] = r
        ok += 1; changed.append((name, g, o['x'], o['y']))
    if APPLY: open(d, 'w').write(json.dumps(j, indent=2) + '\n')
print('candidates', tot, 'converted', ok, 'skipped', skip)
if not APPLY:
    for c in changed[:200]: print(*c)
