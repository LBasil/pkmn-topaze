#include "global.h"
#include "pokemon.h"
#include "event_data.h"
#include "constants/flags.h"
#include "topaze_options.h"
#include "item.h"
#include "string_util.h"
#include "constants/items.h"
#include "constants/vars.h"

// Topaze: optional level cap (OPTION menu: OFF / LIGHT / MEDIUM / HARD).
// Base cap = level of the next gym leader's ace, by number of badges; LIGHT/MEDIUM add a margin.
// Once the game is cleared (Hall of Fame) the cap is lifted.
static const u8 sBaseCapByBadges[9] = {16, 22, 29, 35, 40, 45, 50, 55, 71};
static const u8 sCapMargin[4] = {0, 8, 4, 0}; // index = mode (0 OFF unused, 1 LIGHT, 2 MEDIUM, 3 HARD)

u8 TopazeGetLevelCap(void)
{
    u8 mode = TOPAZE_OPT_LVCAP();
    u8 i, badges = 0;
    u16 cap;

    if (mode == 0 || FlagGet(FLAG_SYS_GAME_CLEAR))
        return MAX_LEVEL;
    for (i = 0; i < 8; i++)
        if (FlagGet(FLAG_BADGE01_GET + i))
            badges++;
    cap = sBaseCapByBadges[badges] + sCapMargin[mode];
    return cap > MAX_LEVEL ? MAX_LEVEL : cap;
}

// Largest amount of exp the mon may still receive without exceeding the cap (0 if already at/above it).
u32 TopazeClampExp(struct Pokemon *mon, u32 exp)
{
    u8 cap = TopazeGetLevelCap();
    u16 species = GetMonData(mon, MON_DATA_SPECIES);
    u32 curr = GetMonData(mon, MON_DATA_EXP);
    u32 limit;

    if (cap >= MAX_LEVEL)
        return exp;
    limit = gExperienceTables[gSpeciesInfo[species].growthRate][cap + 1] - 1;
    if (curr >= limit)
        return 0;
    return exp > limit - curr ? limit - curr : exp;
}

// Topaze: OPTION POKéMON CENTER = INSTANT skips the healing animation (VAR_RESULT = TRUE when on).
u16 TopazeInstantHeal(void)
{
    return TOPAZE_OPT_INSTANTHEAL();
}

// Topaze: when a REPEL wears off, offer to use another one (last type used first).
// TopazeRepelNext: returns the item id to offer (0 = none) and puts its name in STR_VAR_1.
u16 TopazeRepelNext(void)
{
    u16 list[4];
    u8 i;

    list[0] = VarGet(VAR_LAST_REPEL_ITEM);
    list[1] = ITEM_REPEL;
    list[2] = ITEM_SUPER_REPEL;
    list[3] = ITEM_MAX_REPEL;
    for (i = 0; i < 4; i++)
    {
        if (list[i] != ITEM_NONE && CheckBagHasItem(list[i], 1))
        {
            CopyItemName(list[i], gStringVar1);
            gSpecialVar_0x8004 = list[i];
            return list[i];
        }
    }
    return ITEM_NONE;
}

void TopazeRepelUse(void)
{
    u16 item = gSpecialVar_0x8004;

    RemoveBagItem(item, 1);
    VarSet(VAR_REPEL_STEP_COUNT, ItemId_GetHoldEffectParam(item));
    VarSet(VAR_LAST_REPEL_ITEM, item);
}
