# Encyclopédie : cartes, PNJ, dialogues, boutiques, talents, légendaires, index de recherche.
# Exécuté par build_site.py (partage son espace de noms : place, folder_id, wild_raw, tr_blocks, party, SP, MV, IT, AB, ...).
import sys, shutil, collections
sys.path.insert(0, os.path.join(R, 'tools/topaze/maps'))
D = os.path.join(R, 'docs')

# ---------- textes (EN + FR) ----------
def parse_strings(path):
    res = {}; lab = None; buf = []
    for l in open(path, encoding='utf-8', errors='replace'):
        m = re.match(r'^(\w+)::?\s*$', l)
        if m:
            if lab and buf: res[lab] = ''.join(buf)
            lab = m.group(1); buf = []; continue
        m = re.match(r'^\s*\.string "(.*)"\s*$', l)
        if m and lab is not None: buf.append(m.group(1))
        elif l.strip() and not l.strip().startswith(('//', '@')) and lab is not None and buf:
            res[lab] = ''.join(buf); lab = None; buf = []
    if lab and buf: res[lab] = ''.join(buf)
    return res
TXT_EN = {}
for f in glob.glob(R + '/data/maps/*/text.inc') + glob.glob(R + '/data/text/*.inc') + glob.glob(R + '/data/scripts/*.inc') + [R + '/data/event_scripts.s'] + glob.glob(R + '/data/maps/*/scripts.inc'):
    try: TXT_EN.update(parse_strings(f))
    except Exception: pass
TXT_FR = {}
for f in glob.glob(R + '/i18n/fr/*.json'):
    try:
        j = json.load(open(f, encoding='utf-8'))
        for k, v in (j.items() if isinstance(j, dict) else j):
            if isinstance(v, dict) and 'fr' in v: TXT_FR[k] = v['fr']; TXT_EN.setdefault(k, v.get('en', ''))
    except Exception: pass
for f in glob.glob(R + '/' + FR + 'inc*.txt'):
    for l in open(f, encoding='utf-8'):
        if '|' in l and not l.startswith('#'):
            a, b = l.rstrip('\n').split('|', 1); TXT_FR.setdefault(a, b)
def tclean(s, lang):
    s = s.replace('\\p', '\n\n').replace('\\n', ' ').replace('\\l', ' ').replace('$', '').replace('\\"', '"')
    s = s.replace('{PLAYER}', '[Joueur]' if lang == 'fr' else '[Player]').replace('{RIVAL}', '[Rival]').replace('{PKMN}', 'POKéMON')
    s = re.sub(r'\{(?:STR_VAR_\d|PLAYER|RIVAL|PKMN)\}', '…', s); s = re.sub(r'\{[^}]*\}', '', s)
    s = re.sub(r'[ ]+', ' ', s).replace(' \n', '\n').replace('\n ', '\n')
    return s.strip()
def T(lab):
    en = TXT_EN.get(lab, ''); fr = TXT_FR.get(lab, en)
    if not en and not fr: return None
    return dict(en=tclean(en or fr, 'en'), fr=tclean(fr or en, 'fr'))

# ---------- scripts ----------
SCR = {}      # label -> corps (lignes)
LOCAL = {}    # dossier -> set(labels)
def parse_scripts(path, folder=None):
    lab = None; body = []
    for l in open(path, encoding='utf-8', errors='replace'):
        m = re.match(r'^(\w+)::?\s*$', l)
        if m:
            if lab: SCR[lab] = '\n'.join(body)
            lab = m.group(1); body = []
            if folder: LOCAL.setdefault(folder, set()).add(lab)
        elif lab: body.append(l)
    if lab: SCR[lab] = '\n'.join(body)
for f in glob.glob(R + '/data/scripts/*.inc') + [R + '/data/event_scripts.s']: parse_scripts(f)
for f in glob.glob(R + '/data/maps/*/scripts.inc'): parse_scripts(f, os.path.basename(os.path.dirname(f)))
TOK = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')
STOP = {'EventScript_Return', 'EventScript_SetResultTrue', 'EventScript_SetResultFalse'}
def script_texts(lab, depth=4, seen=None, out_=None):
    seen = seen if seen is not None else set(); out_ = out_ if out_ is not None else []
    if lab in seen or lab in STOP or lab not in SCR or len(out_) > 16: return out_
    seen.add(lab)
    for tok in TOK.findall(SCR[lab]):
        if tok in TXT_EN and tok not in out_ and not tok.startswith('g') or (tok in TXT_EN and tok.startswith('g') and '_Text' in tok):
            if tok not in out_: out_.append(tok)
        elif tok in SCR and depth > 0 and tok != lab: script_texts(tok, depth - 1, seen, out_)
    return out_

