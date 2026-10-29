CrystalGrotto_MapScripts::
	.byte 0

CrystalGrotto_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox CrystalGrotto_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CrystalGrotto_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

CrystalGrotto_EventScript_Stay::
	msgbox CrystalGrotto_Text_Stay
	release
	end

CrystalGrotto_EventScript_Npc0::
	msgbox CrystalGrotto_Text_Npc0, MSGBOX_NPC
	end

CrystalGrotto_EventScript_Npc1::
	msgbox CrystalGrotto_Text_Npc1, MSGBOX_NPC
	end

