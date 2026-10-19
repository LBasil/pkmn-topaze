#include "global.h"
#include "battle.h"
#include "battle_main.h"
#include "battle_util.h"
#include "battle_script_commands.h"
#include "pokemon.h"
#include "topaze_abilities.h"
#include "constants/abilities.h"
#include "constants/moves.h"
#include "constants/pokemon.h"
#include "constants/battle_move_effects.h"

// Topaze: helpers for the Gen 5-9 abilities (Sheer Force, Tough Claws, Aerilate, Multiscale, Prankster...)

static const u16 sBiteMoves[] =
{
    MOVE_BITE, MOVE_CRUNCH, MOVE_FIRE_FANG, MOVE_ICE_FANG, MOVE_THUNDER_FANG, MOVE_POISON_FANG,
    MOVE_HYPER_FANG, MOVE_PSYCHIC_FANGS, MOVE_BUG_BITE, MOVE_NONE
};

static const u16 sPulseMoves[] =
{
    MOVE_WATER_PULSE, MOVE_DARK_PULSE, MOVE_DRAGON_PULSE, MOVE_AURA_SPHERE, MOVE_ORIGIN_PULSE, MOVE_NONE
};

static const u16 sSliceMoves[] =
{
    MOVE_CUT, MOVE_SLASH, MOVE_NIGHT_SLASH, MOVE_SACRED_SWORD, MOVE_AIR_SLASH, MOVE_X_SCISSOR,
    MOVE_PSYCHO_CUT, MOVE_LEAF_BLADE, MOVE_AERIAL_ACE, MOVE_RAZOR_LEAF, MOVE_FURY_CUTTER,
    MOVE_KOWTOW_CLEAVE, MOVE_BEHEMOTH_BLADE, MOVE_AIR_CUTTER, MOVE_RAZOR_SHELL, MOVE_NONE
};

static const u16 sSoundMoves[] =
{
    MOVE_HYPER_VOICE, MOVE_SCREECH, MOVE_ROAR, MOVE_SING, MOVE_SUPERSONIC, MOVE_SNORE, MOVE_UPROAR, MOVE_METAL_SOUND,
    MOVE_GRASS_WHISTLE, MOVE_PERISH_SONG, MOVE_BUG_BUZZ, MOVE_ECHOED_VOICE, MOVE_BOOMBURST, MOVE_ALLURING_VOICE, MOVE_NONE
};

static const u16 sHealMoves[] =
{
    MOVE_RECOVER, MOVE_SOFT_BOILED, MOVE_MILK_DRINK, MOVE_SYNTHESIS, MOVE_MOONLIGHT, MOVE_MORNING_SUN, MOVE_REST, MOVE_ROOST,
    MOVE_SLACK_OFF, MOVE_HEAL_PULSE, MOVE_LIFE_DEW, MOVE_SHORE_UP, MOVE_DRAIN_PUNCH, MOVE_GIGA_DRAIN, MOVE_ABSORB, MOVE_MEGA_DRAIN, MOVE_NONE
};

static bool8 InMoveList(const u16 *list, u16 move)
{
    u32 i;

    for (i = 0; list[i] != MOVE_NONE; i++)
    {
        if (list[i] == move)
            return TRUE;
    }
    return FALSE;
}

bool8 TopazeIsContactMove(u16 move)
{
    return (gBattleMoves[move].flags & FLAG_MAKES_CONTACT) != 0;
}

bool8 TopazeAbilityConvertsNormal(u8 ability)
{
    return ability == ABILITY_AERILATE || ability == ABILITY_PIXILATE
        || ability == ABILITY_REFRIGERATE || ability == ABILITY_GALVANIZE;
}

u8 TopazeAdjustMoveType(u8 ability, u8 type)
{
    if (type == TYPE_MYSTERY)
        return type;
    switch (ability)
    {
    case ABILITY_NORMALIZE:
        return TYPE_NORMAL;
    case ABILITY_AERILATE:
        if (type == TYPE_NORMAL)
            return TYPE_FLYING;
        break;
    case ABILITY_PIXILATE:
        if (type == TYPE_NORMAL)
            return TYPE_FAIRY;
        break;
    case ABILITY_REFRIGERATE:
        if (type == TYPE_NORMAL)
            return TYPE_ICE;
        break;
    case ABILITY_GALVANIZE:
        if (type == TYPE_NORMAL)
            return TYPE_ELECTRIC;
        break;
    }
    return type;
}

