CyclePond_MapScripts::
	.byte 0

CyclePond_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox CyclePond_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CyclePond_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

CyclePond_EventScript_Stay::
	msgbox CyclePond_Text_Stay
	release
	end

CyclePond_EventScript_Npc0::
	msgbox CyclePond_Text_Npc0, MSGBOX_NPC
	end

CyclePond_EventScript_Spa::
	lock
	faceplayer
	msgbox CyclePond_Text_SpaOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CyclePond_EventScript_SpaNo
	checkmoney 2000
	goto_if_eq VAR_RESULT, FALSE, CyclePond_EventScript_SpaPoor
	msgbox CyclePond_Text_SpaWhich
	special ChoosePartyMon
	waitstate
	lock
	faceplayer
	goto_if_ge VAR_0x8004, PARTY_SIZE, CyclePond_EventScript_SpaNo
	specialvar VAR_RESULT, GetPartyMonSpecies
	goto_if_eq VAR_RESULT, SPECIES_EGG, CyclePond_EventScript_SpaNo
	removemoney 2000
	closemessage
	fadescreen FADE_TO_BLACK
	playfanfare MUS_HEAL
	waitfanfare
	special TopazeBondMax
	setflag FLAG_TOPAZE_BOND
	fadescreen FADE_FROM_BLACK
	special BufferMonNickname
	msgbox CyclePond_Text_SpaDone
	release
	end

CyclePond_EventScript_SpaNo::
	msgbox CyclePond_Text_SpaNo
	release
	end

CyclePond_EventScript_SpaPoor::
	msgbox CyclePond_Text_SpaPoor
	release
	end

CyclePond_EventScript_Hermit::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_EVERSTONE, CyclePond_EventScript_HermitDone
	msgbox CyclePond_Text_Hermit
	checkitemspace ITEM_EVERSTONE, 1
	goto_if_eq VAR_RESULT, FALSE, CyclePond_EventScript_HermitFull
	giveitem ITEM_EVERSTONE
	setflag FLAG_TOPAZE_EVERSTONE
	release
	end

CyclePond_EventScript_HermitDone::
	msgbox CyclePond_Text_HermitDone
	release
	end

CyclePond_EventScript_HermitFull::
	msgbox CyclePond_Text_HermitFull
	release
	end

