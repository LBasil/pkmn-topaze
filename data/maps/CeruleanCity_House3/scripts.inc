CeruleanCity_House3_MapScripts::
	.byte 0

CeruleanCity_House3_EventScript_OldWoman::
	lock
	faceplayer
	goto_if_set FLAG_QUEST_CERULEAN_WATER, CeruleanCity_House3_EventScript_OldWomanDone
	checkitem ITEM_FRESH_WATER, 2
	goto_if_eq VAR_RESULT, TRUE, CeruleanCity_House3_EventScript_OldWomanOffer
	msgbox CeruleanCity_House3_Text_OldWomanAsk
	release
	end

CeruleanCity_House3_EventScript_OldWomanOffer::
	msgbox CeruleanCity_House3_Text_OldWomanOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CeruleanCity_House3_EventScript_OldWomanRefuse
	removeitem ITEM_FRESH_WATER, 2
	setflag FLAG_QUEST_CERULEAN_WATER
	msgbox CeruleanCity_House3_Text_OldWomanGives
	giveitem ITEM_PP_UP
	release
	end

CeruleanCity_House3_EventScript_OldWomanRefuse::
	msgbox CeruleanCity_House3_Text_OldWomanNo
	release
	end

CeruleanCity_House3_EventScript_OldWomanDone::
	msgbox CeruleanCity_House3_Text_PleaseTradeWithMyHusband
	release
	end

CeruleanCity_House3_EventScript_Dontae::
	lock
	faceplayer
	goto_if_set FLAG_DID_ZYNX_TRADE, CeruleanCity_House3_EventScript_Dontae_Done
	msgbox CeruleanCity_House3_Text_QuestAsk
	specialvar VAR_RESULT, TopazePartyMaxLevel
	goto_if_lt VAR_RESULT, 45, CeruleanCity_House3_EventScript_Dontae_No
	checkitemspace ITEM_LINK_CABLE
	goto_if_eq VAR_RESULT, FALSE, CeruleanCity_House3_EventScript_Dontae_NoRoom
	msgbox CeruleanCity_House3_Text_QuestOk
	giveitem_msg CeruleanCity_House3_Text_QuestGot, ITEM_LINK_CABLE
	setflag FLAG_DID_ZYNX_TRADE
	release
	end

CeruleanCity_House3_EventScript_Dontae_No::
	msgbox CeruleanCity_House3_Text_QuestNo
	release
	end

CeruleanCity_House3_EventScript_Dontae_NoRoom::
	msgbox CeruleanCity_House3_Text_QuestNoRoom
	release
	end

CeruleanCity_House3_EventScript_Dontae_Done::
	msgbox CeruleanCity_House3_Text_QuestDone
	release
	end

CeruleanCity_House3_EventScript_CellA::
	trainerbattle_single TRAINER_RICH_BOY, CeruleanCity_House3_Text_CellAIntro, CeruleanCity_House3_Text_CellADefeat
	msgbox CeruleanCity_House3_Text_CellAPost, MSGBOX_AUTOCLOSE
	end

CeruleanCity_House3_EventScript_CellB::
	trainerbattle_single TRAINER_HEX_MANIAC, CeruleanCity_House3_Text_CellBIntro, CeruleanCity_House3_Text_CellBDefeat
	msgbox CeruleanCity_House3_Text_CellBPost, MSGBOX_AUTOCLOSE
	end

CeruleanCity_House3_EventScript_CellMemo::
	lockall
	goto_if_set FLAG_TOPAZE_CELL_CERULEAN, CeruleanCity_House3_EventScript_CellMemoDone
	goto_if_not_defeated TRAINER_RICH_BOY, CeruleanCity_House3_EventScript_CellMemoLocked
	goto_if_not_defeated TRAINER_HEX_MANIAC, CeruleanCity_House3_EventScript_CellMemoLocked
	msgbox CeruleanCity_House3_Text_CellMemo, MSGBOX_DEFAULT
	giveitem ITEM_PP_UP, 1
	setflag FLAG_TOPAZE_CELL_CERULEAN
	releaseall
	end

CeruleanCity_House3_EventScript_CellMemoLocked::
	msgbox CeruleanCity_House3_Text_CellMemoLocked, MSGBOX_DEFAULT
	releaseall
	end

CeruleanCity_House3_EventScript_CellMemoDone::
	msgbox CeruleanCity_House3_Text_CellMemoDone, MSGBOX_DEFAULT
	releaseall
	end

CeruleanCity_House3_Text_CellAIntro::
	.string "Nothing to see. Move along, kid.$"

CeruleanCity_House3_Text_CellADefeat::
	.string "Branch two will hear about this...$"

CeruleanCity_House3_Text_CellAPost::
	.string "It is only a list. Lists are not"
	.string "crimes.$"

CeruleanCity_House3_Text_CellBIntro::
	.string "The boss says no witnesses. No"
	.string "children either.$"

CeruleanCity_House3_Text_CellBDefeat::
	.string "...Fine. Go ahead and read it.$"

CeruleanCity_House3_Text_CellBPost::
	.string "We do not even hate you.$"

CeruleanCity_House3_Text_CellMemo::
	.string "A ledger lies in a crate.\p"
	.string "BRANCH 2 of 7. Forty uniforms paid,"
	.string "sixty POKé BALLS withdrawn.\p"
	.string "Next pickup: after the gym job."
	.string "Report to K.\p"
	.string "In the corner, a PP UP in a box.$"

CeruleanCity_House3_Text_CellMemoLocked::
	.string "Crates, stacked to the ceiling. The"
	.string "guards will not let you look.$"

CeruleanCity_House3_Text_CellMemoDone::
	.string "The crates are empty now. Only the"
	.string "ring on the wall remains.$"
