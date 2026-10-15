CeruleanCity_House3_MapScripts::
	.byte 0

CeruleanCity_House3_EventScript_OldWoman::
	msgbox CeruleanCity_House3_Text_PleaseTradeWithMyHusband, MSGBOX_NPC
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
