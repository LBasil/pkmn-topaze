#!/usr/bin/env python3
"""Nouveaux effets d'attaque (Gen 4+) : Danse Papillon, Coquille, Bobine, Cran, Aiguisage, Close Combat, Marto-Poing,
Demi-tour, Piege de Roc, Pics Toxiques, Rayon Charge. Usage : python3 docs/topaze/add_effects2.py <depot>. Idempotent."""
import sys, re
repo = sys.argv[1]
R = lambda p: open(repo + '/' + p).read()
def W(p, s): open(repo + '/' + p, 'w').write(s)
if 'EFFECT_QUIVER_DANCE' in R('include/constants/battle_move_effects.h'):
    print('effets deja appliques'); sys.exit(0)
NEW = ['QUIVER_DANCE', 'SHELL_SMASH', 'COIL', 'WORK_UP', 'HONE_CLAWS', 'CLOSE_COMBAT', 'HAMMER_ARM', 'U_TURN',
       'STEALTH_ROCK', 'TOXIC_SPIKES', 'SP_ATK_UP_HIT']
h = R('include/constants/battle_move_effects.h')
defs = ''.join('#define EFFECT_%s %d\n' % (n, 214 + i) for i, n in enumerate(NEW))
h = h.replace('#define EFFECT_CAMOUFLAGE 213\n', '#define EFFECT_CAMOUFLAGE 213\n' + defs)
W('include/constants/battle_move_effects.h', h)
# MOVE_EFFECT_DEF_SPDEF_DOWN reutilise l'emplacement inutilise 55
b = R('include/constants/battle.h')
b = b.replace('#define MOVE_EFFECT_NOTHING_37          55', '#define MOVE_EFFECT_DEF_SPDEF_DOWN      55 // Topaze (Close Combat)')
W('include/constants/battle.h', b)

# ---- table des effets + scripts
s = R('data/battle_scripts_1.s')
tab = ''.join('\t.4byte BattleScript_Effect%-27s @ EFFECT_%s\n' % (''.join(w.capitalize() for w in n.split('_')), n) for n in NEW)
s = s.replace('\t.4byte BattleScript_EffectCamouflage             @ EFFECT_CAMOUFLAGE\n', '\t.4byte BattleScript_EffectCamouflage             @ EFFECT_CAMOUFLAGE\n' + tab)

def cap(n): return ''.join(w.capitalize() for w in n.split('_'))
def multistat(name, changes):
    """changes : liste (STAT, delta). delta > 0 hausse, < 0 baisse. Tous sur l'utilisateur."""
    label = 'BattleScript_Effect' + name
    out = '%s::\n\tattackcanceler\n\tattackstring\n\tppreduce\n' % label
    ups = [c for c in changes if c[1] > 0]
    for st, d in ups[:-1]:
        out += '\tjumpifstat BS_ATTACKER, CMP_LESS_THAN, STAT_%s, MAX_STAT_STAGE, %sDoMoveAnim\n' % (st, label)
    st, d = ups[-1]
    out += '\tjumpifstat BS_ATTACKER, CMP_EQUAL, STAT_%s, MAX_STAT_STAGE, BattleScript_CantRaiseMultipleStats\n' % st
    out += '%sDoMoveAnim::\n\tattackanimation\n\twaitanimation\n\tsetbyte sSTAT_ANIM_PLAYED, FALSE\n' % label
    bit = {'ATK': 'BIT_ATK', 'DEF': 'BIT_DEF', 'SPEED': 'BIT_SPEED', 'SPATK': 'BIT_SPATK', 'SPDEF': 'BIT_SPDEF', 'ACC': 'BIT_ACC'}
    bits = ' | '.join(bit[c[0]] for c in ups)
    two = any(abs(c[1]) == 2 for c in ups)
    fl = ['STAT_CHANGE_BY_TWO'] if two else []
    if len(ups) > 1: fl.append('STAT_CHANGE_MULTIPLE_STATS')
    out += '\tplaystatchangeanimation BS_ATTACKER, %s, %s\n' % (bits, ' | '.join(fl) if fl else '0')
    downs = [c for c in changes if c[1] < 0]
    if downs:
        bits = ' | '.join(bit[c[0]] for c in downs)
        fl = ['STAT_CHANGE_NEGATIVE', 'STAT_CHANGE_CANT_PREVENT']
        if len(downs) > 1: fl.append('STAT_CHANGE_MULTIPLE_STATS')
        out += '\tplaystatchangeanimation BS_ATTACKER, %s, %s\n' % (bits, ' | '.join(fl))
    for i, (st, d) in enumerate(ups + downs):
        nxt = '%sNext%d' % (label, i)
        neg = d < 0
        out += '\tsetstatchanger STAT_%s, %d, %s\n' % (st, abs(d), 'TRUE' if neg else 'FALSE')
        out += '\tstatbuffchange MOVE_EFFECT_AFFECTS_USER | STAT_CHANGE_ALLOW_PTR%s, %s\n' % (' | MOVE_EFFECT_CERTAIN' if neg else '', nxt)
        out += '\tjumpifbyte CMP_EQUAL, cMULTISTRING_CHOOSER, %s, %s\n' % ('2' if neg else 'B_MSG_STAT_WONT_INCREASE', nxt)
        out += '\tprintfromtable %s\n\twaitmessage B_WAIT_TIME_LONG\n%s::\n' % ('gStatDownStringIds' if neg else 'gStatUpStringIds', nxt)
    out += '\tgoto BattleScript_MoveEnd\n\n'
    return out

