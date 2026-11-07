#!/usr/bin/env python3
"""Génère les données du wiki (docs/data/*.js) à partir des sources du jeu, en français ET en anglais.
Usage : python3 tools/topaze/build_site.py   (depuis la racine du dépôt)
Les pages (docs/*.html + docs/app.js) lisent ces fichiers ; ne pas éditer docs/data/*.js à la main.
Sources lues : src/data/*, include/constants/*, data/maps/*/map.json, tools/topaze/i18n/fr/* (traductions)."""
import re, json, os, glob
R = os.getcwd()
def rd(p): return open(os.path.join(R, p), encoding='utf-8').read()
def table(p):  # fichier EN=FR
    d = {}
    for l in rd(p).splitlines():
        if '=' in l and not l.startswith('#'):
            a, b = l.split('=', 1); d[a.strip()] = b.strip()
    return d
def pretty(s): return ' '.join(w.capitalize() for w in s.split('_'))
def clean(s): return s.replace('\\n', ' ').replace('\\p', ' ').replace('\\l', ' ').replace('{PKMN}', 'POKéMON').replace('  ', ' ').strip()

FR = 'tools/topaze/i18n/fr/'
fr_species, fr_moves, fr_abil, fr_items = (table(FR + f) for f in ('species.txt', 'moves.txt', 'abilities.txt', 'items.txt'))

# ---------- types ----------
TYPES = [('NORMAL','Normal','Normal'),('FIGHTING','Fighting','Combat'),('FLYING','Flying','Vol'),('POISON','Poison','Poison'),('GROUND','Ground','Sol'),('ROCK','Rock','Roche'),('BUG','Bug','Insecte'),('GHOST','Ghost','Spectre'),('STEEL','Steel','Acier'),('FIRE','Fire','Feu'),('WATER','Water','Eau'),('GRASS','Grass','Plante'),('ELECTRIC','Electric','Électrik'),('PSYCHIC','Psychic','Psy'),('ICE','Ice','Glace'),('DRAGON','Dragon','Dragon'),('DARK','Dark','Ténèbres'),('FAIRY','Fairy','Fée')]
tkey = {c: en for c, en, fr in TYPES}; tkey['MYSTERY'] = '???'
tfr = {en: fr for c, en, fr in TYPES}; tfr['???'] = '???'
def T(c): return tkey[c.replace('TYPE_', '')]

# ---------- noms ----------
sp_names = {c: n for c, n in re.findall(r'\[SPECIES_(\w+)\] = _\("([^"]*)"\)', rd('src/data/text/species_names.h')) if c != 'NONE'}
mv_names = {c: n for c, n in re.findall(r'\[MOVE_(\w+)\]\s*= _\("([^"]*)"\)', rd('src/data/text/move_names.h'))}
ab_names = {c: n for c, n in re.findall(r'\[ABILITY_(\w+)\] = _\("([^"]*)"\)', rd('src/data/text/abilities.h'))}
_SMALL = {'de', 'du', 'des', 'la', 'le', 'les', 'en', 'et', 'au', 'aux', 'sur', 'sous', 'à', 'un', 'une', 'dans', 'par', 'pour', 'of', 'the', 'and', 'in', 'on', 'to'}
def nice(en):
    t_ = en.title().replace("'S", "'s")
    ws = t_.split(' ')
    ws = [re.sub(r"^([DdLl])['’]([A-Za-zÀ-ÿ])", lambda m: m.group(1).lower() + "'" + m.group(2).upper(), w) if i > 0 else w for i, w in enumerate(ws)]
    t_ = ' '.join(ws)
    ws = t_.split(' ')
    return ' '.join(w if i == 0 or w.lower() not in _SMALL else w.lower() for i, w in enumerate(ws))
def rev(t): return {v.upper(): k for k, v in t.items()}
rsp, rmv, rab = rev(fr_species), rev(fr_moves), rev(fr_abil)
def pair(src, fr_t, r_t):
    u = src.upper()
    if u in r_t: return dict(en=nice(r_t[u]), fr=nice(u))      # source en français
    if u in fr_t: return dict(en=nice(u), fr=nice(fr_t[u]))    # source en anglais
    return dict(en=nice(src), fr=nice(src))
