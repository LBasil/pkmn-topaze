#include "global.h"
#include "constants/layouts.h"
#include "gflib.h"
#include "overworld.h"
#include "script.h"
#include "new_menu_helpers.h"
#include "quest_log.h"
#include "fieldmap.h"
#include "field_camera.h"

struct ConnectionFlags
{
    u8 south:1;
    u8 north:1;
    u8 west:1;
    u8 east:1;
};

COMMON_DATA struct BackupMapLayout VMap = {0};
EWRAM_DATA u16 gBackupMapData[VIRTUAL_MAP_SIZE] = {};
EWRAM_DATA struct MapHeader gMapHeader = {};
EWRAM_DATA struct Camera gCamera = {};
static EWRAM_DATA struct ConnectionFlags gMapConnectionFlags = {};
EWRAM_DATA u8 gGlobalFieldTintMode = QL_TINT_NONE;

static const struct ConnectionFlags sDummyConnectionFlags = {};

static void InitMapLayoutData(struct MapHeader *);
static void InitBackupMapLayoutData(const u16 *, u16, u16);
static void InitBackupMapLayoutConnections(struct MapHeader *);
static void FillSouthConnection(struct MapHeader const *, struct MapHeader const *, s32);
static void FillNorthConnection(struct MapHeader const *, struct MapHeader const *, s32);
static void FillWestConnection(struct MapHeader const *, struct MapHeader const *, s32);
static void FillEastConnection(struct MapHeader const *, struct MapHeader const *, s32);
static void LoadSavedMapView(void);
static const struct MapConnection *GetIncomingConnection(u8, s32, s32);
static bool8 IsPosInIncomingConnectingMap(u8, s32, s32, const struct MapConnection *);
static bool8 IsCoordInIncomingConnectingMap(s32, s32, s32, s32);
static u32 GetAttributeByMetatileIdAndMapLayout(const struct MapLayout *, u16, u8);

#define GetBorderBlockAt(x, y) ({                                                                 \
    u16 block;                                                                                    \
    s32 xprime;                                                                                   \
    s32 yprime;                                                                                   \
                                                                                                  \
    const struct MapLayout *mapLayout = gMapHeader.mapLayout;                                     \
                                                                                                  \
    xprime = x - MAP_OFFSET;                                                                      \
    xprime += 8 * mapLayout->borderWidth;                                                         \
    xprime %= mapLayout->borderWidth;                                                             \
                                                                                                  \
    yprime = y - MAP_OFFSET;                                                                      \
    yprime += 8 * mapLayout->borderHeight;                                                        \
    yprime %= mapLayout->borderHeight;                                                            \
                                                                                                  \
    block = mapLayout->border[xprime + yprime * mapLayout->borderWidth] | MAPGRID_COLLISION_MASK; \
})

#define AreCoordsWithinMapGridBounds(x, y) (x >= 0 && x < VMap.Xsize && y >= 0 && y < VMap.Ysize)

#define GetMapGridBlockAt(x, y) (AreCoordsWithinMapGridBounds(x, y) ? VMap.map[x + VMap.Xsize * y] : GetBorderBlockAt(x, y))

// Masks/shifts for metatile attributes
// This is the format of the data stored in each data/tilesets/*/*/metatile_attributes.bin file
static const u32 sMetatileAttrMasks[METATILE_ATTRIBUTE_COUNT] = {
    [METATILE_ATTRIBUTE_BEHAVIOR]       = 0x000001ff, // Bits 0-8
    [METATILE_ATTRIBUTE_TERRAIN]        = 0x00003e00, // Bits 9-13
    [METATILE_ATTRIBUTE_2]              = 0x0003c000, // Bits 14-17
    [METATILE_ATTRIBUTE_3]              = 0x00fc0000, // Bits 18-23
    [METATILE_ATTRIBUTE_ENCOUNTER_TYPE] = 0x07000000, // Bits 24-26
    [METATILE_ATTRIBUTE_5]              = 0x18000000, // Bits 27-28
    [METATILE_ATTRIBUTE_LAYER_TYPE]     = 0x60000000, // Bits 29-30
    [METATILE_ATTRIBUTE_7]              = 0x80000000  // Bit  31
};

static const u8 sMetatileAttrShifts[METATILE_ATTRIBUTE_COUNT] = {
    [METATILE_ATTRIBUTE_BEHAVIOR]       = 0,
    [METATILE_ATTRIBUTE_TERRAIN]        = 9,
    [METATILE_ATTRIBUTE_2]              = 14,
    [METATILE_ATTRIBUTE_3]              = 18,
    [METATILE_ATTRIBUTE_ENCOUNTER_TYPE] = 24,
    [METATILE_ATTRIBUTE_5]              = 27,
    [METATILE_ATTRIBUTE_LAYER_TYPE]     = 29,
    [METATILE_ATTRIBUTE_7]              = 31
};

const struct MapHeader * GetMapHeaderFromConnection(const struct MapConnection * connection)
{
    return Overworld_GetMapHeaderByGroupAndId(connection->mapGroup, connection->mapNum);
}

void InitMap(void)
{
    InitMapLayoutData(&gMapHeader);
    RunOnLoadMapScript();
}

void InitMapFromSavedGame(void)
{
    InitMapLayoutData(&gMapHeader);
    LoadSavedMapView();
    RunOnLoadMapScript();
}

static void InitMapLayoutData(struct MapHeader * mapHeader)
{
    const struct MapLayout * mapLayout = mapHeader->mapLayout;
    CpuFastFill16(MAPGRID_UNDEFINED, gBackupMapData, sizeof(gBackupMapData));
    VMap.map = gBackupMapData;
    VMap.Xsize = mapLayout->width + MAP_OFFSET_W;
    VMap.Ysize = mapLayout->height + MAP_OFFSET_H;
    AGB_ASSERT_EX(VMap.Xsize * VMap.Ysize <= VIRTUAL_MAP_SIZE, ABSPATH("fieldmap.c"), 158);
    InitBackupMapLayoutData(mapLayout->map, mapLayout->width, mapLayout->height);
    InitBackupMapLayoutConnections(mapHeader);
}

static void InitBackupMapLayoutData(const u16 *map, u16 width, u16 height)
{
    s32 y;
    u16 *dest = VMap.map;
    dest += VMap.Xsize * 7 + MAP_OFFSET;

    for (y = 0; y < height; y++)
    {
        CpuCopy16(map, dest, width * sizeof(u16));
        dest += width + MAP_OFFSET_W;
        map += width;
    }
}

