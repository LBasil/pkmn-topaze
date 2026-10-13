VictoryRoadLair_2F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, VictoryRoadLair_2F_OnTransition
	.byte 0

VictoryRoadLair_2F_OnTransition::
	goto_if_unset FLAG_VR_BOSS_DONE, VictoryRoadLair_2F_EventScript_StonesStay
	setflag FLAG_TEMP_1
	setflag FLAG_TEMP_2
	setflag FLAG_TEMP_3
	setflag FLAG_TEMP_4
	setflag FLAG_TEMP_5
	setflag FLAG_TEMP_6
	setflag FLAG_TEMP_7
	end

VictoryRoadLair_2F_EventScript_StonesStay::
	end

VictoryRoadLair_2F_EventScript_Selene::
	trainerbattle_single TRAINER_RS_AROMA_LADY, VictoryRoadLair_2F_Text_SeleneIntro, VictoryRoadLair_2F_Text_SeleneDefeat
	msgbox VictoryRoadLair_2F_Text_SelenePost, MSGBOX_AUTOCLOSE
	end

VictoryRoadLair_2F_EventScript_StoneGrenat::
	msgbox VictoryRoadLair_2F_Text_StoneGrenat, MSGBOX_SIGN
	end

VictoryRoadLair_2F_EventScript_StonePyrope::
	msgbox VictoryRoadLair_2F_Text_StonePyrope, MSGBOX_SIGN
	end

VictoryRoadLair_2F_EventScript_StoneTourmaline::
	msgbox VictoryRoadLair_2F_Text_StoneTourmaline, MSGBOX_SIGN
	end

VictoryRoadLair_2F_EventScript_PedestalApatite::
	msgbox VictoryRoadLair_2F_Text_PedestalApatite, MSGBOX_SIGN
	end

VictoryRoadLair_2F_EventScript_StoneSpinelle::
	msgbox VictoryRoadLair_2F_Text_StoneSpinelle, MSGBOX_SIGN
	end

VictoryRoadLair_2F_EventScript_PedestalTopaz::
	msgbox VictoryRoadLair_2F_Text_PedestalTopaz, MSGBOX_SIGN
	end

VictoryRoadLair_2F_EventScript_StoneQuartz::
	msgbox VictoryRoadLair_2F_Text_StoneQuartz, MSGBOX_SIGN
	end

VictoryRoadLair_2F_EventScript_StoneAmethiolite::
	msgbox VictoryRoadLair_2F_Text_StoneAmethiolite, MSGBOX_SIGN
	end

VictoryRoadLair_2F_EventScript_StoneHematite::
	msgbox VictoryRoadLair_2F_Text_StoneHematite, MSGBOX_SIGN
	end

VictoryRoadLair_2F_EventScript_PedestalOpal::
	msgbox VictoryRoadLair_2F_Text_PedestalOpal, MSGBOX_SIGN
	end
