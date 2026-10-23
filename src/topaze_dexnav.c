// Topaze: POKE RADAR screen (DexNav style). Lists the Pokemon of the current zone
// (water row + land rows), shows their info and lets the player pick one to search.
#include "global.h"
#include "gflib.h"
#include "scanline_effect.h"
#include "menu.h"
#include "task.h"
#include "overworld.h"
#include "field_fadetransition.h"
#include "pokemon_icon.h"
#include "pokemon.h"
#include "pokedex.h"
#include "wild_encounter.h"
#include "battle_main.h"
#include "item.h"
#include "region_map.h"
#include "string_util.h"
#include "sound.h"
#include "data.h"
#include "constants/songs.h"
#include "constants/species.h"

#define ROW_WATER 0
#define ROW_LAND1 1
#define ROW_LAND2 2
#define COLS 5

#define WIN_HEADER 0
#define WIN_GRID   1
#define WIN_INFO   2
#define WIN_FOOTER 3

// palette 15 indices
#define C_BG    1
#define C_WHITE 2
#define C_GRAY  3
#define C_GOLD  4
#define C_BOX   5
#define C_SEL   6
#define C_BAR   7

struct DexNavData
{
    struct TopazeRadarEntry entries[3][COLS];
    u8 count[3];
    u8 seen[3][COLS];
    u8 sprite[3][COLS];
    u8 row;
    u8 col;
    u8 state;
    u8 surfing;
};

static struct DexNavData *sDex;

static const struct WindowTemplate sWinTemplates[] =
{
    { .bg = 0, .tilemapLeft = 0,  .tilemapTop = 0,  .width = 30, .height = 2,  .paletteNum = 15, .baseBlock = 1 },
    { .bg = 0, .tilemapLeft = 0,  .tilemapTop = 2,  .width = 20, .height = 15, .paletteNum = 15, .baseBlock = 61 },
    { .bg = 0, .tilemapLeft = 20, .tilemapTop = 2,  .width = 10, .height = 15, .paletteNum = 15, .baseBlock = 361 },
    { .bg = 0, .tilemapLeft = 0,  .tilemapTop = 17, .width = 30, .height = 3,  .paletteNum = 15, .baseBlock = 511 },
    DUMMY_WIN_TEMPLATE
};

static const struct BgTemplate sBgTemplates[] =
{
    { .bg = 0, .charBaseIndex = 1, .mapBaseIndex = 31, .screenSize = 0, .paletteMode = 0, .priority = 3, .baseTile = 0 },
};

static const u16 sPalette[16] =
{
    RGB(1, 3, 8),     // 0 backdrop
    RGB(2, 5, 12),    // 1 background
    RGB(31, 31, 31),  // 2 white
    RGB(12, 14, 19),  // 3 shadow / gray
    RGB(31, 27, 5),   // 4 gold
    RGB(5, 9, 19),    // 5 empty box
    RGB(12, 19, 30),  // 6 selected box
    RGB(4, 8, 22),    // 7 bar
    RGB(31, 31, 31), RGB(31, 31, 31), RGB(31, 31, 31), RGB(31, 31, 31),
    RGB(31, 31, 31), RGB(31, 31, 31), RGB(31, 31, 31), RGB(31, 31, 31),
};

static const u8 sTxtNormal[] = {C_BG, C_WHITE, C_GRAY};
static const u8 sTxtGold[]   = {C_BG, C_GOLD, C_GRAY};
static const u8 sTxtGray[]   = {C_BG, C_GRAY, C_BOX};
static const u8 sTxtBar[]    = {C_BAR, C_WHITE, C_GRAY};
static const u8 sTxtBarGold[] = {C_BAR, C_GOLD, C_GRAY};

static const u8 sText_Title[]    = _("POKé RADAR");
static const u8 sText_Water[]    = _("WATER (surf)");
static const u8 sText_Land[]     = _("LAND (grass, caves)");
static const u8 sText_None[]     = _("nothing here");
static const u8 sText_Lv[]       = _("Lv ");
static const u8 sText_Dash[]     = _("-");
static const u8 sText_Unknown[]  = _("?????");
static const u8 sText_NotSeen[]  = _("Not seen yet.");
static const u8 sText_Ability[]  = _("ABILITY");
static const u8 sText_Item[]     = _("HELD ITEM");
static const u8 sText_Chain[]    = _("CHAIN ");
static const u8 sText_Footer1[]  = _("A: search      B: close");
static const u8 sText_Footer2[]  = _("Water mons: surf first. Land: on foot.");
static const u8 sText_OnFoot[]   = _("  (on foot)");
static const u8 sText_Surfing[]  = _("  (surfing)");

