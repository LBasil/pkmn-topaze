#!/usr/bin/env python3
"""Mine de Grenalux (post-game) : remplie un peu (mineurs qui racontent la veine, objets, objets caches). Idempotent."""
import json, re
ROOT = '/home/claude/pkmn-topaze/'
FL = {0x126: 'MINE_1F_REVIVE', 0x127: 'MINE_1F_HEART', 0x128: 'MINE_2F_ETHER', 0x129: 'MINE_2F_ELIXIR', 0x12A: 'MINE_2F_PPUP', 0x12B: 'MINE_3F_MAXREVIVE', 0x12C: 'MINE_3F_CALCIUM'}
f = open(ROOT + 'include/constants/flags.h').read()
for n, name in FL.items():
    a = '#define FLAG_0x%X               0x%X\n' % (n, n)
    d = '#define FLAG_TOPAZE_%s FLAG_0x%X // mine de Grenalux (post-game)\n' % (name, n)
    assert a in f
    if d not in f: f = f.replace(a, a + d, 1)
open(ROOT + 'include/constants/flags.h', 'w').write(f)
def body(label, text):
    for l in re.split(r'\\n|\\p|\\l', text): assert len(l) <= 35, l
    parts = re.split(r'(?<=\\n)|(?<=\\p)|(?<=\\l)', text)
    return label + '::\n' + '\n'.join('    .string "%s%s"' % (p, '$' if i == len(parts) - 1 else '') for i, p in enumerate(parts)) + '\n\n'
M = {
 '1F': dict(
  npcs=[(36, 22, 'Miner2', r"I came to dig for stones, and I\nfound the walls humming instead.\pThe old foreman says the vein is\nafraid of something. Of what?"),
        (8, 12, 'Miner3', r"Ten years ago the whole mine shook\nand nobody has dug a stone since.\pWe still come down for the quiet.\nAnd the warm light, deeper in.")],
  items=[(40, 7, 'ItemRevive', 'ITEM_REVIVE', 0x126)], hidden=[(4, 34, 'ITEM_HEART_SCALE', 0x127)]),
 '2F': dict(
  npcs=[(10, 16, 'Miner4', r"Careful on the lower floor. That\nlight is not from our lamps.\pMy old lamp flickers whenever I\nstep close to the glow.")],
  items=[(36, 5, 'ItemMaxEther', 'ITEM_MAX_ETHER', 0x128), (34, 34, 'ItemElixir', 'ITEM_ELIXIR', 0x129)], hidden=[(20, 5, 'ITEM_PP_UP', 0x12A)]),
 '3F': dict(npcs=[], items=[], hidden=[(19, 10, 'ITEM_MAX_REVIVE', 0x12B), (28, 29, 'ITEM_CALCIUM', 0x12C)]),
}
for fl, d in M.items():
    P = ROOT + 'data/maps/GrenaluxMine_%s/' % fl
    m = json.load(open(P + 'map.json')); pre = 'GrenaluxMine_%s_' % fl
    sc = open(P + 'scripts.inc').read(); tx = open(P + 'text.inc').read()
    def add_obj(x, y, gfx, script, flag):
        if any(o['script'] == pre + 'EventScript_' + script for o in m['object_events']): return
        m['object_events'].append({'type': 'object', 'graphics_id': gfx, 'x': x, 'y': y, 'elevation': 3, 'movement_type': 'MOVEMENT_TYPE_FACE_DOWN', 'movement_range_x': 0, 'movement_range_y': 0,
            'trainer_type': 'TRAINER_TYPE_NONE', 'trainer_sight_or_berry_tree_id': '0', 'script': pre + 'EventScript_' + script, 'flag': flag})
    for x, y, k, t in d['npcs']:
        add_obj(x, y, 'OBJ_EVENT_GFX_WORKER_M', k, '0')
        if pre + 'EventScript_%s::' % k not in sc:
            sc += '\n%sEventScript_%s::\n\tmsgbox %sText_%s, MSGBOX_NPC\n\tend\n' % (pre, k, pre, k)
            tx += '\n' + body(pre + 'Text_' + k, t).rstrip('\n') + '\n'
    for x, y, k, item, n in d['items']:
        add_obj(x, y, 'OBJ_EVENT_GFX_ITEM_BALL', k, 'FLAG_TOPAZE_' + FL[n])
        if pre + 'EventScript_%s::' % k not in sc: sc += '\n%sEventScript_%s::\n\tfinditem %s\n\tend\n' % (pre, k, item)
    for x, y, item, n in d['hidden']:
        if not any(b.get('item') == item and b.get('x') == x for b in m['bg_events']):
            m['bg_events'].append({'type': 'hidden_item', 'x': x, 'y': y, 'elevation': 0, 'item': item, 'flag': 'FLAG_TOPAZE_' + FL[n], 'quantity': 1, 'underfoot': False})
    json.dump(m, open(P + 'map.json', 'w'), indent=2); open(P + 'map.json', 'a').write('\n')
    open(P + 'scripts.inc', 'w').write(sc); open(P + 'text.inc', 'w').write(tx)
print('ok')
