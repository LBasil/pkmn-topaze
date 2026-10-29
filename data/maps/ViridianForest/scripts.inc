ViridianForest_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, ViridianForest_OnTransition
	.byte 0

ViridianForest_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_VIRIDIAN_FOREST
	end

ViridianForest_EventScript_Youngster::
	msgbox ViridianForest_Text_FriendsItchingToBattle, MSGBOX_NPC
	end

ViridianForest_EventScript_Boy::
	msgbox ViridianForest_Text_RanOutOfPokeBalls, MSGBOX_NPC
	end

ViridianForest_EventScript_TrainerTips1::
	msgbox ViridianForest_Text_AvoidGrassyAreasWhenWeak, MSGBOX_SIGN
	end

ViridianForest_EventScript_TrainerTips2::
	msgbox ViridianForest_Text_UseAntidoteForPoison, MSGBOX_SIGN
	end

ViridianForest_EventScript_TrainerTips3::
	msgbox ViridianForest_Text_ContactOakViaPCToRatePokedex, MSGBOX_SIGN
	end

ViridianForest_EventScript_TrainerTips4::
	msgbox ViridianForest_Text_CantCatchOwnedMons, MSGBOX_SIGN
	end

ViridianForest_EventScript_TrainerTips5::
	msgbox ViridianForest_Text_WeakenMonsBeforeCapture, MSGBOX_SIGN
	end

ViridianForest_EventScript_ExitSign::
	msgbox ViridianForest_Text_LeavingViridianForest, MSGBOX_SIGN
	end

ViridianForest_EventScript_Rick::
	trainerbattle_single TRAINER_BUG_CATCHER_RICK, ViridianForest_Text_RickIntro, ViridianForest_Text_RickDefeat
	msgbox ViridianForest_Text_RickPostBattle, MSGBOX_AUTOCLOSE
	end

ViridianForest_EventScript_Doug::
	trainerbattle_single TRAINER_BUG_CATCHER_DOUG, ViridianForest_Text_DougIntro, ViridianForest_Text_DougDefeat
	msgbox ViridianForest_Text_DougPostBattle, MSGBOX_AUTOCLOSE
	end

ViridianForest_EventScript_Sammy::
	trainerbattle_single TRAINER_BUG_CATCHER_SAMMY, ViridianForest_Text_SammyIntro, ViridianForest_Text_SammyDefeat
	msgbox ViridianForest_Text_SammyPostBattle, MSGBOX_AUTOCLOSE
	end

ViridianForest_EventScript_Anthony::
	trainerbattle_single TRAINER_BUG_CATCHER_ANTHONY, ViridianForest_Text_AnthonyIntro, ViridianForest_Text_AnthonyDefeat
	msgbox ViridianForest_Text_AnthonyPostBattle, MSGBOX_AUTOCLOSE
	end

ViridianForest_EventScript_Charlie::
	trainerbattle_single TRAINER_BUG_CATCHER_CHARLIE, ViridianForest_Text_CharlieIntro, ViridianForest_Text_CharlieDefeat
	msgbox ViridianForest_Text_CharliePostBattle, MSGBOX_AUTOCLOSE
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
ViridianForest_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_VIRIDIANFOREST_0, ViridianForest_EventScript_TopazeFind0_Done
	checkitemspace ITEM_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, ViridianForest_EventScript_TopazeFind0_Full
	giveitem ITEM_POTION, 1
	setflag FLAG_TOPAZE_HID_VIRIDIANFOREST_0
	release
	end

ViridianForest_EventScript_TopazeFind0_Done::
	release
	end

ViridianForest_EventScript_TopazeFind0_Full::
	msgbox ViridianForest_Text_TopazeFindFull
	release
	end

ViridianForest_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_VIRIDIANFOREST_1, ViridianForest_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ANTIDOTE, 1
	goto_if_eq VAR_RESULT, FALSE, ViridianForest_EventScript_TopazeFind1_Full
	giveitem ITEM_ANTIDOTE, 1
	setflag FLAG_TOPAZE_HID_VIRIDIANFOREST_1
	release
	end

ViridianForest_EventScript_TopazeFind1_Done::
	release
	end

ViridianForest_EventScript_TopazeFind1_Full::
	msgbox ViridianForest_Text_TopazeFindFull
	release
	end


ViridianForest_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
