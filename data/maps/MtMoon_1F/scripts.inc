MtMoon_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtMoon_1F_OnTransition
	.byte 0

MtMoon_1F_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_MT_MOON_1F
	end

MtMoon_1F_EventScript_ZubatSign::
	msgbox MtMoon_1F_Text_ZubatIsABloodsucker, MSGBOX_SIGN
	end

MtMoon_1F_EventScript_Marcos::
	trainerbattle_single TRAINER_HIKER_MARCOS, MtMoon_1F_Text_MarcosIntro, MtMoon_1F_Text_MarcosDefeat
	msgbox MtMoon_1F_Text_MarcosPostBattle, MSGBOX_AUTOCLOSE
	end

MtMoon_1F_EventScript_Josh::
	trainerbattle_single TRAINER_YOUNGSTER_JOSH, MtMoon_1F_Text_JoshIntro, MtMoon_1F_Text_JoshDefeat
	msgbox MtMoon_1F_Text_JoshPostBattle, MSGBOX_AUTOCLOSE
	end

MtMoon_1F_EventScript_Miriam::
	trainerbattle_single TRAINER_LASS_MIRIAM, MtMoon_1F_Text_MiriamIntro, MtMoon_1F_Text_MiriamDefeat
	msgbox MtMoon_1F_Text_MiriamPostBattle, MSGBOX_AUTOCLOSE
	end

MtMoon_1F_EventScript_Iris::
	trainerbattle_single TRAINER_LASS_IRIS, MtMoon_1F_Text_IrisIntro, MtMoon_1F_Text_IrisDefeat
	msgbox MtMoon_1F_Text_IrisPostBattle, MSGBOX_AUTOCLOSE
	end

MtMoon_1F_EventScript_Jovan::
	trainerbattle_single TRAINER_SUPER_NERD_JOVAN, MtMoon_1F_Text_JovanIntro, MtMoon_1F_Text_JovanDefeat
	msgbox MtMoon_1F_Text_JovanPostBattle, MSGBOX_AUTOCLOSE
	end

MtMoon_1F_EventScript_Kent::
	trainerbattle_single TRAINER_BUG_CATCHER_KENT, MtMoon_1F_Text_KentIntro, MtMoon_1F_Text_KentDefeat
	msgbox MtMoon_1F_Text_KentPostBattle, MSGBOX_AUTOCLOSE
	end

MtMoon_1F_EventScript_Robby::
	trainerbattle_single TRAINER_BUG_CATCHER_ROBBY, MtMoon_1F_Text_RobbyIntro, MtMoon_1F_Text_RobbyDefeat
	msgbox MtMoon_1F_Text_RobbyPostBattle, MSGBOX_AUTOCLOSE
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
MtMoon_1F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_MTMOON_1F_0, MtMoon_1F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_MOON_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, MtMoon_1F_EventScript_TopazeFind0_Full
	giveitem ITEM_MOON_STONE, 1
	setflag FLAG_TOPAZE_HID_MTMOON_1F_0
	release
	end

MtMoon_1F_EventScript_TopazeFind0_Done::
	release
	end

MtMoon_1F_EventScript_TopazeFind0_Full::
	msgbox MtMoon_1F_Text_TopazeFindFull
	release
	end

MtMoon_1F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_MTMOON_1F_1, MtMoon_1F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, MtMoon_1F_EventScript_TopazeFind1_Full
	giveitem ITEM_POTION, 1
	setflag FLAG_TOPAZE_HID_MTMOON_1F_1
	release
	end

MtMoon_1F_EventScript_TopazeFind1_Done::
	release
	end

MtMoon_1F_EventScript_TopazeFind1_Full::
	msgbox MtMoon_1F_Text_TopazeFindFull
	release
	end


MtMoon_1F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