#include "topaze_fog_pairs.h"
#include "topaze_fog_strips.h"
static u32 TopazeFogMetaAttr(u16 id, bool8 *found);
void TopazeLoadFogData(void);
const u16 *TopazeFogMetatile(u16 id);

// Topaze: when the two maps of a connection use different tilesets, the neighbour strip would be
// drawn with the wrong tiles. Replicate the current map's own edge metatiles instead (hard cut, same passability).
static s32 sFogW, sFogH;
static const struct MapLayout *sFogLayout;
static bool8 sFogActive;
static u16 sFogLayoutA;

// Topaze: strip of the neighbour (real shape and collision, drawn with this map's own metatiles), see docs/topaze/fog_strips.py
static const struct TopazeFogStrip *TopazeFindFogStrip(u16 a, u16 b)
{
    u32 i;
    for (i = 0; sTopazeFogStrips[i].layoutA != 0xFFFF; i++)
        if (sTopazeFogStrips[i].layoutA == a && sTopazeFogStrips[i].layoutB == b)
            return &sTopazeFogStrips[i];
    return NULL;
}

static bool8 TopazeIsFogPair(u16 a, u16 b)
{
    u32 i;
    for (i = 0; sTopazeFogPairs[i][0] != 0xFFFF; i++)
        if (sTopazeFogPairs[i][0] == a && sTopazeFogPairs[i][1] == b)
            return TRUE;
    return FALSE;
}

static void TopazeFillFogStrip(s32 dir, const struct TopazeFogStrip *st, const struct MapHeader *cMap, s32 offset)
{
    s32 cw = cMap->mapLayout->width, ch = cMap->mapLayout->height;
    s32 cx, cy, cx0 = 0, cx1 = VMap.Xsize, cy0 = 0, cy1 = VMap.Ysize;

    switch (dir)
    {
    case CONNECTION_WEST: cx1 = MAP_OFFSET; break;
    case CONNECTION_EAST: cx0 = sFogW + MAP_OFFSET; break;
    case CONNECTION_NORTH: cy1 = MAP_OFFSET; break;
    case CONNECTION_SOUTH: cy0 = sFogH + MAP_OFFSET; break;
    }
    for (cy = cy0; cy < cy1; cy++)
        for (cx = cx0; cx < cx1; cx++)
        {
            s32 bx, by, sx, sy;

            switch (dir)
            {
            case CONNECTION_WEST: bx = cw - MAP_OFFSET + cx; by = cy - MAP_OFFSET - offset; break;
            case CONNECTION_EAST: bx = cx - sFogW - MAP_OFFSET; by = cy - MAP_OFFSET - offset; break;
            case CONNECTION_NORTH: bx = cx - MAP_OFFSET - offset; by = ch - MAP_OFFSET + cy; break;
            default: bx = cx - MAP_OFFSET - offset; by = cy - sFogH - MAP_OFFSET; break;
            }
            sx = bx - st->x0;
            sy = by - st->y0;
            if (sx >= 0 && sy >= 0 && sx < st->w && sy < st->h)
                VMap.map[VMap.Xsize * cy + cx] = st->data[sy * st->w + sx];
        }
}

static void InitBackupMapLayoutConnections(struct MapHeader *mapHeader)
{
    s32 count;
    const struct MapConnection *connection;
    s32 i;

    gMapConnectionFlags = sDummyConnectionFlags;

    /*
     * This null pointer check is new to FireRed.  It was kept in
     * Emerald, with the above struct assignment moved to after
     * this check.
     */
    if (mapHeader->connections)
    {
        count = mapHeader->connections->count;
        connection = mapHeader->connections->connections;
        for (i = 0; i < count; i++, connection++)
        {
            struct MapHeader const *cMap = GetMapHeaderFromConnection(connection);
            u32 offset = connection->offset;
            sFogActive = cMap && (TopazeIsFogPair(mapHeader->mapLayoutId, cMap->mapLayoutId) || TopazeFindFogStrip(mapHeader->mapLayoutId, cMap->mapLayoutId) != NULL);
            sFogLayout = mapHeader->mapLayout;
            sFogLayoutA = mapHeader->mapLayoutId;
            sFogW = mapHeader->mapLayout->width;
            sFogH = mapHeader->mapLayout->height;
            if (sFogActive && cMap && TopazeFindFogStrip(mapHeader->mapLayoutId, cMap->mapLayoutId) != NULL)
            {
                // Topaze: the strip covers the whole margin of this side (neighbour cells AND the neighbour's own border)
                TopazeFillFogStrip(connection->direction, TopazeFindFogStrip(mapHeader->mapLayoutId, cMap->mapLayoutId), cMap, offset);
                switch (connection->direction)
                {
                case CONNECTION_SOUTH: gMapConnectionFlags.south = TRUE; break;
                case CONNECTION_NORTH: gMapConnectionFlags.north = TRUE; break;
                case CONNECTION_WEST: gMapConnectionFlags.west = TRUE; break;
                case CONNECTION_EAST: gMapConnectionFlags.east = TRUE; break;
                }
                sFogActive = FALSE;
                continue;
            }
            switch (connection->direction)
            {
            case CONNECTION_SOUTH:
                FillSouthConnection(mapHeader, cMap, offset);
                gMapConnectionFlags.south = TRUE;
                break;
            case CONNECTION_NORTH:
                FillNorthConnection(mapHeader, cMap, offset);
                gMapConnectionFlags.north = TRUE;
                break;
            case CONNECTION_WEST:
                FillWestConnection(mapHeader, cMap, offset);
                gMapConnectionFlags.west = TRUE;
                break;
            case CONNECTION_EAST:
                FillEastConnection(mapHeader, cMap, offset);
                gMapConnectionFlags.east = TRUE;
                break;
            }
            sFogActive = FALSE;
        }
    }
}