# ---------- sprites ----------
gfx_ptr = dict(re.findall(r'\[(OBJ_EVENT_GFX_\w+)\]\s*=\s*&(gObjectEventGraphicsInfo_\w+)', rd('src/data/object_events/object_event_graphics_info_pointers.h')))
info_txt = rd('src/data/object_events/object_event_graphics_info.h')
pic_file = dict(re.findall(r'const u16 (gObjectEventPic_\w+)\[\] = INCBIN_U16\("([^"]+)\.4bpp"\)', rd('src/data/object_events/object_event_graphics.h')))
def sprite(g):
    out_p = os.path.join(D, 'img/npc/%s.png' % g.replace('OBJ_EVENT_GFX_', '').lower())
    if os.path.exists(out_p): return True
    info = gfx_ptr.get(g)
    if not info: return False
    m = re.search(r'%s = \{(.*?)\n\};' % info, info_txt, re.S)
    if not m: return False
    body = m.group(1); w = int(re.search(r'\.width = (\d+)', body).group(1)); h = int(re.search(r'\.height = (\d+)', body).group(1))
    pm = re.search(r'\.images = (\w+)', body); pic = None
    if pm:
        fm = re.search(r'%s\[\] = \{\s*overworld_frame\((\w+)' % pm.group(1), rd('src/data/object_events/object_event_pic_tables.h'))
        pic = pic_file.get(fm.group(1)) if fm else None
    if not pic or not os.path.exists(os.path.join(R, pic + '.png')): return False
    from PIL import Image
    im = Image.open(os.path.join(R, pic + '.png')); tr = im.info.get('transparency', 0)
    im = im.convert('RGBA'); im = im.crop((0, 0, w, h)); px = im.load(); bg = px[0, 0]
    for y in range(h):
        for x in range(w):
            if px[x, y] == bg: px[x, y] = (0, 0, 0, 0)
    im.save(out_p, optimize=True); return True
GFX_FR = dict(AGATHA='Agatha', ARTICUNO='Artikodin', BALDING_MAN='Homme chauve', BEAUTY='Canon', BIKER='Motard', BILL='Bill', BLACK_BELT='Karatéka', BLAINE='Auguste', BLUE='Blue', BOY='Garçon', BROCK='Pierre', BRUNO='Aldo', BUG_CATCHER='Aspirant', CAMPER='Campeur', CAPTAIN='Capitaine', CELEBI='Celebi', CELIO='Celio', CHANNELER='Médium', CHANSEY='Leveinard', CHEF='Cuisinier', CLEFAIRY='Mélofée', CLERK='Vendeur', CLIPBOARD='Pancarte', COOLTRAINER_F='Topdresseuse', COOLTRAINER_M='Topdresseur', CRUSH_GIRL='Fille Costaud', CUBONE='Osselait', CUT_TREE='Arbre', DAISY='Marguerite', DEOXYS_N='Deoxys', DODUO='Doduo', ENTEI='Entei', ERIKA='Érika', FAT_MAN='Homme corpulent', FEAROW='Rapasdepic', FISHER='Pêcheur', FOSSIL='Fossile', GBA_KID='Enfant', GENTLEMAN='Gentleman', GIOVANNI='Giovanni', GROUDON='Groudon', GYM_GUY='Guide d’arène', HIKER='Montagnard', HO_OH='Ho-Oh', ITEM_BALL='Objet', JIGGLYPUFF='Rondoudou', JIRACHI='Jirachi', KABUTO='Kabuto', KANGASKHAN='Kangourex', KOGA='Koga', KYOGRE='Kyogre', LANCE='Peter', LAPRAS_DOLL='Peluche Lokhlass', LASS='Fillette', LATIAS='Latias', LATIOS='Latios', LITTLE_BOY='Petit garçon', LITTLE_GIRL='Petite fille', LORELEI='Olga', LT_SURGE='Major Bob', LUGIA='Lugia', MACHOKE='Machopeur', MACHOP='Machoc', MAN='Homme', MEOWTH='Miaouss', METEORITE='Météorite', MEW='Mew', MEWTWO='Mewtwo', MG_DELIVERYMAN='Livreur', MISTY='Ondine', MOLTRES='Sulfura', MOM='Maman', MR_FUJI='M. Fuji', NIDORAN_F='Nidoran♀', NIDORAN_M='Nidoran♂', NIDORINO='Nidorino', NURSE='Infirmière', OLD_AMBER='Ambre', OLD_MAN_1='Vieil homme', OLD_MAN_2='Vieil homme', OLD_WOMAN='Vieille dame', PICNICKER='Pique-niqueuse', PIDGEOT='Roucarnage', PIDGEY='Roucool', PIKACHU='Pikachu', POKEDEX='Pokédex', POKE_MANIAC='Fan de Pokémon', POLICEMAN='Policier', POLIWRATH='Tartard', PROF_OAK='Prof. Chen', PSYDUCK='Psykokwak', PUSHABLE_BOULDER='Rocher', RAIKOU='Raikou', RAYQUAZA='Rayquaza', RED_NORMAL='Red', REGICE='Regice', REGIROCK='Regirock', REGISTEEL='Registeel', ROCKER='Rockeur', ROCKET_F='Sbire (F)', ROCKET_M='Sbire (H)', ROCK_SMASH_ROCK='Rocher fissuré', RS_BRENDAN='Brendan', RUBY='Rubis', SABRINA='Morgane', SAILOR='Marin', SAPPHIRE='Saphir', SCIENTIST='Scientifique', SEAGALLOP='Bateau', SEEL='Otaria', SLOWBRO='Flagadosse', SLOWPOKE='Ramoloss', SNORLAX='Ronflex', SPEAROW='Piafabec', SS_ANNE='S.S. Anne', SUICUNE='Suicune', SWIMMER_F_LAND='Nageuse', SWIMMER_F_WATER='Nageuse', SWIMMER_M_LAND='Nageur', SWIMMER_M_WATER='Nageur', TOWN_MAP='Carte', TRAINER_TOWER_DUDE='Gars de la Tour', TUBER_F='Fillette à bouée', TUBER_M_WATER='Garçon à bouée', UNION_ROOM_RECEPTIONIST='Réceptionniste', VOLTORB='Voltorbe', WIGGLYTUFF='Grodoudou', WOMAN_1='Femme', WOMAN_2='Femme', WOMAN_3='Femme', WORKER_F='Ouvrière', WORKER_M='Ouvrier', YOUNGSTER='Gamin', ZAPDOS='Électhor', CABLE_CLUB_RECEPTIONIST='Réceptionniste')
def gfx_label(g):
    k = g.replace('OBJ_EVENT_GFX_', '')
    if k.startswith('VAR_') or k == '0': return dict(en='Person', fr='Personne')
    return dict(en=nice(k.replace('_', ' ')), fr=GFX_FR.get(k, nice(k.replace('_', ' '))))

