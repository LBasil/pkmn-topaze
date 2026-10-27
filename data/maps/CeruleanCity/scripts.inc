CeruleanCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CeruleanCity_OnTransition
	.byte 0

CeruleanCity_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_CERULEAN_CITY
	call_if_unset FLAG_GOT_SS_TICKET, CeruleanCity_EventScript_BlockExits
	call_if_set FLAG_BADGE02_GET, CeruleanCity_EventScript_NorthPoliceLeaves
	end

CeruleanCity_EventScript_NorthPoliceLeaves::
	setflag FLAG_TEMP_14
	return

CeruleanCity_EventScript_NorthPolice::
	lock
	faceplayer
	msgbox CeruleanCity_Text_NorthPolice
	applymovement LOCALID_CERULEAN_POLICE_N, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

CeruleanCity_EventScript_NorthBlocked::
	msgbox CeruleanCity_Text_NorthPolice
	applymovement LOCALID_PLAYER, CeruleanCity_Movement_PlayerBackOff
	waitmovement 0
	releaseall
	end

CeruleanCity_Movement_PlayerBackOff::
	walk_down
	step_end

CeruleanCity_EventScript_BlockExits::
	setobjectxyperm LOCALID_CERULEAN_SLOWBRO, 24, 31
	setobjectxyperm LOCALID_CERULEAN_LASS, 25, 31
	return

CeruleanCity_EventScript_RivalTriggerLeft::
	lockall
	goto_if_unset FLAG_BADGE02_GET, CeruleanCity_EventScript_NorthBlocked
	setvar VAR_TEMP_1, 0
	goto CeruleanCity_EventScript_Rival
	end

CeruleanCity_EventScript_RivalTriggerMid::
	lockall
	goto_if_unset FLAG_BADGE02_GET, CeruleanCity_EventScript_NorthBlocked
	setvar VAR_TEMP_1, 1
	setobjectxyperm LOCALID_CERULEAN_RIVAL, 23, 0
	goto CeruleanCity_EventScript_Rival
	end

CeruleanCity_EventScript_RivalTriggerRight::
	lockall
	goto_if_unset FLAG_BADGE02_GET, CeruleanCity_EventScript_NorthBlocked
	setvar VAR_TEMP_1, 2
	setobjectxyperm LOCALID_CERULEAN_RIVAL, 24, 0
	goto CeruleanCity_EventScript_Rival
	end

CeruleanCity_EventScript_Rival::
	textcolor NPC_TEXT_COLOR_MALE
	setvar VAR_MAP_SCENE_ROUTE22, 2
	playbgm MUS_ENCOUNTER_RIVAL, 0
	addobject LOCALID_CERULEAN_RIVAL
	applymovement LOCALID_CERULEAN_RIVAL, CeruleanCity_Movement_RivalEnter
	waitmovement 0
	msgbox CeruleanCity_Text_RivalIntro
	setvar VAR_LAST_TALKED, LOCALID_CERULEAN_RIVAL
	call_if_eq VAR_STARTER_MON, 2, CeruleanCity_EventScript_RivalSquirtle
	call_if_eq VAR_STARTER_MON, 1, CeruleanCity_EventScript_RivalBulbasaur
	call_if_eq VAR_STARTER_MON, 0, CeruleanCity_EventScript_RivalCharmander
	famechecker FAMECHECKER_BILL, 0
	msgbox CeruleanCity_Text_RivalPostBattle
	closemessage
	playbgm MUS_RIVAL_EXIT, 0
	call_if_eq VAR_TEMP_1, 0, CeruleanCity_EventScript_RivalStartExit
	call_if_eq VAR_TEMP_1, 1, CeruleanCity_EventScript_RivalStartExit
	call_if_eq VAR_TEMP_1, 2, CeruleanCity_EventScript_RivalStartExitRight
	msgbox CeruleanCity_Text_OhRightLittlePresentAsFavor
	setvar VAR_MAP_SCENE_CERULEAN_CITY_RIVAL, 1
	setflag FLAG_GOT_FAME_CHECKER
	giveitem ITEM_FAME_CHECKER
	msgbox CeruleanCity_Text_ExplainFameCheckerSmellYa
	closemessage
	applymovement LOCALID_CERULEAN_RIVAL, CeruleanCity_Movement_RivalExit
	waitmovement 0
	fadedefaultbgm
	removeobject LOCALID_CERULEAN_RIVAL
	releaseall
	end

