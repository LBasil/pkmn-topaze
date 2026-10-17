// genere par docs/topaze/ramp_gen.py : transformation de palette (gain/256, biais en unites 5 bits) appliquee sur ZONE cases avant le bord
#define TOPAZE_RAMP_ZONE 14
struct TopazeRampEnd { u8 dir; s16 gain[3]; s8 bias[3]; };
struct TopazeRamp { u16 layoutId; u8 n; struct TopazeRampEnd e[3]; };
static const struct TopazeRamp sTopazeRamps[] = {
    { LAYOUT_FIVE_ISLAND_MEADOW, 2, {{2, {247,236,219}, {0,-1,6}}, {3, {221,192,183}, {1,3,8}} } }, // FiveIsland_Meadow->FiveIsland d=53; FiveIsland_Meadow->FiveIsland_MemorialPillar d=66
    { LAYOUT_FIVE_ISLAND_MEMORIAL_PILLAR, 1, {{2, {304,371,371}, {-1,-6,-14}} } }, // FiveIsland_MemorialPillar->FiveIsland_Meadow d=66
    { LAYOUT_FIVE_ISLAND_WATER_LABYRINTH, 1, {{1, {371,371,371}, {1,-5,-15}} } }, // FiveIsland_WaterLabyrinth->FiveIsland d=80
    { LAYOUT_ONE_ISLAND_KINDLE_ROAD, 1, {{2, {230,307,293}, {1,-5,-6}} } }, // OneIsland_KindleRoad->OneIsland d=47
    { LAYOUT_ONE_ISLAND_TREASURE_BEACH, 1, {{0, {279,371,367}, {4,-5,-14}} } }, // OneIsland_TreasureBeach->OneIsland d=84
    { LAYOUT_ROUTE10, 2, {{1, {305,314,343}, {-8,-7,-10}}, {2, {250,272,274}, {-2,-1,-2}} } }, // Route10->LavenderTown d=91; Route10->Route9 d=50
    { LAYOUT_ROUTE12, 2, {{0, {179,260,294}, {-2,-4,-7}}, {1, {258,241,261}, {1,2,1}} } }, // Route12->LavenderTown d=119; Route12->Route13 d=42
    { LAYOUT_ROUTE13, 1, {{0, {254,272,251}, {-1,-2,0}} } }, // Route13->Route12 d=42
    { LAYOUT_ROUTE15, 1, {{2, {255,186,371}, {-6,-3,-15}} } }, // Route15->FuchsiaCity d=146
    { LAYOUT_ROUTE16, 1, {{3, {222,244,247}, {0,-2,-2}} } }, // Route16->CeladonCity d=75
    { LAYOUT_ROUTE18, 1, {{3, {232,179,371}, {-2,-1,-13}} } }, // Route18->FuchsiaCity d=94
    { LAYOUT_ROUTE19, 2, {{0, {341,239,261}, {-15,-7,0}}, {2, {242,198,179}, {2,6,11}} } }, // Route19->FuchsiaCity d=127; Route19->Route20 d=202
    { LAYOUT_ROUTE2, 2, {{1, {257,292,314}, {-2,-3,-5}}, {0, {371,371,371}, {1,2,1}} } }, // Route2->ViridianCity d=43; Route2->PewterCity d=123
    { LAYOUT_ROUTE20, 2, {{3, {271,362,371}, {-2,-11,-19}}, {2, {371,371,371}, {5,-1,-14}} } }, // Route20->Route19 d=202; Route20->CinnabarIsland d=137
    { LAYOUT_ROUTE21_NORTH, 2, {{1, {264,289,355}, {0,3,3}}, {0, {254,371,371}, {0,0,-1}} } }, // Route21_North->Route21_South d=188; Route21_North->PalletTown d=49
    { LAYOUT_ROUTE21_SOUTH, 2, {{0, {249,230,200}, {0,-3,-2}}, {1, {336,371,371}, {2,-2,-11}} } }, // Route21_South->Route21_North d=188; Route21_South->CinnabarIsland d=85
    { LAYOUT_ROUTE22, 2, {{0, {309,332,260}, {5,3,2}}, {3, {218,293,298}, {-1,-3,-6}} } }, // Route22->Route23 d=237; Route22->ViridianCity_WestLane d=56
    { LAYOUT_ROUTE23, 2, {{0, {200,258,186}, {6,-4,4}}, {1, {218,208,252}, {-3,-2,-2}} } }, // Route23->IndigoPlateau_Exterior d=52; Route23->Route22 d=237
    { LAYOUT_ROUTE24, 1, {{1, {349,371,295}, {-1,-2,-13}} } }, // Route24->CeruleanCity d=144
    { LAYOUT_ROUTE3, 1, {{2, {371,371,371}, {4,1,-1}} } }, // Route3->PewterCity d=104
    { LAYOUT_ROUTE4_EAST, 1, {{3, {292,267,237}, {4,0,1}} } }, // Route4East->CeruleanCity d=56
    { LAYOUT_ROUTE8, 2, {{2, {314,267,307}, {1,5,-7}}, {3, {193,337,371}, {-5,-11,-14}} } }, // Route8->SaffronCity_Connection d=104; Route8->LavenderTown d=142
    { LAYOUT_ROUTE9, 2, {{3, {262,242,240}, {2,1,2}}, {2, {272,327,238}, {-1,-10,-5}} } }, // Route9->Route10 d=50; Route9->CeruleanCity d=77
    { LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON, 1, {{1, {226,254,239}, {0,1,3}} } }, // SevenIsland_SevaultCanyon->SevenIsland_TanobyRuins d=63
    { LAYOUT_SEVEN_ISLAND_TANOBY_RUINS, 1, {{0, {294,258,276}, {0,-1,-4}} } }, // SevenIsland_TanobyRuins->SevenIsland_SevaultCanyon d=63
    { LAYOUT_SEVEN_ISLAND_TRAINER_TOWER, 1, {{1, {285,328,371}, {-5,-9,-9}} } }, // SevenIsland_TrainerTower->SevenIsland d=51
    { LAYOUT_THREE_ISLAND_PORT, 1, {{0, {254,217,226}, {1,6,3}} } }, // ThreeIsland_Port->ThreeIsland d=43
    { LAYOUT_TWO_ISLAND_CAPE_BRINK, 1, {{1, {294,352,371}, {-8,-9,-10}} } }, // TwoIsland_CapeBrink->TwoIsland d=59
    { 0xFFFF, 0, {{0,{0,0,0},{0,0,0}}} },
};
