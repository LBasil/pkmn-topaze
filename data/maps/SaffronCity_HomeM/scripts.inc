SaffronCity_HomeM_MapScripts::
	.byte 0

SaffronCity_HomeM_EventScript_Master::
	lock
	faceplayer
	goto_if_unset FLAG_BADGE08_GET, SaffronCity_HomeM_EventScript_Early
	msgbox SaffronCity_HomeM_Text_Intro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SaffronCity_HomeM_EventScript_Decline
	special HealPlayerParty
	msgbox SaffronCity_HomeM_Text_Go
	closemessage
	trainerbattle_no_intro TRAINER_TRIAL_1, SaffronCity_HomeM_Text_Beat1
	trainerbattle_no_intro TRAINER_TRIAL_2, SaffronCity_HomeM_Text_Beat2
	trainerbattle_no_intro TRAINER_TRIAL_3, SaffronCity_HomeM_Text_Beat3
	trainerbattle_no_intro TRAINER_TRIAL_4, SaffronCity_HomeM_Text_Beat4
	trainerbattle_no_intro TRAINER_TRIAL_5, SaffronCity_HomeM_Text_Beat5
	goto_if_defeated TRAINER_TRIAL_5, SaffronCity_HomeM_EventScript_Repeat
	release
	end
SaffronCity_HomeM_EventScript_Repeat::
	msgbox SaffronCity_HomeM_Text_Clear
	checkitemspace ITEM_RARE_CANDY, 5
	goto_if_eq VAR_RESULT, FALSE, SaffronCity_HomeM_EventScript_NoRoom
	giveitem ITEM_RARE_CANDY, 5
	release
	end
SaffronCity_HomeM_EventScript_Early::
	msgbox SaffronCity_HomeM_Text_Early
	release
	end
SaffronCity_HomeM_EventScript_Decline::
	msgbox SaffronCity_HomeM_Text_Decline
	release
	end
SaffronCity_HomeM_EventScript_NoRoom::
	msgbox SaffronCity_HomeM_Text_NoRoom
	release
	end
