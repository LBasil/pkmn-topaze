#ifndef GUARD_TOPAZE_OPTIONS_H
#define GUARD_TOPAZE_OPTIONS_H

// Topaze quality-of-life options, packed in gSaveBlock2Ptr->optionsTopaze (0 = vanilla behaviour)
#define TOPAZE_OPT_HPBAR()   (gSaveBlock2Ptr->optionsTopaze & 3)         // 0 normal, 1 fast, 2 instant
#define TOPAZE_OPT_EXPBAR()  ((gSaveBlock2Ptr->optionsTopaze >> 2) & 3)  // 0 normal, 1 fast, 2 instant
#define TOPAZE_OPT_STACKLV() ((gSaveBlock2Ptr->optionsTopaze >> 4) & 1)  // 0 one level at a time, 1 stacked
#define TOPAZE_OPT_SPEED()   ((gSaveBlock2Ptr->optionsTopaze >> 5) & 3)  // 0..3 = x1..x4

#define TOPAZE_OPT_LVCAP()   ((gSaveBlock2Ptr->optionsTopaze >> 7) & 3)  // 0 off, 1 light, 2 medium, 3 hard

#define TOPAZE_OPT_INSTANTHEAL() ((gSaveBlock2Ptr->optionsTopaze >> 9) & 1) // 0 normal POKéMON CENTER animation, 1 instant heal

#define TOPAZE_OPT_SHINY() ((gSaveBlock2Ptr->optionsTopaze >> 10) & 7) // 0 vanilla 1/8192, 1 = 1/2048, 2 = 1/1024, 3 = 1/512 (max)

#define TOPAZE_OPT_HARD() ((gSaveBlock2Ptr->optionsTopaze >> 13) & 1) // 0 normal, 1 hard (trainers +3 levels, smart AI)

#define TOPAZE_OPT_EXPSHARE_OFF() ((gSaveBlock2Ptr->optionsTopaze >> 14) & 1) // 0 built-in EXP share on (default), 1 off (toggled with the EXP. SHARE item)

#define TOPAZE_OPT_SET(shift, mask, v) (gSaveBlock2Ptr->optionsTopaze = (gSaveBlock2Ptr->optionsTopaze & ~((mask) << (shift))) | (((v) & (mask)) << (shift)))

struct Pokemon;
u8 TopazeGetLevelCap(void);
u16 TopazeInstantHeal(void);
bool8 TopazeQuickBallReady(void);
u32 TopazeClampExp(struct Pokemon *mon, u32 exp);
extern u8 gTopazeBattleLvFrom;
extern u8 gTopazeLearnFrom;

#endif