def SP(c): return pair(sp_names.get(c, c.replace('_', ' ')), fr_species, rsp)
FR_FULL = dict(DAZZLING_GLEAM='Éclat Magique', DISARMING_VOICE='Voix Enjôleuse', MYSTICAL_FIRE='Feu Ensorcelé', FREEZE_DRY='Lyophilisation', ASTRAL_BARRAGE='Éclat Spectral',
    HIGH_HORSEPOWER='Cavalcade Lourde', HEADLONG_RUSH='Assaut Frontal', DIAMOND_STORM='Orage Adamantin', DRAGON_HAMMER='Draco-Marteau', V_CREATE='Coup Victoire',
    SPARKLING_ARIA="Aria de l'Écume", STEAM_ERUPTION='Jet de Vapeur', PETAL_BLIZZARD='Tempête Florale', EERIE_IMPULSE='Ondes Étranges', DRAGON_ASCENT='Draco-Ascension',
    BLEAKWIND_STORM='Typhon Hivernal', BABY_DOLL_EYES='Regard Touchant', MULTI_ATTACK='Coup Varia-Type', TERRAIN_PULSE='Champlification', PRECIPICE_BLADES='Lame Pangéenne',
    THOUSAND_ARROWS='Mille Flèches', MALIGNANT_CHAIN='Chaîne Maléfique', NOXIOUS_TORQUE='Crash Toxique', MOONGEIST_BEAM='Rayon Spectral', LAST_RESPECTS='Hommage Posthume',
    TACHYON_CUTTER='Lame Tachyon', FREEZING_GLARE='Regard Glaçant', EXPANDING_FORCE='Vaste Pouvoir', PSYCHIC_NOISE='Dissonance Psy', HYPERSPACE_HOLE='Trou Dimensionnel',
    DRAGON_ENERGY='Draco-Énergie', BLAZING_TORQUE='Crash Brûlant', MAGICAL_TORQUE='Crash Magique', ALLURING_VOICE='Voix Envoûtante', RISING_VOLTAGE='Monte-Tension',
    DOUBLE_IRON_BASH="Écrous d'Poing", ORIGIN_PULSE='Onde Originelle', JET_PUNCH='Poing Sonique', EERIE_SPELL='Sort Sinistre')
def MV(c):
    for k in (c.replace('_', ' '), c.replace('_', '')):
        if k in fr_moves: return dict(en=nice(k), fr=nice(fr_moves[k]))
    r = pair(mv_names.get(c, c.replace('_', ' ')), fr_moves, rmv)
    if r['en'] == r['fr'] and c in mv_names:   # attaque ajoutée par Topaze : EN depuis la constante, FR complet si connu
        r = dict(en=nice(c.replace('_', ' ').title().replace(' Of ', ' of ').replace("'S", "'s")), fr=FR_FULL.get(c, r['fr']))
    return r
def AB(c): return pair(ab_names.get(c, c.replace('_', ' ')), fr_abil, rab)
_ij = json.loads(rd('src/data/items.json'))['items']
it_names = {i['itemId'].replace('ITEM_', ''): i['english'] for i in _ij}
def IT(c):
    en = it_names.get(c, c.replace('_', ' '))
    return dict(en=nice(en), fr=nice(fr_items.get(en, en)))

# ---------- Pokédex ----------
nat = re.search(r'enum\s*\{\s*NATIONAL_DEX_NONE,(.*?)\};', rd('include/constants/pokedex.h'), re.S).group(1)
order = [x for x in re.findall(r'NATIONAL_DEX_(\w+)', nat)]
si = rd('src/data/pokemon/species_info.h')
lv_ptr = dict(re.findall(r'\[SPECIES_(\w+)\] = (\w+),', rd('src/data/pokemon/level_up_learnset_pointers.h')))
lv_src = rd('src/data/pokemon/level_up_learnsets.h')
def learnset(label):
    m = re.search(r'%s\[\] = \{(.*?)LEVEL_UP_END' % label, lv_src, re.S)
    return [[int(l), MV(mv)] for l, mv in re.findall(r'LEVEL_UP_MOVE\(\s*(\d+),\s*MOVE_(\w+)\)', m.group(1))] if m else []
# CT / CS
items_c = rd('include/constants/items.h')
machine = {}  # TM06_TOXIC -> ('TM', 6, 'TOXIC')
for m in re.finditer(r'#define ITEM_(TM|HM)(\d\d)_(\w+) ', items_c): machine[m.group(1) + m.group(2) + '_' + m.group(3)] = (m.group(1), int(m.group(2)), m.group(3))
tm_src = rd('src/data/pokemon/tmhm_learnsets.h')
tm_by_sp = {}
for c, body in re.findall(r'\[SPECIES_(\w+)\]\s*=\s*TMHM_LEARNSET\((.*?)\),\s*(?=\n\s*\n|\n\s*\[|\n\s*\};)', tm_src, re.S):
    tm_by_sp[c] = [machine[k] for k in re.findall(r'TMHM\((\w+)\)', body) if k in machine]
tm_by_sp_all = tm_by_sp
# capacités œuf
egg_src = rd('src/data/pokemon/egg_moves.h')
egg = {}
for sp, body in re.findall(r'egg_moves\((\w+),(.*?)\)', egg_src, re.S):
    egg[sp] = [MV(m) for m in re.findall(r'MOVE_(\w+)', body)]
