FuchsiaCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FuchsiaCity_OnTransition
	.byte 0

FuchsiaCity_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_FUCHSIA_CITY
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
