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
	setvar VAR_0x8004, 0
	goto_if_unset FLAG_TOPAZE_CLOCK_DONE, FuchsiaCity_EventScript_EchoFerryman_EventScript_Closed
	msgbox FuchsiaCity_Text_Ferry_Hello
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate0
	msgbox FuchsiaCity_Text_Ferry_Ask0, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest1
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest5
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_EchoFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_LIGHTHOUSE_1F, 1, 0, 0
	waitstate
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate0::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest1
FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest1::
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate1
	msgbox FuchsiaCity_Text_Ferry_Ask1, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest2
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest6
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_EchoFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_CLOCK_BEACH, 255, 12, 24
	waitstate
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate1::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest2
FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest2::
	goto_if_unset FLAG_BADGE07_GET, FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate2
	msgbox FuchsiaCity_Text_Ferry_Ask2, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest3
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest6
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_EchoFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_NO_TOMORROW_VILLAGE, 255, 9, 11
	waitstate
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate2::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest3
FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest3::
	goto_if_unset FLAG_BADGE08_GET, FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate3
	msgbox FuchsiaCity_Text_Ferry_Ask3, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest4
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest6
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_EchoFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_DEPTHS_1F, 255, 18, 21
	waitstate
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate3::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest4
FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest4::
	goto_if_unset FLAG_TOPAZE_ARCHIVE_DONE, FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate4
	msgbox FuchsiaCity_Text_Ferry_Ask4, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest5
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest6
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_EchoFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_ECHO_GARDEN, 255, 12, 23
	waitstate
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate4::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest5
FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest5::
	goto_if_unset FLAG_TOPAZE_POSTGAME, FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate5
	msgbox FuchsiaCity_Text_Ferry_Ask5, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest6
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest6
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_EchoFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_LAST_DAY_ISLAND, 255, 15, 20
	waitstate
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate5::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest6
FuchsiaCity_EventScript_EchoFerryman_EventScript_Dest6::
	goto_if_not_defeated TRAINER_PROCHE_ADRIAN, FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate6
	msgbox FuchsiaCity_Text_Ferry_Ask6, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_EchoFerryman_EventScript_End
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_EchoFerryman_EventScript_End
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_EchoFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_FRIENDS_CLEARING, 255, 43, 38
	waitstate
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_Gate6::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_EchoFerryman_EventScript_End
FuchsiaCity_EventScript_EchoFerryman_EventScript_End::
	msgbox FuchsiaCity_Text_Ferry_Never
	goto_if_eq VAR_0x8004, 1, FuchsiaCity_EventScript_EchoFerryman_EventScript_EndLocked
	release
	end
FuchsiaCity_EventScript_EchoFerryman_EventScript_EndLocked::
	msgbox FuchsiaCity_Text_FerryLocked
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
	setvar VAR_0x8004, 0
	goto_if_unset FLAG_TOPAZE_CLOCK_DONE, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Closed
	msgbox FuchsiaCity_Text_Tide_Hello
	goto_if_unset FLAG_BADGE03_GET, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate0
	msgbox FuchsiaCity_Text_Tide_Ask0, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest1
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest4
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_TideFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_REFLECTION_MARSH, 255, 30, 23
	waitstate
	end
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate0::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest1
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest1::
	goto_if_unset FLAG_BADGE04_GET, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate1
	msgbox FuchsiaCity_Text_Tide_Ask1, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest2
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest4
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_TideFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_STONE_GREENHOUSE, 255, 12, 36
	waitstate
	end
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate1::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest2
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest2::
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate2
	msgbox FuchsiaCity_Text_Tide_Ask2, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest3
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest4
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_TideFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_TRADE_DOCK, 255, 48, 11
	waitstate
	end
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate2::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest3
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest3::
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate3
	msgbox FuchsiaCity_Text_Tide_Ask3, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest4
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest4
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_TideFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_FOSSIL_DIG, 255, 24, 30
	waitstate
	end
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate3::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest4
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Dest4::
	goto_if_unset FLAG_BADGE07_GET, FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate4
	msgbox FuchsiaCity_Text_Tide_Ask4, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_TideFerrywoman_EventScript_End
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_TideFerrywoman_EventScript_End
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_TideFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_CYCLE_POND, 255, 14, 75
	waitstate
	end
