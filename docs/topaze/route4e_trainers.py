# ROUTE 4 EST : 5 dresseurs (identifiants recycles, inutilises), textes, equipes, Pokemon sauvages. A lancer apres route4e_events.py. Idempotent.
# Positions : calculees par BFS (chemin ouest->est le plus court), dresseur a 3 cases du chemin, regard droit vers lui, jamais sur le chemin.
import json, re
M = 'Route4East'
# (id, classe, pic, nom, genre('M'/'F'), gfx, x, y, face, sight, equipe, intro, defaite, apres)
T = [
 ('TRAINER_BUG_CATCHER_3', 'HIKER', 'HIKER', 'MARCO', 'M', 'HIKER', 15, 11, 'DOWN', 3, [('GEODUDE', 13), ('MACHOP', 13)],
  "I climbed the whole MT. MOON\\nflank. This trail is easy!", "My legs are fine.\\nMy POKéMON, less so.",
  "The dust turns to moss further\\neast. That is where the\\pTOURMALINE starts to grow."),
 ('TRAINER_PICNICKER_HANNAH', 'PICNICKER', 'PICNICKER', 'TESSA', 'F', 'PICNICKER', 25, 13, 'UP', 3, [('PARAS', 13), ('CLEFAIRY', 14)],
  "The ground sparkles here!\\nIt's moon dust, you know.", "Oh no, my sparkles!",
  "CLEFAIRY dance in the moon dust\\nwhen the sky is clear."),
 ('TRAINER_CAMPER_2', 'CAMPER', 'CAMPER', 'LEO', 'M', 'CAMPER', 34, 12, 'RIGHT', 3, [('VENONAT', 15), ('MANKEY', 15)],
  "Camping here is great. No one\\nbothers you, except TRAINERS!", "You ruined my evening.",
  "The trees get thicker toward the\\ncrystals. Watch your step."),
 ('TRAINER_LASS_2', 'LASS', 'LASS', 'NINA', 'F', 'LASS', 46, 20, 'UP', 3, [('ODDISH', 15), ('BELLSPROUT', 16)],
  "These crystals sing when the\\nwind blows. Listen!", "You broke my concentration!",
  "TOURMALIA is just ahead. Its\\nhouses are built in the trees."),
 ('TRAINER_BUG_CATCHER_4', 'BUG_CATCHER', 'BUG_CATCHER', 'RIO', 'M', 'BUG_CATCHER', 59, 15, 'DOWN', 3, [('CATERPIE', 14), ('WEEDLE', 14), ('VENONAT', 15)],
  "Bugs are different since the\\nAURA. Check their types!", "My bugs are special!",
  "CATERPIE is PSYCHIC now.\\nWEEDLE is ELECTRIC.\\pMind its sting."),
]
for t in T:
    for s in t[11:14]:
        for line in re.split(r'\\n|\\p', s): assert len(line) <= 35, (t[3], line)

# ---- trainers.h
f = 'src/data/trainers.h'; s = open(f).read()
for (i, cl, pic, name, g, gfx, *_r) in T:
    m = re.search(r'(\[%s\] = \{.*?\n    \},)' % i, s, re.S); b = m.group(1)
    b2 = re.sub(r'TRAINER_CLASS_\w+', 'TRAINER_CLASS_' + cl, b, count=1)
    b2 = re.sub(r'TRAINER_PIC_\w+', 'TRAINER_PIC_' + pic, b2, count=1)
    b2 = re.sub(r'\.trainerName = _\("[^"]*"\)', '.trainerName = _("%s")' % name, b2, count=1)
    mus = 'MALE' if g == 'M' else 'FEMALE | F_TRAINER_FEMALE'
    b2 = re.sub(r'\.encounterMusic_gender = [^,]+,', '.encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_%s,' % mus, b2, count=1)
    s = s.replace(b, b2)
open(f, 'w').write(s)
# ---- equipes (types NoItemDefaultMoves)
PN = {'TRAINER_BUG_CATCHER_3': 'sParty_BugCatcher3', 'TRAINER_PICNICKER_HANNAH': 'sParty_PicnickerHannah', 'TRAINER_CAMPER_2': 'sParty_Camper2',
      'TRAINER_LASS_2': 'sParty_Lass2', 'TRAINER_BUG_CATCHER_4': 'sParty_BugCatcher4'}
