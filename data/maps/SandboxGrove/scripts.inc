SandboxGrove_MapScripts::
	.byte 0

SandboxGrove_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SandboxGrove_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SandboxGrove_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SandboxGrove_EventScript_Stay::
	msgbox SandboxGrove_Text_Stay
	release
	end

SandboxGrove_EventScript_Npc0::
	msgbox SandboxGrove_Text_Npc0, MSGBOX_NPC
	end

SandboxGrove_EventScript_Npc1::
	msgbox SandboxGrove_Text_Npc1, MSGBOX_NPC
	end

