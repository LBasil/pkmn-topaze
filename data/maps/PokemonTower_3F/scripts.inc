PokemonTower_3F_MapScripts::
	.byte 0

PokemonTower_3F_EventScript_Patricia::
	trainerbattle_single TRAINER_CHANNELER_PATRICIA, PokemonTower_3F_Text_PatriciaIntro, PokemonTower_3F_Text_PatriciaDefeat
	msgbox PokemonTower_3F_Text_PatriciaPostBattle, MSGBOX_AUTOCLOSE
	end

PokemonTower_3F_EventScript_Carly::
	trainerbattle_single TRAINER_CHANNELER_CARLY, PokemonTower_3F_Text_CarlyIntro, PokemonTower_3F_Text_CarlyDefeat
	msgbox PokemonTower_3F_Text_CarlyPostBattle, MSGBOX_AUTOCLOSE
	end

PokemonTower_3F_EventScript_Hope::
	trainerbattle_single TRAINER_CHANNELER_HOPE, PokemonTower_3F_Text_HopeIntro, PokemonTower_3F_Text_HopeDefeat
	msgbox PokemonTower_3F_Text_HopePostBattle, MSGBOX_AUTOCLOSE
	end

PokemonTower_3F_EventScript_MonCubone::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CUBONE, CRY_MODE_NORMAL
	msgbox PokemonTower_3F_Text_MonCubone
	waitmoncry
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
PokemonTower_3F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_POKEMONTOWER_3F_0, PokemonTower_3F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, PokemonTower_3F_EventScript_TopazeFind0_Full
	giveitem ITEM_REVIVE, 1
	setflag FLAG_TOPAZE_HID_POKEMONTOWER_3F_0
	release
	end

PokemonTower_3F_EventScript_TopazeFind0_Done::
	release
	end

PokemonTower_3F_EventScript_TopazeFind0_Full::
	msgbox PokemonTower_3F_Text_TopazeFindFull
	release
	end

PokemonTower_3F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_POKEMONTOWER_3F_1, PokemonTower_3F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ULTRA_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, PokemonTower_3F_EventScript_TopazeFind1_Full
	giveitem ITEM_ULTRA_BALL, 1
	setflag FLAG_TOPAZE_HID_POKEMONTOWER_3F_1
	release
	end

PokemonTower_3F_EventScript_TopazeFind1_Done::
	release
	end

PokemonTower_3F_EventScript_TopazeFind1_Full::
	msgbox PokemonTower_3F_Text_TopazeFindFull
	release
	end


PokemonTower_3F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