# évolutions
evo_src = rd('src/data/pokemon/evolution.h')
evolves = {}; evolved_from = {}
for sp, body in re.findall(r'\[SPECIES_(\w+)\]\s*=\s*\{(.*?)\},?\s*\n(?=\s*\[|\})', evo_src + '\n}', re.S):
    L = []
    for kind, par, tgt in re.findall(r'\{(EVO_\w+),\s*([^,]+?),\s*SPECIES_(\w+)\}', body):
        par = par.strip()
        if par.startswith('ITEM_'): p = IT(par[5:])
        elif par.isdigit(): p = int(par)
        else: p = par
        L.append(dict(to=tgt, kind=kind[4:], p=p)); evolved_from.setdefault(tgt, []).append(sp)
    if L: evolves[sp] = L
# dex EN/FR
dexent = rd('src/data/pokemon/pokedex_entries.h')
dex_en_txt = {m.group(1): clean(re.sub(r'"\s*"', '', m.group(2).replace('"\n    "', ''))) for m in re.finditer(r'const u8 (g\w+PokedexText)\[\] = _\(\s*((?:"[^"]*"\s*)+)\);', rd('src/data/pokemon/pokedex_text_fr.h'))}
def jtxt(raw): return clean(''.join(re.findall(r'"([^"]*)"', raw)))
dex_en_txt = {m.group(1): jtxt(m.group(2)) for m in re.finditer(r'const u8 (g\w+PokedexText)\[\] = _\(\s*((?:"[^"]*"\s*)+)\);', rd('src/data/pokemon/pokedex_text_fr.h'))}
dex_ent = {}
for k, body in re.findall(r'\[NATIONAL_DEX_(\w+)\] =\s*\{(.*?)\n    \}', dexent, re.S):
    cat = re.search(r'categoryName = _\("([^"]*)"\)', body); h = re.search(r'height = (\d+)', body); w = re.search(r'weight = (\d+)', body); d = re.search(r'\.description = (\w+)', body)
    dex_ent[k] = dict(cat=cat.group(1) if cat else '', h=int(h.group(1)) / 10 if h else 0, w=int(w.group(1)) / 10 if w else 0, text=dex_en_txt.get(d.group(1), '') if d else '')
dex_fr = {}
for l in rd(FR + 'dex.txt').splitlines():
    p = l.split('|', 2)
    if len(p) == 3: dex_fr[p[0].replace('NATIONAL_DEX_', '')] = (p[1], clean(p[2]))
EGG = {'MONSTER':('Monster','Monstre'),'WATER_1':('Water 1','Eau 1'),'BUG':('Bug','Insecte'),'FLYING':('Flying','Vol'),'FIELD':('Field','Terrestre'),'FAIRY':('Fairy','Féerique'),'GRASS':('Grass','Végétal'),'HUMAN_LIKE':('Human-Like','Humanoïde'),'WATER_3':('Water 3','Eau 3'),'MINERAL':('Mineral','Minéral'),'AMORPHOUS':('Amorphous','Amorphe'),'WATER_2':('Water 2','Eau 2'),'DITTO':('Ditto','Métamorph'),'DRAGON':('Dragon','Draconique'),'UNDISCOVERED':('Undiscovered','Inconnu')}
GROWTH = {'MEDIUM_FAST':('Medium Fast','Moyenne'),'ERRATIC':('Erratic','Erratique'),'FLUCTUATING':('Fluctuating','Fluctuante'),'MEDIUM_SLOW':('Medium Slow','Parabolique'),'FAST':('Fast','Rapide'),'SLOW':('Slow','Lente')}
dex = []
for k in order:
    if k not in sp_names: continue
    mm = re.search(r'\[SPECIES_%s\] =\s*\{(.*?)\n    \}' % k, si, re.S)
    if not mm: continue
    m = mm.group(1)
    g = lambda key: int(re.search(key + r' = (\d+)', m).group(1))
    st = [g(x) for x in ('baseHP','baseAttack','baseDefense','baseSpAttack','baseSpDefense','baseSpeed')]
    t = re.search(r'types = \{(TYPE_\w+), (TYPE_\w+)\}', m).groups()
    ty = [T(t[0])] + ([T(t[1])] if t[1] != t[0] else [])
    ab = [AB(a) for a in re.search(r'abilities = \{ABILITY_(\w+), ABILITY_(\w+)\}', m).groups() if a != 'NONE']
    ev = {lab: g('evYield_' + x) for lab, x in (('PV','HP'),('Atq','Attack'),('Déf','Defense'),('Vit','Speed'),('AtqSpé','SpAttack'),('DéfSpé','SpDefense')) if g('evYield_' + x)}
    gr = re.search(r'genderRatio = ([^,\n]+),', m).group(1).strip()
    pf = re.search(r'PERCENT_FEMALE\(([\d.]+)\)', gr)
    fem = None if gr == 'MON_GENDERLESS' else 100.0 if gr == 'MON_FEMALE' else 0.0 if gr == 'MON_MALE' else float(pf.group(1)) if pf else None
    eg = list(dict.fromkeys(re.findall(r'EGG_GROUP_(\w+)', re.search(r'eggGroups = \{([^}]*)\}', m).group(1))))
    de = dex_ent.get(k, {}); df = dex_fr.get(k, ('', ''))
    row = dict(n=len(dex) + 1, id=k, name=SP(k), types=ty, stats=st, bst=sum(st), abilities=ab, ev=ev, catch=g('catchRate'), xp=g('expYield'), cycles=g('eggCycles'), friend=g('friendship'),
               growth=dict(zip(('en','fr'), GROWTH[re.search(r'growthRate = GROWTH_(\w+)', m).group(1)])), egg=[dict(zip(('en','fr'), EGG[x])) for x in eg], female=fem,
               cat=dict(en=de.get('cat', '').title(), fr=df[0].title()), h=de.get('h', 0), w=de.get('w', 0), dex=dict(en=de.get('text', ''), fr=df[1]),
               moves=learnset(lv_ptr[k]) if k in lv_ptr else [], tm=[dict(kind=a, n=b, move=MV(c)) for a, b, c in sorted(tm_by_sp.get(k, []))], eggmoves=egg.get(k, []),
               evo=[dict(to=SP(e['to']), kind=e['kind'], p=e['p'], toid=e['to']) for e in evolves.get(k, [])], from_=[x for x in evolved_from.get(k, [])])
    dex.append(row)
