PokemonMansion_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PokemonMansion_1F_OnTransition
	.byte 0

PokemonMansion_1F_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_POWER_PLANT
	call PokemonMansion_1F_EventScript_CheckOnybris
	end

PokemonMansion_1F_EventScript_Ted::
	trainerbattle_single TRAINER_SCIENTIST_TED, PokemonMansion_1F_Text_TedIntro, PokemonMansion_1F_Text_TedDefeat
	msgbox PokemonMansion_1F_Text_TedPostBattle, MSGBOX_AUTOCLOSE
	end

PokemonMansion_1F_EventScript_Johnson::
	trainerbattle_single TRAINER_YOUNGSTER_JOHNSON, PokemonMansion_1F_Text_JohnsonIntro, PokemonMansion_1F_Text_JohnsonDefeat
	msgbox PokemonMansion_1F_Text_JohnsonPostBattle, MSGBOX_AUTOCLOSE
	end

PokemonMansion_1F_EventScript_CheckOnybris::
	goto_if_unset FLAG_CHRONDROLIA_RAID_STARTED, PokemonMansion_1F_EventScript_HideOnybris
	goto_if_set FLAG_CHRONDROLIA_RAID_DONE, PokemonMansion_1F_EventScript_HideOnybris
	return

PokemonMansion_1F_EventScript_HideOnybris::
	setflag FLAG_TEMP_4
	setflag FLAG_TEMP_5
	setflag FLAG_TEMP_6
	return

PokemonMansion_1F_EventScript_Onybris1::
	trainerbattle_single TRAINER_RS_PSYCHIC_M, PokemonMansion_1F_Text_Onybris1Intro, PokemonMansion_1F_Text_Onybris1Defeat
	msgbox PokemonMansion_1F_Text_Onybris1Post, MSGBOX_AUTOCLOSE
	end

PokemonMansion_1F_EventScript_Onybris2::
	trainerbattle_single TRAINER_RS_PSYCHIC_F, PokemonMansion_1F_Text_Onybris2Intro, PokemonMansion_1F_Text_Onybris2Defeat
	msgbox PokemonMansion_1F_Text_Onybris2Post, MSGBOX_AUTOCLOSE
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
PokemonMansion_1F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_POKEMONMANSION_1F_0, PokemonMansion_1F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_FIRE_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, PokemonMansion_1F_EventScript_TopazeFind0_Full
	giveitem ITEM_FIRE_STONE, 1
	setflag FLAG_TOPAZE_HID_POKEMONMANSION_1F_0
	release
	end

PokemonMansion_1F_EventScript_TopazeFind0_Done::
	release
	end

PokemonMansion_1F_EventScript_TopazeFind0_Full::
	msgbox PokemonMansion_1F_Text_TopazeFindFull
	release
	end

PokemonMansion_1F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_POKEMONMANSION_1F_1, PokemonMansion_1F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ULTRA_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, PokemonMansion_1F_EventScript_TopazeFind1_Full
	giveitem ITEM_ULTRA_BALL, 1
	setflag FLAG_TOPAZE_HID_POKEMONMANSION_1F_1
	release
	end

PokemonMansion_1F_EventScript_TopazeFind1_Done::
	release
	end

PokemonMansion_1F_EventScript_TopazeFind1_Full::
	msgbox PokemonMansion_1F_Text_TopazeFindFull
	release
	end


PokemonMansion_1F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
