BerryStand_MapScripts::
	.byte 0

BerryStand_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox BerryStand_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BerryStand_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

BerryStand_EventScript_Stay::
	msgbox BerryStand_Text_Stay
	release
	end

BerryStand_EventScript_Shop::
	lock
	faceplayer
	msgbox BerryStand_Text_ShopHi
	pokemart BerryStand_Stock
	msgbox BerryStand_Text_ShopBye
	release
	end

	.align 2
BerryStand_Stock::
	.2byte ITEM_CHERI_BERRY
	.2byte ITEM_CHESTO_BERRY
	.2byte ITEM_PECHA_BERRY
	.2byte ITEM_RAWST_BERRY
	.2byte ITEM_ASPEAR_BERRY
	.2byte ITEM_ORAN_BERRY
	.2byte ITEM_PERSIM_BERRY
	.2byte ITEM_LUM_BERRY
	.2byte ITEM_SITRUS_BERRY
	.2byte ITEM_NONE

BerryStand_EventScript_Npc0::
	msgbox BerryStand_Text_Npc0, MSGBOX_NPC
	end

