FuchsiaCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FuchsiaCity_OnTransition
	.byte 0

FuchsiaCity_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_FUCHSIA_CITY
	setflag FLAG_CUT_TREE_06 @ retour Basil 21/10 : arbres a couper inutiles retires
	setflag FLAG_CUT_TREE_07
	setflag FLAG_CUT_TREE_08
	setflag FLAG_CUT_TREE_09
	call_if_set FLAG_AMETHYST_RAID_STARTED, FuchsiaCity_EventScript_HideStaffer
	call_if_set FLAG_BADGE05_GET, FuchsiaCity_EventScript_HidePolice
	call_if_set FLAG_CHRONDROLIA_RAID_DONE, FuchsiaCity_EventScript_HideSouthPolice
	call_if_unset FLAG_AMETHYST_RAID_STARTED, FuchsiaCity_EventScript_HideLooseMons
	call_if_set FLAG_AMETHYST_STONE_GIVEN, FuchsiaCity_EventScript_HideLooseMons
	call_if_set FLAG_GOT_DOME_FOSSIL, FuchsiaCity_EventScript_SetOmanyteGfx
	call_if_unset FLAG_GOT_DOME_FOSSIL, FuchsiaCity_EventScript_SetKabutoGfx
	end

FuchsiaCity_EventScript_SetOmanyteGfx::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_OMANYTE
	return

FuchsiaCity_EventScript_SetKabutoGfx::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_KABUTO
	return

FuchsiaCity_EventScript_LittleBoy::
	msgbox FuchsiaCity_Text_DidYouTrySafariGame, MSGBOX_NPC
	end

FuchsiaCity_EventScript_OldMan::
	msgbox FuchsiaCity_Text_SafariZoneZooInFront, MSGBOX_NPC
	end

FuchsiaCity_EventScript_Erik::
	msgbox FuchsiaCity_Text_WheresSara, MSGBOX_NPC
	end

FuchsiaCity_EventScript_Youngster::
	msgbox FuchsiaCity_Text_ItemBallInThere, MSGBOX_NPC
	end

FuchsiaCity_EventScript_Lass::
	lock
	faceplayer
	famechecker FAMECHECKER_KOGA, 3
	msgbox FuchsiaCity_Text_MyFatherIsGymLeader
	release
	end

FuchsiaCity_EventScript_CitySign::
	msgbox FuchsiaCity_Text_CitySign, MSGBOX_SIGN
	end

FuchsiaCity_EventScript_SafariZoneSign::
	msgbox FuchsiaCity_Text_SafariZoneSign, MSGBOX_SIGN
	end

FuchsiaCity_EventScript_SafariGameSign::
	msgbox FuchsiaCity_Text_SafariGameSign, MSGBOX_SIGN
	end

FuchsiaCity_EventScript_WardensHomeSign::
	msgbox FuchsiaCity_Text_WardensHomeSign, MSGBOX_SIGN
	end

@ Unused
FuchsiaCity_EventScript_SafariZoneOfficeSign::
	msgbox FuchsiaCity_Text_SafariZoneOfficeSign, MSGBOX_SIGN
	end

FuchsiaCity_EventScript_GymSign::
	lockall
	famechecker FAMECHECKER_KOGA, 0
	msgbox FuchsiaCity_Text_GymSign
	releaseall
	end

FuchsiaCity_EventScript_ChanseySign::
	lockall
	setvar VAR_0x8004, SPECIES_CHANSEY
	special SetSeenMon
	showmonpic SPECIES_CHANSEY, 10, 3
	msgbox FuchsiaCity_Text_ChanseySign
	hidemonpic
	releaseall
	end

FuchsiaCity_EventScript_VoltorbSign::
	lockall
	setvar VAR_0x8004, SPECIES_VOLTORB
	special SetSeenMon
	showmonpic SPECIES_VOLTORB, 10, 3
	msgbox FuchsiaCity_Text_VoltorbSign
	hidemonpic
	releaseall
	end

