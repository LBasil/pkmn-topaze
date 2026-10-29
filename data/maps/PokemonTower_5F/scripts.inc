PokemonTower_5F_MapScripts::
	.byte 0

PokemonTower_5F_EventScript_Channeler::
	msgbox PokemonTower_5F_Text_RestHereInPurifiedSpace, MSGBOX_NPC
	end

PokemonTower_5F_EventScript_PurifiedZone::
	lockall
	fadescreen FADE_TO_WHITE
	special HealPlayerParty
	fadescreen FADE_FROM_WHITE
	msgbox PokemonTower_5F_Text_PurifiedZoneMonsFullyHealed
	setvar VAR_TEMP_1, 1
	releaseall
	end

PokemonTower_5F_EventScript_ExitPurifiedZone::
	lockall
	setvar VAR_TEMP_1, 0
	releaseall
	end

PokemonTower_5F_EventScript_Tammy::
	trainerbattle_single TRAINER_CHANNELER_TAMMY, PokemonTower_5F_Text_TammyIntro, PokemonTower_5F_Text_TammyDefeat
	msgbox PokemonTower_5F_Text_TammyPostBattle, MSGBOX_AUTOCLOSE
	end

PokemonTower_5F_EventScript_Ruth::
	trainerbattle_single TRAINER_CHANNELER_RUTH, PokemonTower_5F_Text_RuthIntro, PokemonTower_5F_Text_RuthDefeat
	msgbox PokemonTower_5F_Text_RuthPostBattle, MSGBOX_AUTOCLOSE
	end

PokemonTower_5F_EventScript_Karina::
	trainerbattle_single TRAINER_CHANNELER_KARINA, PokemonTower_5F_Text_KarinaIntro, PokemonTower_5F_Text_KarinaDefeat
	msgbox PokemonTower_5F_Text_KarinaPostBattle, MSGBOX_AUTOCLOSE
	end

PokemonTower_5F_EventScript_Janae::
	trainerbattle_single TRAINER_CHANNELER_JANAE, PokemonTower_5F_Text_JanaeIntro, PokemonTower_5F_Text_JanaeDefeat
	msgbox PokemonTower_5F_Text_JanaePostBattle, MSGBOX_AUTOCLOSE
	end

PokemonTower_5F_EventScript_MonJigglypuff::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_JIGGLYPUFF, CRY_MODE_NORMAL
	msgbox PokemonTower_5F_Text_MonJigglypuff
	waitmoncry
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
PokemonTower_5F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_POKEMONTOWER_5F_0, PokemonTower_5F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, PokemonTower_5F_EventScript_TopazeFind0_Full
	giveitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_HID_POKEMONTOWER_5F_0
	release
	end

PokemonTower_5F_EventScript_TopazeFind0_Done::
	release
	end

PokemonTower_5F_EventScript_TopazeFind0_Full::
	msgbox PokemonTower_5F_Text_TopazeFindFull
	release
	end

PokemonTower_5F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_POKEMONTOWER_5F_1, PokemonTower_5F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_MAX_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, PokemonTower_5F_EventScript_TopazeFind1_Full
	giveitem ITEM_MAX_REVIVE, 1
	setflag FLAG_TOPAZE_HID_POKEMONTOWER_5F_1
	release
	end

PokemonTower_5F_EventScript_TopazeFind1_Done::
	release
	end

PokemonTower_5F_EventScript_TopazeFind1_Full::
	msgbox PokemonTower_5F_Text_TopazeFindFull
	release
	end


PokemonTower_5F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