static void FillConnection(s32 x, s32 y, const struct MapHeader *connectedMapHeader, s32 x2, s32 y2, s32 width, s32 height)
{
    s32 i;
    const u16 *src;
    u16 *dest;
    s32 mapWidth;

    if (sFogActive)
    {
        // Topaze: neighbour strip of a different tileset -> cannot draw the neighbour's tiles.
        // A cell is walkable only if the nearest edge cell of this map AND the real neighbour cell are both
        // walkable; walkable cells repeat the edge metatile (a road keeps looking like a road), the others
        // show the map's own border look and block, so what you see always matches where you can go.
        s32 nW = connectedMapHeader->mapLayout->width;
        s32 nH = connectedMapHeader->mapLayout->height;
        const struct TopazeFogStrip *strip = TopazeFindFogStrip(sFogLayoutA, connectedMapHeader->mapLayoutId);

        for (i = 0; i < height; i++)
        {
            s32 j;
            s32 cy = y + i;
            s32 ey = cy;

            if (ey < MAP_OFFSET) ey = MAP_OFFSET;
            if (ey > MAP_OFFSET + sFogH - 1) ey = MAP_OFFSET + sFogH - 1;
            dest = &VMap.map[VMap.Xsize * cy + x];
            for (j = 0; j < width; j++)
            {
                s32 cx = x + j;
                s32 ex = cx;
                u16 edge;
                bool8 open;

                if (ex < MAP_OFFSET) ex = MAP_OFFSET;
                if (ex > MAP_OFFSET + sFogW - 1) ex = MAP_OFFSET + sFogW - 1;
                if (strip)
                {
                    s32 sx = x2 + j - strip->x0;
                    s32 sy = y2 + i - strip->y0;

                    if (sx >= 0 && sy >= 0 && sx < strip->w && sy < strip->h)
                    {
                        dest[j] = strip->data[sy * strip->w + sx];
                        continue;
                    }
                }
                edge = VMap.map[VMap.Xsize * ey + ex];
                open = ((edge & MAPGRID_COLLISION_MASK) == 0);
                if (open)
                {
                    s32 nx = x2 + j;
                    s32 ny = y2 + i;

                    if (nx < 0 || ny < 0 || nx >= nW || ny >= nH
                     || (connectedMapHeader->mapLayout->map[nW * ny + nx] & MAPGRID_COLLISION_MASK) != 0)
                        open = FALSE;
                }
                if (open)
                    dest[j] = edge;
                else
                {
                    s32 bx = (cx - MAP_OFFSET + 8 * sFogLayout->borderWidth) % sFogLayout->borderWidth;
                    s32 by = (cy - MAP_OFFSET + 8 * sFogLayout->borderHeight) % sFogLayout->borderHeight;
                    u16 border = sFogLayout->border[bx + by * sFogLayout->borderWidth] & MAPGRID_METATILE_ID_MASK;

                    dest[j] = border | MAPGRID_COLLISION_MASK | (edge & MAPGRID_ELEVATION_MASK);
                }
            }
        }
        return;
    }
    mapWidth = connectedMapHeader->mapLayout->width;
    src = &connectedMapHeader->mapLayout->map[mapWidth * y2 + x2];
    dest = &VMap.map[VMap.Xsize * y + x];

    for (i = 0; i < height; i++)
    {
        CpuCopy16(src, dest, width * 2);
        dest += VMap.Xsize;
        src += mapWidth;
    }
}

static void FillSouthConnection(struct MapHeader const *mapHeader, struct MapHeader const *connectedMapHeader, s32 offset)
{
    s32 x, y;
    s32 x2;
    s32 width;
    s32 cWidth;

    if (connectedMapHeader)
    {
        cWidth = connectedMapHeader->mapLayout->width;
        x = offset + MAP_OFFSET;
        y = mapHeader->mapLayout->height + MAP_OFFSET;
        if (x < 0)
        {
            x2 = -x;
            x += cWidth;
            if (x < VMap.Xsize)
                width = x;
            else
                width = VMap.Xsize;
            x = 0;
        }
        else
        {
            x2 = 0;
            if (x + cWidth < VMap.Xsize)
                width = cWidth;
            else
                width = VMap.Xsize - x;
        }

        FillConnection(
            x, y,
            connectedMapHeader,
            x2, /*y2*/ 0,
            width, /*height*/ MAP_OFFSET);
    }
}

static void FillNorthConnection(struct MapHeader const *mapHeader, struct MapHeader const *connectedMapHeader, s32 offset)
{
    s32 x;
    s32 x2, y2;
    s32 width;
    s32 cWidth, cHeight;

    if (connectedMapHeader)
    {
        cWidth = connectedMapHeader->mapLayout->width;
        cHeight = connectedMapHeader->mapLayout->height;
        x = offset + MAP_OFFSET;
        y2 = cHeight - MAP_OFFSET;
        if (x < 0)
        {
            x2 = -x;
            x += cWidth;
            if (x < VMap.Xsize)
                width = x;
            else
                width = VMap.Xsize;
            x = 0;
        }
        else
        {
            x2 = 0;
            if (x + cWidth < VMap.Xsize)
                width = cWidth;
            else
                width = VMap.Xsize - x;
        }

        FillConnection(
            x, /*y*/ 0,
            connectedMapHeader,
            x2, y2,
            width, /*height*/ MAP_OFFSET);

    }
}

static void FillWestConnection(struct MapHeader const *mapHeader, struct MapHeader const *connectedMapHeader, s32 offset)
{
    s32 y;
    s32 x2, y2;
    s32 height;
    s32 cWidth, cHeight;
    if (connectedMapHeader)
    {
        cWidth = connectedMapHeader->mapLayout->width;
        cHeight = connectedMapHeader->mapLayout->height;
        y = offset + MAP_OFFSET;
        x2 = cWidth - MAP_OFFSET;
        if (y < 0)
        {
            y2 = -y;
            if (y + cHeight < VMap.Ysize)
                height = y + cHeight;
            else
                height = VMap.Ysize;
            y = 0;
        }
        else
        {
            y2 = 0;
            if (y + cHeight < VMap.Ysize)
                height = cHeight;
            else
                height = VMap.Ysize - y;
        }

        FillConnection(
            /*x*/ 0, y,
            connectedMapHeader,
            x2, y2,
            /*width*/ MAP_OFFSET, height);
    }
}

static void FillEastConnection(struct MapHeader const *mapHeader, struct MapHeader const *connectedMapHeader, s32 offset)
{
    s32 x, y;
    s32 y2;
    s32 height;
    s32 cHeight;
    if (connectedMapHeader)
    {
        cHeight = connectedMapHeader->mapLayout->height;
        x = mapHeader->mapLayout->width + MAP_OFFSET;
        y = offset + MAP_OFFSET;
        if (y < 0)
        {
            y2 = -y;
            if (y + cHeight < VMap.Ysize)
                height = y + cHeight;
            else
                height = VMap.Ysize;
            y = 0;
        }
        else
        {
            y2 = 0;
            if (y + cHeight < VMap.Ysize)
                height = cHeight;
            else
                height = VMap.Ysize - y;
        }

        FillConnection(
            x, y,
            connectedMapHeader,
            /*x2*/ 0, y2,
            /*width*/ MAP_OFFSET + 1, height);
    }
}

u8 MapGridGetElevationAt(s32 x, s32 y)
{
    u16 block = GetMapGridBlockAt(x, y);

    if (block == MAPGRID_UNDEFINED)
        return 0;

    return block >> MAPGRID_ELEVATION_SHIFT;
}