static const u16 sCellX[COLS] = {0, 32, 64, 96, 128};
static const u16 sRowY[3] = {12, 56, 88}; // inside the grid window

static void VBlankCB(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_Main(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
}

static bool8 IsSeen(u16 species)
{
    return GetSetPokedexFlag(SpeciesToNationalPokedexNum(species), FLAG_GET_SEEN);
}

static u8 *PrintNum(u8 *dst, u32 n)
{
    return ConvertIntToDecimalStringN(dst, n, STR_CONV_MODE_LEFT_ALIGN, 3);
}

static void DrawGrid(void)
{
    u8 r, c;

    FillWindowPixelBuffer(WIN_GRID, PIXEL_FILL(C_BG));
    AddTextPrinterParameterized3(WIN_GRID, FONT_SMALL, 2, 0, sTxtGold, 0, sText_Water);
    AddTextPrinterParameterized3(WIN_GRID, FONT_SMALL, 2, 44, sTxtGold, 0, sText_Land);
    if (sDex->count[ROW_WATER] == 0)
        AddTextPrinterParameterized3(WIN_GRID, FONT_SMALL, 6, 20, sTxtGray, 0, sText_None);
    if (sDex->count[ROW_LAND1] == 0)
        AddTextPrinterParameterized3(WIN_GRID, FONT_SMALL, 6, 64, sTxtGray, 0, sText_None);
    for (r = 0; r < 3; r++)
    {
        for (c = 0; c < sDex->count[r]; c++)
        {
            u8 color = (r == sDex->row && c == sDex->col) ? C_SEL : C_BOX;

            FillWindowPixelRect(WIN_GRID, color, sCellX[c] + 1, sRowY[r] + 1, 30, 30);
        }
    }
    CopyWindowToVram(WIN_GRID, COPYWIN_GFX);
}

static void DrawInfo(void)
{
    struct TopazeRadarEntry *e = &sDex->entries[sDex->row][sDex->col];
    const struct SpeciesInfo *info;
    u8 buf[24];
    u8 *p;
    u8 y = 0;
    u16 sp;

    FillWindowPixelBuffer(WIN_INFO, PIXEL_FILL(C_BG));
    if (sDex->count[sDex->row] == 0)
    {
        CopyWindowToVram(WIN_INFO, COPYWIN_GFX);
        return;
    }
    sp = e->species;
    if (!sDex->seen[sDex->row][sDex->col])
    {
        AddTextPrinterParameterized3(WIN_INFO, FONT_SMALL, 4, 0, sTxtGold, 0, sText_Unknown);
        AddTextPrinterParameterized3(WIN_INFO, FONT_SMALL, 4, 16, sTxtGray, 0, sText_NotSeen);
        CopyWindowToVram(WIN_INFO, COPYWIN_GFX);
        return;
    }
    info = &gSpeciesInfo[sp];
    AddTextPrinterParameterized3(WIN_INFO, FONT_SMALL, 4, y, sTxtGold, 0, gSpeciesNames[sp]);
    y += 12;
    AddTextPrinterParameterized3(WIN_INFO, FONT_SMALL, 4, y, sTxtNormal, 0, gTypeNames[info->types[0]]);
    y += 12;
    if (info->types[1] != info->types[0])
    {
        AddTextPrinterParameterized3(WIN_INFO, FONT_SMALL, 4, y, sTxtNormal, 0, gTypeNames[info->types[1]]);
        y += 12;
    }
    p = StringCopy(buf, sText_Lv);
    p = PrintNum(p, e->minLv);
    if (e->maxLv != e->minLv)
    {
        p = StringCopy(p, sText_Dash);
        p = PrintNum(p, e->maxLv);
    }
    AddTextPrinterParameterized3(WIN_INFO, FONT_SMALL, 4, y, sTxtNormal, 0, buf);
    y += 14;
    AddTextPrinterParameterized3(WIN_INFO, FONT_SMALL, 4, y, sTxtGray, 0, sText_Ability);
    y += 12;
    AddTextPrinterParameterized3(WIN_INFO, FONT_SMALL, 4, y, sTxtNormal, 0, gAbilityNames[info->abilities[0]]);
    y += 12;
    if (info->abilities[1] != 0 && info->abilities[1] != info->abilities[0])
    {
        AddTextPrinterParameterized3(WIN_INFO, FONT_SMALL, 4, y, sTxtNormal, 0, gAbilityNames[info->abilities[1]]);
        y += 12;
    }
    if (info->itemCommon != 0 || info->itemRare != 0)
    {
        AddTextPrinterParameterized3(WIN_INFO, FONT_SMALL, 4, y, sTxtGray, 0, sText_Item);
        y += 12;
        AddTextPrinterParameterized3(WIN_INFO, FONT_SMALL, 4, y, sTxtNormal, 0, ItemId_GetName(info->itemCommon != 0 ? info->itemCommon : info->itemRare));
        y += 12;
    }
    if (TopazeRadarGetChain(sp) > 0 && y <= 108)
    {
        p = StringCopy(buf, sText_Chain);
        PrintNum(p, TopazeRadarGetChain(sp));
        AddTextPrinterParameterized3(WIN_INFO, FONT_SMALL, 4, y, sTxtGold, 0, buf);
    }
    CopyWindowToVram(WIN_INFO, COPYWIN_GFX);
}

static void Redraw(void)
{
    DrawGrid();
    DrawInfo();
}

static void DrawStaticTexts(void)
{
    u8 buf[48];
    u8 *p;

    FillWindowPixelBuffer(WIN_HEADER, PIXEL_FILL(C_BAR));
    p = GetMapNameGeneric(buf, gMapHeader.regionMapSectionId);
    StringCopy(p, sDex->surfing ? sText_Surfing : sText_OnFoot);
    AddTextPrinterParameterized3(WIN_HEADER, FONT_SMALL, 6, 1, sTxtBar, 0, buf);
    AddTextPrinterParameterized3(WIN_HEADER, FONT_SMALL, 180, 1, sTxtBarGold, 0, sText_Title);
    FillWindowPixelBuffer(WIN_FOOTER, PIXEL_FILL(C_BAR));
    AddTextPrinterParameterized3(WIN_FOOTER, FONT_SMALL, 6, 1, sTxtBar, 0, sText_Footer1);
    AddTextPrinterParameterized3(WIN_FOOTER, FONT_SMALL, 6, 12, sTxtBarGold, 0, sText_Footer2);
    PutWindowTilemap(WIN_HEADER);
    PutWindowTilemap(WIN_GRID);
    PutWindowTilemap(WIN_INFO);
    PutWindowTilemap(WIN_FOOTER);
    CopyWindowToVram(WIN_HEADER, COPYWIN_FULL);
    CopyWindowToVram(WIN_FOOTER, COPYWIN_FULL);
    CopyWindowToVram(WIN_GRID, COPYWIN_FULL);
    CopyWindowToVram(WIN_INFO, COPYWIN_FULL);
}

static void CreateIcons(void)
{
    u8 r, c;

    LoadMonIconPalettes();
    for (r = 0; r < 3; r++)
    {
        for (c = 0; c < sDex->count[r]; c++)
        {
            u16 sp = sDex->seen[r][c] ? sDex->entries[r][c].species : SPECIES_NONE;
            u8 id = CreateMonIcon(sp, SpriteCallbackDummy, sCellX[c] + 16, 16 + sRowY[r] + 16, 0, 0, FALSE);

            gSprites[id].oam.priority = 0;
            sDex->sprite[r][c] = id;
        }
    }
}

static void LoadZone(void)
{
    struct TopazeRadarEntry water[10];
    struct TopazeRadarEntry land[10];
    u8 nw = TopazeRadarGetZone(TRUE, water);
    u8 nl = TopazeRadarGetZone(FALSE, land);
    u8 i;

    sDex->count[ROW_WATER] = nw > COLS ? COLS : nw;
    sDex->count[ROW_LAND1] = nl > COLS ? COLS : nl;
    sDex->count[ROW_LAND2] = nl > COLS ? nl - COLS : 0;
    for (i = 0; i < sDex->count[ROW_WATER]; i++)
        sDex->entries[ROW_WATER][i] = water[i];
    for (i = 0; i < sDex->count[ROW_LAND1]; i++)
        sDex->entries[ROW_LAND1][i] = land[i];
    for (i = 0; i < sDex->count[ROW_LAND2]; i++)
        sDex->entries[ROW_LAND2][i] = land[COLS + i];
    for (i = 0; i < 3; i++)
    {
        u8 c;

        for (c = 0; c < sDex->count[i]; c++)
            sDex->seen[i][c] = IsSeen(sDex->entries[i][c].species);
    }
    sDex->surfing = TopazeRadarPlayerSurfing();
    sDex->row = (sDex->surfing && sDex->count[ROW_WATER] > 0) ? ROW_WATER : (sDex->count[ROW_LAND1] > 0 ? ROW_LAND1 : ROW_WATER);
    sDex->col = 0;
}

static bool8 MoveRow(s8 dir)
{
    s8 r = sDex->row;

    for (;;)
    {
        r += dir;
        if (r < 0 || r > 2)
            return FALSE;
        if (sDex->count[r] > 0)
            break;
    }
    sDex->row = r;
    if (sDex->col >= sDex->count[r])
        sDex->col = sDex->count[r] - 1;
    return TRUE;
}

static void Close(u8 taskId, bool8 picked)
{
    if (picked)
    {
        gTopazeRadarPick = sDex->entries[sDex->row][sDex->col].species;
        gTopazeRadarPickWater = (sDex->row == ROW_WATER);
    }
    else
    {
        gTopazeRadarPick = SPECIES_NONE;
    }
    BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    sDex->state = 3;
}

static void Task_DexNav(u8 taskId)
{
    switch (sDex->state)
    {
    case 0:
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        SetVBlankCallback(VBlankCB);
        sDex->state = 1;
        break;
    case 1:
        if (gPaletteFade.active)
            return;
        sDex->state = 2;
        break;
    case 2:
        if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            Close(taskId, FALSE);
        }
        else if (JOY_NEW(A_BUTTON))
        {
            if (sDex->count[sDex->row] == 0 || !sDex->seen[sDex->row][sDex->col])
            {
                PlaySE(SE_FAILURE);
            }
            else
            {
                PlaySE(SE_SELECT);
                Close(taskId, TRUE);
            }
        }
        else if (JOY_REPT(DPAD_RIGHT) && sDex->col + 1 < sDex->count[sDex->row])
        {
            sDex->col++;
            PlaySE(SE_SELECT);
            Redraw();
        }
        else if (JOY_REPT(DPAD_LEFT) && sDex->col > 0)
        {
            sDex->col--;
            PlaySE(SE_SELECT);
            Redraw();
        }
        else if (JOY_REPT(DPAD_DOWN) && MoveRow(1))
        {
            PlaySE(SE_SELECT);
            Redraw();
        }
        else if (JOY_REPT(DPAD_UP) && MoveRow(-1))
        {
            PlaySE(SE_SELECT);
            Redraw();
        }
        break;
    case 3:
        if (gPaletteFade.active)
            return;
        FreeMonIconPalettes();
        FreeAllWindowBuffers();
        Free(sDex);
        sDex = NULL;
        gFieldCallback = FieldCB_ContinueScript;
        SetMainCallback2(CB2_ReturnToField);
        DestroyTask(taskId);
        break;
    }
}