sc = '\n@ ---- Topaze: effets Gen 4+ ----\n'
sc += multistat('QuiverDance', [('SPATK', 1), ('SPDEF', 1), ('SPEED', 1)])
sc += multistat('ShellSmash', [('ATK', 2), ('SPATK', 2), ('SPEED', 2), ('DEF', -1), ('SPDEF', -1)])
sc += multistat('Coil', [('ATK', 1), ('DEF', 1), ('ACC', 1)])
sc += multistat('WorkUp', [('ATK', 1), ('SPATK', 1)])
sc += multistat('HoneClaws', [('ATK', 1), ('ACC', 1)])
sc += '''BattleScript_EffectCloseCombat::
	setmoveeffect MOVE_EFFECT_DEF_SPDEF_DOWN | MOVE_EFFECT_AFFECTS_USER | MOVE_EFFECT_CERTAIN
	goto BattleScript_EffectHit

BattleScript_EffectHammerArm::
	setmoveeffect MOVE_EFFECT_SPD_MINUS_1 | MOVE_EFFECT_AFFECTS_USER | MOVE_EFFECT_CERTAIN
	goto BattleScript_EffectHit

BattleScript_EffectSpAtkUpHit::
	setmoveeffect MOVE_EFFECT_SP_ATK_PLUS_1 | MOVE_EFFECT_AFFECTS_USER
	goto BattleScript_EffectHit

BattleScript_DefSpDefDown::
	setbyte sSTAT_ANIM_PLAYED, FALSE
	playstatchangeanimation BS_ATTACKER, BIT_DEF | BIT_SPDEF, STAT_CHANGE_CANT_PREVENT | STAT_CHANGE_NEGATIVE | STAT_CHANGE_MULTIPLE_STATS
	setstatchanger STAT_DEF, 1, TRUE
	statbuffchange MOVE_EFFECT_AFFECTS_USER | MOVE_EFFECT_CERTAIN | STAT_CHANGE_ALLOW_PTR, BattleScript_DefSpDefDownDefFail
	jumpifbyte CMP_EQUAL, cMULTISTRING_CHOOSER, 2, BattleScript_DefSpDefDownDefFail
	printfromtable gStatDownStringIds
	waitmessage B_WAIT_TIME_LONG
BattleScript_DefSpDefDownDefFail::
	setstatchanger STAT_SPDEF, 1, TRUE
	statbuffchange MOVE_EFFECT_AFFECTS_USER | STAT_CHANGE_ALLOW_PTR | MOVE_EFFECT_CERTAIN, BattleScript_DefSpDefDownEnd
	jumpifbyte CMP_EQUAL, cMULTISTRING_CHOOSER, 2, BattleScript_DefSpDefDownEnd
	printfromtable gStatDownStringIds
	waitmessage B_WAIT_TIME_LONG
BattleScript_DefSpDefDownEnd::
	return

@ Demi-tour / Change Eclair / Culbute : frappe puis change de Pokemon (sans transmettre les stats)
BattleScript_EffectUTurn::
	attackcanceler
	accuracycheck BattleScript_PrintMoveMissed, ACC_CURR_MOVE
	attackstring
	ppreduce
	critcalc
	damagecalc
	typecalc
	adjustnormaldamage
	attackanimation
	waitanimation
	effectivenesssound
	hitanimation BS_TARGET
	waitstate
	healthbarupdate BS_TARGET
	datahpupdate BS_TARGET
	critmessage
	waitmessage B_WAIT_TIME_LONG
	resultmessage
	waitmessage B_WAIT_TIME_LONG
	seteffectwithchance
	tryfaintmon BS_TARGET
	jumpifhasnohp BS_TARGET, BattleScript_MoveEnd
	jumpifhasnohp BS_ATTACKER, BattleScript_MoveEnd
	jumpifcantswitch SWITCH_IGNORE_ESCAPE_PREVENTION | BS_ATTACKER, BattleScript_MoveEnd
	moveendall
	openpartyscreen BS_ATTACKER, BattleScript_UTurnEnd
	switchoutabilities BS_ATTACKER
	waitstate
	switchhandleorder BS_ATTACKER, 2
	returntoball BS_ATTACKER
	getswitchedmondata BS_ATTACKER
	switchindataupdate BS_ATTACKER
	hpthresholds BS_ATTACKER
	printstring STRINGID_SWITCHINMON
	switchinanim BS_ATTACKER, TRUE
	waitstate
	switchineffects BS_ATTACKER
BattleScript_UTurnEnd::
	end

BattleScript_EffectStealthRock::
	attackcanceler
	trysetspikes BattleScript_ButItFailedAtkStringPpReduce
	attackstring
	ppreduce
	attackanimation
	waitanimation
	printstring STRINGID_TOPAZEROCKSET
	waitmessage B_WAIT_TIME_LONG
	goto BattleScript_MoveEnd

BattleScript_EffectToxicSpikes::
	attackcanceler
	trysetspikes BattleScript_ButItFailedAtkStringPpReduce
	attackstring
	ppreduce
	attackanimation
	waitanimation
	printstring STRINGID_TOPAZETSPIKESSET
	waitmessage B_WAIT_TIME_LONG
	goto BattleScript_MoveEnd

BattleScript_TopazeHazardAbsorbed::
	printstring STRINGID_TOPAZETSPIKESGONE
	waitmessage B_WAIT_TIME_LONG
	return

BattleScript_TopazeRockFree::
	printstring STRINGID_TOPAZEROCKFREE
	waitmessage B_WAIT_TIME_LONG
	return

BattleScript_TopazeToxicSpikesFree::
	printstring STRINGID_TOPAZETSPIKESFREE
	waitmessage B_WAIT_TIME_LONG
	return
'''
s = s.rstrip('\n') + '\n' + sc
# le texte des degats de pieges depend de gBattleCommunication[MULTISTRING_CHOOSER] (0 = Picots, 1 = Piege de Roc)
s = s.replace('BattleScript_PrintHurtBySpikes::\n\tprintstring STRINGID_PKMNHURTBYSPIKES\n', 'BattleScript_PrintHurtBySpikes::\n\tprintfromtable gTopazeHazardStringIds\n')
W('data/battle_scripts_1.s', s)

