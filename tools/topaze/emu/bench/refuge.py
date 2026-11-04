import sys, struct, re
sys.path.insert(0,'/tmp/gx')
from play import *
ITEMS = {m.group(1): int(m.group(2)) for m in re.finditer(r'#define (ITEM_\w+)\s+(\d+)', open('/home/claude/pkmn-topaze/include/constants/items.h').read())}
CHAIN = [(0,'PalletTown',[('ITEM_POTION',5),('ITEM_MOOMOO_MILK',2)]),(1,'ViridianCity',[('ITEM_NUGGET',1)]),(2,'PewterCity',[('ITEM_FULL_HEAL',3),('ITEM_STAR_PIECE',1)]),
 (3,'CeruleanCity',[]),(4,'VermilionCity',[('ITEM_REVIVE',2),('ITEM_BIG_PEARL',1)]),(5,'LavenderTown',[('ITEM_SPELL_TAG',1)]),(6,'CeladonCity',[('ITEM_LEMONADE',3),('ITEM_ELIXIR',1)]),
 (7,'SaffronCity',[('ITEM_TWISTED_SPOON',1)]),(8,'CinnabarIsland',[('ITEM_MAX_POTION',2),('ITEM_MAGNET',1)]),(9,'OneIsland',[]),(10,'TwoIsland',[('ITEM_HYPER_POTION',3)]),
 (11,'ThreeIsland',[]),(12,'FourIsland',[('ITEM_ICE_HEAL',3)]),(13,'FiveIsland',[]),(14,'SixIsland',[('ITEM_FULL_RESTORE',2)]),(15,'SevenIsland',[])]
ISL = {'OneIsland':1,'TwoIsland':2,'ThreeIsland':3,'FourIsland':4,'FiveIsland':5,'SixIsland':6,'SevenIsland':7}
def bag_add(t, item, qty):
    sb = t.e.u32(0x03005108); sb2 = t.e.u32(0x0300510c); key = t.e.u32(sb2 + 0xF20) & 0xffff
    iid = ITEMS[item]
    for i in range(42):
        a = sb + 0x310 + 4*i; cur, q = struct.unpack('<HH', t.e.peek(a, 4))
        if cur == iid: q = (q ^ key) + qty; break
        if cur == 0: q = qty; break
    for k, b in enumerate(struct.pack('<HH', iid, q ^ key)): t.e.cmd('poke8 %x %x' % (a + k, b))
def talk_land(t, pat, face_n=40):
    pos = t.find_obj(pat); n = t.nav()
    for dx, dy, fc in ((0, 1, 'UP'), (0, -1, 'DOWN'), (-1, 0, 'RIGHT'), (1, 0, 'LEFT')):
        c = (pos[0] + dx, pos[1] + dy)
        if not (0 <= c[0] < n.w and 0 <= c[1] < n.h) or n.blocked(*c) or (n.attr(*c) & 0x1ff) in RF.R.WATER: continue
        if t.walk_to(c) is not False and t.pos()[2:] == c and not t.surfing():
            t.face(fc); t.press('A', 4, 40); t.mash(face_n); t.scene(900); return True
    return False
t = Player.resume(sys.argv[1] if len(sys.argv) > 1 else 'end2_done'); RF.R.SURF = True
log('=== REFUGE (fin 2) depart', t.sync(), 'stage', t.getvar('VAR_REFUGE_STAGE'), [(q['level'], q['hp']) for q in t.party()])
for st, mp, need in CHAIN:
    if t.getvar('VAR_REFUGE_STAGE') > st: continue
    t.heal(True)
    for it, q in need: bag_add(t, it, q); log('  objet fourni (a verifier cote jeu) :', it, q)
    try:
        if mp in ISL and RF.cur_isle(t) is None: RF.stage_pg_ferry(t)
        if mp in ISL: RF.go_isle(t, ISL[mp], mp)
        else: assert t.go(mp), 'inaccessible'
        t.e.run(60, 0)
        for k in range(3):
            if t.getvar('VAR_REFUGE_STAGE') > st: break
            if not talk_land(t, '_Refuge'): t.talk_script('_Refuge', 40, 'ref%d' % st)
            for _ in range(8):
                if not t.inbattle(): break
                t.finish_battle(maxn=900); t.scene(maxn=300)
            t.scene(maxn=400)
    except AssertionError as ex: log('BLOCK poste', st, mp, ex)
    log('POSTE', st, mp, '-> stage', t.getvar('VAR_REFUGE_STAGE'), 'equipe', [(q['level'], q['hp']) for q in t.party()])
    t.save('refuge_%d' % st)
log('=== FIN REFUGE stage', t.getvar('VAR_REFUGE_STAGE'))
