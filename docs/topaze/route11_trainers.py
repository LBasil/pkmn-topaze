# ROUTE 11 : 10 dresseurs remontes (niv. 24-28), textes retouches, sauvages Route 11 et Grotte des Taupiqueurs. Idempotent.
import json, re
T = {  # id: (equipe)
 'TRAINER_YOUNGSTER_EDDIE': [('SANDSHREW', 25), ('DIGLETT', 25), ('EKANS', 26)],
 'TRAINER_YOUNGSTER_DILLON': [('RATTATA', 24), ('RATICATE', 25), ('SANDSHREW', 26)],
 'TRAINER_YOUNGSTER_YASU': [('NIDORINO', 26), ('RATICATE', 26), ('DIGLETT', 25)],
 'TRAINER_YOUNGSTER_DAVE': [('EKANS', 26), ('NIDORINO', 27), ('DUGTRIO', 28)],
 'TRAINER_ENGINEER_BRAXTON': [('MAGNEMITE', 26), ('MAGNEMITE', 26), ('MAGNETON', 28)],
 'TRAINER_ENGINEER_BERNIE': [('MAGNEMITE', 25), ('VOLTORB', 26), ('MAGNETON', 27)],
 'TRAINER_GAMER_HUGO': [('DROWZEE', 26), ('MEOWTH', 26), ('PERSIAN', 28)],
 'TRAINER_GAMER_JASPER': [('MACHOP', 26), ('MACHOKE', 28)],
 'TRAINER_GAMER_DIRK': [('KADABRA', 27), ('DROWZEE', 27), ('MR_MIME', 28)],
 'TRAINER_GAMER_DARIAN': [('GEODUDE', 25), ('GRAVELER', 27), ('ONIX', 27)],
}
tr = open('src/data/trainers.h').read(); pa = open('src/data/trainer_parties.h').read()
for i, team in T.items():
    b = re.search(r'\[%s\] = \{.*?\n    \},' % i, tr, re.S).group(0)
    sym = re.search(r'NO_ITEM_(?:DEFAULT|CUSTOM)_MOVES\((\w+)\)', b).group(1)
    m = re.search(r'static const struct TrainerMon\w+ %s\[\] = \{.*?\n\};' % sym, pa, re.S); assert m, sym
    if 'Custom' in m.group(0).split(sym)[0]: raise SystemExit('custom moves ' + sym)
    body = ''.join('    {\n        .iv = 0,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n' % (lv, sp) for sp, lv in team)
    pa = pa.replace(m.group(0), 'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};' % (sym, body))
open('src/data/trainer_parties.h', 'w').write(pa)
# textes
def setText(label, new):
    p = 'data/maps/Route11/text.inc'; s = open(p).read()
    a = s.index(label + '::'); b = s.index('\n\n', a) if '\n\n' in s[a:] else len(s)
    lines = new.split('\n'); out = ''
    for k, ln in enumerate(lines):
        for part in re.split(r'(?<=\\n)|(?<=\\p)|(?<=\\l)', ln): assert len(part.replace('\\n', '').replace('\\p', '').replace('\\l', '')) <= 35, part
        out += '    .string "%s%s"\n' % (ln, '$' if k == len(lines) - 1 else '')
    open(p, 'w').write(s[:a] + label + '::\n' + out.rstrip('\n') + s[b:])
setText('Route11_Text_EddiePostBattle', 'I dig burrows with my POKéMON.\\nMen in black asked me for the\\pquickest way underground. Weird.')
setText('Route11_Text_DavePostBattle', 'Tch...\\nMen in black dug through the\\pDIGLETT burrows and scared them.\\nThe tunnel is a mess.')
setText('Route11_Text_YasuPostBattle', 'The huge sleeper on ROUTE 12 will\\nnot budge. Take the long way\\pround, through ROCK TUNNEL.')
setText('Route11_Text_DarianPostBattle', 'The men in black pushed past me.\\nThey carried a heavy sack.')
# sauvages
SP = [('SANDSHREW', 22), ('SPEAROW', 23), ('DIGLETT', 22), ('SPEAROW', 22), ('DROWZEE', 23), ('DROWZEE', 24), ('SANDSHREW', 24),
      ('SPEAROW', 25), ('DIGLETT', 24), ('DROWZEE', 25), ('DIGLETT', 25), ('DUGTRIO', 27)]
CV = [('DIGLETT', 22), ('DIGLETT', 23), ('DIGLETT', 24), ('DIGLETT', 22), ('DIGLETT', 25), ('DIGLETT', 26), ('DIGLETT', 27), ('DIGLETT', 24),
      ('DIGLETT', 25), ('DUGTRIO', 29), ('DIGLETT', 26), ('DUGTRIO', 31)]
f = 'src/data/wild_encounters.json'; j = json.load(open(f)); g = j['wild_encounter_groups'][0]
for e in g['encounters']:
    sp = SP if e['map'] == 'MAP_ROUTE11' else CV if e['map'] == 'MAP_DIGLETTS_CAVE_B1F' else None
    if sp:
        e['land_mons']['mons'] = [{"min_level": l, "max_level": l, "species": "SPECIES_" + s} for s, l in sp]
json.dump(j, open(f, 'w'), indent=2, ensure_ascii=False); open(f, 'a').write('\n')
print('route 11 ok')