# ---- chaines
ids = R('include/constants/battle_string_ids.h')
ids = ids.replace('#define STRINGID_TOPAZEBADDREAMS 392\n', '''#define STRINGID_TOPAZEBADDREAMS 392
#define STRINGID_TOPAZEROCKSET 393
#define STRINGID_TOPAZEROCKHURT 394
#define STRINGID_TOPAZEROCKFREE 395
#define STRINGID_TOPAZETSPIKESSET 396
#define STRINGID_TOPAZETSPIKESGONE 397
#define STRINGID_TOPAZETSPIKESFREE 398
''').replace('#define BATTLESTRINGS_COUNT     393', '#define BATTLESTRINGS_COUNT     399')
W('include/constants/battle_string_ids.h', ids)
m = R('src/battle_message.c')
m = m.replace('static const u8 sText_TopazeBadDreams[]', '''static const u8 sText_TopazeRockSet[] = _("Pointed stones float in the air\\naround the foe's team!");
static const u8 sText_TopazeRockHurt[] = _("Pointed stones dug into\\n{B_SCR_ACTIVE_NAME_WITH_PREFIX}!");
static const u8 sText_TopazeRockFree[] = _("{B_ATK_NAME_WITH_PREFIX} blew away\\nthe pointed stones!");
static const u8 sText_TopazeTSpikesSet[] = _("Poison spikes were scattered\\non the ground around the foe!");
static const u8 sText_TopazeTSpikesGone[] = _("{B_SCR_ACTIVE_NAME_WITH_PREFIX} absorbed\\nthe TOXIC SPIKES!");
static const u8 sText_TopazeTSpikesFree[] = _("{B_ATK_NAME_WITH_PREFIX} blew away\\nthe TOXIC SPIKES!");
static const u8 sText_TopazeBadDreams[]''', 1)
m = m.replace('    [STRINGID_TOPAZEBADDREAMS - BATTLESTRINGS_TABLE_START]               = sText_TopazeBadDreams\n};', '''    [STRINGID_TOPAZEBADDREAMS - BATTLESTRINGS_TABLE_START]               = sText_TopazeBadDreams,
    [STRINGID_TOPAZEROCKSET - BATTLESTRINGS_TABLE_START]                 = sText_TopazeRockSet,
    [STRINGID_TOPAZEROCKHURT - BATTLESTRINGS_TABLE_START]                = sText_TopazeRockHurt,
    [STRINGID_TOPAZEROCKFREE - BATTLESTRINGS_TABLE_START]                = sText_TopazeRockFree,
    [STRINGID_TOPAZETSPIKESSET - BATTLESTRINGS_TABLE_START]              = sText_TopazeTSpikesSet,
    [STRINGID_TOPAZETSPIKESGONE - BATTLESTRINGS_TABLE_START]             = sText_TopazeTSpikesGone,
    [STRINGID_TOPAZETSPIKESFREE - BATTLESTRINGS_TABLE_START]             = sText_TopazeTSpikesFree
};

const u16 gTopazeHazardStringIds[] = { STRINGID_PKMNHURTBYSPIKES, STRINGID_TOPAZEROCKHURT };''', 1)
W('src/battle_message.c', m)
mh = R('include/battle_message.h')
if 'gTopazeHazardStringIds' not in mh:
    mh = mh.replace('extern const u16 gMissStringIds[];', 'extern const u16 gMissStringIds[];\nextern const u16 gTopazeHazardStringIds[];')
    W('include/battle_message.h', mh)