u8 MapGridGetCollisionAt(s32 x, s32 y)
{
    u16 block = GetMapGridBlockAt(x, y);

    if (block == MAPGRID_UNDEFINED)
        return TRUE;

    return (block & MAPGRID_COLLISION_MASK) >> MAPGRID_COLLISION_SHIFT;
}

u32 MapGridGetMetatileIdAt(s32 x, s32 y)
{
    u16 block = GetMapGridBlockAt(x, y);

    if (block == MAPGRID_UNDEFINED)
        return GetBorderBlockAt(x, y) & MAPGRID_METATILE_ID_MASK;

    return block & MAPGRID_METATILE_ID_MASK;
}

u32 ExtractMetatileAttribute(u32 attributes, u8 attributeType)
{
    if (attributeType >= METATILE_ATTRIBUTE_COUNT) // Check for METATILE_ATTRIBUTES_ALL
        return attributes;

    return (attributes & sMetatileAttrMasks[attributeType]) >> sMetatileAttrShifts[attributeType];
}

u32 MapGridGetMetatileAttributeAt(s16 x, s16 y, u8 attributeType)
{
    u16 metatileId = MapGridGetMetatileIdAt(x, y);
    return GetAttributeByMetatileIdAndMapLayout(gMapHeader.mapLayout, metatileId, attributeType);
}

u32 MapGridGetMetatileBehaviorAt(s16 x, s16 y)
{
    return MapGridGetMetatileAttributeAt(x, y, METATILE_ATTRIBUTE_BEHAVIOR);
}

u8 MapGridGetMetatileLayerTypeAt(s16 x, s16 y)
{
    return MapGridGetMetatileAttributeAt(x, y, METATILE_ATTRIBUTE_LAYER_TYPE);
}

void MapGridSetMetatileIdAt(s32 x, s32 y, u16 metatile)
{
    s32 i;
    if (AreCoordsWithinMapGridBounds(x, y))
    {
        i = x + y * VMap.Xsize;
        VMap.map[i] = (VMap.map[i] & MAPGRID_ELEVATION_MASK) | (metatile & ~MAPGRID_ELEVATION_MASK);
    }
}

void MapGridSetMetatileEntryAt(s32 x, s32 y, u16 metatile)
{
    s32 i;
    if (AreCoordsWithinMapGridBounds(x, y))
    {
        i = x + VMap.Xsize * y;
        VMap.map[i] = metatile;
    }
}

void MapGridSetMetatileImpassabilityAt(s32 x, s32 y, bool32 impassable)
{
    if (AreCoordsWithinMapGridBounds(x, y))
    {
        if (impassable)
            VMap.map[x + VMap.Xsize * y] |= MAPGRID_COLLISION_MASK;
        else
            VMap.map[x + VMap.Xsize * y] &= ~MAPGRID_COLLISION_MASK;
    }
}

static u32 GetAttributeByMetatileIdAndMapLayout(const struct MapLayout *mapLayout, u16 metatile, u8 attributeType)
{
    const u32 * attributes;
    bool8 fogFound;
    u32 fogAttr = TopazeFogMetaAttr(metatile, &fogFound);

    if (fogFound && mapLayout == gMapHeader.mapLayout)
        return ExtractMetatileAttribute(fogAttr, attributeType);
    if (metatile < NUM_METATILES_IN_PRIMARY)
    {
        attributes = mapLayout->primaryTileset->metatileAttributes;
        return ExtractMetatileAttribute(attributes[metatile], attributeType);
    }
    else if (metatile < NUM_METATILES_TOTAL)
    {
        attributes = mapLayout->secondaryTileset->metatileAttributes;
        return ExtractMetatileAttribute(attributes[metatile - NUM_METATILES_IN_PRIMARY], attributeType);
    }
    else
    {
        return 0xFF;
    }
}

void SaveMapView(void)
{
    s32 i, j;
    s32 x, y;
    u16 *mapView;
    s32 width;
    mapView = gSaveBlock2Ptr->mapView;
    width = VMap.Xsize;
    x = gSaveBlock1Ptr->pos.x;
    y = gSaveBlock1Ptr->pos.y;
    for (i = y; i < y + MAP_OFFSET_H; i++)
    {
        for (j = x; j < x + MAP_OFFSET_W; j++)
            *mapView++ = gBackupMapData[width * i + j];
    }
}

static bool32 SavedMapViewIsEmpty(void)
{
    u16 i;
    u32 marker = 0;

#ifndef UBFIX
    // BUG: This loop extends past the bounds of the mapView array. Its size is only 0x100.
    for (i = 0; i < 0x200; i++)
        marker |= gSaveBlock2Ptr->mapView[i];
#else
    for (i = 0; i < NELEMS(gSaveBlock2Ptr->mapView); i++)
        marker |= gSaveBlock2Ptr->mapView[i];
#endif

    if (marker == 0)
        return TRUE;
    else
        return FALSE;
}

static void ClearSavedMapView(void)
{
    CpuFill16(0, gSaveBlock2Ptr->mapView, sizeof(gSaveBlock2Ptr->mapView));
}

static void LoadSavedMapView(void)
{
    s32 i, j;
    s32 x, y;
    u16 *mapView;
    s32 width;
    mapView = gSaveBlock2Ptr->mapView;
    if (!SavedMapViewIsEmpty())
    {
        width = VMap.Xsize;
        x = gSaveBlock1Ptr->pos.x;
        y = gSaveBlock1Ptr->pos.y;
        for (i = y; i < y + MAP_OFFSET_H; i++)
        {
            for (j = x; j < x + MAP_OFFSET_W; j++)
            {
                gBackupMapData[j + width * i] = *mapView;
                mapView++;
            }
        }
        ClearSavedMapView();
    }
}

static void MoveMapViewToBackup(u8 direction)
{
    s32 width;
    u16 *mapView;
    s32 x0, y0;
    s32 x2, y2;
    u16 *src, *dest;
    s32 srci, desti;
    s32 r9, r8;
    s32 x, y;
    s32 i, j;
    mapView = gSaveBlock2Ptr->mapView;
    width = VMap.Xsize;
    r9 = 0;
    r8 = 0;
    x0 = gSaveBlock1Ptr->pos.x;
    y0 = gSaveBlock1Ptr->pos.y;
    x2 = 15;
    y2 = 14;
    switch (direction)
    {
    case CONNECTION_NORTH:
        y0 += 1;
        y2 = MAP_OFFSET_H - 1;
        break;
    case CONNECTION_SOUTH:
        r8 = 1;
        y2 = MAP_OFFSET_H - 1;
        break;
    case CONNECTION_WEST:
        x0 += 1;
        x2 = MAP_OFFSET_W - 1;
        break;
    case CONNECTION_EAST:
        r9 = 1;
        x2 = MAP_OFFSET_W - 1;
        break;
    }
    for (y = 0; y < y2; y++)
    {
        i = 0;
        j = 0;
        for (x = 0; x < x2; x++)
        {
            desti = width * (y + y0);
            srci = (y + r8) * MAP_OFFSET_W + r9;
            src = &mapView[srci + i];
            dest = &gBackupMapData[x0 + desti + j];
            *dest = *src;
            i++;
            j++;
        }
    }
    ClearSavedMapView();
}

