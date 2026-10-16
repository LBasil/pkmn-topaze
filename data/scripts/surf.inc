EventScript_UseSurf::
	goto_if_questlog EventScript_UseSurfEnd
	setvar VAR_RESULT, 0 @ Topaze: pas besoin de connaître la CS (Pokémon de tête)
	bufferpartymonnick STR_VAR_1, VAR_RESULT
	setfieldeffectargument 0, VAR_RESULT
	lockall
	goto_if_set FLAG_TEMP_10, EventScript_UseSurfLava @ Topaze: lave du volcan Ecume (FLAG_TEMP_10 posé par B3F/B4F)
	msgbox Text_WantToSurf, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_UseSurfRelease
	msgbox Text_UsedSurf
	dofieldeffect FLDEFF_USE_SURF
EventScript_UseSurfLava::
	msgbox Text_WantToSurfLava, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_UseSurfRelease
	msgbox Text_UsedSurfLava
	dofieldeffect FLDEFF_USE_SURF
	goto EventScript_UseSurfRelease
EventScript_UseSurfRelease:
	releaseall
EventScript_UseSurfEnd:
	end

EventScript_CurrentTooFast::
	lockall
	msgbox Text_CurrentTooFast
	releaseall
	end