# ---------- noms de cartes ----------
WORDS_FR = dict(House='Maison', Houses='Maisons', Gym='Arène', Center='Centre', Mart='Boutique', Lab='Labo', Cave='Grotte', Tower='Tour', Room='Salle', Entrance='Entrée', Exit='Sortie', Basement='Sous-sol', Hideout='Planque', Lair='Repaire', Mansion='Manoir', Museum='Musée', Station='Gare', Gate='Poste', Path='Chemin', Tunnel='Tunnel', Forest='Forêt', Mountain='Mont', Mt='Mont', Floor='Étage', Roof='Toit', Rooftop='Toit', Hall='Hall', Office='Bureau', Shop='Magasin', Store='Magasin', Department='Grand Magasin', Library='Bibliothèque', Harbor='Port', Port='Port', Zoo='Zoo', Safari='Safari', Game='Jeux', Corner='Salle', Power='Centrale', Plant='Centrale', Elevator='Ascenseur', Lobby='Hall', Back='Arrière', Front='Avant', Outside='Extérieur', Inside='Intérieur', Chamber='Chambre', Team='Team', North='Nord', South='Sud', East='Est', West='Ouest', Northeast='Nord-Est', Island='Île', Ship='Navire', Deck='Pont', Cabin='Cabine', Dock='Quai', Dojo='Dojo', Pokemon='Pokémon', Move='Attaque', Deleter='Oubli', Relearner='Tuteur', Nursery='Garderie', Daycare='Pension', Restaurant='Restaurant', School='École', Ruins='Ruines', Altar='Autel', Refuge='Refuge', Council='Conseil', Echo='Écho', Echoes='Échos', Time='Temps', Prize='Lots', Trade='Échange', Fan='Fan', Club='Club', Rival='Rival', Cottage='Chaumière', Ranch='Ranch', Mine='Mine', Lighthouse='Phare', Volcano='Volcan', Garden='Jardin', Park='Parc', Bridge='Pont', Hot='Chaud', Spring='Source', Springs='Sources', Door='Porte', Sign='Panneau', Unused='Inutilisé', Upstairs='Étage', Downstairs='Rez-de-chaussée', Stall='Stand', Battle='Combat', Boutique='Boutique', Apothecary='Apothicaire', Library_='Bibliothèque', Base='Base', Beach='Plage', Berry='Baies', Bike='Vélo', Bond='Lien', Building='Bâtiment', Bush='Buisson', Canyon='Canyon', Cape='Cap', Care='Soins', Colosseum='Colisée', Condominiums='Résidence', Connection='Liaison', Corridor='Couloir', Day='Jour', Den='Antre', Depths='Profondeurs', Dotted='Pointillé', Experiment='Expérience', Exterior='Extérieur', Fame='Gloire', Fishing='Pêche', Fork='Bifurcation', Glade='Clairière', Glass='Verre', Gorgeous='Splendide', Green='Vert', Grove='Bosquet', Hole='Trou', Home='Maison', Hotel='Hôtel', Icefall='Chute de Glace', Isle='Île', Joyful='Joyeux', Key='Clé', Kindle='Brasier', Kitchen='Cuisine', Labyrinth='Labyrinthe', Lane='Allée', Lost='Perdu', Lounge='Salon', Meadow='Prairie', Memorial='Mémorial', Mr='M.', Of='de', Outcast='Banni', Pattern='Motif', Pillar='Pilier', Prototype='Prototype', Research='Recherche', Resort='Station', Rest='Repos', Rocket='Onybris', Ruby='Rubis', Ruin='Ruine', Sapphire='Saphir', Sea='Mer', Secret='Secret', Spa='Spa', Stairs='Escaliers', Steel='Acier', Stone='Pierre', Storm='Tempête', Summit='Sommet', Treasure='Trésor', Valley='Vallée', Victory='Victoire', Volunteer='Volontaires', Wardens='Gardiens', Warehouse='Entrepôt', Water='Eau', Trainer='Dresseur', Tide='Marée', Indigo='Indigo', Plateau='Plateau')
POSS_FR = dict(Agathas='Agatha', Brunos='Aldo', Loreleis='Olga', Lances='Peter', Champions='du Maître', Captains='du Capitaine', Copycats='de l’Imitatrice', Psychics='du Médium', Players='du joueur', Rivals='du rival', Oaks='du Prof. Chen')
TYPE_FR = dict(Room='Salle', House='Maison', Lab='Labo', Home='Maison')
def camel(seg): return re.sub(r'(?<=[a-z])(?=[A-Z0-9])', ' ', seg)
SPECIAL_FR = {'Players House': 'Maison du joueur', 'Rivals House': 'Maison du rival', 'Professor Oaks Lab': 'Labo du Prof. Chen', 'Pokemon Center': 'Centre Pokémon', 'Pokemon Mart': 'Boutique Pokémon', 'Mart': 'Boutique', 'Generic House': 'Maison', 'Pokemon League': 'Ligue Pokémon', 'Game Corner': 'Salle de jeux', 'Victory Road': 'Route Victoire', 'Safari Zone': 'Parc Safari', 'Rocket Hideout': 'Planque Onybris', 'Mt Moon': 'Mont Sélénite', 'Department Store': 'Grand Magasin', 'Lances Room': 'Salle de Peter', 'Lorelei': 'Olga'}
import unicodedata
def norm(x): return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', x.lower()).encode('ascii', 'ignore').decode())
def words(seg): return [w for w in camel(seg).replace('Mt', 'Mt').split() if w]
def tr_words(ws, lang):
    t = ' '.join(ws)
    if lang == 'fr':
        for k, v in SPECIAL_FR.items(): t = re.sub(r'\b%s\b' % k, v, t)
        t = re.sub(r'\b(%s) (Room|House|Lab|Home)\b' % '|'.join(POSS_FR), lambda m: '%s %s' % (TYPE_FR[m.group(2)], POSS_FR[m.group(1)] if POSS_FR[m.group(1)].startswith('du') or POSS_FR[m.group(1)].startswith('de') else 'de ' + POSS_FR[m.group(1)]), t)
        t = ' '.join(WORDS_FR.get(w, w) for w in t.split(' '))
    return t
