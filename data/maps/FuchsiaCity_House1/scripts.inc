FuchsiaCity_House1_MapScripts::
	.byte 0

FuchsiaCity_House1_EventScript_Woman::
	lock
	faceplayer
	goto_if_set FLAG_QUEST_FUCHSIA_SUPER, FuchsiaCity_House1_EventScript_WomanDone
	checkitem ITEM_SUPER_POTION, 2
	goto_if_eq VAR_RESULT, TRUE, FuchsiaCity_House1_EventScript_WomanOffer
	msgbox FuchsiaCity_House1_Text_WomanAsk
	release
	end

FuchsiaCity_House1_EventScript_WomanOffer::
	msgbox FuchsiaCity_House1_Text_WomanOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_House1_EventScript_WomanRefuse
	removeitem ITEM_SUPER_POTION, 2
	setflag FLAG_QUEST_FUCHSIA_SUPER
	msgbox FuchsiaCity_House1_Text_WomanGives
	giveitem ITEM_MAX_REVIVE
	release
	end

FuchsiaCity_House1_EventScript_WomanRefuse::
	msgbox FuchsiaCity_House1_Text_WomanNo
	release
	end

FuchsiaCity_House1_EventScript_WomanDone::
	msgbox FuchsiaCity_House1_Text_WardenIsOldHasFalseTeeth
	release
	end

FuchsiaCity_House1_EventScript_OldMan::
	lock
	faceplayer
	famechecker FAMECHECKER_BILL, 2
	msgbox FuchsiaCity_House1_Text_BillIsMyGrandson
	release
	end

FuchsiaCity_House1_EventScript_LittleBoy::
	msgbox FuchsiaCity_House1_Text_BillFilesHisOwnMonData, MSGBOX_NPC
	end
