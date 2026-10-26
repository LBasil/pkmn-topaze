// Topaze: JOURNAL screen (Start menu). Sections as tabs (L / R or left / right), a scrolling list of objectives
// with a Done column, and the hint of the selected objective in the bottom bar.
#include "global.h"
#include "gflib.h"
#include "scanline_effect.h"
#include "menu.h"
#include "task.h"
#include "overworld.h"
#include "field_fadetransition.h"
#include "string_util.h"
#include "sound.h"
#include "topaze_journal.h"
#include "constants/songs.h"

#define WIN_HEADER 0
#define WIN_TAB    1
#define WIN_LIST   2
#define WIN_DESC   3

#define ROWS       6
#define ROW_H      14

// palette 15 indices
#define C_BG    1
#define C_WHITE 2
#define C_GRAY  3
#define C_GOLD  4
#define C_BOX   5
#define C_SEL   6
#define C_BAR   7
#define C_GREEN 8
#define C_DIM   9

struct JournalData
{
    u8 sections[JOURNAL_MAX_SECTIONS];
    u8 numSections;
    u8 tab;
    u16 entries[JOURNAL_MAX_ENTRIES];
    u8 numEntries;
    u8 cursor;
    u8 top;
    u8 state;
};

static struct JournalData *sJ;

static const struct WindowTemplate sWinTemplates[] =
{
    { .bg = 0, .tilemapLeft = 0, .tilemapTop = 0,  .width = 30, .height = 2,  .paletteNum = 15, .baseBlock = 1 },
    { .bg = 0, .tilemapLeft = 0, .tilemapTop = 2,  .width = 30, .height = 2,  .paletteNum = 15, .baseBlock = 61 },
    { .bg = 0, .tilemapLeft = 0, .tilemapTop = 4,  .width = 30, .height = 11, .paletteNum = 15, .baseBlock = 121 },
    { .bg = 0, .tilemapLeft = 0, .tilemapTop = 15, .width = 30, .height = 5,  .paletteNum = 15, .baseBlock = 451 },
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
    RGB(8, 13, 24),   // 5 empty marker
    RGB(6, 11, 22),   // 6 selected row
    RGB(4, 8, 22),    // 7 bar
    RGB(9, 27, 13),   // 8 green
    RGB(21, 24, 30),  // 9 "To do" text
    RGB(31, 31, 31), RGB(31, 31, 31), RGB(31, 31, 31), RGB(31, 31, 31),
    RGB(31, 31, 31), RGB(31, 31, 31),
};

static const u8 sTxtNormal[]  = {C_BG, C_WHITE, C_GRAY};
static const u8 sTxtSel[]     = {C_SEL, C_WHITE, C_GRAY};
static const u8 sTxtGold[]    = {C_BAR, C_GOLD, C_GRAY};
static const u8 sTxtBar[]     = {C_BAR, C_WHITE, C_GRAY};
static const u8 sTxtGreen[]   = {C_BG, C_GREEN, C_GRAY};
static const u8 sTxtGreenSel[] = {C_SEL, C_GREEN, C_GRAY};
static const u8 sTxtDim[]     = {C_BG, C_DIM, C_BOX};
static const u8 sTxtDimSel[]  = {C_SEL, C_DIM, C_BOX};

static const u8 sText_Title[]  = _("JOURNAL");
static const u8 sText_Done[]   = _("Done");
static const u8 sText_Todo[]   = _("To do");
static const u8 sText_Slash[]  = _("/");
static const u8 sText_Left[]   = _("< ");
static const u8 sText_Right[]  = _(" >");
static const u8 sText_Pad[]    = _("  ");

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

static u8 *PrintNum(u8 *dst, u32 n)
{
    u8 digits = 3;

    if (n >= 100000)
        digits = 6;
    else if (n >= 10000)
        digits = 5;
    else if (n >= 1000)
        digits = 4;
    return ConvertIntToDecimalStringN(dst, n, STR_CONV_MODE_LEFT_ALIGN, digits);
}

static u8 CurSection(void)
{
    return sJ->sections[sJ->tab];
}

