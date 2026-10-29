ViridianCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, ViridianCity_OnTransition
	.byte 0

ViridianCity_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_VIRIDIAN_CITY
	@ Topaze: no road block and no automatic tutorial; the old man only offers a demo when spoken to
	setvar VAR_MAP_SCENE_VIRIDIAN_CITY_OLD_MAN, 2
	call ViridianCity_EventScript_SetOldManNormal
	call_if_eq VAR_MAP_SCENE_VIRIDIAN_CITY_GYM_DOOR, 0, ViridianCity_EventScript_TryUnlockGym
	end

ViridianCity_EventScript_SetOldManNormal::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_OLD_MAN_1
	return

ViridianCity_EventScript_TryUnlockGym::
	goto_if_unset FLAG_BADGE01_GET, EventScript_Return
	goto_if_unset FLAG_BADGE02_GET, EventScript_Return
	goto_if_unset FLAG_BADGE03_GET, EventScript_Return
	goto_if_unset FLAG_BADGE04_GET, EventScript_Return
	goto_if_unset FLAG_BADGE05_GET, EventScript_Return
	goto_if_unset FLAG_BADGE06_GET, EventScript_Return
	goto_if_unset FLAG_BADGE07_GET, EventScript_Return
	setvar VAR_MAP_SCENE_VIRIDIAN_CITY_GYM_DOOR, 1
	return

ViridianCity_EventScript_GymDoorLocked::
	lockall
	textcolor NPC_TEXT_COLOR_NEUTRAL
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	delay 20
	msgbox ViridianCity_Text_GymDoorsAreLocked
	closemessage
	applymovement LOCALID_PLAYER, ViridianCity_Movement_JumpDownLedge
	waitmovement 0
	releaseall
	end

ViridianCity_Movement_JumpDownLedge::
	jump_2_down
	step_end

ViridianCity_EventScript_CitySign::
	msgbox ViridianCity_Text_CitySign, MSGBOX_SIGN
	end

ViridianCity_EventScript_TrainerTips1::
	msgbox ViridianCity_Text_CatchMonsForEasierBattles, MSGBOX_SIGN
	end

ViridianCity_EventScript_TrainerTips2::
	msgbox ViridianCity_Text_MovesLimitedByPP, MSGBOX_SIGN
	end

ViridianCity_EventScript_GymSign::
	msgbox ViridianCity_Text_GymSign, MSGBOX_SIGN
	end

ViridianCity_EventScript_GymDoor::
	msgbox ViridianCity_Text_GymDoorsAreLocked, MSGBOX_SIGN
	end

ViridianCity_EventScript_Boy::
	msgbox ViridianCity_Text_CanCarryMonsAnywhere, MSGBOX_NPC
	end

@ Other old man, not the tutorial old man
ViridianCity_EventScript_OldMan::
	lock
	faceplayer
	goto_if_eq VAR_MAP_SCENE_VIRIDIAN_CITY_GYM_DOOR, 1, ViridianCity_EventScript_OldManGymLeaderReturned
	msgbox ViridianCity_Text_GymClosedWonderWhoLeaderIs
	closemessage
	applymovement LOCALID_VIRIDIAN_OLD_MAN, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

ViridianCity_EventScript_OldManGymLeaderReturned::
	msgbox ViridianCity_Text_ViridiansGymLeaderReturned
	release
	end

ViridianCity_EventScript_TutorialOldMan::
	lock
	faceplayer
	goto_if_set FLAG_BADGE01_GET, ViridianCity_EventScript_AskIfTeachyTVHelpful
	goto_if_set FLAG_VIRIDIAN_TUTORIAL_DONE, ViridianCity_EventScript_TutorialCompleted
	msgbox ViridianCity_Text_OfferCatchDemo, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, ViridianCity_EventScript_TutorialStart
	msgbox ViridianCity_Text_DemoAnytime
	release
	end

ViridianCity_EventScript_AskIfTeachyTVHelpful::
	msgbox ViridianCity_Text_HowsTeachyTVHelping, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ViridianCity_EventScript_TeachyTVNotHelpful
	msgbox ViridianCity_Text_MyGrandsonOnTheShow
	release
	end

ViridianCity_EventScript_TeachyTVNotHelpful::
	msgbox ViridianCity_Text_TooBusyForTeachyTV
	release
	end

ViridianCity_EventScript_TutorialCompleted::
	msgbox ViridianCity_Text_WeakenMonsFirstToCatch
	release
	end

ViridianCity_EventScript_TutorialStart::
	call ViridianCity_EventScript_DoTutorialBattle
	release
	end

@ Unused
ViridianCity_EventScript_WatchToLearnBasics::
	msgbox ViridianCity_Text_WatchThatToLearnBasics
	release
	end