static void CB2_Init(void)
{
    SetVBlankCallback(NULL);
    SetHBlankCallback(NULL);
    DmaClearLarge16(3, (void *)VRAM, VRAM_SIZE, 0x1000);
    DmaClear32(3, (void *)OAM, OAM_SIZE);
    DmaClear16(3, (void *)PLTT, PLTT_SIZE);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0);
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, sBgTemplates, NELEMS(sBgTemplates));
    ChangeBgX(0, 0, 0);
    ChangeBgY(0, 0, 0);
    InitWindows(sWinTemplates);
    DeactivateAllTextPrinters();
    ResetSpriteData();
    ResetPaletteFade();
    FreeAllSpritePalettes();
    ResetTasks();
    ScanlineEffect_Stop();
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON);
    LoadPalette(sPalette, BG_PLTT_ID(15), sizeof(sPalette));
    LoadPalette(sPalette, BG_PLTT_ID(0), 2);
    sDex = AllocZeroed(sizeof(struct DexNavData));
    LoadZone();
    DrawStaticTexts();
    Redraw();
    CreateIcons();
    ShowBg(0);
    CreateTask(Task_DexNav, 0);
    SetMainCallback2(CB2_Main);
}

// special: open the screen; the script then does waitstate and reads gTopazeRadarPick via TopazeRadarStart
void TopazeRadarOpenScreen(void)
{
    gTopazeRadarPick = SPECIES_NONE;
    SetMainCallback2(CB2_Init);
}