s32 GetMapBorderIdAt(s32 x, s32 y)
{
    if (GetMapGridBlockAt(x, y) == MAPGRID_UNDEFINED)
        return CONNECTION_INVALID;

    if (x >= VMap.Xsize - (MAP_OFFSET + 1))
    {
        if (!gMapConnectionFlags.east)
            return CONNECTION_INVALID;

        return CONNECTION_EAST;
    }

    if (x < MAP_OFFSET)
    {
        if (!gMapConnectionFlags.west)
            return CONNECTION_INVALID;

        return CONNECTION_WEST;
    }

    if (y >= VMap.Ysize - MAP_OFFSET)
    {
        if (!gMapConnectionFlags.south)
            return CONNECTION_INVALID;

        return CONNECTION_SOUTH;
    }

    if (y < MAP_OFFSET)
    {
        if (!gMapConnectionFlags.north)
            return CONNECTION_INVALID;

        return CONNECTION_NORTH;
    }

    return CONNECTION_NONE;
}

static s32 GetPostCameraMoveMapBorderId(s32 x, s32 y)
{
    return GetMapBorderIdAt(gSaveBlock1Ptr->pos.x + MAP_OFFSET + x, gSaveBlock1Ptr->pos.y + MAP_OFFSET + y);
}

bool32 CanCameraMoveInDirection(s32 direction)
{
    s32 x, y;
    x = gSaveBlock1Ptr->pos.x + MAP_OFFSET + gDirectionToVectors[direction].x;
    y = gSaveBlock1Ptr->pos.y + MAP_OFFSET + gDirectionToVectors[direction].y;

    if (GetMapBorderIdAt(x, y) == CONNECTION_INVALID)
        return FALSE;

    return TRUE;
}

static void SetPositionFromConnection(const struct MapConnection *connection, int direction, s32 x, s32 y)
{
    struct MapHeader const *mapHeader;
    mapHeader = GetMapHeaderFromConnection(connection);
    switch (direction)
    {
    case CONNECTION_EAST:
        gSaveBlock1Ptr->pos.x = -x;
        gSaveBlock1Ptr->pos.y -= connection->offset;
        break;
    case CONNECTION_WEST:
        gSaveBlock1Ptr->pos.x = mapHeader->mapLayout->width;
        gSaveBlock1Ptr->pos.y -= connection->offset;
        break;
    case CONNECTION_SOUTH:
        gSaveBlock1Ptr->pos.x -= connection->offset;
        gSaveBlock1Ptr->pos.y = -y;
        break;
    case CONNECTION_NORTH:
        gSaveBlock1Ptr->pos.x -= connection->offset;
        gSaveBlock1Ptr->pos.y = mapHeader->mapLayout->height;
        break;
    }
}

extern bool8 gTopazeGfxFreeze;
extern void TopazeFlushDma3Requests(void);
extern void TransferTilesetAnimsBuffer(void);

// ---- Topaze: palette ramps at map junctions (generated data: docs/topaze/ramp_gen.py) ----
#include "topaze_ramps.h"
#include "field_weather.h"
static EWRAM_DATA u16 sRampBase[13 * 16] = {0};   // palettes as loaded from the tilesets (before any ramp)
static EWRAM_DATA u32 sRampKey = 0xFFFFFFFF;

static const struct TopazeRamp *TopazeFindRamp(u16 layoutId)
{
    u32 i;
    for (i = 0; sTopazeRamps[i].layoutId != 0xFFFF; i++)
        if (sTopazeRamps[i].layoutId == layoutId)
            return &sTopazeRamps[i];
    return NULL;
}

static s32 sTopazeEdgeDepth, sTopazeEdgeExcess; // parts of the last TopazeEdgeDist result

static s32 TopazeEdgeDist(u8 dir)
{
    s32 d;
    s32 w = gMapHeader.mapLayout->width, h = gMapHeader.mapLayout->height;
    s32 x = gSaveBlock1Ptr->pos.x, y = gSaveBlock1Ptr->pos.y;

    s32 conDir = (dir == 0) ? CONNECTION_NORTH : (dir == 1) ? CONNECTION_SOUTH : (dir == 2) ? CONNECTION_WEST : CONNECTION_EAST;
    s32 i, excess = 0;

    switch (dir)
    {
    case 0: d = y; break;
    case 1: d = h - 1 - y; break;
    case 2: d = x; break;
    default: d = w - 1 - x; break;
    }
    if (d < 0) d = 0;
    // along the edge: only the stretch that really touches the neighbour counts (outside it the neighbour is not on screen)
    if (gMapHeader.connections)
    {
        for (i = 0; i < gMapHeader.connections->count; i++)
        {
            const struct MapConnection *c = &gMapHeader.connections->connections[i];

            if (c->direction == conDir)
            {
                const struct MapHeader *n = GetMapHeaderFromConnection(c);
                s32 p = (dir < 2) ? x : y;
                s32 lo = c->offset;
                s32 hi = c->offset + ((dir < 2) ? n->mapLayout->width : n->mapLayout->height) - 1;

                if (p < lo) excess = lo - p;
                else if (p > hi) excess = p - hi;
                break;
            }
        }
    }
    sTopazeEdgeDepth = d;
    sTopazeEdgeExcess = excess;
    return d + excess;
}

static u8 TopazeRampStep(const struct TopazeRampEnd *e)
{
    s32 d = TopazeEdgeDist(e->dir);

    if (d >= TOPAZE_RAMP_ZONE) return 0;
    if (d <= 7) return 16;      // the neighbour strip (<= 7 cells deep on screen) is drawn with the fully ramped colours
    return ((TOPAZE_RAMP_ZONE - d) * 16) / (TOPAZE_RAMP_ZONE - 7);
}

// ---- Topaze: per-map overlays for the neighbour strips (generated: docs/topaze/fog_strips.py) ----
// tiles: written into VRAM slots no tile of this map uses; metatiles: definitions replaced at unused ids; palettes: free banks.
static EWRAM_DATA u8 sFogMetaIdx[384] = {0};
static EWRAM_DATA const u16 *sFogMetaEnts = NULL;
static EWRAM_DATA const u32 *sFogMetaAttr = NULL;
static EWRAM_DATA bool8 sFogMetaOn = FALSE;
static EWRAM_DATA bool8 sFogPalWas = FALSE;