dex_by_id = {d['id']: d for d in dex}
for d in dex: d['from'] = [dict(id=x, name=dex_by_id[x]['name'], n=dex_by_id[x]['n']) for x in d.pop('from_') if x in dex_by_id]
for d in dex:
    for e in d['evo']: e['n'] = dex_by_id[e['toid']]['n'] if e['toid'] in dex_by_id else 0

# ---------- attaques ----------
bm = rd('src/data/battle_moves.h')
move_desc_en = {}
_md = {c: jtxt(d_) for c, d_ in re.findall(r'gMoveDescription_(\w+)\[\] = _\(\s*((?:"[^"]*"\s*)+)\);', rd('src/move_descriptions.c'))}
for c, lab in re.findall(r'\[MOVE_(\w+)\s*- 1\] = gMoveDescription_(\w+),', rd('src/move_descriptions.c')): move_desc_en[c] = _md.get(lab, '')
md_fr = {}
try:
    for l in rd(FR + 'move_desc.txt').splitlines():
        p = l.split('|', 1)
        if len(p) == 2: md_fr[p[0].replace('MOVE_', '')] = clean(p[1])
except Exception: pass
mv_learners = {}
for d in dex:
    for lv, mv in d['moves']: mv_learners.setdefault(mv['en'], set()).add(d['n'])
    for tm in d['tm']: mv_learners.setdefault(tm['move']['en'], set()).add(d['n'])
tm_of = {}
for a, b, c in machine.values(): tm_of[c] = (a, b)
moves = []
for c, body in re.findall(r'\[MOVE_(\w+)\] =\s*\{(.*?)\n    \}', bm, re.S):
    if c == 'NONE' or c not in mv_names: continue
    g = lambda key: int(re.search(key + r' = (-?\d+)', body).group(1))
    ty = T(re.search(r'\.type = (TYPE_\w+)', body).group(1))
    p = g(r'\.power'); fl = re.search(r'\.flags = ([^\n]*)', body).group(1)
    if p == 0: cat = 'Status'
    elif 'FLAG_FORCE_PHYSICAL' in fl: cat = 'Physical'
    elif 'FLAG_FORCE_SPECIAL' in fl: cat = 'Special'
    else: cat = 'Special' if ty in ('Fire','Water','Grass','Electric','Psychic','Ice','Dragon','Dark','Fairy') else 'Physical'
    mvv = MV(c)
    moves.append(dict(name=mvv, type=ty, cat=cat, power=p, acc=g(r'\.accuracy'), pp=g(r'\.pp'), prio=g(r'\.priority'), eff=g(r'\.secondaryEffectChance') if 'secondaryEffectChance' in body else 0,
                      contact='FLAG_MAKES_CONTACT' in fl, tm=('%s%02d' % tm_of[c]) if c in tm_of else '', desc=dict(en=move_desc_en.get(c, ''), fr=md_fr.get(c, '')), n=len(mv_learners.get(mvv['en'], ()))))