def phrase(folder, lang, area_en=''):
    segs = folder.split('_')
    if len(segs) < 2: return '', True
    s0 = words(segs[0]); an = norm(area_en); n0 = norm(segs[0])
    parent = (segs[0] in MJ) or (an and (n0.startswith(an) or an.startswith(n0)))
    rest = [w for w in s0 if norm(w) not in an] if (an and (n0.startswith(an) or an.startswith(n0))) else ([] if parent else s0)
    for s_ in segs[1:]: rest += words(s_)
    rest = [re.sub(r'^(\d+)\s*F$', r'\1F', w) for w in rest]
    return tr_words(rest, lang), bool(parent)
MAPTYPE = dict(MAP_TYPE_TOWN='town', MAP_TYPE_CITY='city', MAP_TYPE_ROUTE='route', MAP_TYPE_UNDERGROUND='cave', MAP_TYPE_INDOOR='indoor', MAP_TYPE_OCEAN_ROUTE='route', MAP_TYPE_SECRET_BASE='indoor')
id2folder = {v: k for k, v in folder_id.items()}
def mname(folder):
    mid = folder_id.get(folder, ''); pl = place(mid)
    base_en = re.sub(r' (B?\d+F)$', '', pl['en']); base_fr = re.sub(r' (B?\d+F)$', '', pl['fr'])
    segs = folder.split('_')
    if len(segs) < 2: return dict(en=pl['en'], fr=pl['fr'])
    ph_en, with_area = phrase(folder, 'en', base_en); ph_fr, _ = phrase(folder, 'fr', base_en)
    if not ph_en: return dict(en=pl['en'], fr=pl['fr'])
    for k_ in ('Players', 'Rivals', 'Oaks', 'Lances'): ph_en = re.sub(r'\b%s\b' % k_, k_[:-1] + "'s", ph_en)
    if with_area: return dict(en='%s – %s' % (base_en, ph_en), fr=fixfr('%s – %s' % (base_fr, ph_fr)))
    return dict(en=ph_en, fr=fixfr(ph_fr))