const u16 *TopazeFogMetatile(u16 id)
{
    if (!sFogMetaOn || id < 640 || id >= 1024 || sFogMetaIdx[id - 640] == 0xFF)
        return NULL;
    return sFogMetaEnts + sFogMetaIdx[id - 640] * 8;
}

static u32 TopazeFogMetaAttr(u16 id, bool8 *found)
{
    *found = FALSE;
    if (!sFogMetaOn || id < 640 || id >= 1024 || sFogMetaIdx[id - 640] == 0xFF)
        return 0;
    *found = TRUE;
    return sFogMetaAttr[sFogMetaIdx[id - 640]];
}

bool8 TopazeHasFog(u16 lid)
{
    const struct TopazeFogTiles *t;
    const struct TopazeFogMetas *m;

    for (t = sTopazeFogTiles; t->layoutId != 0xFFFF; t++)
        if (t->layoutId == lid)
            return TRUE;
    for (m = sTopazeFogMetas; m->layoutId != 0xFFFF; m++)
        if (m->layoutId == lid)
            return TRUE;
    return FALSE;
}

void TopazeLoadFogData(void)
{
    u32 i;
    u16 lid = gMapHeader.mapLayoutId;
    const struct TopazeFogTiles *t;
    const struct TopazeFogMetas *m;

    sFogMetaOn = FALSE;
    for (m = sTopazeFogMetas; m->layoutId != 0xFFFF; m++)
    {
        if (m->layoutId != lid)
            continue;
        for (i = 0; i < 384; i++)
            sFogMetaIdx[i] = 0xFF;
        for (i = 0; i < m->n; i++)
            sFogMetaIdx[m->ids[i] - 640] = i;
        sFogMetaEnts = m->ents;
        sFogMetaAttr = m->attrs;
        sFogMetaOn = TRUE;
        break;
    }
    for (t = sTopazeFogTiles; t->layoutId != 0xFFFF; t++)
    {
        if (t->layoutId != lid)
            continue;
        for (i = 0; i < t->nRuns; i++)
            LoadBgTiles(2, t->data + t->runs[i].offset, t->runs[i].count * 32, t->runs[i].first);
        break;
    }
}

static s32 TopazeFogSelect(void)
{
    s32 i, best = -1, bestD = 99;

    if (!gMapHeader.mapLayout)
        return -1;
    for (i = 0; sTopazeFogStrips[i].layoutA != 0xFFFF; i++)
    {
        s32 d;
        if (sTopazeFogStrips[i].layoutA != gMapHeader.mapLayoutId || sTopazeFogStrips[i].nPal == 0)
            continue;
        d = TopazeEdgeDist(sTopazeFogStrips[i].dir);
        // the strip is on screen as soon as its depth AND the distance along the edge are within the view (7 cells), not only when their sum is small
        if (sTopazeEdgeDepth > 7 || sTopazeEdgeExcess > 7)
            continue;
        if (d <= bestD)
        {
            bestD = d;
            best = i;
        }
    }
    return best;
}

void TopazeRampApply(bool8 force)
{
    const struct TopazeRamp *r = gMapHeader.mapLayout ? TopazeFindRamp(gMapHeader.mapLayoutId) : NULL;
    s32 sel = TopazeFogSelect();
    u8 q[3] = {0, 0, 0};
    u32 key = 0;
    u32 i, k;

    if (r != NULL)
    {
        for (i = 0; i < r->n; i++)
            q[i] = TopazeRampStep(&r->e[i]);
        // an end that is fully ramped (strip of that neighbour on screen) hides the others: the neighbour's strip is drawn with that end only
        if (r->n > 1)
        {
            u8 q0[3] = {q[0], q[1], q[2]};
            for (i = 0; i < r->n; i++)
            {
                u32 mx = 0;
                for (k = 0; k < r->n; k++)
                    if (k != i && q0[k] > mx) mx = q0[k];
                q[i] = (q0[i] * (16 - mx)) / 16;
            }
        }
        for (i = 0; i < r->n; i++)
            key = key * 17 + q[i];
        key += 1 + r->layoutId * 7;
    }
    key = key * 128 + (sel + 1);
    if (!force && key == sRampKey)
        return;
    sRampKey = key;
    if (r == NULL && sel < 0 && !sFogPalWas && !force)
        return;
    sFogPalWas = (sel >= 0);
    for (i = 0; i < 13 * 16; i++)
    {
        s32 c[3], o[3];
        u16 base = sRampBase[i];

        if ((i & 15) == 0 || r == NULL)
        {
            // colour 0 of each palette is transparent: leave it alone
            gPlttBufferUnfaded[i] = base;
            continue;
        }
        o[0] = base & 31; o[1] = (base >> 5) & 31; o[2] = (base >> 10) & 31;
        c[0] = o[0]; c[1] = o[1]; c[2] = o[2];
        for (k = 0; k < r->n; k++)
        {
            u32 ch;
            if (q[k] == 0) continue;
            for (ch = 0; ch < 3; ch++)
            {
                s32 v = ((o[ch] * r->e[k].gain[ch]) >> 8) + r->e[k].bias[ch];
                if (v < 0) v = 0;
                if (v > 31) v = 31;
                c[ch] += ((v - o[ch]) * q[k]) / 16;
            }
        }
        for (k = 0; k < 3; k++)
        {
            if (c[k] < 0) c[k] = 0;
            if (c[k] > 31) c[k] = 31;
        }
        gPlttBufferUnfaded[i] = c[0] | (c[1] << 5) | (c[2] << 10);
    }
    if (sel >= 0)
    {
        // free palette banks (not used by any tile of this map) receive the colours of the neighbour strip
        const struct TopazeFogStrip *st = &sTopazeFogStrips[sel];
        for (i = 0; i < st->nPal; i++)
            for (k = 0; k < 15; k++)
                gPlttBufferUnfaded[st->palBank[i] * 16 + 1 + k] = st->palCol[i * 15 + k];
    }
    for (i = 0; i < 13; i++)
    {
        CpuCopy16(&gPlttBufferUnfaded[i * 16], &gPlttBufferFaded[i * 16], 32);
        ApplyWeatherGammaShiftToPal(i);
    }
}

bool8 gCameraRedrawAll; // Topaze: set when a connection crossing swapped the primary tileset

