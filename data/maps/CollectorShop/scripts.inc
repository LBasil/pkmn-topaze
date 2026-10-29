CollectorShop_MapScripts::
	.byte 0

CollectorShop_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox CollectorShop_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CollectorShop_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

CollectorShop_EventScript_Stay::
	msgbox CollectorShop_Text_Stay
	release
	end

CollectorShop_EventScript_Npc0::
	msgbox CollectorShop_Text_Npc0, MSGBOX_NPC
	end

CollectorShop_EventScript_Shop::
	lock
	faceplayer
	msgbox CollectorShop_Text_ShopHi
	pokemart CollectorShop_Stock
	msgbox CollectorShop_Text_ShopBye
	release
	end

	.align 2
CollectorShop_Stock::
	.2byte ITEM_SOFT_SAND
	.2byte ITEM_SHARP_BEAK
	.2byte ITEM_POISON_BARB
	.2byte ITEM_SILVER_POWDER
	.2byte ITEM_SCOPE_LENS
	.2byte ITEM_QUICK_CLAW
	.2byte ITEM_FOCUS_BAND
	.2byte ITEM_SMOKE_BALL
	.2byte ITEM_CLEANSE_TAG
	.2byte ITEM_SOOTHE_BELL
	.2byte ITEM_NONE

