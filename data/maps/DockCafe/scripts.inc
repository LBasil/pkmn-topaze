DockCafe_MapScripts::
	.byte 0

DockCafe_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox DockCafe_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, DockCafe_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

DockCafe_EventScript_Stay::
	msgbox DockCafe_Text_Stay
	release
	end

DockCafe_EventScript_Npc0::
	msgbox DockCafe_Text_Npc0, MSGBOX_NPC
	end

DockCafe_EventScript_Npc1::
	msgbox DockCafe_Text_Npc1, MSGBOX_NPC
	end

DockCafe_EventScript_Rest::
	lock
	faceplayer
	msgbox DockCafe_Text_RestOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, DockCafe_EventScript_Rest_No
	fadescreen FADE_TO_BLACK
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox DockCafe_Text_Rested
	release
	end

DockCafe_EventScript_Rest_No::
	msgbox DockCafe_Text_RestNo
	release
	end

DockCafe_EventScript_Shop::
	lock
	faceplayer
	msgbox DockCafe_Text_ShopHi
	pokemart DockCafe_Stock
	msgbox DockCafe_Text_ShopBye
	release
	end

	.align 2
DockCafe_Stock::
	.2byte ITEM_FRESH_WATER
	.2byte ITEM_SODA_POP
	.2byte ITEM_LEMONADE
	.2byte ITEM_MOOMOO_MILK
	.2byte ITEM_BERRY_JUICE
	.2byte ITEM_ENERGY_POWDER
	.2byte ITEM_HEAL_POWDER
	.2byte ITEM_REVIVAL_HERB
	.2byte ITEM_ENERGY_ROOT
	.2byte ITEM_NONE