bool8 CameraMove(s32 x, s32 y)
{
    s32 direction;
    const struct MapConnection *connection;
    s32 old_x, old_y;
    gCamera.active = FALSE;
    direction = GetPostCameraMoveMapBorderId(x, y);
    if (direction == CONNECTION_NONE || direction == CONNECTION_INVALID)
    {
        gSaveBlock1Ptr->pos.x += x;
        gSaveBlock1Ptr->pos.y += y;
        TopazeRampApply(FALSE);
    }
    else
    {
        SaveMapView();
        old_x = gSaveBlock1Ptr->pos.x;
        old_y = gSaveBlock1Ptr->pos.y;
        connection = GetIncomingConnection(direction, gSaveBlock1Ptr->pos.x, gSaveBlock1Ptr->pos.y);
        SetPositionFromConnection(connection, direction, x, y);
        LoadMapFromCameraTransition(connection->mapGroup, connection->mapNum);
        gCamera.active = TRUE;
        gCamera.x = old_x - gSaveBlock1Ptr->pos.x;
        gCamera.y = old_y - gSaveBlock1Ptr->pos.y;
        gSaveBlock1Ptr->pos.x += x;
        gSaveBlock1Ptr->pos.y += y;
        TopazeRampApply(TRUE);
        if (gCameraRedrawAll)
        {
            // Topaze: the saved view holds metatile ids of the old tilesets; do not paste it over the new map.
            // The caller (CameraUpdate) still shifts the tilemap ring and draws the new slice for this step,
            // so the whole view must be drawn from the position BEFORE the step (else one column is off).
            gCameraRedrawAll = FALSE;
            gSaveBlock1Ptr->pos.x -= x;
            gSaveBlock1Ptr->pos.y -= y;
            DrawWholeMapView();
            gSaveBlock1Ptr->pos.x += x;
            gSaveBlock1Ptr->pos.y += y;
        }
        else
            MoveMapViewToBackup(direction);
        if (gTopazeGfxFreeze)
        {
            // Topaze: push tiles, tilemap and palettes to the screen in one go, inside a single vblank
            VBlankIntrWait();
            REG_DISPCNT |= DISPCNT_FORCED_BLANK;
            DoScheduledBgTilemapCopiesToVram();
            TopazeFlushDma3Requests();
            TransferPlttBuffer();
            TransferTilesetAnimsBuffer();
            REG_DISPCNT &= ~DISPCNT_FORCED_BLANK;
            gTopazeGfxFreeze = FALSE;
        }
    }
    return gCamera.active;
}

const struct MapConnection *GetIncomingConnection(u8 direction, s32 x, s32 y)
{
    s32 count;
    const struct MapConnection *connection;
    const struct MapConnections *connections = gMapHeader.connections;
    s32 i;

#ifdef UBFIX // UB: Multiple possible null dereferences
    if (connections == NULL || connections->connections == NULL)
        return NULL;
#endif
    count = connections->count;
    connection = connections->connections;
    for (i = 0; i < count; i++, connection++)
    {
        if (connection->direction == direction && IsPosInIncomingConnectingMap(direction, x, y, connection) == TRUE)
            return connection;
    }
    return NULL;

}

static bool8 IsPosInIncomingConnectingMap(u8 direction, s32 x, s32 y, const struct MapConnection *connection)
{
    struct MapHeader const *mapHeader;
    mapHeader = GetMapHeaderFromConnection(connection);
    switch (direction)
    {
    case CONNECTION_SOUTH:
    case CONNECTION_NORTH:
        return IsCoordInIncomingConnectingMap(x, gMapHeader.mapLayout->width, mapHeader->mapLayout->width, connection->offset);
    case CONNECTION_WEST:
    case CONNECTION_EAST:
        return IsCoordInIncomingConnectingMap(y, gMapHeader.mapLayout->height, mapHeader->mapLayout->height, connection->offset);
    }
    return FALSE;
}

static bool8 IsCoordInIncomingConnectingMap(s32 coord, s32 srcMax, s32 destMax, s32 offset)
{
    s32 offset2 = max(offset, 0);

    if (destMax + offset < srcMax)
        srcMax = destMax + offset;

    if (offset2 <= coord && coord <= srcMax)
        return TRUE;

    return FALSE;
}

static bool32 IsCoordInConnectingMap(s32 coord, s32 max)
{
    if (coord >= 0 && coord < max)
        return TRUE;

    return FALSE;
}

static s32 IsPosInConnectingMap(const struct MapConnection *connection, s32 x, s32 y)
{
    struct MapHeader const *mapHeader;
    mapHeader = GetMapHeaderFromConnection(connection);
    switch (connection->direction)
    {
    case CONNECTION_SOUTH:
    case CONNECTION_NORTH:
        return IsCoordInConnectingMap(x - connection->offset, mapHeader->mapLayout->width);
    case CONNECTION_WEST:
    case CONNECTION_EAST:
        return IsCoordInConnectingMap(y - connection->offset, mapHeader->mapLayout->height);
    }
    return FALSE;
}

const struct MapConnection *GetMapConnectionAtPos(s16 x, s16 y)
{
    s32 count;
    const struct MapConnection *connection;
    s32 i;
    u8 direction;
    if (!gMapHeader.connections)
    {
        return NULL;
    }
    else
    {
        count = gMapHeader.connections->count;
        connection = gMapHeader.connections->connections;
        for (i = 0; i < count; i++, connection++)
        {
            direction = connection->direction;
            if ((direction == CONNECTION_DIVE || direction == CONNECTION_EMERGE)
                || (direction == CONNECTION_NORTH && y > MAP_OFFSET - 1)
                || (direction == CONNECTION_SOUTH && y < gMapHeader.mapLayout->height + MAP_OFFSET)
                || (direction == CONNECTION_WEST && x > MAP_OFFSET - 1)
                || (direction == CONNECTION_EAST && x < gMapHeader.mapLayout->width + MAP_OFFSET))
            {
                continue;
            }

            if (IsPosInConnectingMap(connection, x - MAP_OFFSET, y - MAP_OFFSET) == TRUE)
                return connection;
        }
    }
    return NULL;
}

void SetCameraFocusCoords(u16 x, u16 y)
{
    gSaveBlock1Ptr->pos.x = x - MAP_OFFSET;
    gSaveBlock1Ptr->pos.y = y - MAP_OFFSET;
}

void GetCameraFocusCoords(u16 *x, u16 *y)
{
    *x = gSaveBlock1Ptr->pos.x + MAP_OFFSET;
    *y = gSaveBlock1Ptr->pos.y + MAP_OFFSET;
}