FuchsiaCity_EventScript_KangaskhanSign::
	lockall
	setvar VAR_0x8004, SPECIES_KANGASKHAN
	special SetSeenMon
	showmonpic SPECIES_KANGASKHAN, 10, 3
	msgbox FuchsiaCity_Text_KangaskhanSign
	hidemonpic
	releaseall
	end

FuchsiaCity_EventScript_SlowpokeSign::
	lockall
	setvar VAR_0x8004, SPECIES_SLOWPOKE
	special SetSeenMon
	showmonpic SPECIES_SLOWPOKE, 10, 3
	msgbox FuchsiaCity_Text_SlowpokeSign
	hidemonpic
	releaseall
	end

FuchsiaCity_EventScript_LaprasSign::
	lockall
	setvar VAR_0x8004, SPECIES_LAPRAS
	special SetSeenMon
	showmonpic SPECIES_LAPRAS, 10, 3
	msgbox FuchsiaCity_Text_LaprasSign
	hidemonpic
	releaseall
	end

FuchsiaCity_EventScript_FossilMonSign::
	lockall
	goto_if_set FLAG_GOT_DOME_FOSSIL, FuchsiaCity_EventScript_OmanyteSign
	setvar VAR_0x8004, SPECIES_KABUTO
	special SetSeenMon
	showmonpic SPECIES_KABUTO, 10, 3
	msgbox FuchsiaCity_Text_KabutoSign
	hidemonpic
	releaseall
	end

FuchsiaCity_EventScript_OmanyteSign::
	setvar VAR_0x8004, SPECIES_OMANYTE
	special SetSeenMon
	showmonpic SPECIES_OMANYTE, 10, 3
	msgbox FuchsiaCity_Text_OmanyteSign
	hidemonpic
	releaseall
	end

FuchsiaCity_EventScript_HideStaffer::
	setflag FLAG_TEMP_6
	return

FuchsiaCity_EventScript_HideSouthPolice::
	setflag FLAG_TEMP_9
	return

FuchsiaCity_EventScript_HidePolice::
	setflag FLAG_TEMP_7
	return

FuchsiaCity_EventScript_ArrivalScene::
	lockall
	goto_if_set FLAG_AMETHYST_RAID_STARTED, FuchsiaCity_EventScript_ArrivalDone
	applymovement LOCALID_AMETHYST_STAFFER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_AMETHYST_STAFFER, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox FuchsiaCity_Text_StafferAlarm
	setflag FLAG_AMETHYST_RAID_STARTED
	releaseall
	end

FuchsiaCity_EventScript_ArrivalDone::
	releaseall
	end

FuchsiaCity_EventScript_Staffer::
	msgbox FuchsiaCity_Text_StafferAlarm, MSGBOX_NPC
	end

FuchsiaCity_EventScript_Police::
	lock
	faceplayer
	goto_if_set FLAG_AMETHYST_RAID_DONE, FuchsiaCity_EventScript_PoliceDone
	msgbox FuchsiaCity_Text_PoliceRaid
	release
	end

FuchsiaCity_EventScript_PoliceSouth::
	lock
	faceplayer
	goto_if_unset FLAG_AMETHYST_RAID_DONE, FuchsiaCity_EventScript_PoliceSouthRaid
	msgbox FuchsiaCity_Text_PoliceVolcano
	release
	end

FuchsiaCity_EventScript_PoliceSouthRaid::
	msgbox FuchsiaCity_Text_PoliceRaid
	release
	end

FuchsiaCity_EventScript_PoliceDone::
	msgbox FuchsiaCity_Text_PoliceBadge
	release
	end

FuchsiaCity_EventScript_HideLooseMons::
	setflag FLAG_TEMP_8
	return

FuchsiaCity_EventScript_LooseMonVoltorb::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_VOLTORB, CRY_MODE_NORMAL
	msgbox FuchsiaCity_Text_LooseMonVoltorb
	waitmoncry
	release
	end

