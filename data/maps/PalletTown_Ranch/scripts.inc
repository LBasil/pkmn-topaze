PalletTown_Ranch_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PalletTown_Ranch_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, PalletTown_Ranch_OnLoad
	.byte 0

PalletTown_Ranch_OnTransition::
	setflag FLAG_HIDE_RANCH_ANIMALS
	goto_if_unset FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_Ranch_Peaceful
	goto_if_set FLAG_ONYBRIS_ANIMALS_FOUND, PalletTown_Ranch_ShowAnimals
	clearflag FLAG_HIDE_RANCH_CUT_HAND
	end

PalletTown_Ranch_Peaceful::
	clearflag FLAG_HIDE_RANCH_ANIMALS
	setflag FLAG_HIDE_RANCH_CUT_HAND
	end

PalletTown_Ranch_ShowAnimals::
	clearflag FLAG_HIDE_RANCH_ANIMALS
	clearflag FLAG_HIDE_RANCH_CUT_HAND
	end

PalletTown_Ranch_OnLoad::
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_Ranch_CutFence
	end

PalletTown_Ranch_CutFence::
	setmetatile 27, 13, 0x001, FALSE
	setmetatile 27, 14, 0x001, FALSE
	end

PalletTown_Ranch_EventScript_Hand1::
	goto_if_set FLAG_GRENALUX_GEM_REWARD, PalletTown_Ranch_EventScript_Hand1Thanks
	goto_if_set FLAG_ONYBRIS_ANIMALS_FOUND, PalletTown_Ranch_EventScript_Hand1Reward
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_Ranch_EventScript_Hand1Strike
	msgbox PalletTown_Ranch_Text_Hand1, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Hand1Reward::
	lock
	faceplayer
	msgbox PalletTown_Ranch_Text_Hand1Reward
	giveitem_msg PalletTown_Ranch_Text_ReceivedPotion, ITEM_POTION
	giveitem_msg PalletTown_Ranch_Text_ReceivedBalls, ITEM_POKE_BALL, 5
	setflag FLAG_GRENALUX_GEM_REWARD
	msgbox PalletTown_Ranch_Text_Hand1Reward2
	release
	end

PalletTown_Ranch_EventScript_Hand1Thanks::
	msgbox PalletTown_Ranch_Text_Hand1Thanks, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Hand1Strike::
	msgbox PalletTown_Ranch_Text_Hand1Strike, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Hand2::
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_Ranch_EventScript_Hand2Strike
	msgbox PalletTown_Ranch_Text_Hand2, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Hand2Strike::
	msgbox PalletTown_Ranch_Text_Hand2Strike, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Girl::
	msgbox PalletTown_Ranch_Text_Girl, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Slowpoke::
	msgbox PalletTown_Ranch_Text_Slowpoke, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Psyduck::
	msgbox PalletTown_Ranch_Text_Psyduck, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Hand3::
	msgbox PalletTown_Ranch_Text_Hand3, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Doduo::
	msgbox PalletTown_Ranch_Text_Doduo, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Nidoranm::
	msgbox PalletTown_Ranch_Text_Nidoranm, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Nidoranf::
	msgbox PalletTown_Ranch_Text_Nidoranf, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Meowth::
	msgbox PalletTown_Ranch_Text_Meowth, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Jigglypuff::
	msgbox PalletTown_Ranch_Text_Jigglypuff, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_BarnDoor::
	msgbox PalletTown_Ranch_Text_BarnDoor, MSGBOX_SIGN
	end
