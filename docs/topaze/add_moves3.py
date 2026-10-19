#!/usr/bin/env python3
"""Troisieme vague d'attaques Gen 4-9 (ids 536+). Usage : python3 docs/topaze/add_moves2.py <depot>. Idempotent."""
import re, sys, textwrap
repo = sys.argv[1]
R = lambda p: open(repo + '/' + p).read()
def W(p, s): open(repo + '/' + p, 'w').write(s)
PHYS_TYPES = {'NORMAL','FIGHTING','FLYING','POISON','GROUND','ROCK','BUG','GHOST','STEEL'}
# CONST|NOM|TYPE|cat(P/S/T)|puissance|precision|PP|effet|%sec|priorite|cible|anim|description
M = '''
RETALIATE|RETALIATE|NORMAL|P|70|100|5|HIT|0|0|SEL|DOUBLE_EDGE|Avenges a fallen ally with a savage hit.
ECHOED_VOICE|ECHOED VOICE|NORMAL|S|40|100|15|HIT|0|0|SEL|HYPER_VOICE|A voice that echoes through the air.
TECHNO_BLAST|TECHNO BLAST|NORMAL|S|120|100|5|HIT|0|0|SEL|HYPER_BEAM|A blast of pure energy.
JUDGMENT|JUDGMENT|NORMAL|S|100|100|10|HIT|0|0|SEL|HYPER_VOICE|Releases countless shots of light.
MULTI_ATTACK|MULTI-ATTACK|NORMAL|P|120|100|10|HIT|0|0|SEL|TRI_ATTACK|Cloaks itself in power and strikes.
RELIC_SONG|RELIC SONG|NORMAL|S|75|100|10|HIT|0|0|SEL|SING|An ancient song hits the foe.
RAGING_BULL|RAGING BULL|NORMAL|P|90|100|10|HIT|0|0|SEL|HORN_ATTACK|A raging charge that smashes foes.
HYPER_DRILL|HYPER DRILL|NORMAL|P|100|100|5|HIT|0|0|SEL|DRILL_PECK|Spins a pointed part to pierce.
BLOOD_MOON|BLOOD MOON|NORMAL|S|140|100|5|HIT|0|0|SEL|HYPER_BEAM|Unleashes the energy of a blood moon.
TERRAIN_PULSE|TERRAIN PLSE|NORMAL|S|50|100|10|HIT|0|0|SEL|WATER_PULSE|Uses the land's power to attack.
HEAL_PULSE|HEAL PULSE|PSYCHIC|T|0|0|10|RESTORE_HP|0|0|USER|RECOVER|Recovers half of the user's max HP.
LIFE_DEW|LIFE DEW|WATER|T|0|0|10|RESTORE_HP|0|0|USER|RECOVER|Sprinkles dew. Restores half of max HP.
FORCE_PALM|FORCE PALM|FIGHTING|P|60|100|10|PARALYZE_HIT|30|0|SEL|MEGA_PUNCH|A shock wave from the palm. May paralyze.
SECRET_SWORD|SECRET SWORD|FIGHTING|S|85|100|10|HIT|0|0|SEL|SLASH|A mysterious sword cuts the foe.
BODY_PRESS|BODY PRESS|FIGHTING|P|80|100|10|HIT|0|0|SEL|BODY_SLAM|Presses down with the whole body.
COLLISION_COURSE|COLLISN CRSE|FIGHTING|P|100|100|5|HIT|0|0|SEL|TAKE_DOWN|A crashing dive from above.
THUNDEROUS_KICK|THNDR KICK|FIGHTING|P|90|100|10|DEFENSE_DOWN_HIT|100|0|SEL|MEGA_KICK|A lightning-fast kick. Lowers the foe's DEF.
AXE_KICK|AXE KICK|FIGHTING|P|120|90|10|CONFUSE_HIT|30|0|SEL|HI_JUMP_KICK|A heel drop. May confuse the foe.
COMBAT_TORQUE|COMBAT TORQ|FIGHTING|P|100|100|10|PARALYZE_HIT|30|0|SEL|MEGA_KICK|Fighting energy shoots out. May paralyze.
CIRCLE_THROW|CIRCLE THROW|FIGHTING|P|60|90|10|HIT|0|0|SEL|VITAL_THROW|Throws the foe in a circle.
PRECIPICE_BLADES|PRECIPC BLDS|GROUND|P|120|85|10|HIT|0|0|SEL|EARTHQUAKE|Fierce blades of stone rise up.
THOUSAND_ARROWS|1000 ARROWS|GROUND|P|90|100|10|HIT|0|0|SEL|BONEMERANG|Arrows rain down from the earth.
THOUSAND_WAVES|1000 WAVES|GROUND|P|90|100|10|HIT|0|0|SEL|MUD_SHOT|Waves of earth crash into the foe.
LANDS_WRATH|LAND'S WRATH|GROUND|P|90|100|10|HIT|0|0|SEL|EARTHQUAKE|The land's anger strikes the foe.
MIGHTY_CLEAVE|MIGHTY CLEVE|ROCK|P|95|100|5|HIT|0|0|SEL|ROCK_SLIDE|Cleaves the foe with a rocky crest.
SHELL_SIDE_ARM|SHELLSIDEARM|POISON|S|90|100|10|POISON_HIT|20|0|SEL|SLUDGE_BOMB|Hits with a toxic shell. May poison.
MALIGNANT_CHAIN|MALIGNT CHAN|POISON|S|100|100|5|POISON_HIT|50|0|SEL|SLUDGE_BOMB|Toxic chains bind the foe. May poison.
NOXIOUS_TORQUE|NOXIOUS TORQ|POISON|P|100|100|10|POISON_HIT|30|0|SEL|POISON_STING|Poisonous energy charges. May poison.
MORTAL_SPIN|MORTAL SPIN|POISON|P|30|100|15|POISON_HIT|100|0|SEL|SPIKE_CANNON|Spins and poisons the foe.
BARB_BARRAGE|BARB BARRAGE|POISON|P|60|100|10|POISON_HIT|50|0|SEL|POISON_STING|Barbs fly at the foe. May poison.
STEAMROLLER|STEAMROLLER|BUG|P|65|100|20|FLINCH_HIT|30|0|SEL|ROLLOUT|Rolls over the foe. May flinch.
FELL_STINGER|FELL STINGER|BUG|P|50|100|25|HIT|0|0|SEL|PIN_MISSILE|Stings the foe with sharp venom.
MOONGEIST_BEAM|MOONGEIST BM|GHOST|S|100|100|5|HIT|0|0|SEL|SHADOW_BALL|A ghostly beam from the moon.
SPECTRAL_THIEF|SPCTRL THIEF|GHOST|P|90|100|10|HIT|0|0|SEL|SHADOW_PUNCH|A spectral strike from the dark.
BITTER_MALICE|BITTR MALICE|GHOST|S|75|100|10|ATTACK_DOWN_HIT|100|0|SEL|SHADOW_BALL|A chill of malice. Lowers the foe's ATTACK.
RAGE_FIST|RAGE FIST|GHOST|P|50|100|10|HIT|0|0|SEL|SHADOW_PUNCH|A fist fueled by rage.
LAST_RESPECTS|LAST RESPECT|GHOST|P|50|100|10|HIT|0|0|SEL|SHADOW_PUNCH|Spirits strike on behalf of the fallen.
STEEL_BEAM|STEEL BEAM|STEEL|S|140|95|5|DOUBLE_EDGE|0|0|SEL|HYPER_BEAM|A steel beam. The user takes recoil.
SUNSTEEL_STRIKE|SUNSTEEL STK|STEEL|P|100|100|5|HIT|0|0|SEL|IRON_TAIL|Charges as a meteor of steel.
SMART_STRIKE|SMART STRIKE|STEEL|P|70|100|10|ALWAYS_HIT|0|0|SEL|IRON_TAIL|A sharp horn that never misses.
ANCHOR_SHOT|ANCHOR SHOT|STEEL|P|80|100|5|HIT|0|0|SEL|IRON_TAIL|Strikes with a chain and anchor.
SPIN_OUT|SPIN OUT|STEEL|P|100|100|5|HAMMER_ARM|0|0|SEL|ROLLOUT|Spins hard. Lowers the user's SPEED.
HARD_PRESS|HARD PRESS|STEEL|P|80|100|5|HIT|0|0|SEL|IRON_TAIL|Crushes the foe with a steel claw.
TACHYON_CUTTER|TACHYON CUT|STEEL|S|50|100|10|DOUBLE_HIT|0|0|SEL|SLASH|Fires blades of light twice.
ICE_HAMMER|ICE HAMMER|ICE|P|100|90|10|HAMMER_ARM|0|0|SEL|ICE_PUNCH|A frozen fist. Lowers the user's SPEED.
GLACIAL_LANCE|GLACIAL LNCE|ICE|P|120|100|5|HIT|0|0|SEL|ICICLE_SPEAR|Hurls a huge icicle lance.
FREEZING_GLARE|FREEZE GLARE|PSYCHIC|S|90|100|10|FREEZE_HIT|10|0|SEL|CONFUSION|Psychic power glares. May freeze.
EXPANDING_FORCE|EXPAND FORCE|PSYCHIC|S|80|100|10|HIT|0|0|SEL|PSYCHIC|Psychic power spreads out.
PSYBLADE|PSYBLADE|PSYCHIC|P|80|100|15|HIT|0|0|SEL|SLASH|Slashes with a psychic blade.
PSYCHIC_NOISE|PSYCH NOISE|PSYCHIC|S|75|100|10|HIT|0|0|SEL|SUPERSONIC|Unpleasant waves hurt the foe.
EERIE_SPELL|EERIE SPELL|PSYCHIC|S|80|100|5|HIT|0|0|SEL|PSYCHIC|An eerie spell strikes the foe.
HYPERSPACE_HOLE|SPACE HOLE|PSYCHIC|S|80|100|5|ALWAYS_HIT|0|0|SEL|PSYCHIC|Attacks from a hole in space.
BRUTAL_SWING|BRUTAL SWING|DARK|P|60|100|20|HIT|0|0|SEL|SLASH|Swings wildly at everything.
DARKEST_LARIAT|DARK LARIAT|DARK|P|85|100|10|HIT|0|0|SEL|DYNAMIC_PUNCH|Swings both arms and hits the foe.
LASH_OUT|LASH OUT|DARK|P|75|100|5|HIT|0|0|SEL|FAINT_ATTACK|Lashes out in frustration.
THROAT_CHOP|THROAT CHOP|DARK|P|80|100|15|HIT|0|0|SEL|KARATE_CHOP|A chop to the throat.
CORE_ENFORCER|CORE ENFORCR|DRAGON|S|100|100|10|HIT|0|0|SEL|DRAGON_BREATH|Shoots a ray from the dragon's core.
DRAGON_ENERGY|DRAGON ENRGY|DRAGON|S|150|100|5|HIT|0|0|SEL|DRAGON_BREATH|Converts life into a huge blast.
FICKLE_BEAM|FICKLE BEAM|DRAGON|S|80|100|5|HIT|0|0|SEL|DRAGON_BREATH|Shoots a beam of light.
FUSION_FLARE|FUSION FLARE|FIRE|S|100|100|5|HIT|0|0|SEL|FIRE_BLAST|A giant fiery flame.
MAGMA_STORM|MAGMA STORM|FIRE|S|100|75|5|TRAP|0|0|SEL|FIRE_SPIN|Traps the foe in a vortex of magma.
ARMOR_CANNON|ARMOR CANNON|FIRE|S|120|100|5|CLOSE_COMBAT|0|0|SEL|FIRE_BLAST|Shoots flames. Lowers the user's defenses.
BLAZING_TORQUE|BLAZING TORQ|FIRE|P|80|100|10|BURN_HIT|30|0|SEL|BLAZE_KICK|Fire energy shoots out. May burn.
BURNING_JEALOUSY|BURNING JEAL|FIRE|S|70|100|5|BURN_HIT|30|0|SEL|FLAMETHROWER|Jealous flames. May burn the foe.
TEMPER_FLARE|TEMPER FLARE|FIRE|P|75|100|10|HIT|0|0|SEL|BLAZE_KICK|Throws a fit with flames.
HYDRO_STEAM|HYDRO STEAM|WATER|S|80|100|15|HIT|0|0|SEL|WATER_PULSE|Blasts boiling water at the foe.
AQUA_CUTTER|AQUA CUTTER|WATER|P|70|100|20|HIGH_CRITICAL|0|0|SEL|WATER_PULSE|A jet of water that often crits.
TROP_KICK|TROP KICK|GRASS|P|70|100|15|ATTACK_DOWN_HIT|100|0|SEL|MEGA_KICK|A tropical kick. Lowers the foe's ATTACK.
SYRUP_BOMB|SYRUP BOMB|GRASS|S|60|85|10|SPEED_DOWN_HIT|100|0|SEL|SLUDGE_BOMB|Sticky syrup slows the foe.
IVY_CUDGEL|IVY CUDGEL|GRASS|P|100|100|10|HIGH_CRITICAL|0|0|SEL|SLAM|Strikes with an ivy-wrapped club.
MATCHA_GOTCHA|MATCHA GOTCH|GRASS|S|80|90|15|BURN_HIT|20|0|SEL|GIGA_DRAIN|Fires hot tea. May burn the foe.
RISING_VOLTAGE|RISING VOLT|ELECTRIC|S|70|100|20|HIT|0|0|SEL|THUNDERBOLT|A surge of electricity.
THUNDERCLAP|THUNDERCLAP|ELECTRIC|S|70|100|5|QUICK_ATTACK|0|1|SEL|THUNDER_SHOCK|A swift clap of thunder strikes first.
ELECTRO_DRIFT|ELCTRO DRIFT|ELECTRIC|S|100|100|5|HIT|0|0|SEL|THUNDERBOLT|A futuristic bolt of electricity.
SUPERCELL_SLAM|SUPRCELL SLM|ELECTRIC|P|100|95|15|RECOIL_IF_MISS|0|0|SEL|VOLT_TACKLE|Slams with electricity. Crashes if it misses.
THUNDER_CAGE|THUNDER CAGE|ELECTRIC|S|80|90|15|TRAP|0|0|SEL|THUNDER_WAVE|Traps the foe in a cage of lightning.
LIGHT_OF_RUIN|LIGHT O RUIN|FAIRY|S|140|90|5|DOUBLE_EDGE|0|0|SEL|AURORA_BEAM|A powerful light. The user takes recoil.
MISTY_EXPLOSION|MISTY EXPLSN|FAIRY|S|100|100|5|EXPLOSION|0|0|SEL|EXPLOSION|Explodes in mist. The user faints.
ALLURING_VOICE|ALLURE VOICE|FAIRY|S|80|100|10|CONFUSE_HIT|30|0|SEL|SING|An angelic voice. May confuse the foe.
MAGICAL_TORQUE|MAGICAL TORQ|FAIRY|P|100|100|10|CONFUSE_HIT|30|0|SEL|DOUBLE_EDGE|Magical energy charges. May confuse.
SHIFT_GEAR|SHIFT GEAR|STEEL|T|0|0|10|SPEED_UP_2|0|0|USER|AGILITY|Shifts gears. Sharply raises SPEED.
'''.strip().split('\n')
moves = [l.split('|') for l in M]
if 'MOVE_RETALIATE' in R('include/constants/moves.h'):
    print('deja applique'); sys.exit(0)