// Unused
static void SetCameraCoords(u16 x, u16 y)
{
    gSaveBlock1Ptr->pos.x = x;
    gSaveBlock1Ptr->pos.y = y;
}

void GetCameraCoords(u16 *x, u16 *y)
{
    *x = gSaveBlock1Ptr->pos.x;
    *y = gSaveBlock1Ptr->pos.y;
}

static void CopyTilesetToVram(struct Tileset const *tileset, u16 numTiles, u16 offset)
{
    if (tileset)
    {
        if (!tileset->isCompressed)
            LoadBgTiles(2, tileset->tiles, numTiles * 32, offset);
        else
            DecompressAndCopyTileDataToVram2(2, tileset->tiles, numTiles * 32, offset, 0);
    }
}

static void CopyTilesetToVramUsingHeap(struct Tileset const *tileset, u16 numTiles, u16 offset)
{
    if (tileset)
    {
        if (!tileset->isCompressed)
            LoadBgTiles(2, tileset->tiles, numTiles * 32, offset);
        else
            DecompressAndLoadBgGfxUsingHeap2(2, tileset->tiles, numTiles * 32, offset, 0);
    }
}

static void ApplyGlobalTintToPaletteEntries(u16 offset, u16 size)
{
    switch (gGlobalFieldTintMode)
    {
    case QL_TINT_NONE:
        return;
    case QL_TINT_GRAYSCALE:
        TintPalette_GrayScale(&gPlttBufferUnfaded[offset], size);
        break;
    case QL_TINT_SEPIA:
        TintPalette_SepiaTone(&gPlttBufferUnfaded[offset], size);
        break;
    case QL_TINT_BACKUP_GRAYSCALE:
        QuestLog_BackUpPalette(offset, size);
        TintPalette_GrayScale(&gPlttBufferUnfaded[offset], size);
        break;
    default:
        return;
    }
    CpuCopy16(&gPlttBufferUnfaded[offset], &gPlttBufferFaded[offset], PLTT_SIZEOF(size));
}

void ApplyGlobalTintToPaletteSlot(u8 slot, u8 count)
{
    switch (gGlobalFieldTintMode)
    {
    case QL_TINT_NONE:
        return;
    case QL_TINT_GRAYSCALE:
        TintPalette_GrayScale(&gPlttBufferUnfaded[BG_PLTT_ID(slot)], count * 16);
        break;
    case QL_TINT_SEPIA:
        TintPalette_SepiaTone(&gPlttBufferUnfaded[BG_PLTT_ID(slot)], count * 16);
        break;
    case QL_TINT_BACKUP_GRAYSCALE:
        QuestLog_BackUpPalette(BG_PLTT_ID(slot), count * 16);
        TintPalette_GrayScale(&gPlttBufferUnfaded[BG_PLTT_ID(slot)], count * 16);
        break;
    default:
        return;
    }
    CpuFastCopy(&gPlttBufferUnfaded[BG_PLTT_ID(slot)], &gPlttBufferFaded[BG_PLTT_ID(slot)], count * PLTT_SIZE_4BPP);
}

static void LoadTilesetPalette(struct Tileset const *tileset, u16 destOffset, u16 size)
{
    u16 black = RGB_BLACK;

    if (tileset)
    {
        if (tileset->isSecondary == FALSE)
        {
            LoadPalette(&black, destOffset, PLTT_SIZEOF(1));
            LoadPalette(tileset->palettes[0] + 1, destOffset + 1, size - PLTT_SIZEOF(1));
            ApplyGlobalTintToPaletteEntries(destOffset + 1, (size - 2) >> 1);
        }
        else if (tileset->isSecondary == TRUE)
        {
            LoadPalette(tileset->palettes[NUM_PALS_IN_PRIMARY], destOffset, size);
            ApplyGlobalTintToPaletteEntries(destOffset, size >> 1);
        }
        else
        {
            LoadCompressedPalette((const u32 *)tileset->palettes, destOffset, size);
            ApplyGlobalTintToPaletteEntries(destOffset, size >> 1);
        }
    }
}

void CopyPrimaryTilesetToVram(const struct MapLayout *mapLayout)
{
    CopyTilesetToVram(mapLayout->primaryTileset, NUM_TILES_IN_PRIMARY, 0);
}

void CopySecondaryTilesetToVram(const struct MapLayout *mapLayout)
{
    CopyTilesetToVram(mapLayout->secondaryTileset, NUM_TILES_TOTAL - NUM_TILES_IN_PRIMARY, NUM_TILES_IN_PRIMARY);
    TopazeLoadFogData();
}

void CopySecondaryTilesetToVramUsingHeap(const struct MapLayout *mapLayout)
{
    CopyTilesetToVramUsingHeap(mapLayout->secondaryTileset, NUM_TILES_TOTAL - NUM_TILES_IN_PRIMARY, NUM_TILES_IN_PRIMARY);
    TopazeLoadFogData();
}

static void LoadPrimaryTilesetPalette(const struct MapLayout *mapLayout)
{
    LoadTilesetPalette(mapLayout->primaryTileset, BG_PLTT_ID(0), NUM_PALS_IN_PRIMARY * PLTT_SIZE_4BPP);
    CpuCopy16(&gPlttBufferUnfaded[0], &sRampBase[0], NUM_PALS_IN_PRIMARY * 32);
}

void LoadSecondaryTilesetPalette(const struct MapLayout *mapLayout)
{
    LoadTilesetPalette(mapLayout->secondaryTileset, BG_PLTT_ID(NUM_PALS_IN_PRIMARY), (NUM_PALS_TOTAL - NUM_PALS_IN_PRIMARY) * PLTT_SIZE_4BPP);
    CpuCopy16(&gPlttBufferUnfaded[NUM_PALS_IN_PRIMARY * 16], &sRampBase[NUM_PALS_IN_PRIMARY * 16], (NUM_PALS_TOTAL - NUM_PALS_IN_PRIMARY) * 32);
    TopazeRampApply(TRUE);
}

void CopyMapTilesetsToVram(struct MapLayout const *mapLayout)
{
    if (mapLayout)
    {
        CopyTilesetToVramUsingHeap(mapLayout->primaryTileset, NUM_TILES_IN_PRIMARY, 0);
        CopyTilesetToVramUsingHeap(mapLayout->secondaryTileset, NUM_TILES_TOTAL - NUM_TILES_IN_PRIMARY, NUM_TILES_IN_PRIMARY);
        TopazeLoadFogData();
    }
}

void LoadMapTilesetPalettes(struct MapLayout const *mapLayout)
{
    if (mapLayout)
    {
        LoadPrimaryTilesetPalette(mapLayout);
        LoadSecondaryTilesetPalette(mapLayout);
    }
}
