ReflectionMarsh_MapScripts::
	.byte 0

ReflectionMarsh_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox ReflectionMarsh_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ReflectionMarsh_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

ReflectionMarsh_EventScript_Stay::
	msgbox ReflectionMarsh_Text_Stay
	release
	end

ReflectionMarsh_EventScript_Npc0::
	msgbox ReflectionMarsh_Text_Npc0, MSGBOX_NPC
	end

ReflectionMarsh_EventScript_Npc1::
	msgbox ReflectionMarsh_Text_Npc1, MSGBOX_NPC
	end

ReflectionMarsh_EventScript_Radar::
	lock
	faceplayer
	msgbox ReflectionMarsh_Text_Radar0
	random 3
	goto_if_eq VAR_RESULT, 0, ReflectionMarsh_EventScript_R1
	goto_if_eq VAR_RESULT, 1, ReflectionMarsh_EventScript_R2
	msgbox ReflectionMarsh_Text_Radar3
	release
	end

ReflectionMarsh_EventScript_R1::
	msgbox ReflectionMarsh_Text_Radar1
	release
	end

ReflectionMarsh_EventScript_R2::
	msgbox ReflectionMarsh_Text_Radar2
	release
	end

