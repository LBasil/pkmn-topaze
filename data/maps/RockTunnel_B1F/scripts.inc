RockTunnel_B1F_MapScripts::
	.byte 0

RockTunnel_B1F_EventScript_Sofia::
	trainerbattle_single TRAINER_PICNICKER_SOFIA, RockTunnel_B1F_Text_SofiaIntro, RockTunnel_B1F_Text_SofiaDefeat
	msgbox RockTunnel_B1F_Text_SofiaPostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_B1F_EventScript_Martha::
	trainerbattle_single TRAINER_PICNICKER_MARTHA, RockTunnel_B1F_Text_MarthaIntro, RockTunnel_B1F_Text_MarthaDefeat
	msgbox RockTunnel_B1F_Text_MarthaPostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_B1F_EventScript_Dudley::
	trainerbattle_single TRAINER_HIKER_DUDLEY, RockTunnel_B1F_Text_DudleyIntro, RockTunnel_B1F_Text_DudleyDefeat
	msgbox RockTunnel_B1F_Text_DudleyPostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_B1F_EventScript_Allen::
	trainerbattle_single TRAINER_HIKER_ALLEN, RockTunnel_B1F_Text_AllenIntro, RockTunnel_B1F_Text_AllenDefeat
	msgbox RockTunnel_B1F_Text_AllenPostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_B1F_EventScript_Eric::
	trainerbattle_single TRAINER_HIKER_ERIC, RockTunnel_B1F_Text_EricIntro, RockTunnel_B1F_Text_EricDefeat
	msgbox RockTunnel_B1F_Text_EricPostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_B1F_EventScript_Cooper::
	trainerbattle_single TRAINER_POKEMANIAC_COOPER, RockTunnel_B1F_Text_CooperIntro, RockTunnel_B1F_Text_CooperDefeat
	msgbox RockTunnel_B1F_Text_CooperPostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_B1F_EventScript_Steve::
	trainerbattle_single TRAINER_POKEMANIAC_STEVE, RockTunnel_B1F_Text_SteveIntro, RockTunnel_B1F_Text_SteveDefeat
	msgbox RockTunnel_B1F_Text_StevePostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_B1F_EventScript_Winston::
	trainerbattle_single TRAINER_POKEMANIAC_WINSTON, RockTunnel_B1F_Text_WinstonIntro, RockTunnel_B1F_Text_WinstonDefeat
	msgbox RockTunnel_B1F_Text_WinstonPostBattle, MSGBOX_AUTOCLOSE
	end

RockTunnel_B1F_EventScript_MonSlowpoke::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SLOWPOKE, CRY_MODE_NORMAL
	msgbox RockTunnel_B1F_Text_MonSlowpoke
	waitmoncry
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
RockTunnel_B1F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROCKTUNNEL_B1F_0, RockTunnel_B1F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, RockTunnel_B1F_EventScript_TopazeFind0_Full
	giveitem ITEM_REVIVE, 1
	setflag FLAG_TOPAZE_HID_ROCKTUNNEL_B1F_0
	release
	end

RockTunnel_B1F_EventScript_TopazeFind0_Done::
	release
	end

RockTunnel_B1F_EventScript_TopazeFind0_Full::
	msgbox RockTunnel_B1F_Text_TopazeFindFull
	release
	end

RockTunnel_B1F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROCKTUNNEL_B1F_1, RockTunnel_B1F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, RockTunnel_B1F_EventScript_TopazeFind1_Full
	giveitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_HID_ROCKTUNNEL_B1F_1
	release
	end

RockTunnel_B1F_EventScript_TopazeFind1_Done::
	release
	end

RockTunnel_B1F_EventScript_TopazeFind1_Full::
	msgbox RockTunnel_B1F_Text_TopazeFindFull
	release
	end


RockTunnel_B1F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