FuchsiaCity_EventScript_LooseMonChansey::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CHANSEY, CRY_MODE_NORMAL
	msgbox FuchsiaCity_Text_LooseMonChansey
	waitmoncry
	release
	end

FuchsiaCity_EventScript_LooseMonSlowpoke::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SLOWPOKE, CRY_MODE_NORMAL
	msgbox FuchsiaCity_Text_LooseMonSlowpoke
	waitmoncry
	release
	end

FuchsiaCity_EventScript_LooseMonKangaskhan::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_KANGASKHAN, CRY_MODE_NORMAL
	msgbox FuchsiaCity_Text_LooseMonKangaskhan
	waitmoncry
	release
	end

FuchsiaCity_EventScript_LooseMonPsyduck::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PSYDUCK, CRY_MODE_NORMAL
	msgbox FuchsiaCity_Text_LooseMonPsyduck
	waitmoncry
	release
	end

FuchsiaCity_EventScript_CellWitness::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_CELL_FUCHSIA, FuchsiaCity_EventScript_CellWitnessDone
	goto_if_defeated TRAINER_POKEFAN_M, FuchsiaCity_EventScript_CellWitnessHalf
	msgbox FuchsiaCity_Text_CellWitness, MSGBOX_DEFAULT
	release
	end

FuchsiaCity_EventScript_CellWitnessHalf::
	msgbox FuchsiaCity_Text_CellWitnessHalf, MSGBOX_DEFAULT
	release
	end

FuchsiaCity_EventScript_CellWitnessDone::
	msgbox FuchsiaCity_Text_CellWitnessDone, MSGBOX_DEFAULT
	release
	end

FuchsiaCity_Text_CellWitness::
	.string "Strange. The keeper of that house"
	.string "left town without a word.\p"
	.string "Now black coats walk in and out as"
	.string "if they owned the street.$"

FuchsiaCity_Text_CellWitnessHalf::
	.string "You went in? Then read what they"
	.string "left on the north wall.$"

FuchsiaCity_Text_CellWitnessDone::
	.string "The street feels like ours again.\p"
	.string "Though I count them everywhere now."
	.string "In every town. Do you notice too?$"

@ Topaze: PROCHE THIBAULT (optionnel, fort)
FuchsiaCity_EventScript_ProcheThibault::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_POSTGAME, FuchsiaCity_EventScript_ProcheThibault_TooEarly
	goto_if_defeated TRAINER_PROCHE_THIBAULT, FuchsiaCity_EventScript_ProcheThibault_After
	msgbox FuchsiaCity_Text_ProcheThibault_Intro
	checkitemspace ITEM_MYSTIC_WATER
	goto_if_eq VAR_RESULT, FALSE, FuchsiaCity_EventScript_ProcheThibault_NoRoom
	trainerbattle_no_intro TRAINER_PROCHE_THIBAULT, FuchsiaCity_Text_ProcheThibault_Defeat
	msgbox FuchsiaCity_Text_ProcheThibault_Win
	giveitem ITEM_MYSTIC_WATER
	msgbox FuchsiaCity_Text_ProcheThibault_After
	release
	end

FuchsiaCity_EventScript_ProcheThibault_After::
	msgbox FuchsiaCity_Text_ProcheThibault_After
	release
	end

FuchsiaCity_EventScript_ProcheThibault_TooEarly::
	msgbox FuchsiaCity_Text_ProcheThibault_Early
	release
	end

FuchsiaCity_EventScript_ProcheThibault_NoRoom::
	msgbox FuchsiaCity_Text_ProcheThibault_NoRoom
	release
	end

@ Topaze: le PASSEUR des Echos (menu des zones du Temps)
FuchsiaCity_EventScript_EchoFerryman::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_CLOCK_DONE, FuchsiaCity_EventScript_EchoFerryman_EventScript_Closed
	msgbox FuchsiaCity_Text_Ferry_Hello
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate0
	msgbox FuchsiaCity_Text_Ferry_Ask0, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest1
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_LIGHTHOUSE_1F, 1, 0, 0
	waitstate
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate0::
	msgbox FuchsiaCity_Text_Ferry_GateText0
	goto FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest1
FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest1::
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate1
	msgbox FuchsiaCity_Text_Ferry_Ask1, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest2
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_CLOCK_BEACH, 255, 12, 24
	waitstate
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate1::
	msgbox FuchsiaCity_Text_Ferry_GateText1
	goto FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest2
FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest2::
	goto_if_unset FLAG_BADGE07_GET, FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate2
	msgbox FuchsiaCity_Text_Ferry_Ask2, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest3
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_NO_TOMORROW_VILLAGE, 255, 9, 11
	waitstate
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate2::
	msgbox FuchsiaCity_Text_Ferry_GateText2
	goto FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest3
FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest3::
	goto_if_unset FLAG_BADGE08_GET, FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate3
	msgbox FuchsiaCity_Text_Ferry_Ask3, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest4
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_DEPTHS_1F, 255, 18, 21
	waitstate
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate3::
	msgbox FuchsiaCity_Text_Ferry_GateText3
	goto FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest4
FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest4::
	goto_if_unset FLAG_TOPAZE_ARCHIVE_DONE, FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate4
	msgbox FuchsiaCity_Text_Ferry_Ask4, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest5
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_ECHO_GARDEN, 255, 12, 23
	waitstate
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate4::
	msgbox FuchsiaCity_Text_Ferry_GateText4
	goto FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest5
FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest5::
	goto_if_unset FLAG_TOPAZE_POSTGAME, FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate5
	msgbox FuchsiaCity_Text_Ferry_Ask5, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest6
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_LAST_DAY_ISLAND, 255, 15, 20
	waitstate
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate5::
	msgbox FuchsiaCity_Text_Ferry_GateText5
	goto FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest6
FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest6::
	goto_if_not_defeated TRAINER_PROCHE_ADRIAN, FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate6
	msgbox FuchsiaCity_Text_Ferry_Ask6, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_EchoFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_FRIENDS_CLEARING, 255, 43, 38
	waitstate
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate6::
	msgbox FuchsiaCity_Text_Ferry_GateText6
	goto FuchsiaCity_EventScript_EchoFerryman_EventScript_End
FuchsiaCity_EventScript_EchoFerryman_EventScript_End::
	msgbox FuchsiaCity_Text_Ferry_Never
	release
	end

FuchsiaCity_EventScript_EchoFerryman_EventScript_Closed::
	msgbox FuchsiaCity_Text_Ferry_Closed
	release
	end

@ Topaze: la PASSEUSE (zones de capture)
FuchsiaCity_EventScript_TideFerrywoman::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_CLOCK_DONE, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Closed
	msgbox FuchsiaCity_Text_Tide_Hello
	goto_if_unset FLAG_BADGE03_GET, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate0
	msgbox FuchsiaCity_Text_Tide_Ask0, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest1
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_REFLECTION_MARSH, 255, 30, 23
	waitstate
	end
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate0::
	msgbox FuchsiaCity_Text_Tide_GateText0
	goto FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest1
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest1::
	goto_if_unset FLAG_BADGE04_GET, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate1
	msgbox FuchsiaCity_Text_Tide_Ask1, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest2
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_STONE_GREENHOUSE, 255, 12, 36
	waitstate
	end
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate1::
	msgbox FuchsiaCity_Text_Tide_GateText1
	goto FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest2
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest2::
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate2
	msgbox FuchsiaCity_Text_Tide_Ask2, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest3
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_TRADE_DOCK, 255, 48, 11
	waitstate
	end
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate2::
	msgbox FuchsiaCity_Text_Tide_GateText2
	goto FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest3
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest3::
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate3
	msgbox FuchsiaCity_Text_Tide_Ask3, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest4
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_FOSSIL_DIG, 255, 24, 30
	waitstate
	end
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate3::
	msgbox FuchsiaCity_Text_Tide_GateText3
	goto FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest4
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest4::
	goto_if_unset FLAG_BADGE07_GET, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate4
	msgbox FuchsiaCity_Text_Tide_Ask4, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_TideFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_CYCLE_POND, 255, 14, 75
	waitstate
	end
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate4::
	msgbox FuchsiaCity_Text_Tide_GateText4
	goto FuchsiaCity_EventScript_TideFerrywoman_EventScript_End
