PewterCity_House3_MapScripts::
	.byte 0

PewterCity_House3_EventScript_Mother::
	lock
	faceplayer
	goto_if_set FLAG_QUEST_PEWTER_REVIVE, PewterCity_House3_EventScript_MotherDone
	checkitem ITEM_REVIVE, 1
	goto_if_eq VAR_RESULT, TRUE, PewterCity_House3_EventScript_MotherOffer
	msgbox PewterCity_House3_Text_MotherAsk
	release
	end

PewterCity_House3_EventScript_MotherOffer::
	msgbox PewterCity_House3_Text_MotherOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PewterCity_House3_EventScript_MotherRefuse
	removeitem ITEM_REVIVE, 1
	setflag FLAG_QUEST_PEWTER_REVIVE
	msgbox PewterCity_House3_Text_MotherGives
	giveitem ITEM_RARE_CANDY, 1
	release
	end

PewterCity_House3_EventScript_MotherRefuse::
	msgbox PewterCity_House3_Text_MotherNo
	release
	end

PewterCity_House3_EventScript_MotherDone::
	msgbox PewterCity_House3_Text_Mother
	release
	end

PewterCity_House3_EventScript_Boy::
	msgbox PewterCity_House3_Text_Boy, MSGBOX_NPC
	end

PewterCity_House3_EventScript_CellA::
	trainerbattle_single TRAINER_GUITARIST, PewterCity_House3_Text_CellAIntro, PewterCity_House3_Text_CellADefeat
	msgbox PewterCity_House3_Text_CellAPost, MSGBOX_AUTOCLOSE
	end

PewterCity_House3_EventScript_CellB::
	trainerbattle_single TRAINER_KINDLER, PewterCity_House3_Text_CellBIntro, PewterCity_House3_Text_CellBDefeat
	msgbox PewterCity_House3_Text_CellBPost, MSGBOX_AUTOCLOSE
	end

PewterCity_House3_EventScript_CellMemo::
	lockall
	goto_if_set FLAG_TOPAZE_CELL_PEWTER, PewterCity_House3_EventScript_CellMemoDone
	goto_if_not_defeated TRAINER_GUITARIST, PewterCity_House3_EventScript_CellMemoLocked
	goto_if_not_defeated TRAINER_KINDLER, PewterCity_House3_EventScript_CellMemoLocked
	msgbox PewterCity_House3_Text_CellMemo, MSGBOX_DEFAULT
	giveitem ITEM_RARE_CANDY, 2
	setflag FLAG_TOPAZE_CELL_PEWTER
	releaseall
	end

PewterCity_House3_EventScript_CellMemoLocked::
	msgbox PewterCity_House3_Text_CellMemoLocked, MSGBOX_DEFAULT
	releaseall
	end

PewterCity_House3_EventScript_CellMemoDone::
	msgbox PewterCity_House3_Text_CellMemoDone, MSGBOX_DEFAULT
	releaseall
	end

PewterCity_House3_Text_CellAIntro::
	.string "Wrong house, kid. Nothing to see."
	.string "Nothing at all.$"

PewterCity_House3_Text_CellADefeat::
	.string "Branch work is not supposed to"
	.string "fail...$"

PewterCity_House3_Text_CellAPost::
	.string "Read the memo if you like. It will"
	.string "not change anything.$"

PewterCity_House3_Text_CellBIntro::
	.string "The boss said to ignore tourists."
	.string "He did not say how.$"

PewterCity_House3_Text_CellBDefeat::
	.string "...I only carry crates.$"

PewterCity_House3_Text_CellBPost::
	.string "Nobody told me kids fight this"
	.string "hard.$"

PewterCity_House3_Text_CellMemo::
	.string "A delivery note lies in a crate.\p"
	.string "BRANCH 4 of 7. Eleven crates of"
	.string "POKé BALLS, forty uniforms.\p"
	.string "Next pickup: after the school job."
	.string "Report to V.\p"
	.string "Under it, a black ring with a red dot."
	.string "Under the note, 2 RARE CANDY.$"

PewterCity_House3_Text_CellMemoLocked::
	.string "Crates, stacked to the ceiling. The"
	.string "guards will not let you look.$"

PewterCity_House3_Text_CellMemoDone::
	.string "The crates are empty now. Only the"
	.string "ring on the wall remains.$"
