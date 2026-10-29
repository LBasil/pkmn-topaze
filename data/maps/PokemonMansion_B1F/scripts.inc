PokemonMansion_B1F_MapScripts::
	.byte 0

PokemonMansion_B1F_EventScript_DiarySep1st::
	msgbox PokemonMansion_B1F_Text_MewtwoIsFarTooPowerful, MSGBOX_SIGN
	end

PokemonMansion_B1F_EventScript_Lewis::
	trainerbattle_single TRAINER_BURGLAR_LEWIS, PokemonMansion_B1F_Text_LewisIntro, PokemonMansion_B1F_Text_LewisDefeat
	msgbox PokemonMansion_B1F_Text_LewisPostBattle, MSGBOX_AUTOCLOSE
	end

PokemonMansion_B1F_EventScript_Ivan::
	trainerbattle_single TRAINER_SCIENTIST_IVAN, PokemonMansion_B1F_Text_IvanIntro, PokemonMansion_B1F_Text_IvanDefeat
	msgbox PokemonMansion_B1F_Text_IvanPostBattle, MSGBOX_AUTOCLOSE
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
PokemonMansion_B1F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_POKEMONMANSION_B1F_0, PokemonMansion_B1F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_RARE_CANDY, 1
	goto_if_eq VAR_RESULT, FALSE, PokemonMansion_B1F_EventScript_TopazeFind0_Full
	giveitem ITEM_RARE_CANDY, 1
	setflag FLAG_TOPAZE_HID_POKEMONMANSION_B1F_0
	release
	end

PokemonMansion_B1F_EventScript_TopazeFind0_Done::
	release
	end

PokemonMansion_B1F_EventScript_TopazeFind0_Full::
	msgbox PokemonMansion_B1F_Text_TopazeFindFull
	release
	end

PokemonMansion_B1F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_POKEMONMANSION_B1F_1, PokemonMansion_B1F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_NUGGET, 1
	goto_if_eq VAR_RESULT, FALSE, PokemonMansion_B1F_EventScript_TopazeFind1_Full
	giveitem ITEM_NUGGET, 1
	setflag FLAG_TOPAZE_HID_POKEMONMANSION_B1F_1
	release
	end

PokemonMansion_B1F_EventScript_TopazeFind1_Done::
	release
	end

PokemonMansion_B1F_EventScript_TopazeFind1_Full::
	msgbox PokemonMansion_B1F_Text_TopazeFindFull
	release
	end


PokemonMansion_B1F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
