VermilionCity_House3_MapScripts::
	.byte 0

VermilionCity_House3_EventScript_Boy::
	lock
	faceplayer
	goto_if_set FLAG_QUEST_VERMILION_PARA, VermilionCity_House3_EventScript_BoyDone
	checkitem ITEM_PARALYZE_HEAL, 2
	goto_if_eq VAR_RESULT, TRUE, VermilionCity_House3_EventScript_BoyOffer
	msgbox VermilionCity_House3_Text_BoyAsk
	release
	end

VermilionCity_House3_EventScript_BoyOffer::
	msgbox VermilionCity_House3_Text_BoyOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, VermilionCity_House3_EventScript_BoyRefuse
	removeitem ITEM_PARALYZE_HEAL, 2
	setflag FLAG_QUEST_VERMILION_PARA
	msgbox VermilionCity_House3_Text_BoyGives
	giveitem ITEM_PROTEIN
	release
	end

VermilionCity_House3_EventScript_BoyRefuse::
	msgbox VermilionCity_House3_Text_BoyNo
	release
	end

VermilionCity_House3_EventScript_BoyDone::
	msgbox VermilionCity_House3_Text_PidgeyFlyLetterToSaffron
	release
	end

VermilionCity_House3_EventScript_Lass::
	msgbox VermilionCity_House3_Text_SendMyPidgeyToUnionRoom, MSGBOX_NPC
	end

VermilionCity_House3_EventScript_Pidgey::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PIDGEY, CRY_MODE_NORMAL
	msgbox VermilionCity_House3_Text_Pidgey
	waitmoncry
	release
	end

VermilionCity_House3_EventScript_Letter::
	msgbox VermilionCity_House3_Text_DearPippiLetter, MSGBOX_SIGN
	end