# ---- code C
c = R('src/battle_script_commands.c')
# secondary effect : Def + SpDef -1 sur l'utilisateur
c = c.replace('''            case MOVE_EFFECT_RECOIL_33: // Double Edge''', '''            case MOVE_EFFECT_DEF_SPDEF_DOWN: // Topaze: Close Combat
                BattleScriptPush(gBattlescriptCurrInstr + 1);
                gBattlescriptCurrInstr = BattleScript_DefSpDefDown;
                break;
            case MOVE_EFFECT_RECOIL_33: // Double Edge''', 1)
# pieges : Cmd_trysetspikes
c = c.replace('''static void Cmd_trysetspikes(void)
{
    u8 targetSide = GetBattlerSide(gBattlerAttacker) ^ BIT_SIDE;

    if (gSideTimers[targetSide].spikesAmount == 3)''', '''static void Cmd_trysetspikes(void)
{
    u8 targetSide = GetBattlerSide(gBattlerAttacker) ^ BIT_SIDE;

    // Topaze: Stealth Rock (fieldB bit 0) and Toxic Spikes (fieldB bits 1-2, 0-2 layers)
    if (gBattleMoves[gCurrentMove].effect == EFFECT_STEALTH_ROCK)
    {
        if (gSideTimers[targetSide].fieldB & 1)
        {
            gSpecialStatuses[gBattlerAttacker].ppNotAffectedByPressure = 1;
            gBattlescriptCurrInstr = T1_READ_PTR(gBattlescriptCurrInstr + 1);
        }
        else
        {
            gSideTimers[targetSide].fieldB |= 1;
            gBattlescriptCurrInstr += 5;
        }
        return;
    }
    if (gBattleMoves[gCurrentMove].effect == EFFECT_TOXIC_SPIKES)
    {
        u8 layers = (gSideTimers[targetSide].fieldB >> 1) & 3;

        if (layers >= 2)
        {
            gSpecialStatuses[gBattlerAttacker].ppNotAffectedByPressure = 1;
            gBattlescriptCurrInstr = T1_READ_PTR(gBattlescriptCurrInstr + 1);
        }
        else
        {
            gSideTimers[targetSide].fieldB = (gSideTimers[targetSide].fieldB & 1) | ((layers + 1) << 1);
            gBattlescriptCurrInstr += 5;
        }
        return;
    }

    if (gSideTimers[targetSide].spikesAmount == 3)''', 1)