def fixfr(n):
    n = re.sub(r'\bde ([AEIOUYÉ])', r"d'\1", n)
    n = re.sub(r'\b(Salle|Maison|Labo) d\'(Agatha|Aldo|Olga)', lambda m: m.group(1) + ' d\'' + m.group(2), n)
    n = n.replace('Cave Taupiqueur', 'Tunnel Taupiqueur').replace('Altering Grotte', 'Grotte Métamo').replace('Grotte Métamo – Grotte Métamo', 'Grotte Métamo')
    n = re.sub(r'\bSecret Maison\b', 'Maison secrète', n)
    n = re.sub(r'(\w+) (Maison|Entrée|Sortie)$', lambda m: m.group(2) + ' ' + m.group(1) if m.group(1) not in ('Maison','Entrée') and m.group(1)[0].isupper() and False else m.group(0), n)
    n = re.sub(r' – (Nord|Sud|Est|Ouest|Nord-Est|Sud-Est) Entrée', r' – Entrée \1', n)
    n = n.replace('Est Ouest Tunnel', 'Tunnel Est-Ouest').replace('Nord Sud Tunnel', 'Tunnel Nord-Sud')
    n = n.replace('Victory Road Lair', 'Antre Route Victoire').replace('Grenalux – Mine', 'Grenalux – Mine').replace('Cap Brink', 'Cap Falaise').replace('Cap Falaise – Cap Falaise', 'Cap Falaise')
    return n
MJ = {}
for p_ in glob.glob(R + '/data/maps/*/map.json'):
    try: MJ[os.path.basename(os.path.dirname(p_))] = json.load(open(p_, encoding='utf-8'))
    except Exception: pass
LAY = {l['id']: l for l in json.load(open(R + '/data/layouts/layouts.json'))['layouts'] if 'id' in l}
tr_by_id = {t['id']: t for t in tr_out}
wild_by_map = collections.defaultdict(list)
for w in wild_raw: wild_by_map['MAP_' + w['map']].append(w)
ITEM_PRICE = {i['itemId'].replace('ITEM_', ''): i.get('price', 0) for i in _ij}
FLAGMSG = re.compile(r'msgbox\s+(\w+)')
def item_pair(tok):
    k = tok.replace('ITEM_', ''); return dict(IT(k), id=k)

