Route2_House_MapScripts::
	.byte 0

Route2_House_EventScript_Scientist::
	lock
	faceplayer
	goto_if_set FLAG_QUEST_ROUTE2_ETHER, Route2_House_EventScript_ScientistDone
	checkitem ITEM_ETHER, 2
	goto_if_eq VAR_RESULT, TRUE, Route2_House_EventScript_ScientistOffer
	msgbox Route2_House_Text_ScientistAsk
	release
	end

Route2_House_EventScript_ScientistOffer::
	msgbox Route2_House_Text_ScientistOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Route2_House_EventScript_ScientistRefuse
	removeitem ITEM_ETHER, 2
	setflag FLAG_QUEST_ROUTE2_ETHER
	msgbox Route2_House_Text_ScientistGives
	giveitem ITEM_PP_UP, 1
	release
	end

Route2_House_EventScript_ScientistRefuse::
	msgbox Route2_House_Text_ScientistNo
	release
	end

Route2_House_EventScript_ScientistDone::
	msgbox Route2_House_Text_FaintedMonsCanUseFieldMoves
	release
	end

Route2_House_EventScript_Reyley::
	lock
	faceplayer
	setvar VAR_0x8008, INGAME_TRADE_MR_MIME
	call EventScript_GetInGameTradeSpeciesInfo
	goto_if_set FLAG_DID_MIMIEN_TRADE, Route2_House_EventScript_AlreadyTraded
	msgbox Trade_Text_LookingForMonWannaTradeForMon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Route2_House_EventScript_DeclineTrade
	call EventScript_ChooseMonForInGameTrade
	goto_if_ge VAR_0x8004, PARTY_SIZE, Route2_House_EventScript_DeclineTrade
	call EventScript_GetInGameTradeSpecies
	goto_if_ne VAR_RESULT, VAR_0x8009, Route2_House_EventScript_NotRequestedMon
	call EventScript_DoInGameTrade
	msgbox Trade_Text_HeyThanks
	setflag FLAG_DID_MIMIEN_TRADE
	release
	end

Route2_House_EventScript_DeclineTrade::
	msgbox Trade_Text_AwwOhWell
	release
	end

Route2_House_EventScript_NotRequestedMon::
	bufferspeciesname STR_VAR_1, VAR_0x8009
	msgbox Trade_Text_WhatThatsNoMon
	release
	end

Route2_House_EventScript_AlreadyTraded::
	msgbox Trade_Text_IsntMyOldMonGreat
	release
	end
