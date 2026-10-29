BattleStall_MapScripts::
	.byte 0

BattleStall_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox BattleStall_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleStall_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

BattleStall_EventScript_Stay::
	msgbox BattleStall_Text_Stay
	release
	end

BattleStall_EventScript_Shop::
	lock
	faceplayer
	msgbox BattleStall_Text_ShopHi
	pokemart BattleStall_Stock
	msgbox BattleStall_Text_ShopBye
	release
	end

	.align 2
BattleStall_Stock::
	.2byte ITEM_X_ATTACK
	.2byte ITEM_X_DEFEND
	.2byte ITEM_X_SPEED
	.2byte ITEM_X_SPECIAL
	.2byte ITEM_X_ACCURACY
	.2byte ITEM_GUARD_SPEC
	.2byte ITEM_DIRE_HIT
	.2byte ITEM_NONE

BattleStall_EventScript_Npc0::
	msgbox BattleStall_Text_Npc0, MSGBOX_NPC
	end

