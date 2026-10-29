StoneGreenhouse_MapScripts::
	.byte 0

StoneGreenhouse_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox StoneGreenhouse_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StoneGreenhouse_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

StoneGreenhouse_EventScript_Stay::
	msgbox StoneGreenhouse_Text_Stay
	release
	end

StoneGreenhouse_EventScript_Npc0::
	msgbox StoneGreenhouse_Text_Npc0, MSGBOX_NPC
	end

StoneGreenhouse_EventScript_Merchant::
	lock
	faceplayer
	msgbox StoneGreenhouse_Text_Merchant
	pokemart StoneGreenhouse_Stock
	msgbox StoneGreenhouse_Text_Bye
	release
	end

	.align 2
StoneGreenhouse_Stock::
	.2byte ITEM_FIRE_STONE
	.2byte ITEM_WATER_STONE
	.2byte ITEM_THUNDER_STONE
	.2byte ITEM_LEAF_STONE
	.2byte ITEM_MOON_STONE
	.2byte ITEM_SUN_STONE
	.2byte ITEM_DRAGON_SCALE
	.2byte ITEM_UP_GRADE
	.2byte ITEM_METAL_COAT
	.2byte ITEM_KINGS_ROCK
	.2byte ITEM_DEEP_SEA_TOOTH
	.2byte ITEM_DEEP_SEA_SCALE
	.2byte ITEM_LINK_CABLE
	.2byte ITEM_NONE

