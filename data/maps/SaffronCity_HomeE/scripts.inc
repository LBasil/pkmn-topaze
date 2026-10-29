SaffronCity_HomeE_MapScripts::
	.byte 0

SaffronCity_HomeE_EventScript_Attendant::
	lock
	faceplayer
	msgbox SaffronCity_HomeE_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SaffronCity_HomeE_EventScript_No
	fadescreen FADE_TO_BLACK
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox SaffronCity_HomeE_Text_Done
	release
	end
SaffronCity_HomeE_EventScript_No::
	msgbox SaffronCity_HomeE_Text_No
	release
	end
