#ifndef GUARD_TOPAZE_ABILITIES_H
#define GUARD_TOPAZE_ABILITIES_H

// Topaze: Gen 5-9 abilities support (docs/topaze/add_abilities.py)
u8 TopazeAdjustMoveType(u8 ability, u8 type);
bool8 TopazeAbilityConvertsNormal(u8 ability);
bool8 TopazeSheerForceApplies(u16 move);
u16 TopazePowerPct(struct BattlePokemon *atk, struct BattlePokemon *def, u16 move, u8 type, u8 baseType, u8 battlerAtk, u8 battlerDef);
s8 TopazeMovePriority(u8 battler, u16 move);
bool8 TopazeIsContactMove(u16 move);

#endif // GUARD_TOPAZE_ABILITIES_H