FuchsiaCity_EventScript_TideFerrywoman_EventScript_Gate4::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_TideFerrywoman_EventScript_End
FuchsiaCity_EventScript_TideFerrywoman_EventScript_End::
	msgbox FuchsiaCity_Text_Tide_Never
	goto_if_eq VAR_0x8004, 1, FuchsiaCity_EventScript_TideFerrywoman_EventScript_EndLocked
	release
	end
FuchsiaCity_EventScript_TideFerrywoman_EventScript_EndLocked::
	msgbox FuchsiaCity_Text_FerryLocked
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
	setvar VAR_0x8004, 0
	goto_if_unset FLAG_TOPAZE_CLOCK_DONE, FuchsiaCity_EventScript_LanternBoatman_EventScript_Closed
	msgbox FuchsiaCity_Text_Lantern_Hello
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate0
	msgbox FuchsiaCity_Text_Lantern_Ask0, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest1
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest5
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_LanternBoatman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_HOENN_WEST_RESERVE, 255, 14, 105
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate0::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest1
FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest1::
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate1
	msgbox FuchsiaCity_Text_Lantern_Ask1, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest2
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest6
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_LanternBoatman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_HOENN_EAST_RESERVE, 255, 12, 45
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate1::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest2
FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest2::
	goto_if_unset FLAG_BADGE04_GET, FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate2
	msgbox FuchsiaCity_Text_Lantern_Ask2, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest3
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest7
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_LanternBoatman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_SUNRISE_MEADOW, 255, 12, 31
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate2::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest3
FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest3::
	goto_if_unset FLAG_BADGE07_GET, FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate3
	msgbox FuchsiaCity_Text_Lantern_Ask3, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest4
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest7
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_LanternBoatman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_ASHEN_MINE, 255, 11, 60
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate3::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest4
FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest4::
	goto_if_unset FLAG_BADGE03_GET, FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate4
	msgbox FuchsiaCity_Text_Lantern_Ask4, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest5
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest7
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_LanternBoatman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_BERRY_ORCHARD, 255, 31, 35
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_Gate4::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest5
FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest5::
	msgbox FuchsiaCity_Text_Lantern_Ask5, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest6
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest7
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_LanternBoatman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_DOCK_CAFE, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest6::
	msgbox FuchsiaCity_Text_Lantern_Ask6, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest7
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest7
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_LanternBoatman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_EVOLUTION_LIBRARY, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_Dest7::
	msgbox FuchsiaCity_Text_Lantern_Ask7, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_LanternBoatman_EventScript_End
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_LanternBoatman_EventScript_End
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_LanternBoatman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_COLLECTOR_SHOP, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_End::
	msgbox FuchsiaCity_Text_Lantern_Never
	goto_if_eq VAR_0x8004, 1, FuchsiaCity_EventScript_LanternBoatman_EventScript_EndLocked
	release
	end
