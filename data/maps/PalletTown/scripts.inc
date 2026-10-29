.equ SIGN_LADY_READY, VAR_TEMP_2

PalletTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PalletTown_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, PalletTown_OnFrame
	.byte 0

PalletTown_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_PALLET_TOWN
	call_if_set FLAG_TOPAZE_POSTGAME, PalletTown_EventScript_CheckMineHint
	call_if_set FLAG_PALLET_LADY_NOT_BLOCKING_SIGN, PalletTown_EventScript_TryReadySignLady
	call_if_eq VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 0, PalletTown_EventScript_SetSignLadyPos
	call_if_eq VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 1, PalletTown_EventScript_SetSignLadyDone
	end

PalletTown_EventScript_TryReadySignLady::
	goto_if_unset FLAG_OPENED_START_MENU, EventScript_Return
	goto_if_ge VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 1, EventScript_Return
	setvar VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 1
	return

PalletTown_EventScript_SetSignLadyDone::
	setvar VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 2
	return

PalletTown_EventScript_SetSignLadyPos::
	goto_if_set FLAG_PALLET_LADY_NOT_BLOCKING_SIGN, PalletTown_EventScript_MoveSignLadyToRouteEntrance
	setobjectxyperm LOCALID_PALLET_SIGN_LADY, 10, 20
	setobjectmovementtype LOCALID_PALLET_SIGN_LADY, MOVEMENT_TYPE_FACE_UP
	return

PalletTown_EventScript_MoveSignLadyToRouteEntrance::
	setobjectxyperm LOCALID_PALLET_SIGN_LADY, 22, 6
	setobjectmovementtype LOCALID_PALLET_SIGN_LADY, MOVEMENT_TYPE_FACE_DOWN
	setvar SIGN_LADY_READY, TRUE
	return

PalletTown_OnFrame::
	map_script_2 VAR_MAP_SCENE_PALLET_TOWN_OAK, 2, PalletTown_EventScript_OakRatingScene
	map_script_2 VAR_TEMP_F, 1, PalletTown_EventScript_MineHint
	.2byte 0

@ Oak approaches player after exiting their house post Elite Four to check if they should receieve the National Dex
PalletTown_EventScript_OakRatingScene::
	lockall
	textcolor NPC_TEXT_COLOR_MALE
	setobjectxyperm LOCALID_PALLET_PROF_OAK, 22, 19
	setobjectmovementtype LOCALID_PALLET_PROF_OAK, MOVEMENT_TYPE_FACE_LEFT
	addobject LOCALID_PALLET_PROF_OAK
	applymovement LOCALID_PALLET_PROF_OAK, PalletTown_Movement_OakWalkToPlayersDoor
	waitmovement 0
	goto_if_unset FLAG_WORLD_MAP_ONE_ISLAND, PalletTown_EventScript_NotBeenToOneIslandYet
	msgbox PalletTown_Text_OakLetMeSeePokedex
	setvar VAR_0x8004, 0
	specialvar VAR_RESULT, GetPokedexCount
	copyvar VAR_0x8008, VAR_0x8005
	copyvar VAR_0x8009, VAR_0x8006
	buffernumberstring STR_VAR_1, VAR_0x8008
	buffernumberstring STR_VAR_2, VAR_0x8009
	goto_if_lt VAR_0x8009, 60, PalletTown_EventScript_NotEnoughMonsForNationalDex
	msgbox PalletTown_Text_CaughtXImpressiveFollowMe
	closemessage
	playbgm MUS_FOLLOW_ME, 0
	applymovement LOCALID_PLAYER, PalletTown_Movement_PlayerWalkToLabFromHouse
	applymovement LOCALID_PALLET_PROF_OAK, PalletTown_Movement_OakWalkToLabFromHouse
	waitmovement 0
	opendoor 35, 25
	waitdooranim
	applymovement LOCALID_PALLET_PROF_OAK, PalletTown_Movement_OakEnterLab
	applymovement LOCALID_PLAYER, PalletTown_Movement_PlayerEnterLab
	waitmovement 0
	closedoor 35, 25
	waitdooranim
	setvar VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB, 7
	setvar VAR_MAP_SCENE_PALLET_TOWN_OAK, 3
	setflag FLAG_HIDE_OAK_IN_PALLET_TOWN
	warp MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB, 6, 12
	waitstate
	releaseall
	end