bool8 TopazeSheerForceApplies(u16 move)
{
    u8 effect = gBattleMoves[move].effect;

    if (gBattleMoves[move].secondaryEffectChance == 0)
        return FALSE;
    // Moves whose "secondary" effect hits the user as a drawback are not affected
    if (effect == EFFECT_OVERHEAT)
        return FALSE;
    return TRUE;
}

// Returns the damage multiplier (percent) coming from the abilities of both battlers.
u16 TopazePowerPct(struct BattlePokemon *atk, struct BattlePokemon *def, u16 move, u8 type, u8 baseType, u8 battlerAtk, u8 battlerDef)
{
    u32 pct = 100;

    switch (atk->ability)
    {
    case ABILITY_SHEER_FORCE:
        if (TopazeSheerForceApplies(move))
            pct = 130;
        break;
    case ABILITY_TOUGH_CLAWS:
        if (TopazeIsContactMove(move))
            pct = 130;
        break;
    case ABILITY_STRONG_JAW:
        if (InMoveList(sBiteMoves, move))
            pct = 150;
        break;
    case ABILITY_MEGA_LAUNCHER:
        if (InMoveList(sPulseMoves, move))
            pct = 150;
        break;
    case ABILITY_SHARPNESS:
        if (InMoveList(sSliceMoves, move))
            pct = 150;
        break;
    case ABILITY_STEELWORKER:
        if (type == TYPE_STEEL)
            pct = 150;
        break;
    case ABILITY_PUNK_ROCK:
        if (InMoveList(sSoundMoves, move))
            pct = 130;
        break;
    case ABILITY_STEELY_SPIRIT:
        if (type == TYPE_STEEL)
            pct = 150;
        break;
    case ABILITY_DEFEATIST:
        if (atk->hp <= atk->maxHP / 2)
            pct = 50;
        break;
    case ABILITY_TRANSISTOR:
        if (type == TYPE_ELECTRIC)
            pct = 150;
        break;
    case ABILITY_DRAGONS_MAW:
        if (type == TYPE_DRAGON)
            pct = 150;
        break;
    case ABILITY_ROCKY_PAYLOAD:
        if (type == TYPE_ROCK)
            pct = 150;
        break;
    case ABILITY_WATER_BUBBLE:
        if (type == TYPE_WATER)
            pct = 200;
        break;
    case ABILITY_AERILATE:
    case ABILITY_PIXILATE:
    case ABILITY_REFRIGERATE:
    case ABILITY_GALVANIZE:
        if (type != baseType)
            pct = 120;
        break;
    case ABILITY_ANALYTIC:
        if (GetBattlerTurnOrderNum(battlerAtk) > GetBattlerTurnOrderNum(battlerDef))
            pct = 130;
        break;
    case ABILITY_SAND_FORCE:
        if (WEATHER_HAS_EFFECT && (gBattleWeather & B_WEATHER_SANDSTORM)
         && (type == TYPE_ROCK || type == TYPE_GROUND || type == TYPE_STEEL))
            pct = 130;
        break;
    }

    switch (def->ability)
    {
    case ABILITY_MULTISCALE:
        if (def->hp == def->maxHP)
            pct = pct / 2;
        break;
    case ABILITY_FLUFFY:
        if (TopazeIsContactMove(move))
            pct = pct / 2;
        break;
    case ABILITY_WATER_BUBBLE:
        if (type == TYPE_FIRE)
            pct = pct / 2;
        break;
    }
    return pct;
}

s8 TopazeMovePriority(u8 battler, u16 move)
{
    s8 priority = gBattleMoves[move].priority;

    if (move == MOVE_NONE)
        return priority;
    switch (gBattleMons[battler].ability)
    {
    case ABILITY_PRANKSTER:
        if (gBattleMoves[move].power == 0)
            priority++;
        break;
    case ABILITY_TRIAGE:
        if (InMoveList(sHealMoves, move))
            priority += 3;
        break;
    case ABILITY_GALE_WINGS:
        if (gBattleMoves[move].type == TYPE_FLYING && gBattleMons[battler].hp == gBattleMons[battler].maxHP)
            priority++;
        break;
    }
    return priority;
}