FuchsiaCity_EventScript_LanternBoatman_EventScript_EndLocked::
	msgbox FuchsiaCity_Text_FerryLocked
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
	setvar VAR_0x8004, 0
	goto_if_unset FLAG_TOPAZE_CLOCK_DONE, FuchsiaCity_EventScript_Apprentice_EventScript_Closed
	msgbox FuchsiaCity_Text_Apprentice_Hello
	msgbox FuchsiaCity_Text_Apprentice_Ask0, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_Apprentice_EventScript_Dest1
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_Apprentice_EventScript_Dest5
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_Apprentice_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_BABY_NURSERY, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_Apprentice_EventScript_Dest1::
	msgbox FuchsiaCity_Text_Apprentice_Ask1, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_Apprentice_EventScript_Dest2
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_Apprentice_EventScript_Dest6
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_Apprentice_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_BARTER_HOUSE, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_Apprentice_EventScript_Dest2::
	msgbox FuchsiaCity_Text_Apprentice_Ask2, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_Apprentice_EventScript_Dest3
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_Apprentice_EventScript_Dest7
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_Apprentice_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_APOTHECARY, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_Apprentice_EventScript_Dest3::
	goto_if_unset FLAG_BADGE01_GET, FuchsiaCity_EventScript_Apprentice_EventScript_Gate3
	msgbox FuchsiaCity_Text_Apprentice_Ask3, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_Apprentice_EventScript_Dest4
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_Apprentice_EventScript_Dest8
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_Apprentice_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_MEADOW_PATH, 255, 30, 23
	waitstate
	end
FuchsiaCity_EventScript_Apprentice_EventScript_Gate3::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_Apprentice_EventScript_Dest4
FuchsiaCity_EventScript_Apprentice_EventScript_Dest4::
	goto_if_unset FLAG_BADGE03_GET, FuchsiaCity_EventScript_Apprentice_EventScript_Gate4
	msgbox FuchsiaCity_Text_Apprentice_Ask4, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_Apprentice_EventScript_Dest5
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_Apprentice_EventScript_Dest9
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_Apprentice_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_COTTON_FIELD, 255, 12, 30
	waitstate
	end
FuchsiaCity_EventScript_Apprentice_EventScript_Gate4::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_Apprentice_EventScript_Dest5
FuchsiaCity_EventScript_Apprentice_EventScript_Dest5::
	goto_if_unset FLAG_BADGE01_GET, FuchsiaCity_EventScript_Apprentice_EventScript_Gate5
	msgbox FuchsiaCity_Text_Apprentice_Ask5, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_Apprentice_EventScript_Dest6
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_Apprentice_EventScript_Dest9
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_Apprentice_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_BREEZE_HILL, 255, 26, 17
	waitstate
	end
FuchsiaCity_EventScript_Apprentice_EventScript_Gate5::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_Apprentice_EventScript_Dest6
FuchsiaCity_EventScript_Apprentice_EventScript_Dest6::
	goto_if_unset FLAG_BADGE04_GET, FuchsiaCity_EventScript_Apprentice_EventScript_Gate6
	msgbox FuchsiaCity_Text_Apprentice_Ask6, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_Apprentice_EventScript_Dest7
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_Apprentice_EventScript_Dest9
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_Apprentice_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_DROWSY_DOWN, 255, 36, 15
	waitstate
	end
FuchsiaCity_EventScript_Apprentice_EventScript_Gate6::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_Apprentice_EventScript_Dest7
FuchsiaCity_EventScript_Apprentice_EventScript_Dest7::
	goto_if_unset FLAG_BADGE01_GET, FuchsiaCity_EventScript_Apprentice_EventScript_Gate7
	msgbox FuchsiaCity_Text_Apprentice_Ask7, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_Apprentice_EventScript_Dest8
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_Apprentice_EventScript_Dest9
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_Apprentice_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_WEED_PATCH, 255, 36, 6
	waitstate
	end
FuchsiaCity_EventScript_Apprentice_EventScript_Gate7::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_Apprentice_EventScript_Dest8
FuchsiaCity_EventScript_Apprentice_EventScript_Dest8::
	goto_if_unset FLAG_BADGE02_GET, FuchsiaCity_EventScript_Apprentice_EventScript_Gate8
	msgbox FuchsiaCity_Text_Apprentice_Ask8, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_Apprentice_EventScript_Dest9
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_Apprentice_EventScript_Dest9
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_Apprentice_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_FOX_FIELD, 255, 36, 15
	waitstate
	end