PalletTown_EventScript_EndOakRatingScene::
	closemessage
	applymovement LOCALID_PALLET_PROF_OAK, PalletTown_Movement_OakExit
	waitmovement 0
	removeobject LOCALID_PALLET_PROF_OAK
	setvar VAR_MAP_SCENE_PALLET_TOWN_OAK, 3
	releaseall
	end

PalletTown_EventScript_NotEnoughMonsForNationalDex::
	msgbox PalletTown_Text_CaughtXPuttingInHonestEffort
	goto PalletTown_EventScript_EndOakRatingScene
	end

PalletTown_EventScript_NotBeenToOneIslandYet::
	msgbox PalletTown_Text_OakYouEnjoyingTraveling
	goto PalletTown_EventScript_EndOakRatingScene
	end

PalletTown_Movement_OakWalkToPlayersDoor::
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_in_place_faster_left
	step_end

PalletTown_Movement_OakExit::
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	step_end

PalletTown_Movement_OakWalkToLabFromHouse::
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_in_place_faster_up
	step_end

PalletTown_Movement_PlayerWalkToLabFromHouse::
	walk_right
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

PalletTown_EventScript_OakTriggerLeft::
	lockall
	setvar VAR_TEMP_1, 0
	goto PalletTown_EventScript_OakTrigger
	end

PalletTown_EventScript_OakTriggerRight::
	lockall
	setvar VAR_TEMP_1, 1
	goto PalletTown_EventScript_OakTrigger
	end

PalletTown_EventScript_OakTrigger::
	goto_if_eq VAR_GRENALUX_OPENING, 2, PalletTown_EventScript_ExitGate
	goto_if_eq VAR_GRENALUX_OPENING, 3, PalletTown_EventScript_ExitGate
	goto_if_ne VAR_GRENALUX_OPENING, 0, PalletTown_EventScript_ExitFree
	@ Topaze: the rival stops the player and takes them to his family's RANCH, where OAK waits
	textcolor NPC_TEXT_COLOR_MALE
	delay 30
	playbgm MUS_RIVAL_EXIT, 0
	message PalletTown_Text_RivalDontGoOut
	waitmessage
	delay 85
	closemessage
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_PLAYER, Common_Movement_ExclamationMark
	waitmovement 0
	delay 30
	addobject LOCALID_PALLET_RIVAL
	call_if_eq VAR_TEMP_1, 0, PalletTown_EventScript_RivalEnterLeft
	call_if_eq VAR_TEMP_1, 1, PalletTown_EventScript_RivalEnterRight
	delay 30
	msgbox PalletTown_Text_RivalGrassUnsafeNeedMon
	closemessage
	delay 30
	call_if_eq VAR_TEMP_1, 0, PalletTown_EventScript_RivalLeadPlayerToRanchLeft
	call_if_eq VAR_TEMP_1, 1, PalletTown_EventScript_RivalLeadPlayerToRanchRight
	removeobject LOCALID_PALLET_RIVAL
	setflag FLAG_HIDE_PALLET_RIVAL
	setvar VAR_GRENALUX_OPENING, 1
	setflag FLAG_DONT_TRANSITION_MUSIC
	warp MAP_PALLET_TOWN_RANCH, 0, 7
	waitstate
	releaseall
	end

PalletTown_EventScript_ExitGate::
	msgbox PalletTown_Text_ExitGate
	closemessage
	applymovement LOCALID_PLAYER, PalletTown_Movement_ExitGateBack
	waitmovement 0
	releaseall
	end

PalletTown_Movement_ExitGateBack::
	walk_down
	step_end

PalletTown_EventScript_ExitFree::
	releaseall
	end

PalletTown_EventScript_RivalEnterLeft::
	applymovement LOCALID_PALLET_RIVAL, PalletTown_Movement_OakEnterLeft
	waitmovement 0
	return

PalletTown_EventScript_RivalEnterRight::
	applymovement LOCALID_PALLET_RIVAL, PalletTown_Movement_OakEnterRight
	waitmovement 0
	return

PalletTown_EventScript_RivalLeadPlayerToRanchLeft::
	applymovement LOCALID_PALLET_RIVAL, PalletTown_Movement_RivalWalkToRanchLeft
	applymovement LOCALID_PLAYER, PalletTown_Movement_PlayerWalkToRanchLeft
	waitmovement 0
	return

