#!/usr/bin/env python3
"""LOT 4 : 14 quetes d'objets sur les routes, ~45 objets caches sur les routes, Nursery (bebes Pokemon, 1 par badge), Maison du Troc (objets -> Pokemon rares),
passeur de l'apprenti. Textes anglais PROVISOIRES. Idempotent."""
import sys; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'FuchsiaCity_EventScript_Apprentice' in rd('data/maps/FuchsiaCity/scripts.inc'): print('deja applique'); raise SystemExit
journal = []
# ---------------- (a) quetes de routes
Q = [
 ('Route1', 'LITTLE_BOY', 'POTION', 3, 'GREAT_BALL', 5, 'A SIP OF HEALTH', 'ROUTE 1: a boy needs 3 POTIONS.', 'My buddy is hurt! Could you spare 3 POTIONS?', 'Thanks! Take these BALLS.', 'He is up and running again!'),
 ('Route3', 'PICNICKER', 'PARALYZE_HEAL', 2, 'SUPER_POTION', 2, 'STIFF AS A BOARD', 'ROUTE 3: a girl needs 2 PARALYZE HEALS.', 'My team is paralyzed. Please bring 2 PARALYZE HEALS!', 'Wonderful! A little thank you.', 'They are dancing again!'),
 ('Route4', 'HIKER', 'ESCAPE_ROPE', 1, 'REVIVE', 1, 'LOST IN THE CAVE', 'ROUTE 4: a hiker needs an ESCAPE ROPE.', 'I got lost in the cave. One ESCAPE ROPE would save me.', 'Saved! Take this, I found it down there.', 'I am never going back in without a rope.'),
 ('Route6', 'GENTLEMAN', 'SUPER_POTION', 2, 'ULTRA_BALL', 3, 'THE HURT PARTNER', 'ROUTE 6: a man needs 2 SUPER POTIONS.', 'My partner is wounded. Two SUPER POTIONS, if you please.', 'Excellent. Please accept these.', 'He is as good as new.'),
 ('Route7', 'LASS', 'BURN_HEAL', 2, 'HYPER_POTION', 2, 'PLAYING WITH FIRE', 'ROUTE 7: a lass needs 2 BURN HEALS.', 'I played with fire. I need 2 BURN HEALS!', 'Phew! This is for you.', 'No more burns. Promise.'),
 ('Route8', 'BUG_CATCHER', 'AWAKENING', 2, 'FULL_HEAL', 2, 'THE SLEEPYHEADS', 'ROUTE 8: a kid needs 2 AWAKENINGS.', 'My team will not wake up. I need 2 AWAKENINGS.', 'They are up! Take these.', 'We are wide awake now.'),
 ('Route10', 'SCIENTIST', 'HYPER_POTION', 2, 'MAX_REPEL', 2, 'THE FIELD RESEARCH', 'ROUTE 10: a nerd needs 2 HYPER POTIONS.', 'My research subject is injured. 2 HYPER POTIONS, quick!', 'Data saved. Thanks, take these.', 'The study goes on.'),
 ('Route11', 'FISHER', 'ICE_HEAL', 2, 'GREAT_BALL', 5, 'COLD CATCH', 'ROUTE 11: an angler needs 2 ICE HEALS.', 'My catch froze solid! 2 ICE HEALS, please.', 'Thaw complete! Here.', 'It swam off, warm and happy.'),
 ('Route12', 'FISHER', 'SUPER_REPEL', 2, 'ULTRA_BALL', 4, 'QUIET FISHING', 'ROUTE 12: an angler needs 2 SUPER REPELS.', 'Wild POKeMON scare the fish. 2 SUPER REPELS, please.', 'Peace and quiet. Thanks!', 'The fish are biting.'),
 ('Route14', 'BIKER', 'FULL_HEAL', 2, 'MAX_REVIVE', 1, 'ENGINE TROUBLE', 'ROUTE 14: a biker needs 2 FULL HEALS.', 'My crew is a mess. 2 FULL HEALS and I owe you.', 'Back on the road! Thanks.', 'The engine purrs again.'),
 ('Route15', 'GENTLEMAN', 'REVIVE', 1, 'RARE_CANDY', 1, 'THE LAST WISH', 'ROUTE 15: a man needs a REVIVE.', 'My oldest friend fainted. A single REVIVE would mean everything.', 'You are kind. Take this treasure.', 'He is up. He says thank you.'),
 ('Route16', 'BIKER', 'ANTIDOTE', 3, 'SUPER_POTION', 3, 'ROAD RASH', 'ROUTE 16: a biker needs 3 ANTIDOTES.', 'Poison all over my team. 3 ANTIDOTES, fast!', 'You saved the ride. Here.', 'We are riding again.'),
 ('Route18', 'COOLTRAINER_M', 'MAX_POTION', 1, 'PP_UP', 1, 'THE ENDURANCE TEST', 'ROUTE 18: a trainer needs a MAX POTION.', 'One MAX POTION would let me finish my training run.', 'Strong! Take this reward.', 'Run complete. Thanks.'),
 ('Route24', 'COOLTRAINER_F', 'MAX_REPEL', 2, 'RARE_CANDY', 2, 'THE BRIDGE WATCH', 'ROUTE 24: a trainer needs 2 MAX REPELS.', 'I guard this bridge. 2 MAX REPELS would keep it calm.', 'Calm at last. Take these.', 'The bridge is quiet.'),
]
for (m, gfx, w, wn, r, rn, name, hint, ask, ok, done) in Q:
    nav = R.Nav(m); d = json.load(open('data/maps/%s/map.json' % m)); cells = comp(nav)
    taken = [(o['x'], o['y']) for o in d['object_events']] + [(b['x'], b['y']) for b in d['bg_events']] + list(nav.warps)
    trainers = [(o['x'], o['y']) for o in d['object_events'] if o.get('trainer_type', 'TRAINER_TYPE_NONE') != 'TRAINER_TYPE_NONE']
    cand = [c for c in cells if not any((c[0] == t[0] and abs(c[1] - t[1]) <= 7) or (c[1] == t[1] and abs(c[0] - t[0]) <= 7) for t in trainers) and 2 <= c[0] < nav.w - 2 and 2 <= c[1] < nav.h - 2
            and all(not nav.blocked(c[0] + dx, c[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1))]
    c = near(nav, cand, (nav.w // 2 + 5, nav.h // 2 + 2), taken, margin=3)
    F = flag('RQ_%s' % m.upper()); S = '%s_EventScript_RQuest' % m; T = '%s_Text_RQuest' % m
    d['object_events'].append(N.obj(gfx, c[0], c[1], S, el=EL(nav, c))); N.jdump(d, 'data/maps/%s/map.json' % m)
    sc = ('\n@ Topaze: quete de route (%s)\n%s::\n\tlock\n\tfaceplayer\n\tgoto_if_set %s, %s_Done\n\tcheckitem %s, %d\n\tgoto_if_eq VAR_RESULT, FALSE, %s_Ask\n\tcheckitemspace %s, %d\n\tgoto_if_eq VAR_RESULT, FALSE, %s_NoRoom\n'
          '\tremoveitem %s, %d\n\tsetflag %s\n\tmsgbox %s_Ok\n\tgiveitem %s, %d\n\trelease\n\tend\n\n%s_Ask::\n\tmsgbox %s_Ask\n\trelease\n\tend\n\n%s_Done::\n\tmsgbox %s_Done\n\trelease\n\tend\n\n%s_NoRoom::\n\tmsgbox %s_NoRoom\n\trelease\n\tend\n') % (
        name, S, F, S, it(w), wn, S, it(r), rn, S, it(w), wn, F, T, it(r), rn, S, T, S, T, S, T)
    open('data/maps/%s/scripts.inc' % m, 'a').write(sc)
    open('data/maps/%s/text.inc' % m, 'a').write(N.text(T + '_Ask', ask) + N.text(T + '_Ok', ok) + N.text(T + '_Done', done) + N.text(T + '_NoRoom', 'Your BAG is full. Make room, then come back.'))
    journal.append(jl('SIDE QUESTS', F, name, hint, 'A'))
# ---------------- (b) objets caches sur les routes
H = {'Route1': ['POTION', 'POKE_BALL'], 'Route2': ['ANTIDOTE', 'GREAT_BALL'], 'Route3': ['SUPER_POTION', 'GREAT_BALL'], 'Route4': ['REVIVE', 'ULTRA_BALL'], 'Route5': ['ETHER', 'SUPER_POTION'], 'Route6': ['ULTRA_BALL', 'ANTIDOTE'],
     'Route7': ['REVIVE', 'NUGGET'], 'Route8': ['ELIXIR', 'HYPER_POTION'], 'Route9': ['MAX_REPEL', 'PP_UP'], 'Route10': ['MAX_ETHER', 'REVIVE'], 'Route11': ['HYPER_POTION', 'NUGGET'], 'Route12': ['ELIXIR', 'ULTRA_BALL'],
     'Route13': ['RARE_CANDY', 'FULL_HEAL'], 'Route14': ['MAX_REVIVE', 'ULTRA_BALL'], 'Route15': ['PP_UP', 'MAX_ETHER'], 'Route16': ['NUGGET', 'HYPER_POTION'], 'Route17': ['RARE_CANDY', 'MAX_POTION'], 'Route18': ['ELIXIR', 'STAR_PIECE'],
     'Route19': ['MAX_REVIVE'], 'Route20': ['PP_UP', 'ULTRA_BALL'], 'Route22': ['HYPER_POTION'], 'Route23': ['RARE_CANDY', 'MAX_REVIVE'], 'Route24': ['NUGGET', 'MAX_ELIXIR'], 'Route25': ['PP_UP', 'STAR_PIECE']}
nh = 0
for m, items in H.items():
    nav = R.Nav(m); d = json.load(open('data/maps/%s/map.json' % m)); cells = comp(nav)
    taken = [(o['x'], o['y']) for o in d['object_events']] + [(b['x'], b['y']) for b in d['bg_events']] + list(nav.warps)
    cand = [c for c in cells if 2 <= c[0] < nav.w - 2 and 2 <= c[1] < nav.h - 2]
    for i, itn in enumerate(items):
        pref = (int(nav.w * (0.25 + 0.5 * i + 0.1 * len(m) % 3 * 0.05)), int(nav.h * (0.3 + 0.35 * i)))
        c = near(nav, cand, pref, taken, margin=4); taken.append(c)
        d['bg_events'].append({'type': 'hidden_item', 'x': c[0], 'y': c[1], 'elevation': 0, 'item': it(itn), 'flag': flag('HID_%s_%d' % (m.upper(), i)), 'quantity': 1, 'underfoot': False}); nh += 1
    N.jdump(d, 'data/maps/%s/map.json' % m)
print('quetes', len(Q), 'caches', nh)
# ---------------- (c)(d) nursery + troc
def chain_building(mn, tpl, npcgfx, entries, hello, kind):
    N.clone(mn, tpl, objects=[], warps=[], scripts='', txt=''); nav = R.Nav(mn); cells = comp(nav); a = near(nav, cells, (nav.w // 2, int(nav.h * .75)), [], margin=0); taken = [a]
    def place(gfx, pref, script, mg=1):
        c = near(nav, cells, pref, taken, mg); taken.append(c); return N.obj(gfx, c[0], c[1], script, el=EL(nav, c))
    objs = [place('SAILOR', (a[0] + 2, a[1]), mn + '_EventScript_ReturnFerry'), place(npcgfx, (a[0], a[1] - 3), mn + '_EventScript_Clerk')]
    sc = ('%s_EventScript_ReturnFerry::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_ReturnAsk, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s_EventScript_Stay\n\twarp MAP_FUCHSIA_CITY, 255, 24, 27\n\twaitstate\n\tend\n\n%s_EventScript_Stay::\n\tmsgbox %s_Text_Stay\n\trelease\n\tend\n\n') % ((mn,) * 5)
    tx = N.text(mn + '_Text_ReturnAsk', 'Ready to go back to the dock?') + N.text(mn + '_Text_Stay', 'Take your time. The tide can wait.') + N.text(mn + '_Text_Hello', hello) + N.text(mn + '_Text_Nothing', 'Nothing for you right now. Come back with more.')
    C = mn + '_EventScript_Clerk'; sc += '%s::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_Hello\n' % (C, mn)
    for i, e in enumerate(entries):
        nxt = '%s_%d' % (C, i + 1) if i < len(entries) - 1 else C + '_End'
        F = flag('%s_%d' % (kind, i)); e['F'] = F; sc += ('%s_%d::\n' % (C, i) if i else '')
        sc += '\tgoto_if_set %s, %s\n' % (F, nxt)
        if e.get('badge'): sc += '\tgoto_if_unset FLAG_BADGE0%d_GET, %s\n' % (e['badge'], nxt)
        if e.get('item'): sc += '\tcheckitem %s, %d\n\tgoto_if_eq VAR_RESULT, FALSE, %s\n' % (it(e['item'][0]), e['item'][1], nxt)
        sc += '\tmsgbox %s_Text_O%d, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s\n' % (mn, i, nxt)
        if e.get('item'): sc += '\tremoveitem %s, %d\n' % (it(e['item'][0]), e['item'][1])
        sc += '\tgivemon %s, %d\n\tgoto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon\n\tsetflag %s\n\tmsgbox %s_Text_G%d\n\tgoto %s\n' % (sp(e['sp']), e['lv'], F, mn, i, nxt)
        tx += N.text('%s_Text_O%d' % (mn, i), e['offer']) + N.text('%s_Text_G%d' % (mn, i), 'Take good care of it!')
    sc += '%s_End::\n\tmsgbox %s_Text_Nothing\n\trelease\n\tend\n' % (C, mn)
    N.rewrite(mn, objs, sc, tx); return a
NURS = [dict(sp='PICHU', lv=10, badge=2, offer='A PICHU, shy and sparkling. Adopt it?'), dict(sp='CLEFFA', lv=10, badge=2, offer='A CLEFFA fell from the stars. Adopt it?'),
        dict(sp='IGGLYBUFF', lv=10, badge=3, offer='An IGGLYBUFF, soft as a cloud. Adopt it?'), dict(sp='AZURILL', lv=10, badge=3, offer='An AZURILL, bouncy and blue. Adopt it?'),
        dict(sp='SMOOCHUM', lv=12, badge=4, offer='A SMOOCHUM, always ready for a kiss. Adopt it?'), dict(sp='ELEKID', lv=14, badge=5, offer='An ELEKID, full of sparks. Adopt it?'),
        dict(sp='MAGBY', lv=14, badge=6, offer='A MAGBY, warm and curious. Adopt it?'), dict(sp='TYROGUE', lv=16, badge=7, offer='A TYROGUE, ready to brawl. Adopt it?'), dict(sp='WYNAUT', lv=18, badge=8, offer='A WYNAUT, always smiling. Adopt it?')]
BART = [dict(sp='FEEBAS', lv=20, item=('HEART_SCALE', 5), offer='5 HEART SCALES for a FEEBAS. Deal?'), dict(sp='SPHEAL', lv=25, item=('SHOAL_SHELL', 1), offer='A SHOAL SHELL for a SPHEAL. Deal?'),
        dict(sp='SNORUNT', lv=25, item=('SHOAL_SALT', 1), offer='A SHOAL SALT for a SNORUNT. Deal?'), dict(sp='SHROOMISH', lv=20, item=('TINY_MUSHROOM', 1), offer='A TINY MUSHROOM for a SHROOMISH. Deal?'),
        dict(sp='BRELOOM', lv=30, item=('BIG_MUSHROOM', 1), offer='A BIG MUSHROOM for a BRELOOM. Deal?'), dict(sp='CLAMPERL', lv=25, item=('PEARL', 1), offer='A PEARL for a CLAMPERL. Deal?'),
        dict(sp='LUNATONE', lv=30, item=('STARDUST', 2), offer='2 STARDUST for a LUNATONE. Deal?'), dict(sp='SOLROCK', lv=30, item=('STAR_PIECE', 2), offer='2 STAR PIECES for a SOLROCK. Deal?')]
an = chain_building('BabyNursery', 'SaffronCity_HomeD', 'WOMAN_3', NURS, 'Little ones need a home. Each BADGE opens a new cradle. Take one?', 'NURSERY')
ab = chain_building('BarterHouse', 'SaffronCity_HomeE', 'MAN', BART, 'I trade small treasures for rare POKeMON. Let us see what you carry.', 'BARTER')
ferry('Apprentice', 'LITTLE_BOY', (31, 26), 'The master is busy. I row the small trips, {PLAYER}.', 'The boat is not ready. Come back when the clocks make sense.', 'Another time, then.',
      [('BabyNursery', an, 0, 'The BABY NURSERY: little POKeMON need a home. Visit?', ''), ('BarterHouse', ab, 0, 'The BARTER HOUSE: trade treasures for rare POKeMON. Visit?', '')])
journal += [jl('SIDE QUESTS', NURS[-1]['F'], 'THE BABY NURSERY', 'Ferry from AMETHIOLITE: one baby\nPOKeMON per badge.'), jl('SIDE QUESTS', BART[-1]['F'], 'THE BARTER HOUSE', 'Ferry from AMETHIOLITE: treasures\nfor rare POKeMON.')]
journal_add(['# ---- LOT 4 (quetes de routes, nursery, troc)'] + journal); flush_flags()