FuchsiaCity_EventScript_Apprentice_EventScript_Gate8::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_Apprentice_EventScript_Dest9
FuchsiaCity_EventScript_Apprentice_EventScript_Dest9::
	goto_if_unset FLAG_BADGE08_GET, FuchsiaCity_EventScript_Apprentice_EventScript_Gate9
	msgbox FuchsiaCity_Text_Apprentice_Ask9, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_Apprentice_EventScript_End
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_Apprentice_EventScript_End
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_Apprentice_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_CROWN_FIELD, 255, 26, 17
	waitstate
	end
FuchsiaCity_EventScript_Apprentice_EventScript_Gate9::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_Apprentice_EventScript_End
FuchsiaCity_EventScript_Apprentice_EventScript_End::
	msgbox FuchsiaCity_Text_Apprentice_Never
	goto_if_eq VAR_0x8004, 1, FuchsiaCity_EventScript_Apprentice_EventScript_EndLocked
	release
	end
FuchsiaCity_EventScript_Apprentice_EventScript_EndLocked::
	msgbox FuchsiaCity_Text_FerryLocked
	release
	end

FuchsiaCity_EventScript_Apprentice_EventScript_Closed::
	msgbox FuchsiaCity_Text_Apprentice_Closed
	release
	end

@ Topaze: passeur DuskFerrywoman
FuchsiaCity_EventScript_DuskFerrywoman::
	lock
	faceplayer
	setvar VAR_0x8004, 0
	goto_if_unset FLAG_TOPAZE_CLOCK_DONE, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Closed
	msgbox FuchsiaCity_Text_DuskFerrywoman_Hello
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate0
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask0, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest1
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest5
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_WHISPER_GROVE, 255, 7, 9
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate0::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest1
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest1::
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate1
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask1, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest2
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest6
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_SPARK_GLADE, 255, 7, 9
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate1::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest2
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest2::
	goto_if_unset FLAG_BADGE08_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate2
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask2, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest3
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest7
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_DRAGON_PERCH, 255, 8, 34
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate2::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest3
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest3::
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate3
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask3, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest4
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest8
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_ZEN_GARDEN, 255, 28, 30
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate3::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest4
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest4::
	goto_if_unset FLAG_BADGE04_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate4
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask4, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest5
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest9
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_GIANTS_PLAIN, 255, 27, 23
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate4::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest5
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest5::
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate5
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask5, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest6
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest10
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_DUNE_SEA, 255, 24, 28
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate5::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest6
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest6::
	goto_if_unset FLAG_BADGE07_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate6
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask6, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest7
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest11
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_RUIN_HOLLOW, 255, 24, 30
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate6::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest7
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest7::
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate7
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask7, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest8
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest12
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_TIDE_CAVE, 255, 14, 75
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate7::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest8
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest8::
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate8
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask8, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest9
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest13
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_SOUL_PILLAR, 255, 12, 45
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate8::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest9
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest9::
	goto_if_unset FLAG_BADGE07_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate9
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask9, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest10
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest14
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_OUTCAST_SHORE, 255, 14, 75
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate9::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest10
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest10::
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate10
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask10, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest11
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest15
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_CENTER_MEADOW, 255, 25, 25
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate10::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest11
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest11::
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask11, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest12
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest16
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_BERRY_STAND, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest12::
	goto_if_unset FLAG_BADGE02_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate12
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask12, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest13
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest17
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_MIST_LAKE, 255, 12, 28
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate12::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest13
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest13::
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate13
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask13, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest14
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest18
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_FANG_VALLEY, 255, 38, 12
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate13::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest14
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest14::
	goto_if_unset FLAG_BADGE07_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate14
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask14, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest15
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest19
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_SILENT_HOLLOW, 255, 24, 12
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate14::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest15
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest15::
	goto_if_unset FLAG_BADGE02_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate15
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask15, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest16
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest19
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_IVY_MAZE, 255, 23, 36
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate15::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest16
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest16::
	goto_if_unset FLAG_BADGE08_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate16
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask16, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest17
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest19
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_STONE_CIRCLE, 255, 26, 17
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate16::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest17
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest17::
	goto_if_unset FLAG_BADGE04_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate17
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask17, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest18
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest19
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_ASHEN_HEIGHTS, 255, 11, 30
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate17::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest18
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest18::
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate18
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask18, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest19
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest19
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_GALE_CLIFF, 255, 24, 12
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate18::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest19
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Dest19::
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate19
	msgbox FuchsiaCity_Text_DuskFerrywoman_Ask19, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_MIRROR_POND, 255, 12, 28
	waitstate
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Gate19::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_End::
	msgbox FuchsiaCity_Text_DuskFerrywoman_Never
	goto_if_eq VAR_0x8004, 1, FuchsiaCity_EventScript_DuskFerrywoman_EventScript_EndLocked
	release
	end