# ---------- table des types ----------
te = rd('src/battle_main.c')
blk = re.search(r'gTypeEffectiveness\[\d+\] =\s*\{(.*?)\n\};', te, re.S).group(1)
mul = {'TYPE_MUL_NO_EFFECT': 0, 'TYPE_MUL_NOT_EFFECTIVE': 0.5, 'TYPE_MUL_SUPER_EFFECTIVE': 2}
chart = {}
for a, d_, m in re.findall(r'(TYPE_\w+), (TYPE_\w+), (TYPE_MUL_\w+)', blk):
    if a in ('TYPE_FORESIGHT', 'TYPE_ENDTABLE'): continue
    chart.setdefault(T(a), {})[T(d_)] = mul[m]
tlist = [en for c, en, fr in TYPES]

# ---------- champions ----------
tp = rd('src/data/trainer_parties.h')
leaders = [('Kay','Pyropia','Fire','Brock'),('Sylvestre','Tourmalia','Bug / Grass','Misty'),('Hera','Apatia','Dragon / Fairy','LtSurge'),('Grim','Bourg Quartz','Ice','Erika'),('Achlys','Amethiolite','Poison','Koga'),('Nox','Hematown','Dark','Sabrina'),('Eddie','Chrondrolia','Electric','Blaine'),('Hepha','Opanihrum','Steel','Giovanni')]
def party(arr):
    team = []
    for lvl, sp, it, mv in re.findall(r'\.lvl = (\d+),\s*\.species = SPECIES_(\w+),(?:\s*\.heldItem = ITEM_(\w+),)?(?:\s*\.moves = \{([^}]*)\})?', arr):
        team.append(dict(species=SP(sp), n=(dex_by_id[sp]['n'] if sp in dex_by_id else 0), lvl=int(lvl), item=IT(it) if it else None, moves=[MV(x.strip()[5:]) for x in mv.split(',') if x.strip() and x.strip() != 'MOVE_NONE']))
    return team
champs = []
for i, (nm, city, ty, slot) in enumerate(leaders, 1):
    arr = re.search(r'sParty_Leader%s\[\] = \{(.*?)\n\};' % slot, tp, re.S).group(1)
    champs.append(dict(n=i, name=nm, city=city, type=ty, team=party(arr)))

# ---------- noms de lieux ----------
sec_str = {c: n for c, n in re.findall(r'sMapsecName_(\w+)\[\] = _\("([^"]*)"\)', rd('src/data/region_map/region_map_entry_strings.h'))}
sec_fr = {}
for f in glob.glob(R + '/' + FR + 'strings/*.txt'):
    for l in open(f, encoding='utf-8'):
        if l.startswith('sMapsecName_') and '|' in l:
            a, b = l.rstrip('\n').split('|', 1); sec_fr[a.replace('sMapsecName_', '')] = b
sec_sym = {}
for m in re.finditer(r'\[MAPSEC_(\w+) - \w+\]\s*=\s*sMapsecName_(\w+),', rd('src/data/region_map/region_map_entries.h')): sec_sym[m.group(1)] = m.group(2)
map_sec = {}; folder_id = {}
for p in glob.glob(R + '/data/maps/*/map.json'):
    try: j = json.load(open(p, encoding='utf-8'))
    except Exception: continue
    map_sec[j['id']] = (j.get('region_map_section', ''), os.path.basename(os.path.dirname(p))); folder_id[os.path.basename(os.path.dirname(p))] = j['id']
def place(mp):
    sec, folder = map_sec.get(mp, ('', ''))
    sym = sec_sym.get(sec.replace('MAPSEC_', ''), '')
    en = sec_str.get(sym, '') or pretty(mp.replace('MAP_', ''))
    fr = sec_fr.get(sym, en)
    tail = re.search(r'_(B?\d+F|ENTRANCE|OUTSIDE|EXTERIOR|ROOF|ROOFTOP|BASEMENT|SOUTH|NORTH|EAST|WEST|WATERFALL|SUMMIT|PATH|RUBY_PATH|ICEFALL_CAVE_BACK|\w*CHAMBER)(?:_|$)', mp)
    f = re.search(r'_(B?\d+F)(?:_|$)', mp)
    if f and f.group(1) not in en: en += ' ' + f.group(1); fr += ' ' + f.group(1)
    return dict(en=nice(en).replace('Pokémon', 'Pokémon'), fr=nice(fr))

