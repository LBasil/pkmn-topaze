Apothecary_MapScripts::
	.byte 0

Apothecary_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox Apothecary_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Apothecary_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

Apothecary_EventScript_Stay::
	msgbox Apothecary_Text_Stay
	release
	end

Apothecary_EventScript_Npc0::
	msgbox Apothecary_Text_Npc0, MSGBOX_NPC
	end

Apothecary_EventScript_Shop::
	lock
	faceplayer
	msgbox Apothecary_Text_ShopHi
	pokemart Apothecary_Stock
	msgbox Apothecary_Text_ShopBye
	release
	end

	.align 2
Apothecary_Stock::
	.2byte ITEM_HP_UP
	.2byte ITEM_PROTEIN
	.2byte ITEM_IRON
	.2byte ITEM_CALCIUM
	.2byte ITEM_ZINC
	.2byte ITEM_CARBOS
	.2byte ITEM_NONE

