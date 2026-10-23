VermilionCity_House2_MapScripts::
	.byte 0

VermilionCity_House2_EventScript_Elyssa::
	lock
	faceplayer
	goto_if_set FLAG_DID_CH_DING_TRADE, VermilionCity_House2_EventScript_Elyssa_Done
	msgbox VermilionCity_House2_Text_QuestAsk
	specialvar VAR_RESULT, GetLeadMonFriendship
	goto_if_lt VAR_RESULT, 5, VermilionCity_House2_EventScript_Elyssa_No
	checkitemspace ITEM_MOON_STONE
	goto_if_eq VAR_RESULT, FALSE, VermilionCity_House2_EventScript_Elyssa_NoRoom
	msgbox VermilionCity_House2_Text_QuestOk
	giveitem_msg VermilionCity_House2_Text_QuestGot, ITEM_MOON_STONE
	setflag FLAG_DID_CH_DING_TRADE
	release
	end

VermilionCity_House2_EventScript_Elyssa_No::
	msgbox VermilionCity_House2_Text_QuestNo
	release
	end

VermilionCity_House2_EventScript_Elyssa_NoRoom::
	msgbox VermilionCity_House2_Text_QuestNoRoom
	release
	end

VermilionCity_House2_EventScript_Elyssa_Done::
	msgbox VermilionCity_House2_Text_QuestDone
	release
	end

VermilionCity_House2_EventScript_CellA::
	trainerbattle_single TRAINER_BUG_MANIAC, VermilionCity_House2_Text_CellAIntro, VermilionCity_House2_Text_CellADefeat
	msgbox VermilionCity_House2_Text_CellAPost, MSGBOX_AUTOCLOSE
	end

VermilionCity_House2_EventScript_CellB::
	trainerbattle_single TRAINER_INTERVIEWER, VermilionCity_House2_Text_CellBIntro, VermilionCity_House2_Text_CellBDefeat
	msgbox VermilionCity_House2_Text_CellBPost, MSGBOX_AUTOCLOSE
	end

VermilionCity_House2_EventScript_CellMemo::
	lockall
	goto_if_set FLAG_TOPAZE_CELL_VERMILION, VermilionCity_House2_EventScript_CellMemoDone
	goto_if_not_defeated TRAINER_BUG_MANIAC, VermilionCity_House2_EventScript_CellMemoLocked
	goto_if_not_defeated TRAINER_INTERVIEWER, VermilionCity_House2_EventScript_CellMemoLocked
	msgbox VermilionCity_House2_Text_CellMemo, MSGBOX_DEFAULT
	giveitem ITEM_REVIVE, 3
	setflag FLAG_TOPAZE_CELL_VERMILION
	releaseall
	end

VermilionCity_House2_EventScript_CellMemoLocked::
	msgbox VermilionCity_House2_Text_CellMemoLocked, MSGBOX_DEFAULT
	releaseall
	end

VermilionCity_House2_EventScript_CellMemoDone::
	msgbox VermilionCity_House2_Text_CellMemoDone, MSGBOX_DEFAULT
	releaseall
	end

VermilionCity_House2_Text_CellAIntro::
	.string "The harbor is ours. This too.$"

VermilionCity_House2_Text_CellADefeat::
	.string "The harbor is... still ours.$"

VermilionCity_House2_Text_CellAPost::
	.string "Check the wall if you like. It"
	.string "means nothing to you.$"

VermilionCity_House2_Text_CellBIntro::
	.string "Do not touch the crates, kid.$"

VermilionCity_House2_Text_CellBDefeat::
	.string "Tch. The count will be off.$"

VermilionCity_House2_Text_CellBPost::
	.string "Seven branches. You cannot stop"
	.string "them all.$"

VermilionCity_House2_Text_CellMemo::
	.string "A slip is pinned to a crate.\p"
	.string "BRANCH 6 of 7. Harbor division."
	.string "Three ships a week, no markings.\p"
	.string "The stone from the SS ANNE job is"
	.string "overdue. Report to V.\p"
	.string "Beside it, 3 REVIVE in a box.$"

VermilionCity_House2_Text_CellMemoLocked::
	.string "Crates, stacked to the ceiling. The"
	.string "guards will not let you look.$"

VermilionCity_House2_Text_CellMemoDone::
	.string "The crates are empty now. Only the"
	.string "ring on the wall remains.$"
