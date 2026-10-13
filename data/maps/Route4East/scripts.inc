Route4East_MapScripts::
	.byte 0

Route4East_EventScript_WestSign::
	msgbox Route4East_Text_WestSign, MSGBOX_SIGN
	end

Route4East_EventScript_EastSign::
	msgbox Route4East_Text_EastSign, MSGBOX_SIGN
	end

@ ---- TRAINERS (route4e_trainers.py)

Route4East_EventScript_Marco::
	trainerbattle_single TRAINER_BUG_CATCHER_3, Route4East_Text_MarcoIntro, Route4East_Text_MarcoDefeat
	msgbox Route4East_Text_MarcoPostBattle, MSGBOX_AUTOCLOSE
	end

Route4East_EventScript_Tessa::
	trainerbattle_single TRAINER_PICNICKER_HANNAH, Route4East_Text_TessaIntro, Route4East_Text_TessaDefeat
	msgbox Route4East_Text_TessaPostBattle, MSGBOX_AUTOCLOSE
	end

Route4East_EventScript_Leo::
	trainerbattle_single TRAINER_CAMPER_2, Route4East_Text_LeoIntro, Route4East_Text_LeoDefeat
	msgbox Route4East_Text_LeoPostBattle, MSGBOX_AUTOCLOSE
	end

Route4East_EventScript_Nina::
	trainerbattle_single TRAINER_LASS_2, Route4East_Text_NinaIntro, Route4East_Text_NinaDefeat
	msgbox Route4East_Text_NinaPostBattle, MSGBOX_AUTOCLOSE
	end

Route4East_EventScript_Rio::
	trainerbattle_single TRAINER_BUG_CATCHER_4, Route4East_Text_RioIntro, Route4East_Text_RioDefeat
	msgbox Route4East_Text_RioPostBattle, MSGBOX_AUTOCLOSE
	end
