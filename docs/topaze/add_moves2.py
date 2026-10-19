#!/usr/bin/env python3
"""Seconde vague d'attaques Gen 4-9 (ids 427+). Usage : python3 docs/topaze/add_moves2.py <depot>. Idempotent."""
import re, sys, textwrap
repo = sys.argv[1]
R = lambda p: open(repo + '/' + p).read()
def W(p, s): open(repo + '/' + p, 'w').write(s)
PHYS_TYPES = {'NORMAL','FIGHTING','FLYING','POISON','GROUND','ROCK','BUG','GHOST','STEEL'}
# CONST|NOM|TYPE|cat(P/S/T)|puissance|precision|PP|effet|%sec|priorite|cible|anim|description
M = '''
CLOSE_COMBAT|CLOSE COMBAT|FIGHTING|P|120|100|5|CLOSE_COMBAT|0|0|SEL|DYNAMIC_PUNCH|All-out attack. Lowers the user's DEF and SP. DEF.
HAMMER_ARM|HAMMER ARM|FIGHTING|P|100|90|10|HAMMER_ARM|0|0|SEL|MEGA_PUNCH|A heavy swing. Lowers the user's SPEED.
POWER_UP_PUNCH|POWER-UP PCH|FIGHTING|P|40|100|20|ATTACK_UP_HIT|100|0|SEL|MACH_PUNCH|Each hit raises the user's ATTACK.
VACUUM_WAVE|VACUUM WAVE|FIGHTING|S|40|100|30|QUICK_ATTACK|0|1|SEL|GUST|A wave of air that always strikes first.
SACRED_SWORD|SACRED SWORD|FIGHTING|P|90|100|15|HIT|0|0|SEL|SLASH|Cuts the foe with a long blade.
STORM_THROW|STORM THROW|FIGHTING|P|60|100|10|HIGH_CRITICAL|0|0|SEL|VITAL_THROW|A throw that often lands a critical hit.
LOW_SWEEP|LOW SWEEP|FIGHTING|P|65|100|20|SPEED_DOWN_HIT|100|0|SEL|ROLLING_KICK|A low kick that lowers the foe's SPEED.
FOCUS_BLAST|FOCUS BLAST|FIGHTING|S|120|70|5|SPECIAL_DEFENSE_DOWN_HIT|10|0|SEL|SHOCK_WAVE|A blast of focus. May lower SP. DEF.
PSYCHO_CUT|PSYCHO CUT|PSYCHIC|P|70|100|20|HIGH_CRITICAL|0|0|SEL|SLASH|Slashes with psychic blades. Often critical.
HEART_STAMP|HEART STAMP|PSYCHIC|P|60|100|25|FLINCH_HIT|30|0|SEL|HEADBUTT|A sudden stamp. May flinch the foe.
PSYSTRIKE|PSYSTRIKE|PSYCHIC|S|100|100|10|HIT|0|0|SEL|PSYCHIC|A mighty wave of psychic power.
PSYCHIC_FANGS|PSYCH FANGS|PSYCHIC|P|85|100|10|HIT|0|0|SEL|BITE|Bites with psychic power.
ESPER_WING|ESPER WING|PSYCHIC|S|80|100|10|HIGH_CRITICAL|0|0|SEL|AIR_CUTTER|Slashing wings. Often a critical hit.
TWIN_BEAM|TWIN BEAM|PSYCHIC|S|40|100|10|DOUBLE_HIT|0|0|SEL|CONFUSION|Two mystical beams hit twice.
NASTY_PLOT|NASTY PLOT|DARK|T|0|0|20|SPECIAL_ATTACK_UP_2|0|0|USER|CALM_MIND|Plots wickedly. Sharply raises SP. ATK.
ASSURANCE|ASSURANCE|DARK|P|60|100|10|HIT|0|0|SEL|FAINT_ATTACK|A sneaky strike from behind.
SNARL|SNARL|DARK|S|55|95|15|SPECIAL_ATTACK_DOWN_HIT|100|0|SEL|SCARY_FACE|Snarls at the foe. Lowers SP. ATK.
FIERY_WRATH|FIERY WRATH|DARK|S|90|100|10|FLINCH_HIT|20|0|SEL|SHADOW_BALL|Dark rage strikes. May flinch the foe.
KOWTOW_CLEAVE|KOWTOW CLEAV|DARK|P|85|100|10|ALWAYS_HIT|0|0|SEL|SLASH|A treacherous cut that never misses.
WICKED_BLOW|WICKED BLOW|DARK|P|75|100|5|HIGH_CRITICAL|0|0|SEL|DYNAMIC_PUNCH|A wicked blow. Often a critical hit.
DARK_VOID|DARK VOID|DARK|T|0|80|10|SLEEP|0|0|SEL|HYPNOSIS|Drags the foe into a deep, dark sleep.
AUTOTOMIZE|AUTOTOMIZE|STEEL|T|0|0|15|SPEED_UP_2|0|0|USER|AGILITY|Sheds weight. Sharply raises SPEED.
DOUBLE_IRON_BASH|DBL IRONBASH|STEEL|P|60|100|5|DOUBLE_HIT|0|0|SEL|METAL_CLAW|Two steel punches in a row.
BEHEMOTH_BLADE|BEHEMOTH BLD|STEEL|P|100|100|5|HIT|0|0|SEL|SLASH|A giant blade cleaves the foe.
MAGNET_BOMB|MAGNET BOMB|STEEL|P|60|100|20|ALWAYS_HIT|0|0|SEL|SPIKE_CANNON|Steel bombs that never miss.
GEAR_GRIND|GEAR GRIND|STEEL|P|50|85|15|DOUBLE_HIT|0|0|SEL|METAL_CLAW|Throws steel gears twice.
SHADOW_BONE|SHADOW BONE|GHOST|P|85|100|10|DEFENSE_DOWN_HIT|20|0|SEL|BONE_CLUB|Strikes with a haunted bone. May lower DEF.
POLTERGEIST|POLTERGEIST|GHOST|P|110|90|5|HIT|0|0|SEL|SHADOW_PUNCH|Hurls haunted objects at the foe.
ASTRAL_BARRAGE|ASTRAL BRRGE|GHOST|S|120|100|5|HIT|0|0|SEL|SHADOW_BALL|A barrage of ghostly spirits.
STRUGGLE_BUG|STRUGGLE BUG|BUG|S|50|100|20|SPECIAL_ATTACK_DOWN_HIT|100|0|SEL|SIGNAL_BEAM|Resists and lowers the foe's SP. ATK.
QUIVER_DANCE|QUIVER DANCE|BUG|T|0|0|20|QUIVER_DANCE|0|0|USER|DRAGON_DANCE|A mystic dance. Raises SP. ATK, SP. DEF, SPEED.
BUG_BITE|BUG BITE|BUG|P|60|100|20|HIT|0|0|SEL|BITE|Bites the foe with sharp mandibles.
ATTACK_ORDER|ATTACK ORDER|BUG|P|90|100|15|HIGH_CRITICAL|0|0|SEL|PIN_MISSILE|Calls insects to attack. Often critical.
FIRST_IMPRESSION|1ST IMPRESSN|BUG|P|90|100|10|FAKE_OUT|0|2|SEL|FURY_CUTTER|Strongest first. Only on the first turn.
DEFEND_ORDER|DEFEND ORDER|BUG|T|0|0|10|COSMIC_POWER|0|0|USER|COSMIC_POWER|Raises the user's DEFENSE and SP. DEF.
HEAL_ORDER|HEAL ORDER|BUG|T|0|0|10|RESTORE_HP|0|0|USER|RECOVER|Restores half of the user's max HP.
POUNCE|POUNCE|BUG|P|50|100|20|SPEED_DOWN_HIT|100|0|SEL|PIN_MISSILE|Pounces and lowers the foe's SPEED.
SKITTER_SMACK|SKITTR SMACK|BUG|P|70|90|10|SPECIAL_ATTACK_DOWN_HIT|100|0|SEL|FURY_SWIPES|Smacks the foe. Lowers its SP. ATK.
SLUDGE_WAVE|SLUDGE WAVE|POISON|S|95|100|10|POISON_HIT|10|0|SEL|SLUDGE_BOMB|A wave of filth. May poison the foe.
TOXIC_SPIKES|TOXIC SPIKES|POISON|T|0|0|20|TOXIC_SPIKES|0|0|FIELD|POISON_STING|Scatters poison spikes around the foe's team.
CLEAR_SMOG|CLEAR SMOG|POISON|S|50|100|15|ALWAYS_HIT|0|0|SEL|SMOG|Hurls clouds of smog. Never misses.
COIL|COIL|POISON|T|0|0|20|COIL|0|0|USER|BULK_UP|Coils up. Raises ATTACK, DEFENSE, accuracy.
MUD_BOMB|MUD BOMB|GROUND|S|65|85|10|ACCURACY_DOWN_HIT|30|0|SEL|MUD_SLAP|Hurls mud. May lower accuracy.
SHORE_UP|SHORE UP|GROUND|T|0|0|10|RESTORE_HP|0|0|USER|RECOVER|Gathers sand to restore half the user's HP.
HIGH_HORSEPOWER|HI HORSEPWR|GROUND|P|95|95|10|HIT|0|0|SEL|STOMP|Hits the foe with a full-body slam.
STOMPING_TANTRUM|STOMP TANTRM|GROUND|P|75|100|10|HIT|0|0|SEL|STOMP|Stomps in a fit of anger.
SCORCHING_SANDS|SCORCH SANDS|GROUND|S|70|100|10|BURN_HIT|30|0|SEL|SAND_TOMB|Throws scorching sand. May burn the foe.
HEADLONG_RUSH|HEADLONG RSH|GROUND|P|120|100|5|CLOSE_COMBAT|0|0|SEL|TAKE_DOWN|A full-body charge. Lowers DEF and SP. DEF.
STEALTH_ROCK|STEALTH ROCK|ROCK|T|0|0|20|STEALTH_ROCK|0|0|FIELD|ROCK_THROW|Pointed stones hurt foes that switch in.
ROCK_WRECKER|ROCK WRECKER|ROCK|P|150|90|5|RECHARGE|0|0|SEL|ROCK_SLIDE|Launches a huge boulder. The user must rest.
ACCELEROCK|ACCELEROCK|ROCK|P|40|100|20|QUICK_ATTACK|0|1|SEL|ROCK_THROW|Charges at high speed. Always first.
SMACK_DOWN|SMACK DOWN|ROCK|P|50|100|15|HIT|0|0|SEL|ROCK_THROW|Throws a rock to smack the foe down.
DIAMOND_STORM|DIAMOND STRM|ROCK|P|100|95|5|DEFENSE_UP_HIT|50|0|SEL|ANCIENT_POWER|A diamond storm. May raise the user's DEF.
DRAGON_HAMMER|DRAGON HMMR|DRAGON|P|90|100|15|HIT|0|0|SEL|DRAGON_CLAW|Swings the body like a heavy hammer.
SCALE_SHOT|SCALE SHOT|DRAGON|P|25|90|20|MULTI_HIT|0|0|SEL|SPIKE_CANNON|Fires scales 2 to 5 times in a row.
DRAGON_DARTS|DRAGON DARTS|DRAGON|P|50|100|10|DOUBLE_HIT|0|0|SEL|DRAGON_BREATH|Fires two fierce dragon darts.
DUAL_CHOP|DUAL CHOP|DRAGON|P|40|90|15|DOUBLE_HIT|0|0|SEL|KARATE_CHOP|Chops twice with the arms.
ROAR_OF_TIME|ROAR OF TIME|DRAGON|S|150|90|5|RECHARGE|0|0|SEL|HYPER_BEAM|Distorts time. The user must rest next turn.
SPACIAL_REND|SPACIAL REND|DRAGON|S|100|95|5|HIGH_CRITICAL|0|0|SEL|AEROBLAST|Tears space. Often a critical hit.
CLANGING_SCALES|CLANG SCALES|DRAGON|S|110|100|5|HIT|0|0|SEL|SCREECH|Rubs scales to make a deafening clang.
FIERY_DANCE|FIERY DANCE|FIRE|S|80|100|10|SP_ATK_UP_HIT|50|0|SEL|PETAL_DANCE|Dances in flames. May raise SP. ATK.
BLUE_FLARE|BLUE FLARE|FIRE|S|130|85|5|BURN_HIT|20|0|SEL|FIRE_BLAST|A beautiful blue flame. May burn.
V_CREATE|V-CREATE|FIRE|P|180|95|5|CLOSE_COMBAT|0|0|SEL|SACRED_FIRE|Fiery brow strike. Lowers DEF and SP. DEF.
TORCH_SONG|TORCH SONG|FIRE|S|80|100|10|SP_ATK_UP_HIT|100|0|SEL|FLAMETHROWER|Scorches the foe and raises SP. ATK.
FLAME_BURST|FLAME BURST|FIRE|S|70|100|15|HIT|0|0|SEL|FIRE_SPIN|A burst of flame hits the foe.
PYRO_BALL|PYRO BALL|FIRE|P|120|90|5|BURN_HIT|10|0|SEL|FIRE_BLAST|Kicks a flaming ball. May burn the foe.
SPARKLING_ARIA|SPRKLNG ARIA|WATER|S|90|100|10|HIT|0|0|SEL|BUBBLE_BEAM|Sings a bubbly aria at the foe.
FLIP_TURN|FLIP TURN|WATER|P|60|100|20|U_TURN|0|0|SEL|WATERFALL|Strikes, then swaps with a party Pokemon.
RAZOR_SHELL|RAZOR SHELL|WATER|P|75|95|10|DEFENSE_DOWN_HIT|50|0|SEL|SLASH|Cuts with sharp shells. May lower DEF.
SHELL_SMASH|SHELL SMASH|NORMAL|T|0|0|15|SHELL_SMASH|0|0|USER|BULK_UP|Breaks the shell. Boosts offense, lowers defense.
WAVE_CRASH|WAVE CRASH|WATER|P|120|100|10|DOUBLE_EDGE|0|0|SEL|SURF|Crashes like a wave. The user takes recoil.
ORIGIN_PULSE|ORIGIN PULSE|WATER|S|110|85|10|HIT|0|0|SEL|WATER_PULSE|Blue beams of light pierce the foe.
JET_PUNCH|JET PUNCH|WATER|P|60|100|15|QUICK_ATTACK|0|1|SEL|WATER_GUN|A punch at jet speed. Always strikes first.
STEAM_ERUPTION|STEAM ERUPTN|WATER|S|110|95|5|BURN_HIT|30|0|SEL|HEAT_WAVE|Boiling steam erupts. May burn the foe.
POWER_WHIP|POWER WHIP|GRASS|P|120|85|10|HIT|0|0|SEL|VINE_WHIP|Violently whips the foe with vines.
HORN_LEECH|HORN LEECH|GRASS|P|75|100|10|ABSORB|0|0|SEL|MEGA_DRAIN|Drains the foe's energy with a horn.
SEED_FLARE|SEED FLARE|GRASS|S|120|85|5|SPECIAL_DEFENSE_DOWN_HIT|40|0|SEL|SOLAR_BEAM|A shockwave of seeds. May lower SP. DEF.
PETAL_BLIZZARD|PETAL BLZRD|GRASS|P|90|100|15|HIT|0|0|SEL|PETAL_DANCE|Stirs up a storm of petals.
GRASSY_GLIDE|GRASSY GLIDE|GRASS|P|55|100|20|QUICK_ATTACK|0|1|SEL|VINE_WHIP|Glides on the grass. Always strikes first.
LEAFAGE|LEAFAGE|GRASS|P|40|100|40|HIT|0|0|SEL|MAGICAL_LEAF|Pelts the foe with leaves.
DRUM_BEATING|DRUM BEATING|GRASS|P|80|100|10|SPEED_DOWN_HIT|100|0|SEL|BONE_RUSH|Beats a root drum. Lowers the foe's SPEED.
LEAF_TORNADO|LEAF TORNADO|GRASS|S|65|90|10|ACCURACY_DOWN_HIT|50|0|SEL|TWISTER|A leaf whirlwind. May lower accuracy.
COTTON_GUARD|COTTON GUARD|GRASS|T|0|0|10|DEFENSE_UP_2|0|0|USER|COSMIC_POWER|Wraps in cotton. Sharply raises DEFENSE.
VOLT_SWITCH|VOLT SWITCH|ELECTRIC|S|70|100|20|U_TURN|0|0|SEL|SPARK|Strikes, then swaps with a party Pokemon.
ZING_ZAP|ZING ZAP|ELECTRIC|P|80|100|10|FLINCH_HIT|30|0|SEL|SPARK|A jolt of electricity. May flinch the foe.
PARABOLIC_CHARGE|PARABOLIC CH|ELECTRIC|S|65|100|20|ABSORB|0|0|SEL|THUNDER_SHOCK|Drains the foe's HP with electricity.
ELECTROWEB|ELECTROWEB|ELECTRIC|S|55|95|15|SPEED_DOWN_HIT|100|0|SEL|THUNDER_WAVE|A web of electricity that slows the foe.
PLASMA_FISTS|PLASMA FISTS|ELECTRIC|P|100|100|15|HIT|0|0|SEL|THUNDER_PUNCH|Hits with electrically charged fists.
BOLT_STRIKE|BOLT STRIKE|ELECTRIC|P|130|85|5|PARALYZE_HIT|20|0|SEL|VOLT_TACKLE|Charges with lightning. May paralyze.
FUSION_BOLT|FUSION BOLT|ELECTRIC|P|100|100|5|HIT|0|0|SEL|THUNDERBOLT|Throws a bolt of electricity at the foe.
CHARGE_BEAM|CHARGE BEAM|ELECTRIC|S|50|90|10|SP_ATK_UP_HIT|70|0|SEL|THUNDERBOLT|A beam of electricity. May raise SP. ATK.
EERIE_IMPULSE|EERIE IMPLSE|ELECTRIC|T|0|100|15|SPECIAL_ATTACK_DOWN_2|0|0|SEL|SUPERSONIC|Sharply lowers the foe's SP. ATK.
ICE_SHARD|ICE SHARD|ICE|P|40|100|30|QUICK_ATTACK|0|1|SEL|ICICLE_SPEAR|Hurls ice shards. Always strikes first.
AVALANCHE|AVALANCHE|ICE|P|60|100|10|HIT|0|0|SEL|ICE_BALL|Unleashes an icy avalanche.
GLACIATE|GLACIATE|ICE|S|65|95|10|SPEED_DOWN_HIT|100|0|SEL|BLIZZARD|Freezing wind that lowers the foe's SPEED.
FREEZE_SHOCK|FREEZE SHOCK|ICE|P|100|90|5|PARALYZE_HIT|30|0|SEL|ICE_PUNCH|Ice-charged electricity. May paralyze.
ICE_BURN|ICE BURN|ICE|S|140|90|5|BURN_HIT|30|0|SEL|BLIZZARD|A freezing blast of flames. May burn.
DRAGON_ASCENT|DRGN ASCENT|FLYING|P|120|100|5|CLOSE_COMBAT|0|0|SEL|SKY_ATTACK|Soars and strikes. Lowers DEF and SP. DEF.
OBLIVION_WING|OBLIVION WNG|FLYING|S|80|100|10|ABSORB|0|0|SEL|STEEL_WING|Wings drain the foe's HP.
PLUCK|PLUCK|FLYING|P|60|100|20|HIT|0|0|SEL|PECK|Pecks the foe sharply.
DUAL_WINGBEAT|DUAL WINGBT|FLYING|P|40|90|10|DOUBLE_HIT|0|0|SEL|WING_ATTACK|Beats the foe with wings twice.
BLEAKWIND_STORM|BLEAKWIND ST|FLYING|S|100|80|10|SPEED_DOWN_HIT|30|0|SEL|TWISTER|A freezing gale. May lower SPEED.
CHATTER|CHATTER|FLYING|S|65|100|20|CONFUSE_HIT|100|0|SEL|SUPERSONIC|A noisy chatter that confuses the foe.
GIGA_IMPACT|GIGA IMPACT|NORMAL|P|150|90|5|RECHARGE|0|0|SEL|DOUBLE_EDGE|Charges with all power. The user must rest.
DOUBLE_HIT|DOUBLE HIT|NORMAL|P|35|90|10|DOUBLE_HIT|0|0|SEL|DOUBLE_SLAP|Slams the foe with a tail twice.
BOOMBURST|BOOMBURST|NORMAL|S|140|100|10|HIT|0|0|SEL|HYPER_VOICE|A destructive sound wave.
WORK_UP|WORK UP|NORMAL|T|0|0|30|WORK_UP|0|0|USER|BULK_UP|Rouses itself. Raises ATTACK and SP. ATK.
HONE_CLAWS|HONE CLAWS|DARK|T|0|0|15|HONE_CLAWS|0|0|USER|SHARPEN|Sharpens claws. Raises ATTACK and accuracy.
BABY_DOLL_EYES|BABYDOLL EYE|FAIRY|T|0|100|30|ATTACK_DOWN|0|1|SEL|CHARM|Lowers the foe's ATTACK. Always first.
'''.strip().split('\n')
moves = [l.split('|') for l in M]
if 'MOVE_CLOSE_COMBAT' in R('include/constants/moves.h'):
    print('deja applique'); sys.exit(0)
