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