# ---------- rendu des cartes ----------
import mapkit
rendered = {}
def render(lay):
    outp = os.path.join(D, 'maps/%s.png' % lay.replace('LAYOUT_', '').lower())
    if lay in rendered: return rendered[lay]
    ok = os.path.exists(outp)
    if not ok:
        os.system('python3 %s/tools/topaze/maps/mapkit.py render %s %s >/dev/null 2>&1' % (R, lay, outp))
        ok = os.path.exists(outp)
        if ok:
            from PIL import Image
            Image.open(outp).convert('RGB').quantize(64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(outp, optimize=True)
    rendered[lay] = lay.replace('LAYOUT_', '').lower() if ok else None
    return rendered[lay]

# ---------- cartes ----------
RECS = {}; maps_index = []; dialogues = []; shops_all = []; given_all = []
for folder, j in sorted(MJ.items()):
    mid = j['id']; nm = mname(folder); lay = j.get('layout', ''); img = render(lay) if lay in LAY else None
    L_ = LAY.get(lay, {}); sec = j.get('region_map_section', '')
    pl = place(mid); area = re.sub(r' (B?\d+F)$', '', pl['en'])
    rec = dict(id=folder, name=nm, area=dict(en=area, fr=re.sub(r' (B?\d+F)$', '', pl['fr'])), kind=MAPTYPE.get(j.get('map_type'), 'indoor'), img=img, w=L_.get('width', 0), h=L_.get('height', 0),
               music=(j.get('music') or '').replace('MUS_', '').replace('_', ' ').title(), weather=(j.get('weather') or '').replace('WEATHER_', '').replace('_', ' ').title(), flash=bool(j.get('requires_flash')),
               conn=[], warps=[], npcs=[], signs=[], hidden=[], triggers=[], shops=[], given=[], wild=[], other=[])
    for c in j.get('connections') or []:
        f2 = id2folder.get(c['map']); rec['conn'].append(dict(dir=c['direction'], to=f2, name=mname(f2) if f2 else dict(en=c['map'], fr=c['map'])))
    seen_w = set()
    for w in j.get('warp_events', []):
        f2 = id2folder.get(w['dest_map'])
        if not f2: continue
        rec['warps'].append(dict(x=w['x'], y=w['y'], to=f2, name=mname(f2)))
    used = set()
    def attach(labs, who):
        res = []
        for lb in labs:
            t_ = T(lb)
            if t_ and t_['en'] and lb not in used:
                used.add(lb); res.append(t_); dialogues.append([folder, who['en'], who['fr'], t_['en'], t_['fr']])
        return res
    for o in j.get('object_events', []):
        if o.get('type') == 'clone': continue
        g = o.get('graphics_id', ''); body = SCR.get(o.get('script', ''), '')
        has_spr = sprite(g) if g.startswith('OBJ_EVENT_GFX_') else False
        gl = gfx_label(g); entry = dict(x=o['x'], y=o['y'], gfx=g.replace('OBJ_EVENT_GFX_', '').lower() if has_spr else '', label=gl)
        tm = re.search(r'trainerbattle\w*\s+TRAINER_(\w+)', body)
        if not tm and o.get('script') in ball: 
            entry.update(kind='item', item=item_pair(ball[o['script']])); rec['npcs'].append(entry); continue
        labs = script_texts(o.get('script', ''))
        if tm and tm.group(1) in tr_by_id:
            t_ = tr_by_id[tm.group(1)]; entry.update(kind='trainer', label=dict(en='%s %s' % (t_['cls']['en'], t_['name']), fr='%s %s' % (t_['cls']['fr'], t_['name'])), tid=tm.group(1))
            who = entry['label']
        else:
            entry['kind'] = 'npc'; who = gl
        entry['texts'] = attach(labs, who)
        if entry['kind'] == 'npc' and not entry['texts'] and not g.startswith('OBJ_EVENT_GFX_'): continue
        rec['npcs'].append(entry)
    for b in j.get('bg_events', []):
        if b.get('type') == 'hidden_item': rec['hidden'].append(dict(x=b['x'], y=b['y'], item=item_pair(b['item'])))
        elif b.get('script'):
            tx = attach(script_texts(b['script']), dict(en='Sign', fr='Panneau'))
            if tx: rec['signs'].append(dict(x=b['x'], y=b['y'], texts=tx))
    for c in j.get('coord_events', []):
        if c.get('script'):
            tx = attach(script_texts(c['script']), dict(en='Event', fr='Événement'))
            if tx: rec['triggers'].append(dict(x=c['x'], y=c['y'], texts=tx))
    # texte de la carte non rattaché
    mtxt = parse_strings(os.path.join(R, 'data/maps', folder, 'text.inc')) if os.path.exists(os.path.join(R, 'data/maps', folder, 'text.inc')) else {}
    for lb in mtxt:
        t_ = T(lb)
        if t_ and t_['en'] and lb not in used:
            used.add(lb); rec['other'].append(t_); dialogues.append([folder, 'Other' , 'Autre', t_['en'], t_['fr']])
    # boutiques, cadeaux, statiques
    sp_ = os.path.join(R, 'data/maps', folder, 'scripts.inc'); stxt = open(sp_, encoding='utf-8', errors='replace').read() if os.path.exists(sp_) else ''
    for m in re.finditer(r'(\w+)::\n((?:\s*\.2byte ITEM_\w+\n)+)', stxt):
        its = [item_pair(x) for x in re.findall(r'ITEM_(\w+)', m.group(2)) if x != 'NONE']
        rec['shops'].append(dict(items=[dict(item=i, id=re.sub(r'\W', '', k), price=ITEM_PRICE.get(re.sub(r'\W', '', k), 0)) for i, k in zip(its, [x for x in re.findall(r'ITEM_(\w+)', m.group(2)) if x != 'NONE'])]))
    for m in re.finditer(r'^\s*(givemon|setwildbattle)\s+SPECIES_(\w+),\s*(\d+)', stxt, re.M):
        if m.group(2) in sp_names: rec['given'].append(dict(kind='gift' if m.group(1) == 'givemon' else 'static', sp=SP(m.group(2)), n=dex_by_id[m.group(2)]['n'] if m.group(2) in dex_by_id else 0, lvl=int(m.group(3))))
    for m in re.finditer(r'^\s*(giveitem_msg|giveitem)\s+(?:\w+,\s*)?ITEM_(\w+)', stxt, re.M): rec['given'].append(dict(kind='item', item=item_pair(m.group(2))))
    rows = [dict(sp=w['sp'], n=w['n'], how=w['how'], min=w['min'], max=w['max'], pct=w['pct']) for w in wild_by_map.get(mid, [])]
    rec['wild'] = rows
    rec['nNPC'] = len(rec['npcs']); rec['nTexts'] = sum(len(x.get('texts', [])) for x in rec['npcs']) + len(rec['signs']) + len(rec['other'])
    maps_index.append(dict(id=folder, name=nm, area=rec['area'], kind=rec['kind'], img=img, w=rec['w'], h=rec['h'], npcs=len(rec['npcs']), trainers=sum(1 for n in rec['npcs'] if n['kind'] == 'trainer'), wild=len(rows), texts=rec['nTexts'], shops=len(rec['shops'])))
    RECS[folder] = rec
    for s_ in rec['shops']: shops_all.append(dict(map=folder, name=nm, items=s_['items']))
    for g_ in rec['given']: given_all.append(dict(map=folder, name=nm, **g_))
incoming = collections.defaultdict(list)
for f_, r_ in RECS.items():
    seen_ = set()
    for w_ in r_['warps']:
        if w_['to'] in RECS and (w_['to'], f_) not in seen_: seen_.add((w_['to'], f_)); incoming[w_['to']].append(dict(id=f_, name=r_['name']))
    for c_ in r_['conn']:
        if c_['to'] in RECS and (c_['to'], f_) not in seen_: seen_.add((c_['to'], f_)); incoming[c_['to']].append(dict(id=f_, name=r_['name']))
area_sib = collections.defaultdict(list)
for m_ in maps_index: area_sib[m_['area']['en']].append(m_['id'])
for f_, r_ in RECS.items():
    r_['from'] = incoming.get(f_, [])
    r_['sib'] = [dict(id=x, name=RECS[x]['name']) for x in area_sib[r_['area']['en']] if x != f_ and x in RECS][:60]
    open(os.path.join(D, 'data/map/%s.js' % f_), 'w', encoding='utf-8').write('window.MAPDATA=window.MAPDATA||{};MAPDATA[%s]=%s;\n' % (json.dumps(f_), json.dumps(r_, ensure_ascii=False, separators=(',', ':'))))
# liens carte dans les lignes sauvages
_wm = {}
for w_ in wild:
    f_ = id2folder.get('MAP_' + w_['map'])
    if f_: _wm.setdefault((w_['n'], w_['loc']['en'], w_['how']['en']), f_)
for w_ in wild: w_['mid'] = _wm.get((w_['n'], w_['loc']['en'], w_['how']['en']), '')
for p_ in dex:
    for r_ in p_.get('where', []): r_['mid'] = _wm.get((p_['n'], r_['loc']['en'], r_['how']['en']), '')
out('pokedex', 'POKEDEX', dex); out('wild', 'WILD', [dict(w) for w in wild])
out('maps', 'MAPS', maps_index)
out('shops', 'SHOPS', shops_all)
open(os.path.join(D, 'data/dialogues.js'), 'w', encoding='utf-8').write('window.DIALOGUES=%s;\n' % json.dumps(dialogues, ensure_ascii=False, separators=(',', ':')))
print(len(maps_index), 'cartes,', len(dialogues), 'dialogues,', len(shops_all), 'boutiques,', sum(1 for m in maps_index if m['img']), 'images')

# ---------- images : Pokémon et objets ----------
from PIL import Image
os.makedirs(D + '/img/pokemon', exist_ok=True); os.makedirs(D + '/img/items', exist_ok=True)
def read_pal(path):
    L_ = open(path).read().split(); n = int(L_[2]); return [tuple(int(x) for x in L_[3 + 3 * i:6 + 3 * i]) for i in range(n)]
def conv(png, pal, outp):
    im = Image.open(png)
    if im.mode != 'P': im = im.convert('P')
    if pal:
        flat = []
        for c in pal[:16]: flat += list(c)
        flat += [0] * (768 - len(flat)); im.putpalette(flat)
    im = im.convert('RGBA'); px = im.load(); w, h = im.size
    idx = Image.open(png); idx = idx if idx.mode == 'P' else None
    if idx:
        ip = idx.load()
        for y in range(h):
            for x in range(w):
                if ip[x, y] == 0: px[x, y] = (0, 0, 0, 0)
    im.save(outp, optimize=True)
gm = rd('src/data/graphics/pokemon.h')
front = dict(re.findall(r'gMonFrontPic_(\w+)\[\] = INCBIN_U32\("(graphics/pokemon/[^"]+)/front\.4bpp\.lz"', gm))
pal_ = dict(re.findall(r'gMonPalette_(\w+)\[\] = INCBIN_U32\("([^"]+)\.gbapal\.lz"', gm))
ft = dict(re.findall(r'SPECIES_SPRITE\((\w+), gMonFrontPic_(\w+)\)', rd('src/data/pokemon_graphics/front_pic_table.h')))
pt = dict(re.findall(r'SPECIES_PAL\((\w+), gMonPalette_(\w+)\)', rd('src/data/pokemon_graphics/palette_table.h')))
npk = 0
for sid, e in dex_by_id.items():
    outp = D + '/img/pokemon/%d.png' % e['n']
    if os.path.exists(outp): npk += 1; continue
    f = front.get(ft.get(sid, ''))
    if not f: continue
    pp = pal_.get(pt.get(sid, ''))
    try:
        conv(next(x for x in (os.path.join(R, f, 'front.png'), os.path.join(R, f, 'normal/front.png'), os.path.join(R, f, 'anim_front.png')) if os.path.exists(x)), read_pal(os.path.join(R, pp + '.pal')) if pp and os.path.exists(os.path.join(R, pp + '.pal')) else None, outp); npk += 1
    except Exception as ex: pass
ic = dict(re.findall(r'\[ITEM_(\w+)\]\s*=\s*\{gItemIcon_(\w+), gItemIconPalette_(\w+)\}', rd('src/data/item_icon_table.h')) and [(a, (b, c)) for a, b, c in re.findall(r'\[ITEM_(\w+)\]\s*=\s*\{gItemIcon_(\w+), gItemIconPalette_(\w+)\}', rd('src/data/item_icon_table.h'))])
itx = rd('src/data/graphics/items.h'); icf = dict(re.findall(r'gItemIcon_(\w+)\[\] = INCBIN_U32\("([^"]+)\.4bpp\.lz"', itx)); icp = dict(re.findall(r'gItemIconPalette_(\w+)\[\] = INCBIN_U32\("([^"]+)\.gbapal\.lz"', itx))
nit = 0
for k, (b, c) in ic.items():
    outp = D + '/img/items/%s.png' % k
    if os.path.exists(outp): nit += 1; continue
    f = icf.get(b)
    if not f or not os.path.exists(os.path.join(R, f + '.png')): continue
    pp = icp.get(c)
    try: conv(os.path.join(R, f + '.png'), read_pal(os.path.join(R, pp + '.pal')) if pp and os.path.exists(os.path.join(R, pp + '.pal')) else None, outp); nit += 1
    except Exception: pass
print(npk, 'sprites Pokémon,', nit, 'icônes objets')

# ---------- talents ----------
ab_en = dict(l.rstrip('\n').split('|', 1) for l in open(R + '/tools/topaze/i18n/ability_desc_en.txt', encoding='utf-8') if '|' in l)
ab_fr_d = {}
_m = re.search(r'gAbilityDescriptionPointers\[ABILITIES_COUNT\] =\s*\{(.*?)\};', rd('src/data/text/abilities.h'), re.S)
_dd = dict(re.findall(r'static const u8 (s\w+Description)\[\] = _\("([^"]*)"\)', rd('src/data/text/abilities.h')))
for c, v in re.findall(r'\[ABILITY_(\w+)\]\s*=\s*(s\w+Description)', _m.group(1)): ab_fr_d[c] = _dd.get(v, '')
ab_by_en = {}
for c in ab_names: ab_by_en.setdefault(AB(c)['en'], c)
ab_out = []
for c in ab_names:
    if c == 'NONE': continue
    nm_ = AB(c); mons = [dict(n=p_['n'], name=p_['name'], hidden=False) for p_ in dex if any(a_['en'] == nm_['en'] for a_ in p_['abilities'])]
    ab_out.append(dict(id=c, name=nm_, desc=dict(en=ab_en.get(c, ''), fr=ab_fr_d.get(c, '')), pokemon=mons))
out('abilities', 'ABILITIES', ab_out)
out('gifts', 'GIFTS', given_all)

# ---------- index de recherche ----------
SRCH = []
for p_ in dex: SRCH.append(['pokemon', p_['name']['en'], p_['name']['fr'], 'pokedex.html#%d' % p_['n'], '#%d %s' % (p_['n'], '/'.join(p_['types']))])
for m_ in moves: SRCH.append(['move', m_['name']['en'], m_['name']['fr'], 'movedex.html#' + m_['name']['en'].replace(' ', '%20'), m_['type'] + (' ' + m_['tm'] if m_['tm'] else '')])
for i_ in items_out: SRCH.append(['item', i_['name']['en'], i_['name']['fr'], 'items.html#' + i_['id'], i_['pocket']])
for a_ in ab_out: SRCH.append(['ability', a_['name']['en'], a_['name']['fr'], 'abilities.html#' + a_['id'], ''])
for m_ in maps_index: SRCH.append(['place', m_['name']['en'], m_['name']['fr'], 'lieu.html#' + m_['id'], m_['kind']])
for t_ in tr_out: SRCH.append(['trainer', '%s %s' % (t_['cls']['en'], t_['name']), '%s %s' % (t_['cls']['fr'], t_['name']), 'trainers.html#' + t_['id'], t_['loc']['en']])
for c_ in champs: SRCH.append(['trainer', c_['name'], c_['name'], 'champions.html#%d' % c_['n'], c_['city']])
open(os.path.join(D, 'data/search.js'), 'w', encoding='utf-8').write('window.SEARCH=%s;\n' % json.dumps(SRCH, ensure_ascii=False, separators=(',', ':')))
print(len(ab_out), 'talents,', len(SRCH), 'entrées de recherche')
