#!/usr/bin/env python3
"""Ajoute ~70 attaques (Gen 4+) aux types sous-dotes et les distribue dans les learnsets.
Usage : python3 docs/topaze/add_moves.py <depot>. Idempotent (ne fait rien si les attaques existent deja)."""
import re, sys, zlib, textwrap
repo = sys.argv[1]
R = lambda p: open(repo + '/' + p).read()
def W(p, s): open(repo + '/' + p, 'w').write(s)
PHYS_TYPES = {'NORMAL','FIGHTING','FLYING','POISON','GROUND','ROCK','BUG','GHOST','STEEL'}
# CONST, NOM, TYPE, categorie(P/S/T), puissance, precision, PP, effet, % secondaire, priorite, cible, anim, description
M = '''
MOONBLAST|MOONBLAST|FAIRY|S|95|100|15|SPECIAL_ATTACK_DOWN_HIT|30|0|SEL|MIST_BALL|Draws power from the moon to strike. May lower SP. ATK.
DAZZLING_GLEAM|DAZZLNGLEAM|FAIRY|S|80|100|10|HIT|0|0|SEL|SIGNAL_BEAM|A burst of dazzling light strikes the foe.
PLAY_ROUGH|PLAY ROUGH|FAIRY|P|90|90|10|ATTACK_DOWN_HIT|10|0|SEL|HEADBUTT|Plays rough with the foe. May lower ATTACK.
DRAINING_KISS|DRAIN KISS|FAIRY|S|50|100|10|ABSORB|0|0|SEL|MEGA_DRAIN|A kiss that drains HP from the foe.
FAIRY_WIND|FAIRY WIND|FAIRY|S|40|100|30|HIT|0|0|SEL|GUST|Stirs up a fairy wind to strike the foe.
DISARMING_VOICE|DISARM VOICE|FAIRY|S|40|100|15|ALWAYS_HIT|0|0|SEL|HYPER_VOICE|A charming cry that never misses.
SPIRIT_BREAK|SPIRIT BREAK|FAIRY|P|75|100|15|SPECIAL_ATTACK_DOWN_HIT|100|0|SEL|CRUNCH|Crushes the foe's spirit. Lowers SP. ATK.
STEAM_BLAST|STEAM BLAST|FAIRY|S|90|95|10|CONFUSE_HIT|20|0|SEL|PSYBEAM|Scalding steam that may confuse the foe.
FLARE_BLITZ|FLARE BLITZ|FIRE|P|120|100|15|DOUBLE_EDGE|0|0|SEL|SACRED_FIRE|A fiery charge. The user takes recoil damage.
FIRE_FANG|FIRE FANG|FIRE|P|65|95|15|BURN_HIT|10|0|SEL|FLAME_WHEEL|Bites with flame-cloaked fangs. May burn.
LAVA_PLUME|LAVA PLUME|FIRE|S|80|100|15|BURN_HIT|30|0|SEL|FLAMETHROWER|Scarlet flames torch the foe. May burn.
INFERNO|INFERNO|FIRE|S|100|50|5|BURN_HIT|100|0|SEL|FIRE_BLAST|Engulfs the foe in intense fire. Always burns.
FLAME_CHARGE|FLAME CHARGE|FIRE|P|50|100|20|HIT|0|0|SEL|FLAME_WHEEL|Rams the foe wrapped in flames.
MYSTICAL_FIRE|MYSTIC FIRE|FIRE|S|75|100|10|SPECIAL_ATTACK_DOWN_HIT|100|0|SEL|EMBER|Strange fire that lowers the foe's SP. ATK.
SEARING_SHOT|SEARING SHOT|FIRE|S|100|100|5|BURN_HIT|30|0|SEL|HEAT_WAVE|Scorches the foe with a fiery shot. May burn.
SCALD|SCALD|WATER|S|80|100|15|BURN_HIT|30|0|SEL|WATER_PULSE|Shoots boiling water at the foe. May burn.
AQUA_JET|AQUA JET|WATER|P|40|100|20|QUICK_ATTACK|0|1|SEL|WATER_GUN|Rushes the foe at the speed of water. Always first.
AQUA_TAIL|AQUA TAIL|WATER|P|90|90|10|HIT|0|0|SEL|CRABHAMMER|Swings the tail like a rolling wave.
LIQUIDATION|LIQUIDATION|WATER|P|85|100|10|DEFENSE_DOWN_HIT|20|0|SEL|WATERFALL|Slams water at the foe. May lower DEFENSE.
ENERGY_BALL|ENERGY BALL|GRASS|S|90|100|10|SPECIAL_DEFENSE_DOWN_HIT|10|0|SEL|MAGICAL_LEAF|Draws on nature's power. May lower SP. DEF.
SEED_BOMB|SEED BOMB|GRASS|P|80|100|15|HIT|0|0|SEL|BULLET_SEED|Slams a barrage of hard seeds on the foe.
LEAF_STORM|LEAF STORM|GRASS|S|130|90|5|OVERHEAT|100|0|SEL|RAZOR_LEAF|A storm of sharp leaves. Sharply lowers SP. ATK.
WOOD_HAMMER|WOOD HAMMER|GRASS|P|120|100|15|DOUBLE_EDGE|0|0|SEL|VINE_WHIP|Slams the body into the foe. Recoil damage.
WILD_CHARGE|WILD CHARGE|ELECTRIC|P|90|100|15|DOUBLE_EDGE|0|0|SEL|VOLT_TACKLE|Shrouds the body in electricity and charges.
DISCHARGE|DISCHARGE|ELECTRIC|S|80|100|15|PARALYZE_HIT|30|0|SEL|SPARK|A flare of electricity. May paralyze.
THUNDER_FANG|THUNDER FANG|ELECTRIC|P|65|95|15|PARALYZE_HIT|10|0|SEL|THUNDER_PUNCH|Bites with electrified fangs. May paralyze.
NUZZLE|NUZZLE|ELECTRIC|P|20|100|20|PARALYZE_HIT|100|0|SEL|THUNDER_SHOCK|Nuzzles the foe with electric cheeks. Paralyzes.
ICE_FANG|ICE FANG|ICE|P|65|95|15|FREEZE_HIT|10|0|SEL|ICE_PUNCH|Bites with chilly fangs. May freeze.
FROST_BREATH|FROST BREATH|ICE|S|60|90|10|HIGH_CRITICAL|0|0|SEL|ICY_WIND|A chilling breath. Often a critical hit.
ICICLE_CRASH|ICICLE CRASH|ICE|P|85|90|10|FLINCH_HIT|30|0|SEL|ICICLE_SPEAR|Drops large icicles on the foe. May flinch.
FREEZE_DRY|FREEZE-DRY|ICE|S|70|100|20|FREEZE_HIT|10|0|SEL|POWDER_SNOW|Chills the foe to the bone. May freeze.
AURA_SPHERE|AURA SPHERE|FIGHTING|S|80|100|20|ALWAYS_HIT|0|0|SEL|SHOCK_WAVE|Fires an aura blast that never misses.
DRAIN_PUNCH|DRAIN PUNCH|FIGHTING|P|75|100|10|ABSORB|0|0|SEL|MEGA_PUNCH|A punch that drains the foe's HP.
GUNK_SHOT|GUNK SHOT|POISON|P|120|80|5|POISON_HIT|30|0|SEL|SLUDGE_BOMB|Hurls filthy garbage. May poison.
POISON_JAB|POISON JAB|POISON|P|80|100|20|POISON_HIT|30|0|SEL|POISON_TAIL|Stabs with a toxic tentacle. May poison.
CROSS_POISON|CROSS POISON|POISON|P|70|100|20|POISON_HIT|10|0|SEL|POISON_FANG|Slashes with a poisonous blade. May poison.
VENOSHOCK|VENOSHOCK|POISON|S|65|100|10|HIT|0|0|SEL|ACID|Drenches the foe in a toxic liquid.
ACID_SPRAY|ACID SPRAY|POISON|S|40|100|20|SPECIAL_DEFENSE_DOWN_HIT|100|0|SEL|SMOG|Spits acid that lowers SP. DEF.
EARTH_POWER|EARTH POWER|GROUND|S|90|100|10|SPECIAL_DEFENSE_DOWN_HIT|10|0|SEL|MAGNITUDE|The ground erupts. May lower SP. DEF.
BULLDOZE|BULLDOZE|GROUND|P|60|100|20|SPEED_DOWN_HIT|100|0|SEL|EARTHQUAKE|Stomps the ground. Lowers the foe's SPEED.
DRILL_RUN|DRILL RUN|GROUND|P|80|95|10|HIGH_CRITICAL|0|0|SEL|DRILL_PECK|Spinning drill charge. Often a critical hit.
BRAVE_BIRD|BRAVE BIRD|FLYING|P|120|100|15|DOUBLE_EDGE|0|0|SEL|SKY_ATTACK|A reckless dive. The user takes recoil damage.
ACROBATICS|ACROBATICS|FLYING|P|55|100|15|HIT|0|0|SEL|WING_ATTACK|Nimble, aerial strikes at the foe.
HURRICANE|HURRICANE|FLYING|S|110|70|10|CONFUSE_HIT|30|0|SEL|TWISTER|Whips up a fierce gale. May confuse.
AIR_SLASH|AIR SLASH|FLYING|S|75|95|15|FLINCH_HIT|30|0|SEL|AIR_CUTTER|Slashes with a blade of air. May flinch.
ROOST|ROOST|FLYING|T|0|0|10|RESTORE_HP|0|0|USER|RECOVER|The user lands and rests to restore half its HP.
ZEN_HEADBUTT|ZEN HEADBUTT|PSYCHIC|P|80|90|15|FLINCH_HIT|20|0|SEL|HEADBUTT|A headbutt with focused mind. May flinch.
BUG_BUZZ|BUG BUZZ|BUG|S|90|100|10|SPECIAL_DEFENSE_DOWN_HIT|10|0|SEL|SIGNAL_BEAM|A damaging buzz. May lower SP. DEF.
X_SCISSOR|X-SCISSOR|BUG|P|80|100|15|HIT|0|0|SEL|FURY_CUTTER|Slashes the foe with crossed claws.
U_TURN|U-TURN|BUG|P|70|100|20|HIT|0|0|SEL|LEECH_LIFE|A quick, hard strike on the foe.
LUNGE|LUNGE|BUG|P|80|100|15|ATTACK_DOWN_HIT|100|0|SEL|PIN_MISSILE|Lunges at the foe. Lowers its ATTACK.
POWER_GEM|POWER GEM|ROCK|S|80|100|20|HIT|0|0|SEL|ANCIENT_POWER|Fires a ray of glittering light.
STONE_EDGE|STONE EDGE|ROCK|P|100|80|5|HIGH_CRITICAL|0|0|SEL|ROCK_SLIDE|Stabs with sharp stones. Often a critical hit.
HEAD_SMASH|HEAD SMASH|ROCK|P|150|80|5|DOUBLE_EDGE|0|0|SEL|ROCK_BLAST|A life-risking headbutt. Heavy recoil.
ROCK_POLISH|ROCK POLISH|ROCK|T|0|0|20|SPEED_UP_2|0|0|USER|AGILITY|Polishes the body. Sharply raises SPEED.
SHADOW_CLAW|SHADOW CLAW|GHOST|P|70|100|15|HIGH_CRITICAL|0|0|SEL|SHADOW_PUNCH|Slashes with a shadowy claw. Often critical.
SHADOW_SNEAK|SHADOW SNEAK|GHOST|P|40|100|30|QUICK_ATTACK|0|1|SEL|SHADOW_PUNCH|Extends a shadow to strike first.
HEX|HEX|GHOST|S|65|100|10|HIT|0|0|SEL|LICK|A curse that torments the foe.
OMINOUS_WIND|OMINOUS WIND|GHOST|S|60|100|5|ALL_STATS_UP_HIT|10|0|SEL|SILVER_WIND|A gust of ghostly wind. May raise all stats.
DRAGON_PULSE|DRAGON PULSE|DRAGON|S|85|100|10|HIT|0|0|SEL|DRAGON_BREATH|Shock waves from the mouth strike the foe.
DRAGON_RUSH|DRAGON RUSH|DRAGON|P|100|75|10|FLINCH_HIT|20|0|SEL|DRAGON_CLAW|Charges with menace. May flinch the foe.
DRACO_METEOR|DRACO METEOR|DRAGON|S|130|90|5|OVERHEAT|100|0|SEL|OUTRAGE|Comets fall on the foe. Sharply lowers SP. ATK.
DRAGON_TAIL|DRAGON TAIL|DRAGON|P|60|90|10|HIT|0|0|SEL|IRON_TAIL|Whips the foe with a heavy dragon tail.
DARK_PULSE|DARK PULSE|DARK|S|80|100|15|FLINCH_HIT|20|0|SEL|SHADOW_BALL|Horrible aura strikes. May flinch the foe.
NIGHT_SLASH|NIGHT SLASH|DARK|P|70|100|15|HIGH_CRITICAL|0|0|SEL|SLASH|Slashes the foe. Often a critical hit.
FOUL_PLAY|FOUL PLAY|DARK|P|95|100|15|HIT|0|0|SEL|FAINT_ATTACK|Strikes with a dirty trick.
SUCKER_PUNCH|SUCKER PUNCH|DARK|P|70|100|5|QUICK_ATTACK|0|1|SEL|KNOCK_OFF|Strikes first with a sneaky punch.
FLASH_CANNON|FLASH CANNON|STEEL|S|80|100|10|SPECIAL_DEFENSE_DOWN_HIT|10|0|SEL|AURORA_BEAM|A blast of light. May lower SP. DEF.
IRON_HEAD|IRON HEAD|STEEL|P|80|100|15|FLINCH_HIT|30|0|SEL|IRON_TAIL|Slams a steel-hard head. May flinch.
BULLET_PUNCH|BULLET PUNCH|STEEL|P|40|100|30|QUICK_ATTACK|0|1|SEL|METAL_CLAW|A punch as fast as a bullet. Always first.
GYRO_BALL|GYRO BALL|STEEL|P|80|100|5|HIT|0|0|SEL|RAPID_SPIN|Tackles with a high-speed spin.
MIRROR_SHOT|MIRROR SHOT|STEEL|S|65|85|10|ACCURACY_DOWN_HIT|30|0|SEL|SIGNAL_BEAM|Flashes a mirror-bright light. May lower accuracy.
'''.strip().split('\n')
moves = [l.split('|') for l in M]
if 'MOVE_MOONBLAST' in R('include/constants/moves.h'):
    print('deja applique'); sys.exit(0)
