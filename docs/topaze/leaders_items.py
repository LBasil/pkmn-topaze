#!/usr/bin/env python3
"""Objets tenus par les équipes des 8 champions. Usage : python3 docs/topaze/leaders_items.py <dépôt>
À lancer APRÈS leaders_data.py (qui réécrit les équipes sans objets). Idempotent."""
import re, sys
repo = sys.argv[1]
TP = repo + '/src/data/trainer_parties.h'; TR = repo + '/src/data/trainers.h'
ITEMS = {  # slot d'origine -> objets dans l'ordre de l'équipe
 'Brock': 'CHARCOAL SITRUS_BERRY CHARCOAL LEFTOVERS',
 'Misty': 'SILVER_POWDER MIRACLE_SEED SILVER_POWDER SITRUS_BERRY LEFTOVERS',
 'LtSurge': 'SHARP_BEAK SITRUS_BERRY SHARP_BEAK DRAGON_FANG LEFTOVERS',
 'Erika': 'NEVER_MELT_ICE SITRUS_BERRY NEVER_MELT_ICE HARD_STONE LEFTOVERS',
 'Koga': 'POISON_BARB POISON_BARB SITRUS_BERRY POISON_BARB LEFTOVERS',
 'Sabrina': 'BLACK_GLASSES SITRUS_BERRY SPELL_TAG SPELL_TAG LEFTOVERS',
 'Blaine': 'MAGNET MAGNET SITRUS_BERRY MAGNET LEFTOVERS',
 'Giovanni': 'SITRUS_BERRY METAL_COAT BLACK_BELT METAL_COAT LEFTOVERS',
}
tp = open(TP).read(); tr = open(TR).read()
for slot, items in ITEMS.items():
    items = items.split()
    m = re.search(r'static const struct TrainerMonNoItemCustomMoves (sParty_Leader%s)\[\] = \{(.*?)\n\};' % slot, tp, re.S)
    if not m: continue  # déjà fait
    body = m.group(2); it = iter(items)
    body = re.sub(r'(\.species = SPECIES_\w+,)', lambda x: x.group(1) + '\n        .heldItem = ITEM_%s,' % next(it), body)
    assert next(it, None) is None, slot
    tp = tp.replace(m.group(0), 'static const struct TrainerMonItemCustomMoves %s[] = {%s\n};' % (m.group(1), body))
    tr = tr.replace('NO_ITEM_CUSTOM_MOVES(sParty_Leader%s)' % slot, 'ITEM_CUSTOM_MOVES(sParty_Leader%s)' % slot)
open(TP, 'w').write(tp); open(TR, 'w').write(tr); print('ok')