FuchsiaCity_EventScript_DuskFerrywoman_EventScript_EndLocked::
	msgbox FuchsiaCity_Text_FerryLocked
	release
	end

FuchsiaCity_EventScript_DuskFerrywoman_EventScript_Closed::
	msgbox FuchsiaCity_Text_DuskFerrywoman_Closed
	release
	end

@ Topaze: quete (A BERRY GOOD DEAL)
FuchsiaCity_EventScript_TQ::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_TQ_FUCHSIACITY, FuchsiaCity_EventScript_TQ_Done
	checkitem ITEM_SITRUS_BERRY, 1
	goto_if_eq VAR_RESULT, FALSE, FuchsiaCity_EventScript_TQ_Ask
	checkitemspace ITEM_CHARCOAL, 1
	goto_if_eq VAR_RESULT, FALSE, FuchsiaCity_EventScript_TQ_NoRoom
	removeitem ITEM_SITRUS_BERRY, 1
	setflag FLAG_TOPAZE_TQ_FUCHSIACITY
	msgbox FuchsiaCity_Text_TQ_Ok
	giveitem ITEM_CHARCOAL, 1
	release
	end

FuchsiaCity_EventScript_TQ_Ask::
	msgbox FuchsiaCity_Text_TQ_Ask
	release
	end

FuchsiaCity_EventScript_TQ_Done::
	msgbox FuchsiaCity_Text_TQ_Done
	release
	end

FuchsiaCity_EventScript_TQ_NoRoom::
	msgbox FuchsiaCity_Text_TQ_NoRoom
	release
	end

