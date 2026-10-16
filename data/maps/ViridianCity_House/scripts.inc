ViridianCity_House_MapScripts::
	.byte 0

ViridianCity_House_EventScript_BaldingMan::
	msgbox ViridianCity_House_Text_NicknamingIsFun, MSGBOX_NPC
	end

ViridianCity_House_EventScript_LittleGirl::
	lock
	faceplayer
	goto_if_set FLAG_QUEST_VIRIDIAN_POTIONS, ViridianCity_House_EventScript_GirlThanks
	checkitem ITEM_POTION, 3
	goto_if_eq VAR_RESULT, TRUE, ViridianCity_House_EventScript_GirlOffer
	msgbox ViridianCity_House_Text_GirlAsk
	release
	end

ViridianCity_House_EventScript_GirlOffer::
	msgbox ViridianCity_House_Text_GirlOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ViridianCity_House_EventScript_GirlRefuse
	removeitem ITEM_POTION, 3
	setflag FLAG_QUEST_VIRIDIAN_POTIONS
	msgbox ViridianCity_House_Text_GirlGives
	giveitem ITEM_RARE_CANDY
	release
	end

ViridianCity_House_EventScript_GirlRefuse::
	msgbox ViridianCity_House_Text_GirlSad
	release
	end

ViridianCity_House_EventScript_GirlThanks::
	msgbox ViridianCity_House_Text_MyDaddyLovesMonsToo
	release
	end

ViridianCity_House_EventScript_Speary::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SPEAROW, CRY_MODE_NORMAL
	msgbox ViridianCity_House_Text_Speary
	waitmoncry
	release
	end

ViridianCity_House_EventScript_NicknameSign::
	msgbox ViridianCity_House_Text_SpearowNameSpeary, MSGBOX_SIGN
	end