static void DrawHeader(void)
{
    u8 buf[16];
    u8 *p;
    u8 d, t, s, i;
    u16 totalDone = 0, total = 0;

    for (i = 0; i < sJ->numSections; i++)
    {
        s = sJ->sections[i];
        TopazeJournalCount(s, &d, &t);
        totalDone += d;
        total += t;
    }
    FillWindowPixelBuffer(WIN_HEADER, PIXEL_FILL(C_BAR));
    AddTextPrinterParameterized3(WIN_HEADER, FONT_SMALL, 8, 3, sTxtGold, 0, sText_Title);
    p = PrintNum(buf, totalDone);
    p = StringCopy(p, sText_Slash);
    PrintNum(p, total);
    AddTextPrinterParameterized3(WIN_HEADER, FONT_SMALL, 232 - GetStringWidth(FONT_SMALL, buf, 0), 3, sTxtBar, 0, buf);
    CopyWindowToVram(WIN_HEADER, COPYWIN_GFX);
}

static void DrawTab(void)
{
    u8 buf[48];
    u8 *p;
    u8 d, t, i;
    u8 x;

    TopazeJournalCount(CurSection(), &d, &t);
    p = StringCopy(buf, sJ->tab > 0 ? sText_Left : sText_Pad);
    p = StringCopy(p, TopazeJournalSectionName(CurSection()));
    p = StringCopy(p, sText_Pad);
    p = PrintNum(p, d);
    p = StringCopy(p, sText_Slash);
    p = PrintNum(p, t);
    p = StringCopy(p, sJ->tab + 1 < sJ->numSections ? sText_Right : sText_Pad);
    FillWindowPixelBuffer(WIN_TAB, PIXEL_FILL(C_BG));
    AddTextPrinterParameterized3(WIN_TAB, FONT_SMALL, 120 - GetStringWidth(FONT_SMALL, buf, 0) / 2, 0, sTxtNormal, 0, buf);
    x = 120 - (sJ->numSections * 8) / 2;
    for (i = 0; i < sJ->numSections; i++)
        FillWindowPixelRect(WIN_TAB, i == sJ->tab ? C_GOLD : C_BOX, x + i * 8 + 1, 13, 6, 3);
    CopyWindowToVram(WIN_TAB, COPYWIN_GFX);
}

static void DrawList(void)
{
    u8 r;
    u8 sel;
    u16 e;
    u8 y;
    u8 done;

    FillWindowPixelBuffer(WIN_LIST, PIXEL_FILL(C_BG));
    for (r = 0; r < ROWS; r++)
    {
        u8 i = sJ->top + r;

        if (i >= sJ->numEntries)
            break;
        e = sJ->entries[i];
        sel = (i == sJ->cursor);
        done = TopazeJournalEntryDone(e);
        y = 2 + r * ROW_H;
        if (sel)
            FillWindowPixelRect(WIN_LIST, C_SEL, 0, y - 1, 216, ROW_H);
        // marker: filled green square when done, hollow box otherwise
        FillWindowPixelRect(WIN_LIST, done ? C_GREEN : C_BOX, 8, y + 2, 8, 8);
        if (!done)
            FillWindowPixelRect(WIN_LIST, sel ? C_SEL : C_BG, 9, y + 3, 6, 6);
        AddTextPrinterParameterized3(WIN_LIST, FONT_SMALL, 22, y, sel ? sTxtSel : sTxtNormal, 0, TopazeJournalEntryName(e));
        {
            u8 buf[24];
            const u8 *rt = done ? sText_Done : sText_Todo;
            u32 cur, target;

            if (!done && TopazeJournalEntryProgress(e, &cur, &target))
            {
                u8 *q = PrintNum(buf, cur);

                q = StringCopy(q, sText_Slash);
                PrintNum(q, target);
                rt = buf;
            }
            AddTextPrinterParameterized3(WIN_LIST, FONT_SMALL, 216 - GetStringWidth(FONT_SMALL, rt, 0) - 6, y,
                                         done ? (sel ? sTxtGreenSel : sTxtGreen) : (sel ? sTxtDimSel : sTxtDim), 0, rt);
        }
    }
    // scroll bar
    if (sJ->numEntries > ROWS)
    {
        u8 trackH = ROWS * ROW_H;
        u8 barH = trackH * ROWS / sJ->numEntries;
        u8 barY = (trackH - barH) * sJ->top / (sJ->numEntries - ROWS);

        FillWindowPixelRect(WIN_LIST, C_BOX, 226, 2, 3, trackH);
        FillWindowPixelRect(WIN_LIST, C_GOLD, 226, 2 + barY, 3, barH);
    }
    CopyWindowToVram(WIN_LIST, COPYWIN_GFX);
}