@ Unused. Starts battle after the post battle text, which is odd.
ViridianCity_EventScript_TutorialUnused::
	msgbox ViridianCity_Text_ThatWasEducationalTakeThis
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	special StartOldManTutorialBattle
	waitstate
	release
	end

ViridianCity_EventScript_Youngster::
	lock
	faceplayer
	msgbox ViridianCity_Text_WantToKnowAboutCaterpillarMons, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, ViridianCity_EventScript_YoungsterExplainCaterpillars
	goto_if_eq VAR_RESULT, NO, ViridianCity_EventScript_YoungsterDeclineExplanation
	end

ViridianCity_EventScript_YoungsterExplainCaterpillars::
	msgbox ViridianCity_Text_ExplainCaterpieWeedle
	release
	end

ViridianCity_EventScript_YoungsterDeclineExplanation::
	msgbox ViridianCity_Text_OhOkayThen
	release
	end

ViridianCity_EventScript_Woman::
	lock
	faceplayer
	msgbox ViridianCity_Text_GoShoppingInPewterOccasionally
	release
	end

ViridianCity_EventScript_DreamEaterTutor::
	goto EventScript_DreamEaterTutor
	end

ViridianCity_Movement_WalkDown::
	walk_down
	step_end

ViridianCity_EventScript_DoTutorialBattle::
	msgbox ViridianCity_Text_ShowYouHowToCatchMons
	closemessage
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	special StartOldManTutorialBattle
	waitstate
	lock
	faceplayer
	msgbox ViridianCity_Text_ThatWasEducationalTakeThis
	setflag FLAG_VIRIDIAN_TUTORIAL_DONE
	giveitem ITEM_TEACHY_TV
	msgbox ViridianCity_Text_WatchThatToLearnBasics
	return

@ Topaze, fin 2 « Le Refuge » : poste 2/16 (BRUN) — duel contre 2 chasseurs, recompense : Larvitar
ViridianCity_EventScript_Refuge::
	lock
	faceplayer
	goto_if_ne VAR_TOPAZE_ENDING, 2, ViridianCity_EventScript_RefugeIdle
	goto_if_gt VAR_REFUGE_STAGE, 1, ViridianCity_EventScript_RefugeDone
	goto_if_lt VAR_REFUGE_STAGE, 1, ViridianCity_EventScript_RefugeEarly
	msgbox ViridianCity_Text_RefAsk
	setvar VAR_TOPAZE_BOOST, 46
	trainerbattle_no_intro TRAINER_GENTLEMAN_THOMAS, ViridianCity_Text_RefHunter1
	setvar VAR_TOPAZE_BOOST, 36
	trainerbattle_no_intro TRAINER_JUGGLER_DALTON, ViridianCity_Text_RefHunter2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	goto ViridianCity_EventScript_RefugeReward
	end

ViridianCity_EventScript_RefugeReward::
	msgbox ViridianCity_Text_RefGives
	givemon SPECIES_LARVITAR, 0
	addvar VAR_REFUGE_STAGE, 1
	msgbox ViridianCity_Text_RefAfter
	release
	end

ViridianCity_EventScript_RefugeEarly::
	msgbox ViridianCity_Text_RefEarly
	release
	end

ViridianCity_EventScript_RefugeDone::
	msgbox ViridianCity_Text_RefDone
	release
	end

ViridianCity_EventScript_RefugeIdle::
	msgbox ViridianCity_Text_RefIdle
	release
	end

@ Topaze: quete (THE GILDED GIFT)
ViridianCity_EventScript_TQ::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_TQ_VIRIDIANCITY, ViridianCity_EventScript_TQ_Done
	checkitem ITEM_NUGGET, 1
	goto_if_eq VAR_RESULT, FALSE, ViridianCity_EventScript_TQ_Ask
	checkitemspace ITEM_SILK_SCARF, 1
	goto_if_eq VAR_RESULT, FALSE, ViridianCity_EventScript_TQ_NoRoom
	removeitem ITEM_NUGGET, 1
	setflag FLAG_TOPAZE_TQ_VIRIDIANCITY
	msgbox ViridianCity_Text_TQ_Ok
	giveitem ITEM_SILK_SCARF, 1
	release
	end

ViridianCity_EventScript_TQ_Ask::
	msgbox ViridianCity_Text_TQ_Ask
	release
	end

ViridianCity_EventScript_TQ_Done::
	msgbox ViridianCity_Text_TQ_Done
	release
	end

ViridianCity_EventScript_TQ_NoRoom::
	msgbox ViridianCity_Text_TQ_NoRoom
	release
	end