# ---------- rencontres sauvages ----------
wjson = json.load(open(os.path.join(R, 'src/data/wild_encounters.json')))['wild_encounter_groups'][0]
RATES = {f['type']: f.get('groups') or f.get('encounter_rates') for f in wjson['fields']}
RATES = {'land_mons': [20,20,10,10,10,10,5,5,4,4,1,1], 'water_mons': [60,30,5,4,1], 'rock_smash_mons': [60,30,5,4,1]}
ROD = {'Old Rod': ([0, 1], [70, 30]), 'Good Rod': ([2, 3, 4], [60, 20, 20]), 'Super Rod': ([5, 6, 7, 8, 9], [40, 40, 15, 4, 1])}
HOW = {'land_mons': ('Grass', 'Herbe'), 'water_mons': ('Surf', 'Surf'), 'rock_smash_mons': ('Rock Smash', 'Éclate-Roc')}
ROD_FR = {'Old Rod': 'Canne', 'Good Rod': 'Super Canne', 'Super Rod': 'Méga Canne'}
wild = []
seen_maps = {}
for e in wjson['encounters']:
    if '_LeafGreen' in e['base_label']: continue
    key = (e['map'], e['base_label'])
    pl = place(e['map'])
    def add(how_en, how_fr, mons_rates):
        acc = {}
        for sp, lo, hi, pct in mons_rates:
            if sp not in sp_names: continue
            a = acc.setdefault(sp, [lo, hi, 0]); a[0] = min(a[0], lo); a[1] = max(a[1], hi); a[2] += pct
        for sp, (lo, hi, pct) in acc.items():
            wild.append(dict(sp=SP(sp), n=dex_by_id[sp]['n'] if sp in dex_by_id else 0, map=e['map'].replace('MAP_', ''), loc=pl, how=dict(en=how_en, fr=how_fr), min=lo, max=hi, pct=pct))
    for k, (hen, hfr) in HOW.items():
        if k in e:
            ms = e[k]['mons']; rt = RATES[k]
            add(hen, hfr, [(m['species'].replace('SPECIES_', ''), m['min_level'], m['max_level'], rt[i]) for i, m in enumerate(ms)])
    if 'fishing_mons' in e:
        ms = e['fishing_mons']['mons']
        for rod, (idx, rt) in ROD.items():
            add(rod, ROD_FR[rod], [(ms[i]['species'].replace('SPECIES_', ''), ms[i]['min_level'], ms[i]['max_level'], rt[j]) for j, i in enumerate(idx) if i < len(ms)])
wild_raw = [dict(w) for w in wild]
# fusion : une ligne par (espèce, lieu affiché, méthode) ; cartes distinctes de même nom -> meilleur taux, niveaux étendus
_m = {}
for w in wild:
    k = (w['n'], w['sp']['en'], w['loc']['en'], w['how']['en'])
    if k not in _m: _m[k] = dict(w, _maps={w['map']: w['pct']})
    else:
        a = _m[k]; a['min'] = min(a['min'], w['min']); a['max'] = max(a['max'], w['max'])
        if w['map'] in a['_maps']: a['_maps'][w['map']] = max(a['_maps'][w['map']], w['pct'])
        else: a['_maps'][w['map']] = w['pct']
        a['pct'] = max(a['_maps'].values())
wild = []
for a in _m.values(): a.pop('_maps'); wild.append(a)
by_sp = {}
for w in wild: by_sp.setdefault(w['n'], []).append(w)
for d in dex:
    d['where'] = [dict(loc=w['loc'], how=w['how'], min=w['min'], max=w['max'], pct=w['pct']) for w in sorted(by_sp.get(d['n'], []), key=lambda x: (-x['pct'], x['loc']['en']))][:40]

# ---------- cadeaux / statiques (scripts de cartes) ----------
gifts = []
for p in sorted(glob.glob(R + '/data/maps/*/scripts.inc')):
    folder = os.path.basename(os.path.dirname(p)); txt = open(p, encoding='utf-8').read()
    for kind, rx in (('Gift', r'^\s*givemon SPECIES_(\w+),\s*(\d+)'), ('Static', r'^\s*setwildbattle SPECIES_(\w+),\s*(\d+)')):
        for m in re.finditer(rx, txt, re.M):
            sp = m.group(1)
            if sp in sp_names:
                gifts.append(dict(kind=kind, sp=SP(sp), n=dex_by_id[sp]['n'] if sp in dex_by_id else 0, lvl=int(m.group(2)), loc=place(folder_id.get(folder, 'MAP_' + folder.upper()))))
for g in gifts:
    if g['n']:
        dex_by_id_n = next((d for d in dex if d['n'] == g['n']), None)
        if dex_by_id_n is not None: dex_by_id_n.setdefault('special', []).append(dict(kind=g['kind'], lvl=g['lvl'], loc=g['loc']))

# ---------- couverture Kanto (151) ----------
kanto = [d for d in dex if d['n'] <= 151]
wild_n = {w['n'] for w in wild}
evo_reach = set(wild_n) | {g['n'] for g in gifts}
ch = True
while ch:
    ch = False
    for d in dex:
        if d['n'] in evo_reach:
            for e in d['evo']:
                if e['n'] and e['n'] not in evo_reach: evo_reach.add(e['n']); ch = True
special_n = {g['n'] for g in gifts}
coverage = dict(total=151, wild=len([d for d in kanto if d['n'] in wild_n]), evo=len([d for d in kanto if d['n'] in evo_reach]), special=sorted(d['n'] for d in kanto if d['n'] not in evo_reach and d['n'] in special_n),
                missing=sorted(d['n'] for d in kanto if d['n'] not in evo_reach and d['n'] not in special_n))

