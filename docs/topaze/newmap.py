"""Bibliotheque : creer des cartes qui reutilisent un layout existant (clone d'une carte modele) et reecrire le contenu d'une carte existante.
    clone(new, template, objects=[], warps=None, bgs=[], coords=[], scripts='', text='', **overrides)
    rewrite(name, objects, scripts, text, bgs=[], coords=[])
Les scripts/textes s'ecrivent en TOTALITE (reecriture), donc les generateurs restent idempotents (test d'existence cote appelant)."""
import json, os, re
def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)
def jdump(o, f): json.dump(o, open(f, 'w'), indent=2, ensure_ascii=False); open(f, 'a').write('\n')
def mapid(name): return 'MAP_' + re.sub(r'(?<=[a-z])(?=[A-Z])', '_', name).upper()
def obj(gfx, x, y, script, mv='MOVEMENT_TYPE_FACE_DOWN', flag='0', el=3, rx=1, ry=1, ttype='TRAINER_TYPE_NONE', sight='0'):
    return {"type": "object", "graphics_id": 'OBJ_EVENT_GFX_' + gfx, "x": x, "y": y, "elevation": el, "movement_type": mv, "movement_range_x": rx, "movement_range_y": ry,
            "trainer_type": ttype, "trainer_sight_or_berry_tree_id": sight, "script": script, "flag": flag}
def sign(x, y, script, el=0): return {"type": "sign", "x": x, "y": y, "elevation": el, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": script}
def warp(x, y, dest, wid, el=3): return {"x": x, "y": y, "elevation": el, "dest_map": dest, "dest_warp_id": str(wid)}
def trigger(x, y, var, val, script, el=3): return {"type": "trigger", "x": x, "y": y, "elevation": el, "var": var, "var_value": str(val), "script": script}
def text(label, s):
    """.string en lignes de 35 car. max, 2 lignes par boite"""
    import textwrap
    t = s.replace('{PLAYER}', 'PLAYERX'); L = [l.replace('PLAYERX', '{PLAYER}') for l in textwrap.wrap(t, 35)]
    return '\n%s::\n%s\n' % (label, '\n'.join('\t.string "%s%s"' % (l, '$' if i == len(L) - 1 else ('\\p' if i % 2 else '\\n')) for i, l in enumerate(L)))
def _register(new, template):
    mg = json.load(open('data/maps/map_groups.json'))
    if not any(new in mg[g] for g in mg['group_order']):
        g = next((g for g in mg['group_order'] if template in mg[g]), 'gMapGroup_SpecialArea'); mg[g].append(new); jdump(mg, 'data/maps/map_groups.json')
    s = rd('data/event_scripts.s')
    for kind in ('scripts', 'text'):
        line = '\t.include "data/maps/%s/%s.inc"\n' % (new, kind)
        if line not in s:
            prev = '\t.include "data/maps/%s/%s.inc"\n' % (template, kind)
            if prev in s: s = s.replace(prev, prev + line, 1)
            else:
                alt = '\t.include "data/maps/%s/scripts.inc"\n' % template; assert alt in s, (template, kind)
                s = s.replace(alt, alt + line, 1)
    wr('data/event_scripts.s', s)
def clone(new, template, objects=(), warps=None, bgs=(), coords=(), scripts='', txt='', **ov):
    base = json.load(open('data/maps/%s/map.json' % template))
    base['id'] = mapid(new); base['name'] = new
    base['object_events'] = list(objects); base['bg_events'] = list(bgs); base['coord_events'] = list(coords)
    base['warp_events'] = list(warps) if warps is not None else []
    base['connections'] = None; base['show_map_name'] = False
    base.update(ov)
    os.makedirs('data/maps/%s' % new, exist_ok=True); jdump(base, 'data/maps/%s/map.json' % new)
    wr('data/maps/%s/scripts.inc' % new, '%s_MapScripts::\n\t.byte 0\n\n%s' % (new, scripts)); wr('data/maps/%s/text.inc' % new, txt.lstrip('\n'))
    _register(new, template); return base
def rewrite(name, objects, scripts, txt, bgs=(), coords=(), keep_warps=True, **ov):
    p = 'data/maps/%s/map.json' % name; d = json.load(open(p))
    d['object_events'] = list(objects); d['bg_events'] = list(bgs); d['coord_events'] = list(coords); d.update(ov); jdump(d, p)
    hdr = rd('data/maps/%s/scripts.inc' % name).split('\n\n')[0] if os.path.exists('data/maps/%s/scripts.inc' % name) else '%s_MapScripts::\n\t.byte 0' % name
    wr('data/maps/%s/scripts.inc' % name, hdr + '\n\n' + scripts); wr('data/maps/%s/text.inc' % name, txt.lstrip('\n'))
