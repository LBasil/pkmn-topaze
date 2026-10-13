# ARENE DE GRIM (Bourg Quartz, type Glace/Eau) : dresseurs et textes. Idempotent.
import re
T = {
 'TRAINER_LASS_KAY': ('NORA', [('SEEL', 26), ('SHELLDER', 27)]),
 'TRAINER_BEAUTY_BRIDGET': (None, [('SHELLDER', 25), ('SEEL', 25), ('SHELLDER', 25), ('SEEL', 25)]),
 'TRAINER_PICNICKER_TINA': (None, [('HORSEA', 27), ('STARYU', 27), ('SLOWPOKE', 28)]),
 'TRAINER_BEAUTY_TAMIA': (None, [('STARYU', 27), ('SEEL', 28)]),
 'TRAINER_BEAUTY_LORI': (None, [('JYNX', 29)]),
 'TRAINER_LASS_LISA': (None, [('HORSEA', 26), ('HORSEA', 27)]),
 'TRAINER_COOLTRAINER_MARY': (None, [('SEEL', 26), ('SHELLDER', 26), ('STARYU', 27), ('SLOWPOKE', 27), ('HORSEA', 27)]),
}
tr = open('src/data/trainers.h').read(); pa = open('src/data/trainer_parties.h').read()
for i, (name, team) in T.items():
    b = re.search(r'\[%s\] = \{.*?\n    \},' % i, tr, re.S).group(0)
    nb = b.replace('NO_ITEM_CUSTOM_MOVES', 'NO_ITEM_DEFAULT_MOVES')
    if name: nb = re.sub(r'_\("[^"]*"\)', '_("%s")' % name, nb, 1)
    tr = tr.replace(b, nb)
    sym = re.search(r'NO_ITEM_DEFAULT_MOVES\((\w+)\)', nb).group(1)
    m = re.search(r'static const struct TrainerMon\w+ %s\[\] = \{.*?\n\};' % sym, pa, re.S); assert m, sym
    body = ''.join('    {\n        .iv = 20,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n' % (lv, sp) for sp, lv in team)
    pa = pa.replace(m.group(0), 'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};' % (sym, body))
# Grim un cran plus bas (as 35)
for a, c in (('DEWGONG', 31), ('CLOYSTER', 32), ('JYNX', 33), ('ONIX', 33), ('LAPRAS', 35)):
    pa = re.sub(r'(\.lvl = )\d+(,\s*\.species = SPECIES_%s,\s*\.heldItem)' % a, r'\g<1>%d\2' % c, pa)
open('src/data/trainer_parties.h', 'w').write(pa); open('src/data/trainers.h', 'w').write(tr)
def setText(label, new):
    p = 'data/maps/CeladonCity_Gym/text.inc'
    for part in re.split(r'\\n|\\p|\\l', new): assert len(part) <= 35, part
    s = open(p).read(); a = s.index(label + '::'); b = s.index('\n\n', a) if '\n\n' in s[a:] else len(s)
    open(p, 'w').write(s[:a] + label + '::\n    .string "%s$"' % new + s[b:])
P = 'CeladonCity_Gym_Text_'
setText(P+'KayIntro', 'Welcome to the QUARTZ GYM.\\nIt is cold in here. Deal with it!')
setText(P+'KayDefeat', 'Brr... You melted me!')
setText(P+'KayPostBattle', 'GRIM never raises her voice.\\nThat is what scares me.')
setText(P+'BridgetIntro', 'Oh, welcome.\\nMy POKéMON love the cold.')
setText(P+'BridgetDefeat', 'My ice has cracked!')
setText(P+'BridgetPostBattle', 'ICE-type POKéMON are weak to FIRE\\nand FIGHTING moves.\\pBut they hit GRASS and DRAGON\\nvery hard.')
setText(P+'TinaIntro', '...Weren\'t you peeking in the\\nGAME CORNER earlier?')
setText(P+'TinaPostBattle', 'Men in black have a table down\\nthere. Even GRIM heard them.')
setText(P+'TamiaIntro', 'Look, look!\\nMy POKéMON never feel the cold.')
setText(P+'TamiaPostBattle', 'Our GYM freezes the whole floor.\\pThat is why we all wear boots\\nand thick scarves.')
setText(P+'LisaIntro', 'Oh, hey!\\nWe do not let FIRE-types in here!')
setText(P+'LisaPostBattle', 'Our LEADER GRIM might be quiet,\\nbut she is famous around here.')
setText(P+'LoriIntro', 'Pleased to meet you.\\nMy hobby is training in the snow.')
setText(P+'MaryIntro', 'Welcome to BOURG QUARTZ GYM!\\pYou will need more than a coat to\\nbeat us.')
setText(P+'MaryPostBattle', 'I did not bring my best POKéMON.\\nThe lake keeps them company.')
