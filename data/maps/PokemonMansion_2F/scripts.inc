PokemonMansion_2F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PokemonMansion_2F_OnTransition
	.byte 0

PokemonMansion_2F_OnTransition::
	call PokemonMansion_2F_EventScript_CheckOnybris
	end

PokemonMansion_2F_EventScript_DiaryJuly5th::
	msgbox PokemonMansion_1F_Text_NewMonDiscoveredInGuyanaJungle, MSGBOX_SIGN
	end

PokemonMansion_2F_EventScript_DiaryJuly10th::
	msgbox PokemonMansion_1F_Text_ChristenedDiscoveredMonMew, MSGBOX_SIGN
	end

PokemonMansion_2F_EventScript_Arnie::
	trainerbattle_single TRAINER_BURGLAR_ARNIE, PokemonMansion_1F_Text_ArnieIntro, PokemonMansion_1F_Text_ArnieDefeat
	msgbox PokemonMansion_1F_Text_ArniePostBattle, MSGBOX_AUTOCLOSE
	end

PokemonMansion_2F_EventScript_CheckOnybris::
	goto_if_unset FLAG_CHRONDROLIA_RAID_STARTED, PokemonMansion_2F_EventScript_HideOnybris
	goto_if_set FLAG_CHRONDROLIA_RAID_DONE, PokemonMansion_2F_EventScript_HideOnybris
	return

PokemonMansion_2F_EventScript_HideOnybris::
	setflag FLAG_TEMP_4
	setflag FLAG_TEMP_5
	setflag FLAG_TEMP_6
	return

PokemonMansion_2F_EventScript_Onybris3::
	trainerbattle_single TRAINER_RS_HIKER, PokemonMansion_2F_Text_Onybris3Intro, PokemonMansion_2F_Text_Onybris3Defeat
	msgbox PokemonMansion_2F_Text_Onybris3Post, MSGBOX_AUTOCLOSE
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
PokemonMansion_2F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_POKEMONMANSION_2F_0, PokemonMansion_2F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_HYPER_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, PokemonMansion_2F_EventScript_TopazeFind0_Full
	giveitem ITEM_HYPER_POTION, 1
	setflag FLAG_TOPAZE_HID_POKEMONMANSION_2F_0
	release
	end

PokemonMansion_2F_EventScript_TopazeFind0_Done::
	release
	end

PokemonMansion_2F_EventScript_TopazeFind0_Full::
	msgbox PokemonMansion_2F_Text_TopazeFindFull
	release
	end

PokemonMansion_2F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_POKEMONMANSION_2F_1, PokemonMansion_2F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, PokemonMansion_2F_EventScript_TopazeFind1_Full
	giveitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_HID_POKEMONMANSION_2F_1
	release
	end

PokemonMansion_2F_EventScript_TopazeFind1_Done::
	release
	end

PokemonMansion_2F_EventScript_TopazeFind1_Full::
	msgbox PokemonMansion_2F_Text_TopazeFindFull
	release
	end


PokemonMansion_2F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