os.makedirs(os.path.join(R, 'docs/data'), exist_ok=True)
def out(name, var, obj):
    open(os.path.join(R, 'docs/data/%s.js' % name), 'w', encoding='utf-8').write('window.%s = %s;\n' % (var, json.dumps(obj, ensure_ascii=False, separators=(',', ':'))))
out('pokedex', 'POKEDEX', dex); out('moves', 'MOVES', moves)
out('types', 'TYPES', dict(list=tlist, fr=tfr, chart=chart))
out('champions', 'CHAMPIONS', champs)
out('wild', 'WILD', [dict(w) for w in wild]); out('meta', 'META', dict(coverage=coverage, gifts=gifts, built=__import__('datetime').date.today().isoformat()))

# ---------- quai d'Amethiolite (passeurs) ----------
fs = rd('data/maps/FuchsiaCity/scripts.inc')
dock = []; ferry = None; gate = 0; ask = None
for ln in fs.split('\n'):
    m = re.match(r'FuchsiaCity_EventScript_(\w+?)::', ln)
    if m and m.group(1) in ('EchoFerryman', 'TideFerrywoman', 'LanternBoatman', 'Apprentice', 'DuskFerrywoman', 'ScribeFerryman', 'SeasonsFerryman'): ferry = m.group(1); gate = 0
    m = re.search(r'goto_if_unset FLAG_BADGE0(\d)_GET', ln)
    if m: gate = int(m.group(1))
    m = re.search(r'msgbox (\w+_Ask\d*), MSGBOX_(?:YESNO|DEFAULT)', ln)
    if m: ask = m.group(1)
    m = re.search(r'^\twarp (MAP_\w+), -?\d+, -?\d+, -?\d+', ln)
    if m and ferry and ask:
        mp = m.group(1); sp_ = {}
        for w in wild:
            if 'MAP_' + w['map'] == mp:
                sp_.setdefault(w['sp']['en'], dict(sp=w['sp'], n=w['n'], how=set()))['how'].add(w['how']['en'])
        dock.append(dict(ferry=ferry.replace('Ferryman', '').replace('Ferrywoman', '').replace('Boatman', ''), name=place(mp), badges=gate, species=[dict(sp=v['sp'], n=v['n'], how=sorted(v['how'])) for v in sp_.values()]))
        ask = None; gate = 0
out('dock', 'DOCK', dock)

# ---------- objets : où les trouver (sol, cachés, cadeaux, boutiques, lots) ----------
fr_idesc = {}
for l in open(R + '/tools/topaze/i18n/fr/item_desc.txt', encoding='utf-8'):
    if '|' in l: k, v = l.rstrip('\n').split('|', 1); fr_idesc[k] = v.replace('\\n', ' ')
mach_by_num = {a + '%02d' % b: (a, b, c) for a, b, c in machine.values()}
def item_id(tok): return tok.replace('ITEM_', '')
item_src = {}
def src(tok, kind, mp, extra=''):
    k = item_id(tok)
    if k == 'NONE' or k not in it_names: return
    item_src.setdefault(k, []).append(dict(kind=kind, loc=place(mp), **({'x': extra} if extra else {})))
ball = {}
for m in re.finditer(r'^(\w+)::\n\s*finditem (ITEM_\w+)', rd('data/scripts/item_ball_scripts.inc'), re.M): ball[m.group(1)] = m.group(2)
for p_ in glob.glob(R + '/data/maps/*/map.json'):
    try: j = json.load(open(p_, encoding='utf-8'))
    except Exception: continue
    for o in j.get('object_events', []):
        if o.get('script') in ball: src(ball[o['script']], 'ground', j['id'])
    for b in j.get('bg_events', []):
        if b.get('type') == 'hidden_item': src(b['item'], 'hidden', j['id'])
for p_ in sorted(glob.glob(R + '/data/maps/*/scripts.inc')):
    folder = os.path.basename(os.path.dirname(p_)); mp = folder_id.get(folder, 'MAP_' + folder.upper()); txt = open(p_, encoding='utf-8').read()
    for m in re.finditer(r'^\s*(giveitem_msg|giveitem)\s+(?:\w+,\s*)?(ITEM_\w+)', txt, re.M): src(m.group(2), 'gift', mp)
    for m in re.finditer(r'(\w+)::\n((?:\s*\.2byte ITEM_\w+\n)+)', txt):
        for tok in re.findall(r'ITEM_\w+', m.group(2)): src(tok, 'shop', mp)
    for m in re.finditer(r'^\s*setvar VAR_(?:0x8009|TEMP_1), (ITEM_\w+)', txt, re.M): src(m.group(1), 'prize', mp)
