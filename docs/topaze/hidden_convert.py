#!/usr/bin/env python3
"""Convertit les objets caches 'hidden_item' dont le drapeau n'est PAS dans la plage moteur (FLAG_HIDDEN_ITEMS_START+0..255 = 0x3E8..0x4E7, octet) en panneaux (bg_event sign) a script :
le moteur calcule drapeau = FLAG_HIDDEN_ITEMS_START + octet, donc un drapeau hors plage collisionne avec un AUTRE drapeau. Concerne tous les FLAG_TOPAZE_(HID|FIND|FOSSIL)_*.
Le script donne l'objet (checkitemspace), pose le meme drapeau. Idempotent. Usage : python3 docs/topaze/hidden_convert.py"""
import sys, json, glob, os, re
sys.path.insert(0, 'docs/topaze')
import newmap as N
n = 0
for p in sorted(glob.glob('data/maps/*/map.json')):
    d = json.load(open(p)); m = os.path.basename(os.path.dirname(p)); ch = False; sc = ''; tx = ''; k = 0
    for i, b in enumerate(d.get('bg_events', [])):
        if b.get('type') != 'hidden_item' or not re.match(r'FLAG_TOPAZE_(HID|FIND|FOSSIL)', b.get('flag', '')): continue
        S = '%s_EventScript_TopazeFind%d' % (m, k); T = '%s_Text_TopazeFindFull' % m; k += 1
        sc += ('%s::\n\tlock\n\tgoto_if_set %s, %s_Done\n\tcheckitemspace %s, %d\n\tgoto_if_eq VAR_RESULT, FALSE, %s_Full\n\tgiveitem %s, %d\n\tsetflag %s\n\trelease\n\tend\n\n%s_Done::\n\trelease\n\tend\n\n%s_Full::\n\tmsgbox %s\n\trelease\n\tend\n\n') % (
            S, b['flag'], S, b['item'], b.get('quantity', 1), S, b['item'], b.get('quantity', 1), b['flag'], S, S, T)
        d['bg_events'][i] = N.sign(b['x'], b['y'], S, 0); ch = True; n += 1
    if ch:
        N.jdump(d, p)
        open('data/maps/%s/scripts.inc' % m, 'a').write('\n@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)\n' + sc)
        open('data/maps/%s/text.inc' % m, 'a').write(N.text('%s_Text_TopazeFindFull' % m, 'Something shines here, but your BAG is full.'))
print('convertis', n)
