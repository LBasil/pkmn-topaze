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
