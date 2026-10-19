#!/usr/bin/env python3
"""Ajoute les talents Gen 5-9 (ids 114+) : constantes, noms, descriptions. Idempotent.
Usage : python3 docs/topaze/add_abilities.py <depot>"""
import sys
repo = sys.argv[1]
R = lambda p: open(repo + '/' + p).read()
def W(p, s): open(repo + '/' + p, 'w').write(s)
A = '''
SHEER_FORCE|SHEER FORCE|Power up, no added effects.
TOUGH_CLAWS|TOUGH CLAWS|Boosts contact moves.
STRONG_JAW|STRONG JAW|Boosts biting moves.
MEGA_LAUNCHER|MEGALAUNCHER|Boosts pulse moves.
SHARPNESS|SHARPNESS|Boosts slicing moves.
STEELWORKER|STEELWORKER|Boosts STEEL moves.
TRANSISTOR|TRANSISTOR|Boosts ELECTRIC moves.
DRAGONS_MAW|DRAGON'S MAW|Boosts DRAGON moves.
ROCKY_PAYLOAD|ROCK PAYLOAD|Boosts ROCK moves.
WATER_BUBBLE|WATER BUBBLE|Boosts WATER, blocks burns.
AERILATE|AERILATE|NORMAL moves turn FLYING.
PIXILATE|PIXILATE|NORMAL moves turn FAIRY.
REFRIGERATE|REFRIGERATE|NORMAL moves turn ICE.
GALVANIZE|GALVANIZE|NORMAL moves turn ELECTRIC.
ANALYTIC|ANALYTIC|Boost if it moves last.
TOXIC_BOOST|TOXIC BOOST|Stronger when poisoned.
FLARE_BOOST|FLARE BOOST|Stronger when burned.
SAND_FORCE|SAND FORCE|Boosts some moves in sand.
SAND_RUSH|SAND RUSH|Doubles SPEED in sand.
SLUSH_RUSH|SLUSH RUSH|Doubles SPEED in hail.
MULTISCALE|MULTISCALE|Halves damage at full HP.
FUR_COAT|FUR COAT|Doubles DEFENSE.
ICE_SCALES|ICE SCALES|Halves special damage.
FLUFFY|FLUFFY|Halves contact damage.
PRISM_ARMOR|PRISM ARMOR|Cuts super effective hits.
FULL_METAL_BODY|FULL METAL|Prevents stat reduction.
OVERCOAT|OVERCOAT|Immune to weather damage.
STORM_DRAIN|STORM DRAIN|WATER moves raise SP. ATK.
SAP_SIPPER|SAP SIPPER|GRASS moves raise ATTACK.
EARTH_EATER|EARTH EATER|GROUND moves heal HP.
WELL_BAKED_BODY|WELL-BAKED|FIRE moves raise DEFENSE.
IRON_BARBS|IRON BARBS|Hurts attackers on contact.
GOOEY|GOOEY|Contact slows the attacker.
STAMINA|STAMINA|Getting hit raises DEFENSE.
WEAK_ARMOR|WEAK ARMOR|Hit: DEF down, SPEED up.
RATTLED|RATTLED|Scared by BUG/GHOST/DARK.
JUSTIFIED|JUSTIFIED|DARK hits raise ATTACK.
STEAM_ENGINE|STEAM ENGINE|FIRE/WATER hits ups SPEED.
WATER_COMPACTION|WATER COMPCT|WATER hit sharply ups DEF.
MUMMY|MUMMY|Contact spreads MUMMY.
POISON_TOUCH|POISON TOUCH|May poison on contact.
MOXIE|MOXIE|Each KO raises ATTACK.
INTREPID_SWORD|INTRPD SWORD|Raises ATTACK on entry.
DAUNTLESS_SHIELD|DAUNT SHIELD|Raises DEFENSE on entry.
PRANKSTER|PRANKSTER|Status moves go first.
GALE_WINGS|GALE WINGS|FLYING first at full HP.
CONTRARY|CONTRARY|Stat changes are reversed.
DEFIANT|DEFIANT|Stat drop ups ATK a lot.
COMPETITIVE|COMPETITIVE|Stat drop ups SP. ATK a lot
BIG_PECKS|BIG PECKS|Protects DEFENSE.
REGENERATOR|REGENERATOR|Heals when switching out.
MOODY|MOODY|Random stat up and down.
MAGIC_BOUNCE|MAGIC BOUNCE|Reflects status moves.
PROTEAN|PROTEAN|Takes the move's type.
LIBERO|LIBERO|Takes the move's type.
'''.strip().split('\n')
A = [l.split('|') for l in A]
if 'ABILITY_SHEER_FORCE' in R('include/constants/abilities.h'):
    print('talents deja ajoutes'); sys.exit(0)
assert all(len(a[1]) <= 12 for a in A), [a[1] for a in A if len(a[1]) > 12]
assert all(len(a[2]) <= 27 for a in A), [a[2] for a in A if len(a[2]) > 27]
h = R('include/constants/abilities.h')
defs = ''.join('#define ABILITY_%s %d\n' % (a[0], 114 + i) for i, a in enumerate(A))
h = h.replace('#define ABILITIES_COUNT 114', defs + '\n#define ABILITIES_COUNT %d' % (114 + len(A)))
W('include/constants/abilities.h', h)
t = R('src/data/text/abilities.h')
ident = lambda c: ''.join(w.capitalize() for w in c.split('_'))
strs = ''.join('static const u8 s%sDescription[] = _("%s");\n' % (ident(a[0]), a[2]) for a in A)
t = t.replace('\nconst u8 *const gAbilityDescriptionPointers', strs + '\nconst u8 *const gAbilityDescriptionPointers', 1)
t = t.replace('    [ABILITY_NORMALIZE] = sNormalizeDescription,\n', '    [ABILITY_NORMALIZE] = sNormalizeDescription,\n' + ''.join('    [ABILITY_%s] = s%sDescription,\n' % (a[0], ident(a[0])) for a in A), 1)
t = t.replace('    [ABILITY_NORMALIZE] = _("NORMALIZE"),\n', '    [ABILITY_NORMALIZE] = _("NORMALIZE"),\n' + ''.join('    [ABILITY_%s] = _("%s"),\n' % (a[0], a[1]) for a in A), 1)
W('src/data/text/abilities.h', t)
print(len(A), 'talents ajoutes')
