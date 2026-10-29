RockTunnel_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, RockTunnel_1F_OnTransition
	.byte 0

RockTunnel_1F_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_ROCK_TUNNEL_1F
	end

RockTunnel_1F_EventScript_RouteSign::
	msgbox RockTunnel_1F_Text_RouteSign, MSGBOX_SIGN
	end

RockTunnel_1F_EventScript_Lenny::
	trainerbattle_single TRAINER_HIKER_LENNY, RockTunnel_1F_Text_LennyIntro, RockTunnel_1F_Text_LennyDefeat
	msgbox RockTunnel_1F_Text_LennyPostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_1F_EventScript_Oliver::
	trainerbattle_single TRAINER_HIKER_OLIVER, RockTunnel_1F_Text_OliverIntro, RockTunnel_1F_Text_OliverDefeat
	msgbox RockTunnel_1F_Text_OliverPostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_1F_EventScript_Lucas::
	trainerbattle_single TRAINER_HIKER_LUCAS, RockTunnel_1F_Text_LucasIntro, RockTunnel_1F_Text_LucasDefeat
	msgbox RockTunnel_1F_Text_LucasPostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_1F_EventScript_Ashton::
	trainerbattle_single TRAINER_POKEMANIAC_ASHTON, RockTunnel_1F_Text_AshtonIntro, RockTunnel_1F_Text_AshtonDefeat
	msgbox RockTunnel_1F_Text_AshtonPostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_1F_EventScript_Leah::
	trainerbattle_single TRAINER_PICNICKER_LEAH, RockTunnel_1F_Text_LeahIntro, RockTunnel_1F_Text_LeahDefeat
	msgbox RockTunnel_1F_Text_LeahPostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_1F_EventScript_Ariana::
	trainerbattle_single TRAINER_PICNICKER_ARIANA, RockTunnel_1F_Text_ArianaIntro, RockTunnel_1F_Text_ArianaDefeat
	msgbox RockTunnel_1F_Text_ArianaPostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_1F_EventScript_Dana::
	trainerbattle_single TRAINER_PICNICKER_DANA, RockTunnel_1F_Text_DanaIntro, RockTunnel_1F_Text_DanaDefeat
	msgbox RockTunnel_1F_Text_DanaPostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_1F_EventScript_MonMachop::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MACHOP, CRY_MODE_NORMAL
	msgbox RockTunnel_1F_Text_MonMachop
	waitmoncry
	release
	end

RockTunnel_1F_EventScript_MonNidorino::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NIDORINO, CRY_MODE_NORMAL
	msgbox RockTunnel_1F_Text_MonNidorino
	waitmoncry
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
RockTunnel_1F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROCKTUNNEL_1F_0, RockTunnel_1F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_SUPER_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, RockTunnel_1F_EventScript_TopazeFind0_Full
	giveitem ITEM_SUPER_POTION, 1
	setflag FLAG_TOPAZE_HID_ROCKTUNNEL_1F_0
	release
	end

RockTunnel_1F_EventScript_TopazeFind0_Done::
	release
	end

RockTunnel_1F_EventScript_TopazeFind0_Full::
	msgbox RockTunnel_1F_Text_TopazeFindFull
	release
	end

RockTunnel_1F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROCKTUNNEL_1F_1, RockTunnel_1F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_GREAT_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, RockTunnel_1F_EventScript_TopazeFind1_Full
	giveitem ITEM_GREAT_BALL, 1
	setflag FLAG_TOPAZE_HID_ROCKTUNNEL_1F_1
	release
	end

RockTunnel_1F_EventScript_TopazeFind1_Done::
	release
	end

RockTunnel_1F_EventScript_TopazeFind1_Full::
	msgbox RockTunnel_1F_Text_TopazeFindFull
	release
	end


RockTunnel_1F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