assert len(set(m[0] for m in moves)) == len(moves)
# ---- constantes
h = R('include/constants/moves.h')
last = 354
defs = ''.join('#define MOVE_%s %d\n' % (m[0], last + 1 + i) for i, m in enumerate(moves))
h = h.replace('#define MOVE_PSYCHO_BOOST 354\n', '#define MOVE_PSYCHO_BOOST 354\n' + defs)
h = h.replace('#define MOVES_COUNT 355', '#define MOVES_COUNT %d' % (355 + len(moves)))
W('include/constants/moves.h', h)
# ---- table des attaques
bm = R('src/data/battle_moves.h')
tgt = {'SEL': 'MOVE_TARGET_SELECTED', 'USER': 'MOVE_TARGET_USER'}
out = ''
for c, name, ty, cat, pw, acc, pp, eff, sec, pri, tg, anim, desc in moves:
    pw = int(pw)
    fl = []
    if cat == 'T': fl = ['FLAG_SNATCH_AFFECTED']
    else:
        if cat == 'P': fl.append('FLAG_MAKES_CONTACT') if c not in ('GUNK_SHOT','STONE_EDGE','BULLDOZE','SEED_BOMB','DRAGON_PULSE') else None
        fl += ['FLAG_PROTECT_AFFECTED', 'FLAG_MIRROR_MOVE_AFFECTED', 'FLAG_KINGS_ROCK_AFFECTED']
        if (ty in PHYS_TYPES) != (cat == 'P'): fl.append('FLAG_FORCE_PHYSICAL' if cat == 'P' else 'FLAG_FORCE_SPECIAL')
    out += '''
    [MOVE_%s] =
    {
        .effect = EFFECT_%s,
        .power = %d,
        .type = TYPE_%s,
        .accuracy = %s,
        .pp = %s,
        .secondaryEffectChance = %s,
        .target = %s,
        .priority = %s,
        .flags = %s,
    },
''' % (c, eff, pw, ty, acc, pp, sec, tgt[tg], pri, ' | '.join(fl))
assert bm.rstrip().endswith('};')
bm = bm.rstrip()[:-2].rstrip() + '\n' + out + '};\n'
W('src/data/battle_moves.h', bm)
# ---- noms
mn = R('src/data/text/move_names.h')
mn = mn.replace('_("PSYCHO BOOST")\n', '_("PSYCHO BOOST"),\n')
body = ''.join('    [MOVE_%s]%s = _("%s"),\n' % (m[0], ' ' * max(1, 18 - len(m[0])), m[1]) for m in moves)
assert all(len(m[1]) <= 12 for m in moves), [m[1] for m in moves if len(m[1]) > 12]
mn = mn.rstrip()[:-2].rstrip() + '\n' + body.rstrip(',\n') + '\n};\n'
W('src/data/text/move_names.h', mn)
# ---- descriptions (4 lignes de 18 caracteres max)
md = R('src/move_descriptions.c')
strs = ptrs = ''
for m in moves:
    lines = textwrap.wrap(m[12], 18)
    assert len(lines) <= 4, (m[0], lines)
    ident = ''.join(w.capitalize() for w in m[0].split('_'))
    strs += 'const u8 gMoveDescription_%s[] = _("%s");\n' % (ident, '\\n'.join(lines))
    ptrs += '    [MOVE_%s - 1] = gMoveDescription_%s,\n' % (m[0], ident)
md = md.replace('\nconst u8 *const gMoveDescriptionPointers[', strs + '\nconst u8 *const gMoveDescriptionPointers[', 1)
md = md.replace('[MOVES_COUNT - 1]', '[MOVES_COUNT - 1]')
i = md.index('[MOVE_PSYCHO_BOOST  - 1] = gMoveDescription_PsychoBoost,\n') + len('[MOVE_PSYCHO_BOOST  - 1] = gMoveDescription_PsychoBoost,\n')
md = md[:i] + ptrs + md[i:]
W('src/move_descriptions.c', md)
# ---- animations (on reutilise celles d'attaques existantes)
an = R('data/battle_anim_scripts.s')
for m in moves:
    assert re.search(r'^Move_%s:' % m[11], an, re.M), m[11]
al = ''.join('\t.4byte Move_%s\n' % m[11] for m in moves)
an = an.replace('\t.4byte Move_COUNT @ cannot be reached', al + '\t.4byte Move_COUNT @ cannot be reached', 1)
W('data/battle_anim_scripts.s', an)
print(len(moves), 'attaques ajoutees')