assert len(set(m[0] for m in moves)) == len(moves)
assert all(len(m[1]) <= 12 for m in moves), [m[1] for m in moves if len(m[1]) > 12]
for m in moves: assert len(textwrap.wrap(m[12], 18)) <= 4, m[0]
an0 = R('data/battle_anim_scripts.s')
for m in moves: assert re.search(r'^Move_%s:' % m[11], an0, re.M), m[11]
assert all(len(m) == 13 for m in moves), [m for m in moves if len(m) != 13]
LAST = 535
assert '#define MOVE_BABY_DOLL_EYES 535\n' in R('include/constants/moves.h')
existing = set(re.findall(r'#define MOVE_(\w+) ', R('include/constants/moves.h')))
assert not [m[0] for m in moves if m[0] in existing], [m[0] for m in moves if m[0] in existing]
h = R('include/constants/moves.h')
defs = ''.join('#define MOVE_%s %d\n' % (m[0], LAST + 1 + i) for i, m in enumerate(moves))
h = h.replace('#define MOVE_BABY_DOLL_EYES 535\n', '#define MOVE_BABY_DOLL_EYES 535\n' + defs)
h = h.replace('#define MOVES_COUNT %d' % (LAST + 1), '#define MOVES_COUNT %d' % (LAST + 1 + len(moves)))
W('include/constants/moves.h', h)
bm = R('src/data/battle_moves.h')
tgt = {'SEL': 'MOVE_TARGET_SELECTED', 'USER': 'MOVE_TARGET_USER', 'FIELD': 'MOVE_TARGET_OPPONENTS_FIELD'}
NOCONTACT = set()
out = ''
for c, name, ty, cat, pw, acc, pp, eff, sec, pri, tg, anim, desc in moves:
    fl = []
    if tg == 'FIELD': fl = []
    elif cat == 'T':
        fl = ['FLAG_SNATCH_AFFECTED'] if tg == 'USER' else ['FLAG_PROTECT_AFFECTED', 'FLAG_MAGIC_COAT_AFFECTED', 'FLAG_MIRROR_MOVE_AFFECTED']
    else:
        if cat == 'P' and c not in ('MAGNET_BOMB', 'ASTRAL_BARRAGE', 'LEAFAGE', 'SCALE_SHOT', 'DRAGON_DARTS', 'ACCELEROCK', 'SMACK_DOWN', 'DIAMOND_STORM', 'BARB_BARRAGE', 'PRECIPICE_BLADES', 'THOUSAND_ARROWS', 'THOUSAND_WAVES', 'LANDS_WRATH', 'LAST_RESPECTS'):
            fl.append('FLAG_MAKES_CONTACT')
        fl += ['FLAG_PROTECT_AFFECTED', 'FLAG_MIRROR_MOVE_AFFECTED', 'FLAG_KINGS_ROCK_AFFECTED']
        if (ty in PHYS_TYPES) != (cat == 'P'): fl.append('FLAG_FORCE_PHYSICAL' if cat == 'P' else 'FLAG_FORCE_SPECIAL')
    out += '''
    [MOVE_%s] =
    {
        .effect = EFFECT_%s,
        .power = %s,
        .type = TYPE_%s,
        .accuracy = %s,
        .pp = %s,
        .secondaryEffectChance = %s,
        .target = %s,
        .priority = %s,
        .flags = %s,
    },
''' % (c, eff, pw, ty, acc, pp, sec, tgt[tg], pri, ' | '.join(fl) if fl else '0')
bm = bm.rstrip()[:-2].rstrip() + '\n' + out + '};\n'
W('src/data/battle_moves.h', bm)
mn = R('src/data/text/move_names.h')
assert all(len(m[1]) <= 12 for m in moves), [m[1] for m in moves if len(m[1]) > 12]
assert '_("BABYDOLL EYE")\n' in mn
mn = mn.replace('_("BABYDOLL EYE")\n', '_("BABYDOLL EYE"),\n')
body = ''.join('    [MOVE_%s]%s = _("%s"),\n' % (m[0], ' ' * max(1, 22 - len(m[0])), m[1]) for m in moves)
mn = mn.rstrip()[:-2].rstrip() + '\n' + body.rstrip(',\n') + '\n};\n'
W('src/data/text/move_names.h', mn)
md = R('src/move_descriptions.c')
strs = ptrs = ''
for m in moves:
    lines = textwrap.wrap(m[12], 18)
    assert len(lines) <= 4, (m[0], lines)
    ident = ''.join(w.capitalize() for w in m[0].split('_'))
    strs += 'const u8 gMoveDescription_%s[] = _("%s");\n' % (ident, '\\n'.join(lines))
    ptrs += '    [MOVE_%s - 1] = gMoveDescription_%s,\n' % (m[0], ident)
md = md.replace('\nconst u8 *const gMoveDescriptionPointers[', strs + '\nconst u8 *const gMoveDescriptionPointers[', 1)
k = '    [MOVE_BABY_DOLL_EYES - 1] = gMoveDescription_BabyDollEyes,\n'
md = md.replace(k, k + ptrs, 1)
W('src/move_descriptions.c', md)
an = R('data/battle_anim_scripts.s')
for m in moves:
    assert re.search(r'^Move_%s:' % m[11], an, re.M), m[11]
al = ''.join('\t.4byte Move_%s\n' % m[11] for m in moves)
an = an.replace('\t.4byte Move_COUNT @', al + '\t.4byte Move_COUNT @', 1)
W('data/battle_anim_scripts.s', an)
print(len(moves), 'attaques ajoutees')
