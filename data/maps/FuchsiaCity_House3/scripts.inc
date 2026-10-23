FuchsiaCity_House3_MapScripts::
	.byte 0

FuchsiaCity_House3_EventScript_MoveDeleter::
	lock
	faceplayer
	msgbox FuchsiaCity_House3_Text_WouldYouLikeToForgetMove, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, FuchsiaCity_House3_EventScript_ChooseMonForMoveDeleter
	goto FuchsiaCity_House3_EventScript_CancelForgetMove
	end

FuchsiaCity_House3_EventScript_ChooseMonForMoveDeleter::
	msgbox FuchsiaCity_House3_Text_WhichMonShouldForgetMove
	special ChoosePartyMon
	waitstate
	goto_if_ge VAR_0x8004, PARTY_SIZE, FuchsiaCity_House3_EventScript_CancelForgetMove
	special IsSelectedMonEgg
	goto_if_eq VAR_RESULT, TRUE, FuchsiaCity_House3_EventScript_CantForgetMoveEgg
	special GetNumMovesSelectedMonHas
	goto_if_eq VAR_RESULT, 1, FuchsiaCity_House3_EventScript_CantForgetOnlyMove
	msgbox FuchsiaCity_House3_Text_WhichMoveShouldBeForgotten
	fadescreen FADE_TO_BLACK
	special SelectMoveDeleterMove
	fadescreen FADE_FROM_BLACK
	goto_if_eq VAR_0x8005, MAX_MON_MOVES, FuchsiaCity_House3_EventScript_ChooseMonForMoveDeleter
	special BufferMoveDeleterNicknameAndMove
	msgbox FuchsiaCity_House3_Text_MonsMoveShouldBeForgotten, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, FuchsiaCity_House3_EventScript_ForgetMove
	goto FuchsiaCity_House3_EventScript_CancelForgetMove
	end

FuchsiaCity_House3_EventScript_ForgetMove::
	special MoveDeleterForgetMove
	playfanfare MUS_MOVE_DELETED
	waitfanfare
	msgbox FuchsiaCity_House3_Text_MonHasForgottenMoveCompletely
	release
	end

FuchsiaCity_House3_EventScript_CantForgetOnlyMove::
	special BufferMoveDeleterNicknameAndMove
	msgbox FuchsiaCity_House3_Text_MonOnlyKnowsOneMove
	release
	end

FuchsiaCity_House3_EventScript_CantForgetMoveEgg::
	msgbox FuchsiaCity_House3_Text_NoEggShouldKnowMoves
	release
	end

FuchsiaCity_House3_EventScript_CancelForgetMove::
	msgbox FuchsiaCity_House3_Text_ComeAgainToForgetOtherMoves
	release
	end

FuchsiaCity_House3_EventScript_CellA::
	trainerbattle_single TRAINER_POKEFAN_M, FuchsiaCity_House3_Text_CellAIntro, FuchsiaCity_House3_Text_CellADefeat
	msgbox FuchsiaCity_House3_Text_CellAPost, MSGBOX_AUTOCLOSE
	end

FuchsiaCity_House3_EventScript_CellB::
	trainerbattle_single TRAINER_POKEFAN_F, FuchsiaCity_House3_Text_CellBIntro, FuchsiaCity_House3_Text_CellBDefeat
	msgbox FuchsiaCity_House3_Text_CellBPost, MSGBOX_AUTOCLOSE
	end

FuchsiaCity_House3_EventScript_CellMemo::
	lockall
	goto_if_set FLAG_TOPAZE_CELL_FUCHSIA, FuchsiaCity_House3_EventScript_CellMemoDone
	goto_if_not_defeated TRAINER_POKEFAN_M, FuchsiaCity_House3_EventScript_CellMemoLocked
	goto_if_not_defeated TRAINER_POKEFAN_F, FuchsiaCity_House3_EventScript_CellMemoLocked
	msgbox FuchsiaCity_House3_Text_CellMemo, MSGBOX_DEFAULT
	giveitem ITEM_PP_UP, 2
	setflag FLAG_TOPAZE_CELL_FUCHSIA
	releaseall
	end

FuchsiaCity_House3_EventScript_CellMemoLocked::
	msgbox FuchsiaCity_House3_Text_CellMemoLocked, MSGBOX_DEFAULT
	releaseall
	end

FuchsiaCity_House3_EventScript_CellMemoDone::
	msgbox FuchsiaCity_House3_Text_CellMemoDone, MSGBOX_DEFAULT
	releaseall
	end

FuchsiaCity_House3_Text_CellAIntro::
	.string "This house is our supply room."
	.string "Out.$"

FuchsiaCity_House3_Text_CellADefeat::
	.string "The supply line will be cut...$"

FuchsiaCity_House3_Text_CellAPost::
	.string "Read it. The numbers will keep you"
	.string "awake.$"

FuchsiaCity_House3_Text_CellBIntro::
	.string "You came a long way for a few"
	.string "crates.$"

FuchsiaCity_House3_Text_CellBDefeat::
	.string "...I will be reassigned.$"

FuchsiaCity_House3_Text_CellBPost::
	.string "Seven branches. Four towns are"
	.string "already ours.$"

FuchsiaCity_House3_Text_CellMemo::
	.string "A thick ledger lies open.\p"
	.string "BRANCH 1 of 7. Supply and training."
	.string "Two hundred recruits, nine houses.\p"
	.string "Next shipment: HEMATEK tower."
	.string "Report to V.\p"
	.string "Tucked inside, 2 PP UP.$"

FuchsiaCity_House3_Text_CellMemoLocked::
	.string "Crates, stacked to the ceiling. The"
	.string "guards will not let you look.$"

FuchsiaCity_House3_Text_CellMemoDone::
	.string "The crates are empty now. Only the"
	.string "ring on the wall remains.$"