items_out = []
for i in _ij:
    k = i['itemId'].replace('ITEM_', '')
    if k in ('NONE',) or k.startswith('UNK') or k.startswith('?'): continue
    seen = set(); ss = []
    for x in item_src.get(k, []):
        key = (x['kind'], x['loc']['en'])
        if key in seen: continue
        seen.add(key); ss.append(x)
    tm = re.fullmatch(r'(TM|HM)(\d\d)', k)
    nm = IT(k)
    if tm and tm.group(1) + tm.group(2) in mach_by_num:
        mv_ = MV(mach_by_num[tm.group(1) + tm.group(2)][2]); _tmmv = mach_by_num[tm.group(1) + tm.group(2)][2]; nm = dict(en='%s%s %s' % (tm.group(1), tm.group(2), mv_['en']), fr='%s%s %s' % ('CT' if tm.group(1) == 'TM' else 'CS', tm.group(2), mv_['fr']))
    items_out.append(dict(id=k, name=nm, desc=(dict(en=move_desc_en.get(_tmmv, ''), fr=md_fr.get(_tmmv, '')) if tm and tm.group(1) + tm.group(2) in mach_by_num else dict(en=i.get('description_english', '').replace('\\n', ' ').replace('\n', ' '), fr=fr_idesc.get(i['itemId'], ''))), pocket=i.get('pocket', '').replace('POCKET_', ''), price=i.get('price', 0), tm=(tm.group(1) + tm.group(2)) if tm else '', src=ss))
out('items', 'ITEMS', items_out)
_tmsrc = {x['tm']: x['src'] for x in items_out if x['tm']}
for mv in moves:
    mv['tmsrc'] = _tmsrc.get(mv['tm'], []) if mv['tm'] else []
out('moves', 'MOVES', moves)
print(len(items_out), 'objets,', sum(1 for x in items_out if x['src']), 'avec source,', sum(1 for x in items_out if x['tm'] and x['src']), '/', sum(1 for x in items_out if x['tm']), 'CT/CS localisées')

# ---------- dresseurs : lieu, classe, équipe ----------
tr_src = rd('src/data/trainers.h'); tp_all = rd('src/data/trainer_parties.h')
cls_fr = dict(re.findall(r'\[TRAINER_CLASS_(\w+)\]\s*=\s*_\("([^"]*)"\)', rd('src/data/text/trainer_class_names.h')))
tr_blocks = {}
for m in re.finditer(r'\[TRAINER_(\w+)\] = \{(.*?)\n    \},', tr_src, re.S):
    b = m.group(2)
    c = re.search(r'\.trainerClass = TRAINER_CLASS_(\w+)', b); n = re.search(r'\.trainerName = _\("([^"]*)"\)', b); pt = re.search(r'\.party = \w+\((\w+)\)', b)
    if c and n and pt: tr_blocks[m.group(1)] = (c.group(1), n.group(1), pt.group(1), 'doubleBattle = TRUE' in b)
tr_out = []
seen_tr = set()
for p_ in sorted(glob.glob(R + '/data/maps/*/scripts.inc')):
    folder = os.path.basename(os.path.dirname(p_)); mp = folder_id.get(folder, 'MAP_' + folder.upper()); txt = open(p_, encoding='utf-8').read()
    for tid in re.findall(r'trainerbattle\w*\s+TRAINER_(\w+)', txt):
        if tid in seen_tr or tid not in tr_blocks: continue
        seen_tr.add(tid); cl, nm, pty, dbl = tr_blocks[tid]
        m = re.search(r'%s\[\] = \{(.*?)\n\};' % pty, tp_all, re.S)
        if not m: continue
        team = party(m.group(1))
        if not team: continue
        tr_out.append(dict(id=tid, cls=dict(en=nice(cl.replace('_', ' ').title()).replace('{Pkmn}', 'Pokémon'), fr=nice(cls_fr.get(cl, cl)).replace('{Pkmn} Dresseur', 'Dresseur Pokémon').replace('{Pkmn}', 'Pokémon').replace('{pkmn}', 'Pokémon')), name=nm.title() if nm.isupper() else nm, loc=place(mp), map=folder, dbl=dbl, team=[dict(sp=t_['species'], n=t_['n'], lvl=t_['lvl'], item=t_['item'], moves=t_['moves']) for t_ in team]))
out('trainers', 'TRAINERS', tr_out)
print(len(tr_out), 'dresseurs')
exec(compile(open(os.path.join(R, 'tools/topaze/encyclo.py'), encoding='utf-8').read(), 'encyclo.py', 'exec'))
print(len(dex), 'pokémon,', len(moves), 'attaques,', len(champs), 'champions,', len(wild), 'lignes sauvages,', len(dock), 'destinations quai,', len(gifts), 'cadeaux/statiques')
print('couverture 1G :', coverage)
