SaffronCity_HomeA_MapScripts::
	.byte 0

SaffronCity_HomeA_EventScript_Keeper::
	lock
	faceplayer
	msgbox SaffronCity_HomeA_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SaffronCity_HomeA_EventScript_No
	fadescreen FADE_TO_BLACK
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox SaffronCity_HomeA_Text_Rested
	release
	end
SaffronCity_HomeA_EventScript_No::
	msgbox SaffronCity_HomeA_Text_No
	release
	end
SaffronCity_HomeA_EventScript_Guest::
	msgbox SaffronCity_HomeA_Text_Guest, MSGBOX_NPC
	end
