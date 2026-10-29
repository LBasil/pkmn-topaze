PokemonMansion_3F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PokemonMansion_3F_OnTransition
	.byte 0

PokemonMansion_3F_OnTransition::
	call PokemonMansion_3F_EventScript_CheckOnybris
	end

PokemonMansion_3F_EventScript_DiaryFeb6th::
	msgbox PokemonMansion_1F_Text_MewGaveBirthToMewtwo, MSGBOX_SIGN
	end

PokemonMansion_3F_EventScript_Simon::
	trainerbattle_single TRAINER_BURGLAR_SIMON, PokemonMansion_1F_Text_SimonIntro, PokemonMansion_1F_Text_SimonDefeat
	msgbox PokemonMansion_1F_Text_SimonPostBattle, MSGBOX_AUTOCLOSE
	end

PokemonMansion_3F_EventScript_Braydon::
	trainerbattle_single TRAINER_SCIENTIST_BRAYDON, PokemonMansion_1F_Text_BraydonIntro, PokemonMansion_1F_Text_BraydonDefeat
	msgbox PokemonMansion_1F_Text_BraydonPostBattle, MSGBOX_AUTOCLOSE
	end

PokemonMansion_3F_EventScript_CheckOnybris::
	call_if_defeated TRAINER_AQUA_ADMIN_SHELLY, PokemonMansion_3F_EventScript_HideSelene
	goto_if_unset FLAG_CHRONDROLIA_RAID_STARTED, PokemonMansion_3F_EventScript_HideOnybris
	goto_if_set FLAG_CHRONDROLIA_RAID_DONE, PokemonMansion_3F_EventScript_HideOnybris
	return

PokemonMansion_3F_EventScript_HideOnybris::
	setflag FLAG_TEMP_4
	setflag FLAG_TEMP_5
	setflag FLAG_TEMP_6
	return

PokemonMansion_3F_EventScript_Onybris4::
	trainerbattle_single TRAINER_RS_LASS, PokemonMansion_3F_Text_Onybris4Intro, PokemonMansion_3F_Text_Onybris4Defeat
	msgbox PokemonMansion_3F_Text_Onybris4Post, MSGBOX_AUTOCLOSE
	end

PokemonMansion_3F_EventScript_HideSelene::
	setflag FLAG_TEMP_5
	return

PokemonMansion_3F_EventScript_OnybrisSelene::
	trainerbattle_single TRAINER_AQUA_ADMIN_SHELLY, PokemonMansion_3F_Text_SeleneIntro, PokemonMansion_3F_Text_SeleneDefeat, PokemonMansion_3F_EventScript_SeleneLeaves
	end

PokemonMansion_3F_EventScript_SeleneLeaves::
	msgbox PokemonMansion_3F_Text_SelenePost
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_PLANT_SELENE
	delay 20
	fadescreen FADE_FROM_BLACK
	release
	end

PokemonMansion_3F_EventScript_Topaz::
	lockall
	goto_if_not_defeated TRAINER_AQUA_ADMIN_SHELLY, PokemonMansion_3F_EventScript_SeleneStops
	goto PokemonMansion_3F_EventScript_TopazTake

PokemonMansion_3F_EventScript_SeleneStops::
	msgbox PokemonMansion_3F_Text_SeleneStops
	closemessage
	setvar VAR_LAST_TALKED, LOCALID_PLANT_SELENE
	trainerbattle_no_intro TRAINER_AQUA_ADMIN_SHELLY, PokemonMansion_3F_Text_SeleneDefeat
	msgbox PokemonMansion_3F_Text_SelenePost
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_PLANT_SELENE
	delay 20
	fadescreen FADE_FROM_BLACK
	releaseall
	end

PokemonMansion_3F_EventScript_TopazTake::
	msgbox PokemonMansion_3F_Text_TopazPedestal
	playfanfare MUS_OBTAIN_KEY_ITEM
	message PokemonMansion_3F_Text_ObtainedTopaz
	waitmessage
	waitfanfare
	removeobject LOCALID_PLANT_TOPAZ
	setflag FLAG_CHRONDROLIA_RAID_DONE
	releaseall
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
PokemonMansion_3F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_POKEMONMANSION_3F_0, PokemonMansion_3F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_MAX_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, PokemonMansion_3F_EventScript_TopazeFind0_Full
	giveitem ITEM_MAX_REVIVE, 1
	setflag FLAG_TOPAZE_HID_POKEMONMANSION_3F_0
	release
	end

PokemonMansion_3F_EventScript_TopazeFind0_Done::
	release
	end

PokemonMansion_3F_EventScript_TopazeFind0_Full::
	msgbox PokemonMansion_3F_Text_TopazeFindFull
	release
	end

PokemonMansion_3F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_POKEMONMANSION_3F_1, PokemonMansion_3F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_MAX_ETHER, 1
	goto_if_eq VAR_RESULT, FALSE, PokemonMansion_3F_EventScript_TopazeFind1_Full
	giveitem ITEM_MAX_ETHER, 1
	setflag FLAG_TOPAZE_HID_POKEMONMANSION_3F_1
	release
	end

PokemonMansion_3F_EventScript_TopazeFind1_Done::
	release
	end

PokemonMansion_3F_EventScript_TopazeFind1_Full::
	msgbox PokemonMansion_3F_Text_TopazeFindFull
	release
	end


PokemonMansion_3F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
