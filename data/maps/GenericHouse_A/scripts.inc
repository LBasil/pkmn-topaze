GenericHouse_A_MapScripts::
	.byte 0

GenericHouse_A_EventScript_Resident::
	lock
	faceplayer
	random 6
	switch VAR_RESULT
	case 0, GenericHouse_A_EventScript_Adult0
	case 1, GenericHouse_A_EventScript_Adult1
	case 2, GenericHouse_A_EventScript_Adult2
	case 3, GenericHouse_A_EventScript_Adult3
	case 4, GenericHouse_A_EventScript_Adult4
	case 5, GenericHouse_A_EventScript_Adult5
	end

GenericHouse_A_EventScript_Adult0::
	msgbox GenericHouse_A_Text_Adult0
	release
	end

GenericHouse_A_EventScript_Adult1::
	msgbox GenericHouse_A_Text_Adult1
	release
	end

GenericHouse_A_EventScript_Adult2::
	msgbox GenericHouse_A_Text_Adult2
	release
	end

GenericHouse_A_EventScript_Adult3::
	msgbox GenericHouse_A_Text_Adult3
	release
	end

GenericHouse_A_EventScript_Adult4::
	msgbox GenericHouse_A_Text_Adult4
	release
	end

GenericHouse_A_EventScript_Adult5::
	msgbox GenericHouse_A_Text_Adult5
	release
	end

GenericHouse_A_EventScript_Child::
	lock
	faceplayer
	random 6
	switch VAR_RESULT
	case 0, GenericHouse_A_EventScript_Kid0
	case 1, GenericHouse_A_EventScript_Kid1
	case 2, GenericHouse_A_EventScript_Kid2
	case 3, GenericHouse_A_EventScript_Kid3
	case 4, GenericHouse_A_EventScript_Kid4
	case 5, GenericHouse_A_EventScript_Kid5
	end

GenericHouse_A_EventScript_Kid0::
	msgbox GenericHouse_A_Text_Kid0
	release
	end

GenericHouse_A_EventScript_Kid1::
	msgbox GenericHouse_A_Text_Kid1
	release
	end

GenericHouse_A_EventScript_Kid2::
	msgbox GenericHouse_A_Text_Kid2
	release
	end

GenericHouse_A_EventScript_Kid3::
	msgbox GenericHouse_A_Text_Kid3
	release
	end

GenericHouse_A_EventScript_Kid4::
	msgbox GenericHouse_A_Text_Kid4
	release
	end

GenericHouse_A_EventScript_Kid5::
	msgbox GenericHouse_A_Text_Kid5
	release
	end

