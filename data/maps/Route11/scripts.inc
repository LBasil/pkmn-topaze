Route11_MapScripts::
	.byte 0

Route11_EventScript_DiglettsCaveSign::
	msgbox Route11_Text_DiglettsCave, MSGBOX_SIGN
	end

@ Topaze: indice du temps deregle
Route11_EventScript_TimeHint::
	setflag FLAG_TOPAZE_CLOCK_2
	msgbox Route11_Text_TimeHint, MSGBOX_SIGN
	end