static void DrawDesc(void)
{
    FillWindowPixelBuffer(WIN_DESC, PIXEL_FILL(C_BAR));
    if (sJ->numEntries != 0)
        AddTextPrinterParameterized3(WIN_DESC, FONT_SMALL, 8, 1, sTxtBar, 0, TopazeJournalEntryHint(sJ->entries[sJ->cursor]));
    CopyWindowToVram(WIN_DESC, COPYWIN_GFX);
}

static void LoadTab(void)
{
    sJ->numEntries = TopazeJournalGetEntries(CurSection(), sJ->entries);
    sJ->cursor = 0;
    sJ->top = 0;
}

static void RedrawAll(void)
{
    DrawTab();
    DrawList();
    DrawDesc();
}

static void DrawStatic(void)
{
    DrawHeader();
    PutWindowTilemap(WIN_HEADER);
    PutWindowTilemap(WIN_TAB);
    PutWindowTilemap(WIN_LIST);
    PutWindowTilemap(WIN_DESC);
    RedrawAll();
    CopyWindowToVram(WIN_HEADER, COPYWIN_FULL);
    CopyWindowToVram(WIN_TAB, COPYWIN_FULL);
    CopyWindowToVram(WIN_LIST, COPYWIN_FULL);
    CopyWindowToVram(WIN_DESC, COPYWIN_FULL);
}

static void ChangeTab(s8 dir)
{
    s8 t = sJ->tab + dir;

    if (t < 0 || t >= sJ->numSections)
        return;
    sJ->tab = t;
    LoadTab();
    PlaySE(SE_SELECT);
    RedrawAll();
}

static void MoveCursor(s8 dir)
{
    s8 c = sJ->cursor + dir;

    if (sJ->numEntries == 0 || c < 0 || c >= sJ->numEntries)
        return;
    sJ->cursor = c;
    if (sJ->cursor < sJ->top)
        sJ->top = sJ->cursor;
    else if (sJ->cursor >= sJ->top + ROWS)
        sJ->top = sJ->cursor - ROWS + 1;
    PlaySE(SE_SELECT);
    DrawList();
    DrawDesc();
}

static void Task_Journal(u8 taskId)
{
    switch (sJ->state)
    {
    case 0:
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        SetVBlankCallback(VBlankCB);
        sJ->state = 1;
        break;
    case 1:
        if (gPaletteFade.active)
            return;
        sJ->state = 2;
        break;
    case 2:
        if (JOY_NEW(B_BUTTON) || JOY_NEW(START_BUTTON))
        {
            PlaySE(SE_SELECT);
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            sJ->state = 3;
        }
        else if (JOY_NEW(DPAD_RIGHT) || JOY_NEW(R_BUTTON))
            ChangeTab(1);
        else if (JOY_NEW(DPAD_LEFT) || JOY_NEW(L_BUTTON))
            ChangeTab(-1);
        else if (JOY_REPT(DPAD_DOWN))
            MoveCursor(1);
        else if (JOY_REPT(DPAD_UP))
            MoveCursor(-1);
        break;
    case 3:
        if (gPaletteFade.active)
            return;
        FreeAllWindowBuffers();
        Free(sJ);
        sJ = NULL;
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
    sJ = AllocZeroed(sizeof(struct JournalData));
    sJ->numSections = TopazeJournalGetSections(sJ->sections);
    LoadTab();
    DrawStatic();
    ShowBg(0);
    CreateTask(Task_Journal, 0);
    SetMainCallback2(CB2_Main);
}

// special: opens the screen; the script then does waitstate
void TopazeJournalOpenScreen(void)
{
    SetMainCallback2(CB2_Init);
}
