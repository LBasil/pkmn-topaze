CeladonCity_Hotel_MapScripts::
	.byte 0

CeladonCity_Hotel_EventScript_Receptionist::
	msgbox CeladonCity_Hotel_Text_ThisHotelIsForPeople, MSGBOX_NPC
	end

CeladonCity_Hotel_EventScript_Beauty::
	lock
	faceplayer
	msgbox CeladonCity_Hotel_Text_SpaOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CeladonCity_Hotel_EventScript_SpaDecline
	checkmoney 300
	goto_if_eq VAR_RESULT, FALSE, CeladonCity_Hotel_EventScript_SpaNoMoney
	msgbox CeladonCity_Hotel_Text_SpaWhich
	special ChoosePartyMon
	waitstate
	lock
	faceplayer
	goto_if_ge VAR_0x8004, PARTY_SIZE, CeladonCity_Hotel_EventScript_SpaDecline
	specialvar VAR_RESULT, GetPartyMonSpecies
	goto_if_eq VAR_RESULT, SPECIES_EGG, CeladonCity_Hotel_EventScript_SpaDecline
	removemoney 300
	closemessage
	fadescreen FADE_TO_BLACK
	playfanfare MUS_HEAL
	waitfanfare
	special TopazeMassageOne
	fadescreen FADE_FROM_BLACK
	special BufferMonNickname
	msgbox CeladonCity_Hotel_Text_SpaDone
	release
	end

CeladonCity_Hotel_EventScript_SpaDecline::
	msgbox CeladonCity_Hotel_Text_SpaDecline
	release
	end

CeladonCity_Hotel_EventScript_SpaNoMoney::
	msgbox CeladonCity_Hotel_Text_SpaNoMoney
	release
	end

CeladonCity_Hotel_EventScript_BeautyBoyfriend::
	msgbox CeladonCity_Hotel_Text_WhyDidSheBringBrother, MSGBOX_NPC
	end

CeladonCity_Hotel_EventScript_BeautyBrother::
	msgbox CeladonCity_Hotel_Text_SisBroughtMeOnVacation, MSGBOX_NPC
	end
