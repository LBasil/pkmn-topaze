# ROUTES 9 et 10 : dresseurs remontes (niv. 27-30), indices Onybris, sauvages. Idempotent.
import json, re
T = {
 'TRAINER_PICNICKER_ALICIA': [('CLEFAIRY', 27), ('GLOOM', 28), ('JIGGLYPUFF', 27)],
 'TRAINER_HIKER_JEREMY': [('GEODUDE', 27), ('GRAVELER', 28), ('MACHOP', 28)],
 'TRAINER_HIKER_ALAN': [('ONIX', 28), ('MACHOKE', 29)],
 'TRAINER_CAMPER_CHRIS': [('GROWLITHE', 27), ('PONYTA', 28), ('VULPIX', 27)],
 'TRAINER_BUG_CATCHER_BRENT': [('VENOMOTH', 28), ('BEEDRILL', 28)],
 'TRAINER_BUG_CATCHER_CONNER': [('BUTTERFREE', 28), ('PINSIR', 29)],
 'TRAINER_HIKER_BRICE': [('GRAVELER', 29), ('RHYHORN', 29), ('MACHOKE', 29)],
 'TRAINER_PICNICKER_CAITLIN': [('PIDGEOTTO', 28), ('GLOOM', 28), ('PERSIAN', 29)],
 'TRAINER_CAMPER_DREW': [('SANDSLASH', 28), ('PRIMEAPE', 29)],
 'TRAINER_PICNICKER_CAROL': [('CLEFAIRY', 28), ('GLOOM', 28)],
 'TRAINER_HIKER_CLARK': [('GEODUDE', 28), ('GRAVELER', 29), ('ONIX', 29)],
 'TRAINER_POKEMANIAC_HERMAN': [('SLOWPOKE', 28), ('LICKITUNG', 29), ('SLOWBRO', 29)],
 'TRAINER_HIKER_TRENT': [('MACHOP', 28), ('MACHOKE', 29), ('GRAVELER', 29)],
 'TRAINER_POKEMANIAC_MARK': [('CUBONE', 28), ('RHYHORN', 29), ('LICKITUNG', 29)],
 'TRAINER_PICNICKER_HEIDI': [('CLEFAIRY', 28), ('PIDGEOTTO', 29), ('MEOWTH', 28)],
}
tr = open('src/data/trainers.h').read(); pa = open('src/data/trainer_parties.h').read()
for i, team in T.items():
    b = re.search(r'\[%s\] = \{.*?\n    \},' % i, tr, re.S).group(0)
    sym = re.search(r'NO_ITEM_(DEFAULT|CUSTOM)_MOVES\((\w+)\)', b)
    if sym.group(1) == 'CUSTOM': tr = tr.replace(b, b.replace('NO_ITEM_CUSTOM_MOVES', 'NO_ITEM_DEFAULT_MOVES'))
    sym = sym.group(2)
    m = re.search(r'static const struct TrainerMon\w+ %s\[\] = \{.*?\n\};' % sym, pa, re.S); assert m, sym
    body = ''.join('    {\n        .iv = 0,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n' % (lv, sp) for sp, lv in team)
    pa = pa.replace(m.group(0), 'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};' % (sym, body))
open('src/data/trainer_parties.h', 'w').write(pa); open('src/data/trainers.h', 'w').write(tr)
def setText(p, label, new):
    s = open(p).read(); a = s.index(label + '::'); b = s.index('\n\n', a) if '\n\n' in s[a:] else len(s)
    for part in re.split(r'\\n|\\p|\\l', new): assert len(part) <= 35, part
    open(p, 'w').write(s[:a] + label + '::\n    .string "%s$"' % new + s[b:])
r9, r10 = 'data/maps/Route9/text.inc', 'data/maps/Route10/text.inc'
setText(r9, 'Route9_Text_AlicaPostBattle'.replace('Alica', 'Alicia'), 'Men in black went by at dawn.\\nThey hurried toward ROCK TUNNEL.')
setText(r9, 'Route9_Text_ChrisPostBattle', 'Their bags clinked like stones.\\nI did not dare ask what was in.')
setText(r10, 'Route10_Text_HeidiPostBattle', 'Men in black walked into ROCK\\nTUNNEL with a heavy sack.\\pThey did not even use a light.\\nWho does that?')
setText(r10, 'Route10_Text_CarolPostBattle', 'The POKéMON here are so chunky...\\pThe strange men in black were\\nthin as rails. Odd, no?')
SP9 = [('GEODUDE', 25), ('SPEAROW', 26), ('SANDSHREW', 26), ('MACHOP', 26), ('GEODUDE', 27), ('RATICATE', 27), ('SPEAROW', 28),
       ('MACHOP', 28), ('ONIX', 27), ('SANDSHREW', 28), ('FEAROW', 29), ('GRAVELER', 29)]
SP10 = [('SPEAROW', 27), ('VOLTORB', 27), ('SANDSHREW', 27), ('SPEAROW', 28), ('VOLTORB', 28), ('MACHOP', 28), ('GEODUDE', 28),
        ('VOLTORB', 29), ('MAGNEMITE', 29), ('MACHOP', 29), ('ELECTRODE', 30), ('GRAVELER', 30)]
f = 'src/data/wild_encounters.json'; j = json.load(open(f)); g = j['wild_encounter_groups'][0]
for e in g['encounters']:
    sp = SP9 if e['map'] == 'MAP_ROUTE9' else SP10 if e['map'] == 'MAP_ROUTE10' else None
    if sp: e['land_mons']['mons'] = [{"min_level": l, "max_level": l, "species": "SPECIES_" + s} for s, l in sp]
json.dump(j, open(f, 'w'), indent=2, ensure_ascii=False); open(f, 'a').write('\n')
print('routes 9/10 ok')
