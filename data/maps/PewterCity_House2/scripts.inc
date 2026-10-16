PewterCity_House2_MapScripts::
	.byte 0

PewterCity_House2_EventScript_OldMan::
	lock
	faceplayer
	goto_if_set FLAG_QUEST_PEWTER_BURN, PewterCity_House2_EventScript_OldManDone
	checkitem ITEM_BURN_HEAL, 2
	goto_if_eq VAR_RESULT, TRUE, PewterCity_House2_EventScript_OldManOffer
	msgbox PewterCity_House2_Text_OldManAsk
	release
	end

PewterCity_House2_EventScript_OldManOffer::
	msgbox PewterCity_House2_Text_OldManOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PewterCity_House2_EventScript_OldManRefuse
	removeitem ITEM_BURN_HEAL, 2
	setflag FLAG_QUEST_PEWTER_BURN
	msgbox PewterCity_House2_Text_OldManGives
	giveitem ITEM_IRON, 1
	release
	end

PewterCity_House2_EventScript_OldManRefuse::
	msgbox PewterCity_House2_Text_OldManNo
	release
	end

PewterCity_House2_EventScript_OldManDone::
	msgbox PewterCity_House2_Text_MonsLearnTechniquesAsTheyGrow
	release
	end

PewterCity_House2_EventScript_LittleBoy::
	lock
	faceplayer
	goto_if_set FLAG_QUEST_PEWTER_AWAKEN, PewterCity_House2_EventScript_LittleBoyDone
	checkitem ITEM_AWAKENING, 1
	goto_if_eq VAR_RESULT, TRUE, PewterCity_House2_EventScript_LittleBoyOffer
	msgbox PewterCity_House2_Text_LittleBoyAsk
	release
	end

PewterCity_House2_EventScript_LittleBoyOffer::
	msgbox PewterCity_House2_Text_LittleBoyOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PewterCity_House2_EventScript_LittleBoyRefuse
	removeitem ITEM_AWAKENING, 1
	setflag FLAG_QUEST_PEWTER_AWAKEN
	msgbox PewterCity_House2_Text_LittleBoyGives
	giveitem ITEM_X_ATTACK, 3
	release
	end

PewterCity_House2_EventScript_LittleBoyRefuse::
	msgbox PewterCity_House2_Text_LittleBoyNo
	release
	end

PewterCity_House2_EventScript_LittleBoyDone::
	msgbox PewterCity_House2_Text_MonsEasierCatchIfStatused
	release
	end