f = 'src/data/trainer_parties.h'; s = open(f).read()
for t in T:
    pn = PN[t[0]]
    m = re.search(r'static const struct TrainerMonNoItemDefaultMoves %s\[\] = (?:\{DUMMY_TRAINER_MON\};|\{.*?\n\};)' % pn, s, re.S); assert m, pn
    body = ''.join('    {\n        .iv = 0,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n' % (lv, sp) for sp, lv in t[10])
    s = s.replace(m.group(0), 'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};' % (pn, body))
open(f, 'w').write(s)
# ---- carte
f = 'data/maps/%s/map.json' % M; d = json.load(open(f))
d['object_events'] = []
for (i, cl, pic, name, g, gfx, x, y, face, sight, *_r) in T:
    d['object_events'].append({"type": "object", "graphics_id": "OBJ_EVENT_GFX_" + gfx, "x": x, "y": y, "elevation": 3,
        "movement_type": "MOVEMENT_TYPE_FACE_" + face, "movement_range_x": 0, "movement_range_y": 0, "trainer_type": "TRAINER_TYPE_NORMAL",
        "trainer_sight_or_berry_tree_id": str(sight), "script": "%s_EventScript_%s" % (M, name.capitalize()), "flag": "0"})
json.dump(d, open(f, 'w'), indent=2); open(f, 'a').write('\n')
# ---- scripts + textes (regeneres a chaque lancement)
def cut(path, marker):
    s = open(path).read()
    k = s.find(marker)
    if k >= 0: s = s[:k].rstrip('\n') + '\n'
    return s
sc = cut('data/maps/%s/scripts.inc' % M, '@ ---- TRAINERS (route4e_trainers.py)')
tx = cut('data/maps/%s/text.inc' % M, '@ ---- TRAINERS (route4e_trainers.py)')
sc += '\n@ ---- TRAINERS (route4e_trainers.py)\n'; tx += '\n@ ---- TRAINERS (route4e_trainers.py)\n'
for (i, cl, pic, name, g, gfx, x, y, face, sight, party, intro, defeat, post) in T:
    n = name.capitalize()
    sc += '\n%s_EventScript_%s::\n\ttrainerbattle_single %s, %s_Text_%sIntro, %s_Text_%sDefeat\n\tmsgbox %s_Text_%sPostBattle, MSGBOX_AUTOCLOSE\n\tend\n' % (M, n, i, M, n, M, n, M, n)
    for k, v in (('Intro', intro), ('Defeat', defeat), ('PostBattle', post)):
        lines = v.replace('\\p', '\\p\n').split('\n')
        out = []
        for ln in lines:
            out.append('    .string "%s"' % ln if ln.endswith('\\p') or ln.endswith('\\n') else '    .string "%s"' % ln)
        # reconstitue : une chaine .string par morceau, fin '$'
        body = ''.join('    .string "%s"\n' % ln if j < len(lines) - 1 else '    .string "%s$"\n' % ln for j, ln in enumerate(lines))
        tx += '\n%s_Text_%s%s::\n%s' % (M, n, k, body)
open('data/maps/%s/scripts.inc' % M, 'w').write(sc); open('data/maps/%s/text.inc' % M, 'w').write(tx)
# ---- sauvages (FR et LG identiques)
SP = [('ODDISH', 14), ('PARAS', 14), ('GEODUDE', 13), ('VENONAT', 15), ('BELLSPROUT', 14), ('PIDGEY', 14), ('CLEFAIRY', 14), ('MANKEY', 15),
      ('ODDISH', 16), ('VENONAT', 16), ('EXEGGCUTE', 15), ('CLEFAIRY', 16)]
f = 'src/data/wild_encounters.json'; j = json.load(open(f))
g = j['wild_encounter_groups'][0]
g['encounters'] = [e for e in g['encounters'] if e['map'] != 'MAP_ROUTE4_EAST']
for lab in ('FireRed', 'LeafGreen'):
    g['encounters'].append({"map": "MAP_ROUTE4_EAST", "base_label": "sRoute4East_" + lab,
        "land_mons": {"encounter_rate": 21, "mons": [{"min_level": l, "max_level": l, "species": "SPECIES_" + sp} for sp, l in SP]}})
json.dump(j, open(f, 'w'), indent=2, ensure_ascii=False); open(f, 'a').write('\n')
print('route 4 est : 5 dresseurs, sauvages')