PalletTown_EventScript_RivalLeadPlayerToRanchRight::
	applymovement LOCALID_PALLET_RIVAL, PalletTown_Movement_RivalWalkToRanchRight
	applymovement LOCALID_PLAYER, PalletTown_Movement_PlayerWalkToRanchRight
	waitmovement 0
	return

PalletTown_Movement_RivalWalkToRanchLeft::
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

PalletTown_Movement_PlayerWalkToRanchLeft::
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	step_end

PalletTown_Movement_RivalWalkToRanchRight::
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

PalletTown_Movement_PlayerWalkToRanchRight::
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	step_end

PalletTown_Movement_OakEnterLeft::
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

PalletTown_Movement_OakEnterRight::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

PalletTown_Movement_OakEnterLab::
	walk_up
	set_invisible
	step_end

PalletTown_Movement_PlayerEnterLab::
	walk_right
	walk_up
	set_invisible
	step_end

PalletTown_EventScript_SignLady::
	lock
	goto_if_eq VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 2, PalletTown_EventScript_SignLadyDone
	goto_if_eq VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 1, PalletTown_EventScript_SignLadyJustShowedSign
	goto_if_eq SIGN_LADY_READY, TRUE, PalletTown_EventScript_SignLadyStartShowSign
	goto_if_set FLAG_TEMP_2, PalletTown_EventScript_SignLadyGoReadSign
	msgbox PalletTown_Text_HmmIsThatRight
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_FacePlayer
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_Delay48
	waitmovement 0
	msgbox PalletTown_Text_OhLookLook
	closemessage
	call_if_eq VAR_FACING, DIR_EAST, PalletTown_EventScript_SignLadyMoveOutOfWayRight
	call_if_ne VAR_FACING, DIR_EAST, PalletTown_EventScript_SignLadyMoveOutOfWayLeft
	copyobjectxytoperm LOCALID_PALLET_SIGN_LADY
	setflag FLAG_TEMP_2
	release
	end

PalletTown_EventScript_SignLadyMoveOutOfWayRight::
	applymovement LOCALID_PALLET_SIGN_LADY, PalletTown_Movement_SignLadyMoveOutOfWayRight
	waitmovement 0
	return

PalletTown_EventScript_SignLadyMoveOutOfWayLeft::
	applymovement LOCALID_PALLET_SIGN_LADY, PalletTown_Movement_SignLadyMoveOutOfWayLeft
	waitmovement 0
	return

PalletTown_EventScript_SignLadyDone::
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_FacePlayer
	waitmovement 0
	msgbox PalletTown_Text_RaisingMonsToo
	release
	end

PalletTown_EventScript_SignLadyGoReadSign::
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_FacePlayer
	waitmovement 0
	msgbox PalletTown_Text_ReadItReadIt
	release
	end

PalletTown_EventScript_SignLadyJustShowedSign::
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_FacePlayer
	waitmovement 0
	msgbox PalletTown_Text_SignsAreUsefulArentThey
	release
	end

PalletTown_Movement_SignLadyMoveOutOfWayRight::
	walk_right
	walk_in_place_faster_left
	step_end

PalletTown_Movement_SignLadyMoveOutOfWayLeft::
	walk_left
	walk_in_place_faster_right
	step_end

PalletTown_EventScript_FatMan::
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_EventScript_FatManStrike
	msgbox PalletTown_Text_FatManA, MSGBOX_NPC
	end

PalletTown_EventScript_FatManStrike::
	msgbox PalletTown_Text_FatManB, MSGBOX_NPC
	end

PalletTown_EventScript_OaksLabSign::
	lockall
	famechecker FAMECHECKER_OAK, 0
	msgbox PalletTown_Text_OakPokemonResearchLab
	releaseall
	end

PalletTown_EventScript_PlayersHouseSign::
	msgbox PalletTown_Text_PlayersHouse, MSGBOX_SIGN
	end

PalletTown_EventScript_RivalsHouseSign::
	msgbox PalletTown_Text_RivalsHouse, MSGBOX_SIGN
	end

PalletTown_EventScript_TownSign::
	msgbox PalletTown_Text_TownSign, MSGBOX_SIGN
	end

PalletTown_EventScript_TrainerTips::
	lockall
	msgbox PalletTown_Text_PressStartToOpenMenu
	setvar VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 1
	releaseall
	end

PalletTown_EventScript_SignLadyTrigger::
	lockall
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_WalkInPlaceFasterRight
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	call PalletTown_EventScript_SignLadyShowSign
	releaseall
	end