@ Topaze: passeur ScribeFerryman
FuchsiaCity_EventScript_ScribeFerryman::
	lock
	faceplayer
	setvar VAR_0x8004, 0
	goto_if_unset FLAG_TOPAZE_CLOCK_DONE, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Closed
	msgbox FuchsiaCity_Text_ScribeFerryman_Hello
	msgbox FuchsiaCity_Text_ScribeFerryman_Ask0, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest1
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest5
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_DEX_HALL, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest1::
	goto_if_unset FLAG_BADGE04_GET, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate1
	msgbox FuchsiaCity_Text_ScribeFerryman_Ask1, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest2
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest6
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_THORN_THICKET, 255, 31, 35
	waitstate
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate1::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest2
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest2::
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate2
	msgbox FuchsiaCity_Text_ScribeFerryman_Ask2, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest3
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest7
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_KINDLE_TRAIL, 255, 14, 105
	waitstate
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate2::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest3
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest3::
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate3
	msgbox FuchsiaCity_Text_ScribeFerryman_Ask3, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest4
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest8
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_MIRROR_LABYRINTH, 255, 48, 11
	waitstate
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate3::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest4
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest4::
	goto_if_unset FLAG_BADGE04_GET, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate4
	msgbox FuchsiaCity_Text_ScribeFerryman_Ask4, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest5
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest9
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_QUARRY_HEIGHTS, 255, 20, 63
	waitstate
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate4::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest5
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest5::
	msgbox FuchsiaCity_Text_ScribeFerryman_Ask5, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest6
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest10
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_BATTLE_STALL, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest6::
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate6
	msgbox FuchsiaCity_Text_ScribeFerryman_Ask6, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest7
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest11
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_STARLIT_STEPPE, 255, 36, 15
	waitstate
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate6::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest7
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest7::
	goto_if_unset FLAG_BADGE03_GET, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate7
	msgbox FuchsiaCity_Text_ScribeFerryman_Ask7, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest8
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest12
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_BLOSSOM_CREST, 255, 24, 12
	waitstate
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate7::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest8
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest8::
	goto_if_unset FLAG_BADGE02_GET, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate8
	msgbox FuchsiaCity_Text_ScribeFerryman_Ask8, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest9
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest13
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_LUCKY_CLOVER, 255, 12, 30
	waitstate
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate8::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest9
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest9::
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate9
	msgbox FuchsiaCity_Text_ScribeFerryman_Ask9, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest10
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest13
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_SKY_PERCH, 255, 26, 17
	waitstate
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate9::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest10
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest10::
	goto_if_unset FLAG_BADGE07_GET, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate10
	msgbox FuchsiaCity_Text_ScribeFerryman_Ask10, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest11
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest13
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_NORTH_WIND, 255, 20, 63
	waitstate
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate10::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest11
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest11::
	goto_if_unset FLAG_BADGE02_GET, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate11
	msgbox FuchsiaCity_Text_ScribeFerryman_Ask11, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest12
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest13
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_MOSSY_DELL, 255, 23, 36
	waitstate
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate11::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest12
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest12::
	goto_if_unset FLAG_BADGE04_GET, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate12
	msgbox FuchsiaCity_Text_ScribeFerryman_Ask12, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest13
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest13
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_HUSHED_BOG, 255, 28, 30
	waitstate
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate12::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest13
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Dest13::
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate13
	msgbox FuchsiaCity_Text_ScribeFerryman_Ask13, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_OBSIDIAN_PASS, 255, 5, 18
	waitstate
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_Gate13::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_ScribeFerryman_EventScript_End
FuchsiaCity_EventScript_ScribeFerryman_EventScript_End::
	msgbox FuchsiaCity_Text_ScribeFerryman_Never
	goto_if_eq VAR_0x8004, 1, FuchsiaCity_EventScript_ScribeFerryman_EventScript_EndLocked
	release
	end
FuchsiaCity_EventScript_ScribeFerryman_EventScript_EndLocked::
	msgbox FuchsiaCity_Text_FerryLocked
	release
	end

FuchsiaCity_EventScript_ScribeFerryman_EventScript_Closed::
	msgbox FuchsiaCity_Text_ScribeFerryman_Closed
	release
	end

