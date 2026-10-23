LavenderTown_House2_MapScripts::
	.byte 0

LavenderTown_House2_EventScript_NameRater::
	lock
	faceplayer
	msgbox LavenderTown_House2_Text_WantMeToRateNicknames, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LavenderTown_House2_EventScript_ChooseMon
	goto_if_eq VAR_RESULT, NO, LavenderTown_House2_EventScript_DontRateNickname
	end

LavenderTown_House2_EventScript_ChooseMon::
	msgbox LavenderTown_House2_Text_CritiqueWhichMonsNickname
	special ChoosePartyMon
	waitstate
	goto_if_lt VAR_0x8004, PARTY_SIZE, LavenderTown_House2_EventScript_CheckCanRateMon
	goto_if_ge VAR_0x8004, PARTY_SIZE, LavenderTown_House2_EventScript_DontRateNickname
	end

LavenderTown_House2_EventScript_DontRateNickname::
	msgbox LavenderTown_House2_Text_ISeeComeVisitAgain
	release
	end

LavenderTown_House2_EventScript_CheckCanRateMon::
	specialvar VAR_RESULT, GetPartyMonSpecies
	goto_if_eq VAR_RESULT, SPECIES_EGG, LavenderTown_House2_EventScript_CantNicknameEgg
	special BufferMonNickname
	special IsMonOTIDNotPlayers
	goto_if_eq VAR_RESULT, TRUE, LavenderTown_House2_EventScript_CantNicknameTradeMon
	specialvar VAR_RESULT, IsMonOTNameNotPlayers
	special BufferMonNickname
	goto_if_eq VAR_RESULT, TRUE, LavenderTown_House2_EventScript_CantNicknameTradeMon
	msgbox LavenderTown_House2_Text_GiveItANicerName, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LavenderTown_House2_EventScript_ChooseNewNickname
	goto_if_eq VAR_RESULT, NO, LavenderTown_House2_EventScript_DontRateNickname
	end

LavenderTown_House2_EventScript_CantNicknameEgg::
	msgbox LavenderTown_House2_Text_ThatIsMerelyAnEgg
	release
	end

LavenderTown_House2_EventScript_CantNicknameTradeMon::
	msgbox LavenderTown_House2_Text_TrulyImpeccableName
	release
	end

LavenderTown_House2_EventScript_ChooseNewNickname::
	msgbox LavenderTown_House2_Text_WhatShallNewNicknameBe
	call EventScript_ChangePokemonNickname
	specialvar VAR_RESULT, NameRaterWasNicknameChanged
	special BufferMonNickname
	goto_if_eq VAR_RESULT, TRUE, LavenderTown_House2_EventScript_ChoseNewNickname
	msgbox LavenderTown_House2_Text_FromNowOnShallBeKnownAsSameName
	release
	end

LavenderTown_House2_EventScript_ChoseNewNickname::
	msgbox LavenderTown_House2_Text_FromNowOnShallBeKnownAsName
	release
	end

LavenderTown_House2_EventScript_CellA::
	trainerbattle_single TRAINER_SCHOOL_KID_M, LavenderTown_House2_Text_CellAIntro, LavenderTown_House2_Text_CellADefeat
	msgbox LavenderTown_House2_Text_CellAPost, MSGBOX_AUTOCLOSE
	end

LavenderTown_House2_EventScript_CellB::
	trainerbattle_single TRAINER_SCHOOL_KID_F, LavenderTown_House2_Text_CellBIntro, LavenderTown_House2_Text_CellBDefeat
	msgbox LavenderTown_House2_Text_CellBPost, MSGBOX_AUTOCLOSE
	end

LavenderTown_House2_EventScript_CellMemo::
	lockall
	goto_if_set FLAG_TOPAZE_CELL_LAVENDER, LavenderTown_House2_EventScript_CellMemoDone
	goto_if_not_defeated TRAINER_SCHOOL_KID_M, LavenderTown_House2_EventScript_CellMemoLocked
	goto_if_not_defeated TRAINER_SCHOOL_KID_F, LavenderTown_House2_EventScript_CellMemoLocked
	msgbox LavenderTown_House2_Text_CellMemo, MSGBOX_DEFAULT
	giveitem ITEM_ELIXIR, 2
	setflag FLAG_TOPAZE_CELL_LAVENDER
	releaseall
	end

LavenderTown_House2_EventScript_CellMemoLocked::
	msgbox LavenderTown_House2_Text_CellMemoLocked, MSGBOX_DEFAULT
	releaseall
	end

LavenderTown_House2_EventScript_CellMemoDone::
	msgbox LavenderTown_House2_Text_CellMemoDone, MSGBOX_DEFAULT
	releaseall
	end

LavenderTown_House2_Text_CellAIntro::
	.string "The tower hides us well. Leave.$"

LavenderTown_House2_Text_CellADefeat::
	.string "The tower did not warn us...$"

LavenderTown_House2_Text_CellAPost::
	.string "The radio only talks to us. Do not"
	.string "bother.$"

LavenderTown_House2_Text_CellBIntro::
	.string "The dead do not scare us anymore.$"

LavenderTown_House2_Text_CellBDefeat::
	.string "...You are quite scary yourself.$"

LavenderTown_House2_Text_CellBPost::
	.string "One more wall to read. Then go.$"

LavenderTown_House2_Text_CellMemo::
	.string "A logbook sits among the crates.\p"
	.string "BRANCH 5 of 7. Tower relay, all"
	.string "quiet. Fifty recruits this month.\p"
	.string "Next voice: the BOSS, at noon."
	.string "Report to S.\p"
	.string "In a drawer, 2 ELIXIR.$"

LavenderTown_House2_Text_CellMemoLocked::
	.string "Crates, stacked to the ceiling. The"
	.string "guards will not let you look.$"

LavenderTown_House2_Text_CellMemoDone::
	.string "The crates are empty now. Only the"
	.string "ring on the wall remains.$"
