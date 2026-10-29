DexHall_MapScripts::
	.byte 0

DexHall_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox DexHall_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, DexHall_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

DexHall_EventScript_Stay::
	msgbox DexHall_Text_Stay
	release
	end

DexHall_EventScript_Judge::
	lock
	faceplayer
	msgbox DexHall_Text_Hello
	setvar VAR_0x8004, 1
	specialvar VAR_RESULT, GetPokedexCount
	goto_if_set FLAG_TOPAZE_DEXHALL_25, DexHall_EventScript_Judge_1
	goto_if_lt VAR_0x8006, 25, DexHall_EventScript_Judge_1
	checkitemspace ITEM_ULTRA_BALL, 5
	goto_if_eq VAR_RESULT, FALSE, DexHall_EventScript_Judge_NoRoom
	giveitem ITEM_ULTRA_BALL, 5
	setflag FLAG_TOPAZE_DEXHALL_25
	msgbox DexHall_Text_M25
	setvar VAR_0x8004, 1
	specialvar VAR_RESULT, GetPokedexCount
	goto DexHall_EventScript_Judge_1
DexHall_EventScript_Judge_1::
	goto_if_set FLAG_TOPAZE_DEXHALL_50, DexHall_EventScript_Judge_2
	goto_if_lt VAR_0x8006, 50, DexHall_EventScript_Judge_2
	checkitemspace ITEM_RARE_CANDY, 2
	goto_if_eq VAR_RESULT, FALSE, DexHall_EventScript_Judge_NoRoom
	giveitem ITEM_RARE_CANDY, 2
	setflag FLAG_TOPAZE_DEXHALL_50
	msgbox DexHall_Text_M50
	setvar VAR_0x8004, 1
	specialvar VAR_RESULT, GetPokedexCount
	goto DexHall_EventScript_Judge_2
DexHall_EventScript_Judge_2::
	goto_if_set FLAG_TOPAZE_DEXHALL_75, DexHall_EventScript_Judge_3
	goto_if_lt VAR_0x8006, 75, DexHall_EventScript_Judge_3
	checkitemspace ITEM_PP_UP, 2
	goto_if_eq VAR_RESULT, FALSE, DexHall_EventScript_Judge_NoRoom
	giveitem ITEM_PP_UP, 2
	setflag FLAG_TOPAZE_DEXHALL_75
	msgbox DexHall_Text_M75
	setvar VAR_0x8004, 1
	specialvar VAR_RESULT, GetPokedexCount
	goto DexHall_EventScript_Judge_3
DexHall_EventScript_Judge_3::
	goto_if_set FLAG_TOPAZE_DEXHALL_100, DexHall_EventScript_Judge_4
	goto_if_lt VAR_0x8006, 100, DexHall_EventScript_Judge_4
	checkitemspace ITEM_MAX_REVIVE, 3
	goto_if_eq VAR_RESULT, FALSE, DexHall_EventScript_Judge_NoRoom
	giveitem ITEM_MAX_REVIVE, 3
	setflag FLAG_TOPAZE_DEXHALL_100
	msgbox DexHall_Text_M100
	setvar VAR_0x8004, 1
	specialvar VAR_RESULT, GetPokedexCount
	goto DexHall_EventScript_Judge_4
DexHall_EventScript_Judge_4::
	goto_if_set FLAG_TOPAZE_DEXHALL_150, DexHall_EventScript_Judge_5
	goto_if_lt VAR_0x8006, 150, DexHall_EventScript_Judge_5
	checkitemspace ITEM_RARE_CANDY, 5
	goto_if_eq VAR_RESULT, FALSE, DexHall_EventScript_Judge_NoRoom
	giveitem ITEM_RARE_CANDY, 5
	setflag FLAG_TOPAZE_DEXHALL_150
	msgbox DexHall_Text_M150
	setvar VAR_0x8004, 1
	specialvar VAR_RESULT, GetPokedexCount
	goto DexHall_EventScript_Judge_5
DexHall_EventScript_Judge_5::
	goto_if_set FLAG_TOPAZE_DEXHALL_200, DexHall_EventScript_Judge_6
	goto_if_lt VAR_0x8006, 200, DexHall_EventScript_Judge_6
	checkitemspace ITEM_PP_MAX, 3
	goto_if_eq VAR_RESULT, FALSE, DexHall_EventScript_Judge_NoRoom
	giveitem ITEM_PP_MAX, 3
	setflag FLAG_TOPAZE_DEXHALL_200
	msgbox DexHall_Text_M200
	setvar VAR_0x8004, 1
	specialvar VAR_RESULT, GetPokedexCount
	goto DexHall_EventScript_Judge_6
DexHall_EventScript_Judge_6::
	goto_if_set FLAG_TOPAZE_DEXHALL_250, DexHall_EventScript_Judge_7
	goto_if_lt VAR_0x8006, 250, DexHall_EventScript_Judge_7
	checkitemspace ITEM_MASTER_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, DexHall_EventScript_Judge_NoRoom
	giveitem ITEM_MASTER_BALL, 1
	setflag FLAG_TOPAZE_DEXHALL_250
	msgbox DexHall_Text_M250
	setvar VAR_0x8004, 1
	specialvar VAR_RESULT, GetPokedexCount
	goto DexHall_EventScript_Judge_7
DexHall_EventScript_Judge_7::
	goto_if_set FLAG_TOPAZE_DEXHALL_300, DexHall_EventScript_Judge_8
	goto_if_lt VAR_0x8006, 300, DexHall_EventScript_Judge_8
	checkitemspace ITEM_RARE_CANDY, 10
	goto_if_eq VAR_RESULT, FALSE, DexHall_EventScript_Judge_NoRoom
	giveitem ITEM_RARE_CANDY, 10
	setflag FLAG_TOPAZE_DEXHALL_300
	msgbox DexHall_Text_M300
	setvar VAR_0x8004, 1
	specialvar VAR_RESULT, GetPokedexCount
	goto DexHall_EventScript_Judge_8
DexHall_EventScript_Judge_8::
	goto_if_set FLAG_TOPAZE_DEXHALL_350, DexHall_EventScript_Judge_9
	goto_if_lt VAR_0x8006, 350, DexHall_EventScript_Judge_9
	checkitemspace ITEM_PP_MAX, 5
	goto_if_eq VAR_RESULT, FALSE, DexHall_EventScript_Judge_NoRoom
	giveitem ITEM_PP_MAX, 5
	setflag FLAG_TOPAZE_DEXHALL_350
	msgbox DexHall_Text_M350
	setvar VAR_0x8004, 1
	specialvar VAR_RESULT, GetPokedexCount
	goto DexHall_EventScript_Judge_9
DexHall_EventScript_Judge_9::
	goto_if_set FLAG_TOPAZE_DEXHALL_386, DexHall_EventScript_Judge_End
	goto_if_lt VAR_0x8006, 386, DexHall_EventScript_Judge_End
	checkitemspace ITEM_RARE_CANDY, 30
	goto_if_eq VAR_RESULT, FALSE, DexHall_EventScript_Judge_NoRoom
	giveitem ITEM_RARE_CANDY, 30
	setflag FLAG_TOPAZE_DEXHALL_386
	msgbox DexHall_Text_M386
	setvar VAR_0x8004, 1
	specialvar VAR_RESULT, GetPokedexCount
	goto DexHall_EventScript_Judge_End
DexHall_EventScript_Judge_End::
	msgbox DexHall_Text_Nothing
	release
	end

DexHall_EventScript_Judge_NoRoom::
	msgbox DexHall_Text_NoRoom
	release
	end
