EventScript_RepelWoreOff::
	lockall
	msgbox Text_RepelWoreOff, MSGBOX_DEFAULT
	specialvar VAR_RESULT, TopazeRepelNext
	goto_if_eq VAR_RESULT, ITEM_NONE, EventScript_RepelWoreOff_End
	msgbox Text_RepelUseAnother, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_RepelWoreOff_End
	special TopazeRepelUse
	msgbox Text_RepelUsedAnother, MSGBOX_DEFAULT
EventScript_RepelWoreOff_End::
	releaseall
	end

Text_RepelWoreOff::
	.string "REPEL's effect wore off…$"

Text_RepelUseAnother::
	.string "Use another {STR_VAR_1}?$"

Text_RepelUsedAnother::
	.string "{PLAYER} used the {STR_VAR_1}.$"