FuchsiaCity_EventScript_TideFerrywoman_EventScript_End::
	msgbox FuchsiaCity_Text_Tide_Never
	release
	end

FuchsiaCity_EventScript_TideFerrywoman_EventScript_Closed::
	msgbox FuchsiaCity_Text_Tide_Closed
	release
	end

@ Topaze: le PASSEUR DES LANTERNES (zones lot 3)
FuchsiaCity_EventScript_LanternBoatman::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_CLOCK_DONE, FuchsiaCity_EventScript_LanternBoatman_EventScript_Closed
	msgbox FuchsiaCity_Text_Lantern_Hello
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate0
	msgbox FuchsiaCity_Text_Lantern_Ask0, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest1
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_HOENN_WEST_RESERVE, 255, 14, 105
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate0::
	msgbox FuchsiaCity_Text_Lantern_GateText0
	goto FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest1
FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest1::
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate1
	msgbox FuchsiaCity_Text_Lantern_Ask1, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest2
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_HOENN_EAST_RESERVE, 255, 12, 45
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate1::
	msgbox FuchsiaCity_Text_Lantern_GateText1
	goto FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest2
FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest2::
	goto_if_unset FLAG_BADGE04_GET, FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate2
	msgbox FuchsiaCity_Text_Lantern_Ask2, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest3
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_SUNRISE_MEADOW, 255, 12, 31
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate2::
	msgbox FuchsiaCity_Text_Lantern_GateText2
	goto FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest3
FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest3::
	goto_if_unset FLAG_BADGE07_GET, FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate3
	msgbox FuchsiaCity_Text_Lantern_Ask3, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest4
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_ASHEN_MINE, 255, 11, 60
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate3::
	msgbox FuchsiaCity_Text_Lantern_GateText3
	goto FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest4
FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest4::
	goto_if_unset FLAG_BADGE03_GET, FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate4
	msgbox FuchsiaCity_Text_Lantern_Ask4, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest5
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_BERRY_ORCHARD, 255, 31, 35
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate4::
	msgbox FuchsiaCity_Text_Lantern_GateText4
	goto FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest5
FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest5::
	msgbox FuchsiaCity_Text_Lantern_Ask5, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest6
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_DOCK_CAFE, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest6::
	msgbox FuchsiaCity_Text_Lantern_Ask6, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest7
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_EVOLUTION_LIBRARY, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest7::
	msgbox FuchsiaCity_Text_Lantern_Ask7, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_LanternBoatman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_COLLECTOR_SHOP, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_End::
	msgbox FuchsiaCity_Text_Lantern_Never
	release
	end

FuchsiaCity_EventScript_LanternBoatman_EventScript_Closed::
	msgbox FuchsiaCity_Text_Lantern_Closed
	release
	end

@ Topaze: passeur Apprentice
FuchsiaCity_EventScript_Apprentice::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_CLOCK_DONE, FuchsiaCity_EventScript_Apprentice_EventScript_Closed
	msgbox FuchsiaCity_Text_Apprentice_Hello
	msgbox FuchsiaCity_Text_Apprentice_Ask0, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_Apprentice_EventScript_Dest1
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_BABY_NURSERY, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_Apprentice_EventScript_Dest1::
	msgbox FuchsiaCity_Text_Apprentice_Ask1, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_EventScript_Apprentice_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_BARTER_HOUSE, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_Apprentice_EventScript_End::
	msgbox FuchsiaCity_Text_Apprentice_Never
	release
	end

FuchsiaCity_EventScript_Apprentice_EventScript_Closed::
	msgbox FuchsiaCity_Text_Apprentice_Closed
	release
	end