CeruleanCity_EventScript_RivalSquirtle::
	trainerbattle_no_intro TRAINER_RIVAL_CERULEAN_SQUIRTLE, CeruleanCity_Text_RivalDefeat
	return

CeruleanCity_EventScript_RivalBulbasaur::
	trainerbattle_no_intro TRAINER_RIVAL_CERULEAN_BULBASAUR, CeruleanCity_Text_RivalDefeat
	return

CeruleanCity_EventScript_RivalCharmander::
	trainerbattle_no_intro TRAINER_RIVAL_CERULEAN_CHARMANDER, CeruleanCity_Text_RivalDefeat
	return

CeruleanCity_EventScript_RivalStartExit::
	applymovement LOCALID_PLAYER, CeruleanCity_Movement_PlayerWatchRivalExit
	applymovement LOCALID_CERULEAN_RIVAL, CeruleanCity_Movement_RivalStartExit
	waitmovement 0
	return

CeruleanCity_EventScript_RivalStartExitRight::
	applymovement LOCALID_PLAYER, CeruleanCity_Movement_PlayerWatchRivalExitRight
	applymovement LOCALID_CERULEAN_RIVAL, CeruleanCity_Movement_RivalStartExitRight
	waitmovement 0
	return

CeruleanCity_Movement_PlayerWatchRivalExit::
	delay_16
	delay_8
	walk_in_place_faster_right
	delay_16
	walk_in_place_faster_down
	step_end

CeruleanCity_Movement_PlayerWatchRivalExitRight::
	delay_16
	delay_8
	walk_in_place_faster_left
	delay_16
	walk_in_place_faster_down
	step_end

CeruleanCity_Movement_RivalEnter::
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

CeruleanCity_Movement_RivalStartExit::
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	delay_16
	delay_16
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

CeruleanCity_Movement_RivalStartExitRight::
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	delay_16
	delay_16
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

CeruleanCity_Movement_RivalExit::
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

CeruleanCity_EventScript_Policeman::
	lock
	faceplayer
	goto_if_set FLAG_GOT_SS_TICKET, CeruleanCity_EventScript_PolicemanOpen
	msgbox CeruleanCity_Text_RoadsClosed
	closemessage
	applymovement LOCALID_CERULEAN_POLICEMAN, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

CeruleanCity_EventScript_PolicemanOpen::
	msgbox CeruleanCity_Text_EastTree
	closemessage
	applymovement LOCALID_CERULEAN_POLICEMAN, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

CeruleanCity_EventScript_LittleBoy::
	lock
	faceplayer
	goto_if_set FLAG_GOT_SS_TICKET, CeruleanCity_EventScript_LittleBoySlowbroMoved
	msgbox CeruleanCity_Text_IfSlowbroWasntThereCouldCutTree
	release
	end

CeruleanCity_EventScript_LittleBoySlowbroMoved::
	msgbox CeruleanCity_Text_YouCanCutDownSmallTrees
	release
	end

CeruleanCity_EventScript_BaldingMan::
	msgbox CeruleanCity_Text_PokemonEncyclopediaAmusing, MSGBOX_NPC
	end

CeruleanCity_EventScript_Youngster::
	msgbox CeruleanCity_Text_TrainerLifeIsToughIsntIt, MSGBOX_NPC
	end

CeruleanCity_EventScript_CeruleanCaveGuard::
	msgbox CeruleanCity_Text_ThisIsCeruleanCave, MSGBOX_NPC
	end

CeruleanCity_EventScript_Woman::
	lock
	faceplayer
	msgbox CeruleanCity_Text_WantBrightRedBicycle
	closemessage
	applymovement LOCALID_CERULEAN_WOMAN, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

CeruleanCity_EventScript_SouthPolice::
	lock
	faceplayer
	goto_if_set FLAG_GOT_SS_TICKET, CeruleanCity_EventScript_SouthPoliceOpen
	msgbox CeruleanCity_Text_RoadsClosed
	release
	end