PalletTown_EventScript_SignLadyShowSign::
	textcolor NPC_TEXT_COLOR_FEMALE
	msgbox PalletTown_Text_LookCopiedTrainerTipsSign
	closemessage
	delay 20
	textcolor NPC_TEXT_COLOR_NEUTRAL
	setflag FLAG_OPENED_START_MENU
	setvar VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 1
	setvar SIGN_LADY_READY, FALSE
	special SetWalkingIntoSignVars
	special DisableMsgBoxWalkaway
	signmsg
	msgbox PalletTown_Text_PressStartToOpenMenuCopy
	normalmsg
	return

PalletTown_EventScript_SignLadyStartShowSign::
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_FacePlayer
	waitmovement 0
	call PalletTown_EventScript_SignLadyShowSign
	release
	end

PalletTown_EventScript_SchoolSign::
	msgbox PalletTown_Text_SchoolSign, MSGBOX_SIGN
	end

PalletTown_EventScript_AmbMiner::
	goto_if_set FLAG_SYS_GAME_CLEAR, PalletTown_EventScript_AmbMinerPost
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_EventScript_AmbMinerStrike
	msgbox PalletTown_Text_AmbMinerA, MSGBOX_NPC
	end

PalletTown_EventScript_AmbMinerStrike::
	msgbox PalletTown_Text_AmbMinerB, MSGBOX_NPC
	end

PalletTown_EventScript_AmbMinerPost::
	msgbox PalletTown_Text_AmbMinerD, MSGBOX_NPC
	end

PalletTown_EventScript_AmbOldman::
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_EventScript_AmbOldmanStrike
	msgbox PalletTown_Text_AmbOldmanA, MSGBOX_NPC
	end

PalletTown_EventScript_AmbOldmanStrike::
	msgbox PalletTown_Text_AmbOldmanB, MSGBOX_NPC
	end

PalletTown_EventScript_AmbGirl::
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_EventScript_AmbGirlStrike
	msgbox PalletTown_Text_AmbGirlA, MSGBOX_NPC
	end

PalletTown_EventScript_AmbGirlStrike::
	msgbox PalletTown_Text_AmbGirlB, MSGBOX_NPC
	end

PalletTown_EventScript_AmbBoy::
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_EventScript_AmbBoyStrike
	msgbox PalletTown_Text_AmbBoyA, MSGBOX_NPC
	end

PalletTown_EventScript_AmbBoyStrike::
	msgbox PalletTown_Text_AmbBoyB, MSGBOX_NPC
	end

PalletTown_EventScript_AmbScientist::
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_EventScript_AmbScientistStrike
	msgbox PalletTown_Text_AmbScientistA, MSGBOX_NPC
	end

PalletTown_EventScript_AmbScientistStrike::
	msgbox PalletTown_Text_AmbScientistB, MSGBOX_NPC
	end

PalletTown_EventScript_AmbGardener::
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_EventScript_AmbGardenerStrike
	msgbox PalletTown_Text_AmbGardenerA, MSGBOX_NPC
	end

PalletTown_EventScript_AmbGardenerStrike::
	msgbox PalletTown_Text_AmbGardenerB, MSGBOX_NPC
	end

PalletTown_EventScript_AmbLady::
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_EventScript_AmbLadyStrike
	msgbox PalletTown_Text_AmbLadyA, MSGBOX_NPC
	end

PalletTown_EventScript_AmbLadyStrike::
	msgbox PalletTown_Text_AmbLadyB, MSGBOX_NPC
	end

PalletTown_EventScript_SceneryMonument::
	msgbox PalletTown_Text_SceneryMonument, MSGBOX_SIGN
	end

PalletTown_EventScript_SceneryGuardian::
	msgbox PalletTown_Text_SceneryGuardian, MSGBOX_SIGN
	end

PalletTown_EventScript_SceneryMine::
	goto_if_set FLAG_TOPAZE_POSTGAME, PalletTown_EventScript_SceneryMineOpen
	msgbox PalletTown_Text_SceneryMine, MSGBOX_SIGN
	end

PalletTown_EventScript_SceneryMineOpen::
	msgbox PalletTown_Text_SceneryMineOpen, MSGBOX_SIGN
	end

@ Topaze: the mine opens in the postgame (ending 1)
PalletTown_EventScript_MineGate::
	lockall
	goto_if_set FLAG_TOPAZE_POSTGAME, PalletTown_EventScript_MineEnter
	msgbox PalletTown_Text_SceneryMine
	closemessage
	applymovement LOCALID_PLAYER, PalletTown_Movement_MineBack
	waitmovement 0
	releaseall
	end