assert len(set(m[0] for m in moves)) == len(moves)
assert all(len(m[1]) <= 12 for m in moves), [m[1] for m in moves if len(m[1]) > 12]
for m in moves: assert len(textwrap.wrap(m[12], 18)) <= 4, m[0]
an0 = R('data/battle_anim_scripts.s')
for m in moves: assert re.search(r'^Move_%s:' % m[11], an0, re.M), m[11]
assert all(len(m) == 13 for m in moves), [m for m in moves if len(m) != 13]
LAST = 426
h = R('include/constants/moves.h')
defs = ''.join('#define MOVE_%s %d\n' % (m[0], LAST + 1 + i) for i, m in enumerate(moves))
h = h.replace('#define MOVE_MIRROR_SHOT 426\n', '#define MOVE_MIRROR_SHOT 426\n' + defs)
h = h.replace('#define MOVES_COUNT %d' % (LAST + 1), '#define MOVES_COUNT %d' % (LAST + 1 + len(moves)))
W('include/constants/moves.h', h)
bm = R('src/data/battle_moves.h')
tgt = {'SEL': 'MOVE_TARGET_SELECTED', 'USER': 'MOVE_TARGET_USER', 'FIELD': 'MOVE_TARGET_OPPONENTS_FIELD'}
NOCONTACT = {'POWER_WHIP'}
out = ''
for c, name, ty, cat, pw, acc, pp, eff, sec, pri, tg, anim, desc in moves:
    fl = []
    if tg == 'FIELD': fl = []
    elif cat == 'T':
        fl = ['FLAG_SNATCH_AFFECTED'] if tg == 'USER' else ['FLAG_PROTECT_AFFECTED', 'FLAG_MAGIC_COAT_AFFECTED', 'FLAG_MIRROR_MOVE_AFFECTED']
    else:
        if cat == 'P' and c not in ('MAGNET_BOMB', 'ASTRAL_BARRAGE', 'LEAFAGE', 'SCALE_SHOT', 'DRAGON_DARTS', 'ACCELEROCK', 'SMACK_DOWN', 'DIAMOND_STORM', 'SACRED_SWORD'.replace('SACRED_SWORD', 'X')):
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
# Demi-tour existant : vrai effet de changement de Pokemon
bm = re.sub(r'(\[MOVE_U_TURN\] =\s*\{\s*\.effect = )EFFECT_HIT', r'\1EFFECT_U_TURN', bm)
W('src/data/battle_moves.h', bm)
mn = R('src/data/text/move_names.h')
assert all(len(m[1]) <= 12 for m in moves), [m[1] for m in moves if len(m[1]) > 12]
mn = mn.replace('_("MIRROR SHOT")\n', '_("MIRROR SHOT"),\n')
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
k = '    [MOVE_MIRROR_SHOT - 1] = gMoveDescription_MirrorShot,\n'
md = md.replace(k, k + ptrs, 1)
W('src/move_descriptions.c', md)
an = R('data/battle_anim_scripts.s')
for m in moves:
    assert re.search(r'^Move_%s:' % m[11], an, re.M), m[11]
al = ''.join('\t.4byte Move_%s\n' % m[11] for m in moves)
an = an.replace('\t.4byte Move_COUNT @', al + '\t.4byte Move_COUNT @', 1)
W('data/battle_anim_scripts.s', an)
print(len(moves), 'attaques ajoutees')