CeruleanCity_EventScript_SouthPoliceOpen::
	msgbox CeruleanCity_Text_RoadsOpen
	release
	end

CeruleanCity_EventScript_CitySign::
	msgbox CeruleanCity_Text_CitySign, MSGBOX_SIGN
	end

CeruleanCity_EventScript_TrainerTips::
	msgbox CeruleanCity_Text_TrainerTipsHeldItems, MSGBOX_SIGN
	end

CeruleanCity_EventScript_BikeShopSign::
	msgbox CeruleanCity_Text_BikeShopSign, MSGBOX_SIGN
	end

CeruleanCity_EventScript_GymSign::
	lockall
	famechecker FAMECHECKER_MISTY, 0
	msgbox CeruleanCity_Text_GymSign
	releaseall
	end

@ Topaze, fin 2 « Le Refuge » : poste 4/16 (DANTE) — duel contre 2 chasseurs, recompense : Bagon
CeruleanCity_EventScript_Refuge::
	lock
	faceplayer
	goto_if_ne VAR_TOPAZE_ENDING, 2, CeruleanCity_EventScript_RefugeIdle
	goto_if_gt VAR_REFUGE_STAGE, 3, CeruleanCity_EventScript_RefugeDone
	goto_if_lt VAR_REFUGE_STAGE, 3, CeruleanCity_EventScript_RefugeEarly
	msgbox CeruleanCity_Text_RefAsk
	setvar VAR_TOPAZE_BOOST, 47
	trainerbattle_no_intro TRAINER_GENTLEMAN_ARTHUR, CeruleanCity_Text_RefHunter1
	setvar VAR_TOPAZE_BOOST, 18
	trainerbattle_no_intro TRAINER_JUGGLER_NELSON, CeruleanCity_Text_RefHunter2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	goto CeruleanCity_EventScript_RefugeReward
	end

CeruleanCity_EventScript_RefugeReward::
	msgbox CeruleanCity_Text_RefGives
	givemon SPECIES_BAGON, 0
	addvar VAR_REFUGE_STAGE, 1
	msgbox CeruleanCity_Text_RefAfter
	release
	end

CeruleanCity_EventScript_RefugeEarly::
	msgbox CeruleanCity_Text_RefEarly
	release
	end

CeruleanCity_EventScript_RefugeDone::
	msgbox CeruleanCity_Text_RefDone
	release
	end

CeruleanCity_EventScript_RefugeIdle::
	msgbox CeruleanCity_Text_RefIdle
	release
	end

CeruleanCity_EventScript_CellWitness::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_CELL_CERULEAN, CeruleanCity_EventScript_CellWitnessDone
	goto_if_defeated TRAINER_RICH_BOY, CeruleanCity_EventScript_CellWitnessHalf
	msgbox CeruleanCity_Text_CellWitness, MSGBOX_DEFAULT
	release
	end

CeruleanCity_EventScript_CellWitnessHalf::
	msgbox CeruleanCity_Text_CellWitnessHalf, MSGBOX_DEFAULT
	release
	end

CeruleanCity_EventScript_CellWitnessDone::
	msgbox CeruleanCity_Text_CellWitnessDone, MSGBOX_DEFAULT
	release
	end

CeruleanCity_Text_CellWitness::
	.string "The police watch the north road all"
	.string "day. Nobody watches that house.\p"
	.string "Its lights burn at night and a new"
	.string "lock appears on the door each week.$"

CeruleanCity_Text_CellWitnessHalf::
	.string "You went in? Then look at the wall"
	.string "behind them. They write it down.$"

CeruleanCity_Text_CellWitnessDone::
	.string "The lights are normal again.\p"
	.string "A pity. They paid for every lock"
	.string "in cash. Who has that much cash?$"

@ Topaze: the hollow trunk (CERULEAN CAVE) stays sealed until RED (Sevault summit) is beaten
CeruleanCity_EventScript_CaveSealed::
	goto_if_defeated TRAINER_BIKER_1, EventScript_Return
	lockall
	msgbox CeruleanCity_Text_CaveSealed
	applymovement OBJ_EVENT_ID_PLAYER, CeruleanCity_Movement_CaveBack
	waitmovement 0
	releaseall
	end

CeruleanCity_Movement_CaveBack::
	walk_down
	step_end