PalletTown_EventScript_MineEnter::
	warp MAP_GRENALUX_MINE_1F, 18, 37
	waitstate
	releaseall
	end

PalletTown_EventScript_SceneryBerries::
	msgbox PalletTown_Text_SceneryBerries, MSGBOX_SIGN
	end

PalletTown_Movement_MineBack::
	walk_down
	step_end

@ Topaze, fin 2 « Le Refuge » : poste 1/16 (AYA) — livraison d'objets, recompense : Eevee
PalletTown_EventScript_Refuge::
	lock
	faceplayer
	goto_if_ne VAR_TOPAZE_ENDING, 2, PalletTown_EventScript_RefugeIdle
	goto_if_gt VAR_REFUGE_STAGE, 0, PalletTown_EventScript_RefugeDone
	goto_if_lt VAR_REFUGE_STAGE, 0, PalletTown_EventScript_RefugeEarly
	checkitem ITEM_POTION, 5
	goto_if_eq VAR_RESULT, TRUE, PalletTown_EventScript_RefugeOffer
	msgbox PalletTown_Text_RefAsk
	release
	end

PalletTown_EventScript_RefugeOffer::
	msgbox PalletTown_Text_RefOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PalletTown_EventScript_RefugeRefuse
	removeitem ITEM_POTION, 5
	goto PalletTown_EventScript_RefugeReward
	end

PalletTown_EventScript_RefugeRefuse::
	msgbox PalletTown_Text_RefNo
	release
	end

PalletTown_EventScript_RefugeReward::
	msgbox PalletTown_Text_RefGives
	givemon SPECIES_EEVEE, 0
	addvar VAR_REFUGE_STAGE, 1
	msgbox PalletTown_Text_RefAfter
	release
	end

PalletTown_EventScript_RefugeEarly::
	msgbox PalletTown_Text_RefEarly
	release
	end

PalletTown_EventScript_RefugeDone::
	msgbox PalletTown_Text_RefDone
	release
	end

PalletTown_EventScript_RefugeIdle::
	msgbox PalletTown_Text_RefIdle
	release
	end

@ Topaze: indice automatique post-game (la mine est ouverte)
PalletTown_EventScript_CheckMineHint::
	goto_if_set FLAG_HINT_GRENALUX_MINE, EventScript_Return
	setvar VAR_TEMP_F, 1
	return

PalletTown_EventScript_MineHint::
	lockall
	setflag FLAG_HINT_GRENALUX_MINE
	setvar VAR_TEMP_F, 0
	msgbox PalletTown_Text_MineHint
	releaseall
	end

@ Topaze: PROCHE ADRIAN (optionnel, fort)
PalletTown_EventScript_ProcheAdrian::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_POSTGAME, PalletTown_EventScript_ProcheAdrian_TooEarly
	goto_if_not_defeated TRAINER_PROCHE_THOMAS, PalletTown_EventScript_ProcheAdrian_TooEarly
	goto_if_not_defeated TRAINER_PROCHE_LOLA, PalletTown_EventScript_ProcheAdrian_TooEarly
	goto_if_not_defeated TRAINER_PROCHE_JORDAN, PalletTown_EventScript_ProcheAdrian_TooEarly
	goto_if_not_defeated TRAINER_PROCHE_VIOLETTE, PalletTown_EventScript_ProcheAdrian_TooEarly
	goto_if_not_defeated TRAINER_PROCHE_EDOUARD, PalletTown_EventScript_ProcheAdrian_TooEarly
	goto_if_not_defeated TRAINER_PROCHE_EMMA, PalletTown_EventScript_ProcheAdrian_TooEarly
	goto_if_not_defeated TRAINER_PROCHE_GAUTHIER, PalletTown_EventScript_ProcheAdrian_TooEarly
	goto_if_not_defeated TRAINER_PROCHE_CHLOE, PalletTown_EventScript_ProcheAdrian_TooEarly
	goto_if_not_defeated TRAINER_PROCHE_VINCENT, PalletTown_EventScript_ProcheAdrian_TooEarly
	goto_if_not_defeated TRAINER_PROCHE_THIBAULT, PalletTown_EventScript_ProcheAdrian_TooEarly
	goto_if_not_defeated TRAINER_PROCHE_NATHAN, PalletTown_EventScript_ProcheAdrian_TooEarly
	goto_if_not_defeated TRAINER_PROCHE_DYLAN, PalletTown_EventScript_ProcheAdrian_TooEarly
	goto_if_defeated TRAINER_PROCHE_ADRIAN, PalletTown_EventScript_ProcheAdrian_After
	msgbox PalletTown_Text_ProcheAdrian_Gather
	msgbox PalletTown_Text_ProcheAdrian_Intro
	checkitemspace ITEM_MASTER_BALL
	goto_if_eq VAR_RESULT, FALSE, PalletTown_EventScript_ProcheAdrian_NoRoom
	trainerbattle_no_intro TRAINER_PROCHE_ADRIAN, PalletTown_Text_ProcheAdrian_Defeat
	msgbox PalletTown_Text_ProcheAdrian_Win
	giveitem ITEM_MASTER_BALL
	msgbox PalletTown_Text_ProcheAdrian_After
	release
	end