# Rapid Spin nettoie aussi les nouveaux pieges
c = c.replace('''    else if (gSideStatuses[GetBattlerSide(gBattlerAttacker)] & SIDE_STATUS_SPIKES)
    {
        gSideStatuses[GetBattlerSide(gBattlerAttacker)] &= ~SIDE_STATUS_SPIKES;''', '''    else if (gSideTimers[GetBattlerSide(gBattlerAttacker)].fieldB & 1)
    {
        gSideTimers[GetBattlerSide(gBattlerAttacker)].fieldB &= ~1;
        BattleScriptPushCursor();
        gBattlescriptCurrInstr = BattleScript_TopazeRockFree;
    }
    else if (gSideTimers[GetBattlerSide(gBattlerAttacker)].fieldB & 6)
    {
        gSideTimers[GetBattlerSide(gBattlerAttacker)].fieldB &= ~6;
        BattleScriptPushCursor();
        gBattlescriptCurrInstr = BattleScript_TopazeToxicSpikesFree;
    }
    else if (gSideStatuses[GetBattlerSide(gBattlerAttacker)] & SIDE_STATUS_SPIKES)
    {
        gSideStatuses[GetBattlerSide(gBattlerAttacker)] &= ~SIDE_STATUS_SPIKES;''', 1)
