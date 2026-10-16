CeruleanCity_Gym_MapScripts::
	.byte 0

CeruleanCity_Gym_EventScript_Misty::
	famechecker FAMECHECKER_MISTY, FCPICKSTATE_COLORED, UpdatePickStateFromSpecialVar8005
	trainerbattle_single TRAINER_LEADER_MISTY, CeruleanCity_Gym_Text_MistyIntro, CeruleanCity_Gym_Text_MistyDefeat, CeruleanCity_Gym_EventScript_MistyDefeated, NO_MUSIC
	goto_if_unset FLAG_GOT_TM03_FROM_MISTY, CeruleanCity_Gym_EventScript_GiveTM03
	call_if_set FLAG_TOPAZE_COUNCIL, CeruleanCity_Gym_EventScript_MistyVisit
	msgbox CeruleanCity_Gym_Text_ExplainTM03
	release
	end

CeruleanCity_Gym_EventScript_MistyDefeated::
	famechecker FAMECHECKER_MISTY, 1
	setflag FLAG_DEFEATED_MISTY
	setflag FLAG_BADGE02_GET
	setrespawn HEAL_LOCATION_CERULEAN_CITY
	set_gym_trainers 2
	goto CeruleanCity_Gym_EventScript_GiveTM03
	end

CeruleanCity_Gym_EventScript_GiveTM03::
	msgbox CeruleanCity_Gym_Text_ExplainCascadeBadge
	checkitemspace ITEM_TM19
	goto_if_eq VAR_RESULT, FALSE, CeruleanCity_Gym_EventScript_NoRoomForTM03
	giveitem_msg CeruleanCity_Gym_Text_ReceivedTM03FromMisty, ITEM_TM19
	setflag FLAG_GOT_TM03_FROM_MISTY
	msgbox CeruleanCity_Gym_Text_ExplainTM03
	release
	end

CeruleanCity_Gym_EventScript_NoRoomForTM03::
	msgbox CeruleanCity_Gym_Text_BetterMakeRoomForThis
	release
	end

CeruleanCity_Gym_EventScript_Diana::
	trainerbattle_single TRAINER_PICNICKER_DIANA, CeruleanCity_Gym_Text_DianaIntro, CeruleanCity_Gym_Text_DianaDefeat
	msgbox CeruleanCity_Gym_Text_DianaPostBattle, MSGBOX_AUTOCLOSE
	end

CeruleanCity_Gym_EventScript_Luis::
	trainerbattle_single TRAINER_SWIMMER_MALE_LUIS, CeruleanCity_Gym_Text_LuisIntro, CeruleanCity_Gym_Text_LuisDefeat
	famechecker FAMECHECKER_MISTY, 2
	msgbox CeruleanCity_Gym_Text_LuisPostBattle, MSGBOX_AUTOCLOSE
	end

CeruleanCity_Gym_EventScript_GymGuy::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_MISTY, CeruleanCity_Gym_EventScript_GymGuyPostVictory
	msgbox CeruleanCity_Gym_Text_GymGuyAdvice
	release
	end

CeruleanCity_Gym_EventScript_GymGuyPostVictory::
	msgbox CeruleanCity_Gym_Text_WeMakePrettyGoodTeam
	release
	end

CeruleanCity_Gym_EventScript_GymStatue::
	lockall
	goto_if_set FLAG_BADGE02_GET, CeruleanCity_Gym_EventScript_GymStatuePostVictory
	msgbox CeruleanCity_Gym_Text_GymStatue
	releaseall
	end

CeruleanCity_Gym_EventScript_GymStatuePostVictory::
	msgbox CeruleanCity_Gym_Text_GymStatuePlayerWon
	releaseall
	end

@ Topaze, post-game : le chef revient sur le Conseil et offre un cadeau selon la fin (fin 3 : duel de revanche)
CeruleanCity_Gym_EventScript_MistyVisit::
	goto_if_eq VAR_TOPAZE_ENDING, 3, CeruleanCity_Gym_EventScript_MistyVisit3
	goto_if_set FLAG_QUEST_LEADER_SYLVESTRE, EventScript_Return
	switch VAR_TOPAZE_ENDING
	case 1, CeruleanCity_Gym_EventScript_MistyVisit1
	case 2, CeruleanCity_Gym_EventScript_MistyVisit2
	return

CeruleanCity_Gym_EventScript_MistyVisit1::
	msgbox CeruleanCity_Gym_Text_MistyVisit1
	giveitem ITEM_MYSTIC_WATER, 1
	setflag FLAG_QUEST_LEADER_SYLVESTRE
	return

CeruleanCity_Gym_EventScript_MistyVisit2::
	msgbox CeruleanCity_Gym_Text_MistyVisit2
	giveitem ITEM_FULL_RESTORE, 3
	setflag FLAG_QUEST_LEADER_SYLVESTRE
	return

CeruleanCity_Gym_EventScript_MistyVisit3::
	goto_if_set FLAG_REBEL_SYLVESTRE, EventScript_Return
	msgbox CeruleanCity_Gym_Text_MistyRebel1
	setvar VAR_TOPAZE_BOOST, 50
	trainerbattle_no_intro TRAINER_LEADER_MISTY, CeruleanCity_Gym_Text_MistyRebel2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	setflag FLAG_REBEL_SYLVESTRE
	msgbox CeruleanCity_Gym_Text_MistyRebel3
	giveitem ITEM_RARE_CANDY, 5
	giveitem ITEM_PP_MAX, 2
	return
