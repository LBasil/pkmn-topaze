PewterCity_House1_MapScripts::
	.byte 0

PewterCity_House1_EventScript_BaldingMan::
	lock
	faceplayer
	goto_if_set FLAG_QUEST_PEWTER_ANTIDOTE, PewterCity_House1_EventScript_ManDone
	checkitem ITEM_ANTIDOTE, 2
	goto_if_eq VAR_RESULT, TRUE, PewterCity_House1_EventScript_ManOffer
	msgbox PewterCity_House1_Text_ManAsk
	release
	end

PewterCity_House1_EventScript_ManOffer::
	msgbox PewterCity_House1_Text_ManOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PewterCity_House1_EventScript_ManRefuse
	removeitem ITEM_ANTIDOTE, 2
	setflag FLAG_QUEST_PEWTER_ANTIDOTE
	msgbox PewterCity_House1_Text_ManGives
	giveitem ITEM_NUGGET
	release
	end

PewterCity_House1_EventScript_ManRefuse::
	msgbox PewterCity_House1_Text_ManSad
	release
	end

PewterCity_House1_EventScript_ManDone::
	msgbox PewterCity_House1_Text_TradeMonsAreFinicky
	release
	end

PewterCity_House1_EventScript_LittleBoy::
	lock
	msgbox PewterCity_House1_Text_NidoranSit
	call PewterCity_House1_EventScript_DoNidoranCry
	release
	end

PewterCity_House1_EventScript_Nidoran::
	lock
	faceplayer
	call PewterCity_House1_EventScript_DoNidoranCry
	applymovement LOCALID_PEWTER_HOUSE_NIDORAN, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

PewterCity_House1_EventScript_DoNidoranCry::
	textcolor NPC_TEXT_COLOR_NEUTRAL
	waitse
	playmoncry SPECIES_NIDORAN_M, CRY_MODE_NORMAL
	msgbox PewterCity_House1_Text_Nidoran
	waitmoncry
	call EventScript_RestorePrevTextColor
	return
