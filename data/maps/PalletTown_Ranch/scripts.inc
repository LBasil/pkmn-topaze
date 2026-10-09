PalletTown_Ranch_MapScripts::
	.byte 0

PalletTown_Ranch_EventScript_Hand1::
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_Ranch_EventScript_Hand1Strike
	msgbox PalletTown_Ranch_Text_Hand1, MSGBOX_NPC
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