PalletTown_EventScript_ProcheAdrian_After::
	msgbox PalletTown_Text_ProcheAdrian_After
	release
	end

PalletTown_EventScript_ProcheAdrian_TooEarly::
	msgbox PalletTown_Text_ProcheAdrian_Early
	release
	end

PalletTown_EventScript_ProcheAdrian_NoRoom::
	msgbox PalletTown_Text_ProcheAdrian_NoRoom
	release
	end

@ Topaze: ARCHIVISTE DES ECHOS (recompense quand les 7 Echos sont clos)
PalletTown_EventScript_EchoArchivist::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_ARCHIVE_DONE, PalletTown_EventScript_EchoArchivist_Done
	goto_if_unset FLAG_ECHO_BEAST_DONE, PalletTown_EventScript_EchoArchivist_Ask
	goto_if_unset FLAG_ECHO_BEAST2_DONE, PalletTown_EventScript_EchoArchivist_Ask
	goto_if_unset FLAG_ECHO_BEAST3_DONE, PalletTown_EventScript_EchoArchivist_Ask
	goto_if_unset FLAG_ECHO_BEAST4_DONE, PalletTown_EventScript_EchoArchivist_Ask
	goto_if_unset FLAG_ECHO_BEAST5_DONE, PalletTown_EventScript_EchoArchivist_Ask
	goto_if_unset FLAG_ECHO_BEAST6_DONE, PalletTown_EventScript_EchoArchivist_Ask
	goto_if_unset FLAG_DONE_ECHO_CELEBI, PalletTown_EventScript_EchoArchivist_Ask
	checkitemspace ITEM_RARE_CANDY, 5
	goto_if_eq VAR_RESULT, FALSE, PalletTown_EventScript_EchoArchivist_NoRoom
	setflag FLAG_TOPAZE_ARCHIVE_DONE
	msgbox PalletTown_Text_Archive_Solved
	giveitem ITEM_RARE_CANDY, 5
	release
	end

PalletTown_EventScript_EchoArchivist_Ask::
	msgbox PalletTown_Text_Archive_Ask
	release
	end

PalletTown_EventScript_EchoArchivist_Done::
	msgbox PalletTown_Text_Archive_Done
	release
	end

PalletTown_EventScript_EchoArchivist_NoRoom::
	msgbox PalletTown_Text_Archive_NoRoom
	release
	end

@ Topaze: quete (MILK FOR THE LAB)
PalletTown_EventScript_TQ::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_TQ_PALLETTOWN, PalletTown_EventScript_TQ_Done
	checkitem ITEM_MOOMOO_MILK, 2
	goto_if_eq VAR_RESULT, FALSE, PalletTown_EventScript_TQ_Ask
	checkitemspace ITEM_EXP_SHARE, 1
	goto_if_eq VAR_RESULT, FALSE, PalletTown_EventScript_TQ_NoRoom
	removeitem ITEM_MOOMOO_MILK, 2
	setflag FLAG_TOPAZE_TQ_PALLETTOWN
	msgbox PalletTown_Text_TQ_Ok
	giveitem ITEM_EXP_SHARE, 1
	release
	end

PalletTown_EventScript_TQ_Ask::
	msgbox PalletTown_Text_TQ_Ask
	release
	end

PalletTown_EventScript_TQ_Done::
	msgbox PalletTown_Text_TQ_Done
	release
	end

PalletTown_EventScript_TQ_NoRoom::
	msgbox PalletTown_Text_TQ_NoRoom
	release
	end