# entree en jeu : Piege de Roc, Pics Toxiques, puis Picots
c = c.replace('''static void Cmd_switchineffects(void)
{
    s32 i;

    gActiveBattler = GetBattlerForBattleScript(gBattlescriptCurrInstr[1]);
    UpdateSentPokesToOpponentValue(gActiveBattler);

    gHitMarker &= ~HITMARKER_FAINTED(gActiveBattler);
    gSpecialStatuses[gActiveBattler].faintedHasReplacement = FALSE;

    if (!(gSideStatuses''', '''static u8 sTopazeHazardsDone[MAX_BATTLERS_COUNT]; // bit 0 = Stealth Rock done, bit 1 = Toxic Spikes done (this switch-in)

static u16 TopazeRockDamage(u8 battler)
{
    const u8 *t = gTypeEffectiveness;
    u32 mul = 10;
    u8 i, t1 = gBattleMons[battler].type1, t2 = gBattleMons[battler].type2;
    u32 dmg;

    for (i = 0; t[i] != 0xFF && t[i] != 0xFE; i += 3)
    {
        if (t[i] == TYPE_ROCK && (t[i + 1] == t1 || (t[i + 1] == t2 && t2 != t1)))
            mul = mul * t[i + 2] / 10;
    }
    dmg = gBattleMons[battler].maxHP * mul / 80;
    if (dmg == 0)
        dmg = 1;
    return dmg;
}

// Topaze: Stealth Rock / Toxic Spikes on switch-in. Returns TRUE when a battle script was started
// (the script returns to this same command, which then goes on with the next hazard).
static bool8 TopazeSwitchInHazards(void)
{
    u8 side = GetBattlerSide(gActiveBattler);
    u8 layers = (gSideTimers[side].fieldB >> 1) & 3;
    bool8 grounded = !IS_BATTLER_OF_TYPE(gActiveBattler, TYPE_FLYING) && gBattleMons[gActiveBattler].ability != ABILITY_LEVITATE;

    if (!(sTopazeHazardsDone[gActiveBattler] & 1) && (gSideTimers[side].fieldB & 1))
    {
        sTopazeHazardsDone[gActiveBattler] |= 1;
        gBattleMoveDamage = TopazeRockDamage(gActiveBattler);
        gBattleCommunication[MULTISTRING_CHOOSER] = 1;
        gBattleScripting.battler = gActiveBattler;
        BattleScriptPushCursor();
        if (gBattlescriptCurrInstr[1] == BS_TARGET)
            gBattlescriptCurrInstr = BattleScript_SpikesOnTarget;
        else if (gBattlescriptCurrInstr[1] == BS_ATTACKER)
            gBattlescriptCurrInstr = BattleScript_SpikesOnAttacker;
        else
            gBattlescriptCurrInstr = BattleScript_SpikesOnFaintedBattler;
        return TRUE;
    }
    if (!(sTopazeHazardsDone[gActiveBattler] & 2) && layers != 0 && grounded)
    {
        sTopazeHazardsDone[gActiveBattler] |= 2;
        if (IS_BATTLER_OF_TYPE(gActiveBattler, TYPE_POISON))
        {
            gSideTimers[side].fieldB &= 1;
            gBattleScripting.battler = gActiveBattler;
            BattleScriptPushCursor();
            gBattlescriptCurrInstr = BattleScript_TopazeHazardAbsorbed;
            return TRUE;
        }
        if (!IS_BATTLER_OF_TYPE(gActiveBattler, TYPE_STEEL) && gBattleMons[gActiveBattler].status1 == 0)
        {
            gBattlerAttacker = gActiveBattler;
            gBattleCommunication[MOVE_EFFECT_BYTE] = MOVE_EFFECT_AFFECTS_USER | (layers >= 2 ? MOVE_EFFECT_TOXIC : MOVE_EFFECT_POISON);
            BattleScriptPushCursor();
            gBattlescriptCurrInstr = BattleScript_ApplySecondaryEffect;
            return TRUE;
        }
    }
    return FALSE;
}

static void Cmd_switchineffects(void)
{
    s32 i;

    gActiveBattler = GetBattlerForBattleScript(gBattlescriptCurrInstr[1]);
    UpdateSentPokesToOpponentValue(gActiveBattler);

    gHitMarker &= ~HITMARKER_FAINTED(gActiveBattler);
    gSpecialStatuses[gActiveBattler].faintedHasReplacement = FALSE;

    if (TopazeSwitchInHazards())
        return;

    gBattleCommunication[MULTISTRING_CHOOSER] = 0;
    if (!(gSideStatuses''', 1)
# nettoyage des drapeaux "deja fait"
c = c.replace('''            gSideStatuses[GetBattlerSide(gActiveBattler)] &= ~SIDE_STATUS_SPIKES_DAMAGED;

            for (i = 0; i < gBattlersCount; i++)
            {
                if (gBattlerByTurnOrder[i] == gActiveBattler)''', '''            gSideStatuses[GetBattlerSide(gActiveBattler)] &= ~SIDE_STATUS_SPIKES_DAMAGED;
            sTopazeHazardsDone[gActiveBattler] = 0;

            for (i = 0; i < gBattlersCount; i++)
            {
                if (gBattlerByTurnOrder[i] == gActiveBattler)''', 1)
c = c.replace('''            gSideStatuses[GetBattlerSide(gActiveBattler)] &= ~SIDE_STATUS_SPIKES_DAMAGED;
        }
        else
        {
            gBattlescriptCurrInstr += 7;''', '''            gSideStatuses[GetBattlerSide(gActiveBattler)] &= ~SIDE_STATUS_SPIKES_DAMAGED;
            sTopazeHazardsDone[gActiveBattler] = 0;
        }
        else
        {
            gBattlescriptCurrInstr += 7;''', 1)
W('src/battle_script_commands.c', c)
print('effets ajoutes :', ', '.join(NEW))
