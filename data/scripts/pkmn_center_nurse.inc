EventScript_PkmnCenterNurse::
	goto_if_questlog EventScript_ReleaseEnd
	message Text_WelcomeWantToHealPkmn
	waitmessage
	multichoice 19, 8, MULTICHOICE_YES_NO, FALSE | (TRUE << 1)
	switch VAR_RESULT
	case 0, EventScript_PkmnCenterNurse_HealPkmn
	case 1 EventScript_PkmnCenterNurse_Goodbye
	case SCR_MENU_CANCEL, EventScript_PkmnCenterNurse_Goodbye
	end

EventScript_PkmnCenterNurse_HealPkmn::
	incrementgamestat GAME_STAT_USED_POKECENTER
	message Text_TakeYourPkmnForFewSeconds
	waitmessage
	call EventScript_PkmnCenterNurse_TakeAndHealPkmn
	special SetUsedPkmnCenterQuestLogEvent
	goto EventScript_PkmnCenterNurse_CheckTrainerTowerAndUnionRoom
	end

EventScript_PkmnCenterNurse_TakeAndHealPkmn::
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	dofieldeffect FLDEFF_POKECENTER_HEAL
	waitfieldeffect FLDEFF_POKECENTER_HEAL
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	special HealPlayerParty
	return

EventScript_PkmnCenterNurse_CheckTrainerTowerAndUnionRoom::
	specialvar VAR_RESULT, IsPlayerNotInTrainerTowerLobby
	goto_if_eq VAR_RESULT, FALSE, EventScript_PkmnCenterNurse_ReturnPkmn
	specialvar VAR_RESULT, BufferUnionRoomPlayerName
	copyvar VAR_0x8008, VAR_RESULT
	goto_if_eq VAR_0x8008, 0, EventScript_PkmnCenterNurse_ReturnPkmn
	goto_if_eq VAR_0x8008, 1, EventScript_PkmnCenterNurse_PlayerWaitingInUnionRoom
	end

EventScript_PkmnCenterNurse_ReturnPkmn::
	message Text_RestoredPkmnToFullHealth
	waitmessage
	applymovement VAR_LAST_TALKED, Movement_Bow
	waitmovement 0
	call EventScript_PkmnCenterNurse_Relearner
	msgbox Text_WeHopeToSeeYouAgain
	return

EventScript_PkmnCenterNurse_PlayerWaitingInUnionRoom::
	goto_if_set FLAG_SYS_INFORMED_OF_LOCAL_WIRELESS_PLAYER, EventScript_PkmnCenterNurse_ReturnPkmn
	msgbox Text_RestoredPkmnToFullHealth
	setflag FLAG_SYS_INFORMED_OF_LOCAL_WIRELESS_PLAYER
	message Text_PlayerIsPlayingRightNowGoForIt
	waitmessage
	applymovement VAR_LAST_TALKED, Movement_Bow
	waitmovement 0
	call EventScript_PkmnCenterNurse_Relearner
	msgbox Text_WeHopeToSeeYouAgain
	return

EventScript_PkmnCenterNurse_Goodbye::
	call EventScript_PkmnCenterNurse_Relearner
	msgbox Text_WeHopeToSeeYouAgain
	return

@ Topaze: move relearner built into every POKéMON CENTER (free)
EventScript_PkmnCenterNurse_Relearner::
	msgbox Text_PkmnCenterRelearnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_PkmnCenterNurse_RelearnerEnd
	goto EventScript_PkmnCenterNurse_RelearnChooseMon
	end

EventScript_PkmnCenterNurse_RelearnChooseMon::
	msgbox Text_PkmnCenterRelearnWhich
	special ChooseMonForMoveRelearner
	waitstate
	goto_if_ge VAR_0x8004, PARTY_SIZE, EventScript_PkmnCenterNurse_RelearnerEnd
	special IsSelectedMonEgg
	goto_if_eq VAR_RESULT, TRUE, EventScript_PkmnCenterNurse_RelearnEgg
	goto_if_eq VAR_0x8005, 0, EventScript_PkmnCenterNurse_RelearnNone
	msgbox Text_PkmnCenterRelearnMove
	special TeachMoveRelearnerMove
	waitstate
	goto_if_eq VAR_0x8004, 0, EventScript_PkmnCenterNurse_RelearnChooseMon
	goto EventScript_PkmnCenterNurse_RelearnerEnd
	end

EventScript_PkmnCenterNurse_RelearnNone::
	msgbox Text_PkmnCenterRelearnNone
	goto EventScript_PkmnCenterNurse_RelearnChooseMon
	end

EventScript_PkmnCenterNurse_RelearnEgg::
	msgbox Text_PkmnCenterRelearnEgg
	goto EventScript_PkmnCenterNurse_RelearnChooseMon
	end

EventScript_PkmnCenterNurse_RelearnerEnd::
	return

Text_PkmnCenterRelearnAsk::
	.string "Would you also like me to help a\n"
	.string "POKéMON remember a forgotten move?$"

Text_PkmnCenterRelearnWhich::
	.string "Which POKéMON needs a refresher?$"

Text_PkmnCenterRelearnMove::
	.string "Which move should it remember?$"

Text_PkmnCenterRelearnNone::
	.string "I have nothing to teach that\n"
	.string "POKéMON right now.$"

Text_PkmnCenterRelearnEgg::
	.string "An EGG doesn't know any moves yet!$"

Movement_Bow::
	nurse_joy_bow
	delay_4
	step_end