@ Topaze: passeur SeasonsFerryman
FuchsiaCity_EventScript_SeasonsFerryman::
	lock
	faceplayer
	setvar VAR_0x8004, 0
	goto_if_unset FLAG_TOPAZE_CLOCK_DONE, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Closed
	msgbox FuchsiaCity_Text_SeasonsFerryman_Hello
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate0
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask0, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest1
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest5
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_FROST_HOLLOW, 255, 12, 20
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate0::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest1
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest1::
	goto_if_unset FLAG_BADGE06_GET, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate1
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask1, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest2
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest6
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_EMBER_RIM, 255, 5, 18
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate1::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest2
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest2::
	goto_if_unset FLAG_BADGE03_GET, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate2
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask2, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest3
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest7
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_NOCTURNE_WOOD, 255, 23, 36
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate2::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest3
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest3::
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate3
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask3, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest4
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest8
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_SHELL_COAST, 255, 12, 36
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate3::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest4
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest4::
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate4
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask4, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest5
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest9
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_EEVEE_GROVE, 255, 30, 23
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate4::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest5
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest5::
	goto_if_unset FLAG_BADGE08_GET, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate5
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask5, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest6
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest10
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_PROFESSOR_RESERVE, 255, 12, 31
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate5::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest6
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest6::
	goto_if_unset FLAG_BADGE02_GET, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate6
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask6, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest7
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest11
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_SUNKEN_BEACH, 255, 12, 30
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate6::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest7
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest7::
	goto_if_unset FLAG_BADGE03_GET, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate7
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask7, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest8
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest12
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_POND_OF_SONG, 255, 36, 6
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate7::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest8
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest8::
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask8, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest9
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest13
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_BALL_BOUTIQUE, 255, 4, 6
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest9::
	goto_if_unset FLAG_BADGE04_GET, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate9
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask9, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest10
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest14
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_SALT_FLATS, 255, 36, 14
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate9::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest10
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest10::
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate10
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask10, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest11
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest14
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_THUNDER_RIDGE, 255, 11, 30
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate10::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest11
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest11::
	goto_if_unset FLAG_BADGE03_GET, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate11
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask11, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest12
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest14
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_SANDBOX_GROVE, 255, 24, 28
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate11::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest12
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest12::
	goto_if_unset FLAG_BADGE03_GET, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate12
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask12, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest13
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest14
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_BRIGHT_SHALLOWS, 255, 9, 92
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate12::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest13
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest13::
	goto_if_unset FLAG_BADGE05_GET, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate13
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask13, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest14
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest14
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_SOUND_MEADOW, 255, 12, 31
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate13::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest14
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Dest14::
	goto_if_unset FLAG_BADGE07_GET, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate14
	msgbox FuchsiaCity_Text_SeasonsFerryman_Ask14, MSGBOX_DEFAULT
	multichoice 0, 0, MULTICHOICE_TOPAZE_FERRY, FALSE
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	goto_if_eq VAR_RESULT, 2, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	goto_if_ne VAR_RESULT, 0, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
	setdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27
	warp MAP_PHANTOM_LANE, 255, 36, 15
	waitstate
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Gate14::
	setvar VAR_0x8004, 1
	goto FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_End::
	msgbox FuchsiaCity_Text_SeasonsFerryman_Never
	goto_if_eq VAR_0x8004, 1, FuchsiaCity_EventScript_SeasonsFerryman_EventScript_EndLocked
	release
	end
FuchsiaCity_EventScript_SeasonsFerryman_EventScript_EndLocked::
	msgbox FuchsiaCity_Text_FerryLocked
	release
	end

FuchsiaCity_EventScript_SeasonsFerryman_EventScript_Closed::
	msgbox FuchsiaCity_Text_SeasonsFerryman_Closed
	release
	end

@ Topaze: guide du quai
FuchsiaCity_EventScript_DockGuide::
	msgbox FuchsiaCity_Text_DockGuide0, MSGBOX_NPC
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
FuchsiaCity_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_TOWN_FUCHSIACITY, FuchsiaCity_EventScript_TopazeFind0_Done
	checkitemspace ITEM_HYPER_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, FuchsiaCity_EventScript_TopazeFind0_Full
	giveitem ITEM_HYPER_POTION, 1
	setflag FLAG_TOPAZE_HID_TOWN_FUCHSIACITY
	release
	end

FuchsiaCity_EventScript_TopazeFind0_Done::
	release
	end

FuchsiaCity_EventScript_TopazeFind0_Full::
	msgbox FuchsiaCity_Text_TopazeFindFull
	release
	end


FuchsiaCity_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"

@ Topaze: tableau d'avis (ou trouver les rares)
FuchsiaCity_EventScript_NoticeBoard::
	msgbox FuchsiaCity_Text_NoticeBoard, MSGBOX_SIGN
	end

FuchsiaCity_Text_NoticeBoard::
	.string "WANTED: SHEDINJA: WHISPER GROVE.\n"
	.string "ELECTABUZZ: TRADE DOCK, SPARK\p"
	.string "GLADE. MAGMAR: TRADE DOCK, EMBER\n"
	.string "RIM.$"

@ TOPAZE FERRY CHUNK : passeurs supplementaires (troncons de 1000000 destinations)
