CeladonCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CeladonCity_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CeladonCity_OnResume
	.byte 0

CeladonCity_OnResume::
	call_if_set FLAG_SYS_SPECIAL_WILD_BATTLE, CeladonCity_EventScript_TryRemoveArticuno
	end

CeladonCity_EventScript_TryRemoveArticuno::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, EventScript_Return
	removeobject VAR_LAST_TALKED
	return

@ Topaze: ARTICUNO sleeps in the quartz-geode clearing (behind the cuttable tree) once the League is beaten
CeladonCity_EventScript_ShowArticuno::
	goto_if_unset FLAG_TOPAZE_POSTGAME, EventScript_Return
	clearflag FLAG_HIDE_ARTICUNO
	return

CeladonCity_EventScript_Articuno::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_ARTICUNO, 0
	waitse
	playmoncry SPECIES_ARTICUNO, CRY_MODE_ENCOUNTER
	message Text_Gyaoo
	waitmessage
	waitmoncry
	delay 10
	playbgm MUS_ENCOUNTER_GYM_LEADER, 0
	waitbuttonpress
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, CeladonCity_EventScript_DefeatedArticuno
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, CeladonCity_EventScript_RanFromArticuno
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, CeladonCity_EventScript_RanFromArticuno
	setflag FLAG_FOUGHT_ARTICUNO
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreen FADE_FROM_BLACK
	release
	end

CeladonCity_EventScript_DefeatedArticuno::
	setflag FLAG_FOUGHT_ARTICUNO
	goto EventScript_RemoveStaticMon
	end

CeladonCity_EventScript_RanFromArticuno::
	setvar VAR_0x8004, SPECIES_ARTICUNO
	goto EventScript_MonFlewAway
	end

CeladonCity_OnTransition::
	setflag FLAG_0x14C
	setflag FLAG_0x14D
	setflag FLAG_0x14E
	setflag FLAG_0x14F
	goto_if_set FLAG_FOUGHT_ARTICUNO, CeladonCity_Guards_Done
	goto_if_unset FLAG_TOPAZE_POSTGAME, CeladonCity_Guards_Done
	goto_if_defeated TRAINER_EXPERT_M, CeladonCity_Guards_Skip0
	clearflag FLAG_0x14C
CeladonCity_Guards_Skip0:
	goto_if_defeated TRAINER_EXPERT_F, CeladonCity_Guards_Skip1
	clearflag FLAG_0x14D
CeladonCity_Guards_Skip1:
	goto_if_defeated TRAINER_DRAGON_TAMER, CeladonCity_Guards_Skip2
	clearflag FLAG_0x14E
CeladonCity_Guards_Skip2:
	goto_if_defeated TRAINER_NINJA_BOY, CeladonCity_Guards_Skip3
	clearflag FLAG_0x14F
CeladonCity_Guards_Skip3:
CeladonCity_Guards_Done:
	setworldmapflag FLAG_WORLD_MAP_CELADON_CITY
	call_if_unset FLAG_FOUGHT_ARTICUNO, CeladonCity_EventScript_ShowArticuno
	goto_if_set FLAG_HIDE_CELADON_ROCKETS, CeladonCity_EventScript_WestPoliceLeave
	end

CeladonCity_EventScript_WestPoliceLeave::
	setflag FLAG_TEMP_11
	end

CeladonCity_EventScript_WestPolice::
	lock
	faceplayer
	msgbox CeladonCity_Text_WestBlocked
	release
	end

CeladonCity_EventScript_LittleGirl::
	msgbox CeladonCity_Text_GotMyKoffingInCinnabar, MSGBOX_NPC
	end

CeladonCity_EventScript_OldMan1::
	lock
	msgbox CeladonCity_Text_GymIsGreatFullOfWomen
	release
	end

CeladonCity_EventScript_Woman::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_POSTGAME, CeladonCity_EventScript_WomanPostgame
	msgbox CeladonCity_Text_GameCornerIsBadForCitysImage
	release
	end

CeladonCity_EventScript_WomanPostgame::
	msgbox CeladonCity_Text_WhySnowHere
	release
	end

CeladonCity_EventScript_OldMan2::
	msgbox CeladonCity_Text_BlewItAllAtSlots, MSGBOX_NPC
	end

CeladonCity_EventScript_SoftboiledTutor::
	goto EventScript_SoftboiledTutor
	end

CeladonCity_EventScript_FatMan::
	lock
	faceplayer
	msgbox CeladonCity_Text_MyTrustedPalPoliwrath
	closemessage
	applymovement LOCALID_CELADON_FAT_MAN, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

CeladonCity_EventScript_Poliwrath::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_POLIWRATH, CRY_MODE_NORMAL
	msgbox CeladonCity_Text_Poliwrath
	closemessage
	waitmoncry
	applymovement LOCALID_CELADON_POLIWRATH, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

CeladonCity_EventScript_RocketGrunt1::
	msgbox CeladonCity_Text_KeepOutOfTeamRocketsWay, MSGBOX_NPC
	end

CeladonCity_EventScript_RocketGrunt2::
	msgbox CeladonCity_Text_GetLostOrIllPunchYou, MSGBOX_NPC
	end

CeladonCity_EventScript_Boy::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_POSTGAME, CeladonCity_EventScript_BoyPostgame
	msgbox CeladonCity_Text_ScaldedTongueOnTea
	release
	end

CeladonCity_EventScript_BoyPostgame::
	msgbox CeladonCity_Text_GeodeClearing
	release
	end

CeladonCity_EventScript_SilphCoScientist::
	msgbox CeladonCity_Text_SomeoneStoleSilphScope, MSGBOX_NPC
	end

CeladonCity_EventScript_TrainerTips1::
	msgbox CeladonCity_Text_ExplainXAccuracyDireHit, MSGBOX_SIGN
	end

CeladonCity_EventScript_CitySign::
	msgbox CeladonCity_Text_CitySign, MSGBOX_SIGN
	end

CeladonCity_EventScript_GymSign::
	lockall
	famechecker FAMECHECKER_ERIKA, 0
	msgbox CeladonCity_Text_GymSign
	releaseall
	end

CeladonCity_EventScript_MansionSign::
	msgbox CeladonCity_Text_MansionSign, MSGBOX_SIGN
	end

CeladonCity_EventScript_DeptStoreSign::
	msgbox CeladonCity_Text_DeptStoreSign, MSGBOX_SIGN
	end

CeladonCity_EventScript_TrainerTips2::
	msgbox CeladonCity_Text_GuardSpecProtectsFromStatus, MSGBOX_SIGN
	end

CeladonCity_EventScript_PrizeExchangeSign::
	msgbox CeladonCity_Text_PrizeExchangeSign, MSGBOX_SIGN
	end

CeladonCity_EventScript_GameCornerSign::
	msgbox CeladonCity_Text_GameCornerSign, MSGBOX_SIGN
	end

@ Topaze, fin 2 « Le Refuge » : poste 7/16 (GWEN) — livraison d'objets, recompense : Lapras
CeladonCity_EventScript_Refuge::
	lock
	faceplayer
	goto_if_ne VAR_TOPAZE_ENDING, 2, CeladonCity_EventScript_RefugeIdle
	goto_if_gt VAR_REFUGE_STAGE, 6, CeladonCity_EventScript_RefugeDone
	goto_if_lt VAR_REFUGE_STAGE, 6, CeladonCity_EventScript_RefugeEarly
	checkitem ITEM_LEMONADE, 3
	goto_if_eq VAR_RESULT, TRUE, CeladonCity_EventScript_RefugeOffer
	msgbox CeladonCity_Text_RefAsk
	release
	end

CeladonCity_EventScript_RefugeOffer::
	msgbox CeladonCity_Text_RefOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CeladonCity_EventScript_RefugeRefuse
	removeitem ITEM_LEMONADE, 3
	goto CeladonCity_EventScript_RefugeReward
	end

CeladonCity_EventScript_RefugeRefuse::
	msgbox CeladonCity_Text_RefNo
	release
	end

CeladonCity_EventScript_RefugeReward::
	msgbox CeladonCity_Text_RefGives
	givemon SPECIES_LAPRAS, 0
	addvar VAR_REFUGE_STAGE, 1
	msgbox CeladonCity_Text_RefAfter
	release
	end

CeladonCity_EventScript_RefugeEarly::
	msgbox CeladonCity_Text_RefEarly
	release
	end

CeladonCity_EventScript_RefugeDone::
	msgbox CeladonCity_Text_RefDone
	release
	end

CeladonCity_EventScript_RefugeIdle::
	msgbox CeladonCity_Text_RefIdle
	release
	end

CeladonCity_Guard0::
	trainerbattle_single TRAINER_EXPERT_M, CeladonCity_Text_Guard0Intro, CeladonCity_Text_Guard0Defeat, CeladonCity_Guard0_Vanish
	msgbox CeladonCity_Text_Guard0Post, MSGBOX_AUTOCLOSE
	end

CeladonCity_Guard0_Vanish::
	msgbox CeladonCity_Text_Guard0Post, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_0x14C
	removeobject VAR_LAST_TALKED
	releaseall
	end

CeladonCity_Guard1::
	trainerbattle_single TRAINER_EXPERT_F, CeladonCity_Text_Guard1Intro, CeladonCity_Text_Guard1Defeat, CeladonCity_Guard1_Vanish
	msgbox CeladonCity_Text_Guard1Post, MSGBOX_AUTOCLOSE
	end

CeladonCity_Guard1_Vanish::
	msgbox CeladonCity_Text_Guard1Post, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_0x14D
	removeobject VAR_LAST_TALKED
	releaseall
	end

CeladonCity_Guard2::
	trainerbattle_single TRAINER_DRAGON_TAMER, CeladonCity_Text_Guard2Intro, CeladonCity_Text_Guard2Defeat, CeladonCity_Guard2_Vanish
	msgbox CeladonCity_Text_Guard2Post, MSGBOX_AUTOCLOSE
	end

CeladonCity_Guard2_Vanish::
	msgbox CeladonCity_Text_Guard2Post, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_0x14E
	removeobject VAR_LAST_TALKED
	releaseall
	end

CeladonCity_Guard3::
	trainerbattle_single TRAINER_NINJA_BOY, CeladonCity_Text_Guard3Intro, CeladonCity_Text_Guard3Defeat, CeladonCity_Guard3_Vanish
	msgbox CeladonCity_Text_Guard3Post, MSGBOX_AUTOCLOSE
	end

CeladonCity_Guard3_Vanish::
	msgbox CeladonCity_Text_Guard3Post, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_0x14F
	removeobject VAR_LAST_TALKED
	releaseall
	end

@ Topaze: quete (THE SPA REGULAR)
CeladonCity_EventScript_TQ::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_TQ_CELADONCITY, CeladonCity_EventScript_TQ_Done
	checkitem ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, CeladonCity_EventScript_TQ_Ask
	checkitemspace ITEM_MIRACLE_SEED, 1
	goto_if_eq VAR_RESULT, FALSE, CeladonCity_EventScript_TQ_NoRoom
	removeitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_TQ_CELADONCITY
	msgbox CeladonCity_Text_TQ_Ok
	giveitem ITEM_MIRACLE_SEED, 1
	release
	end

CeladonCity_EventScript_TQ_Ask::
	msgbox CeladonCity_Text_TQ_Ask
	release
	end

CeladonCity_EventScript_TQ_Done::
	msgbox CeladonCity_Text_TQ_Done
	release
	end

CeladonCity_EventScript_TQ_NoRoom::
	msgbox CeladonCity_Text_TQ_NoRoom
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
CeladonCity_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_TOWN_CELADONCITY, CeladonCity_EventScript_TopazeFind0_Done
	checkitemspace ITEM_ULTRA_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, CeladonCity_EventScript_TopazeFind0_Full
	giveitem ITEM_ULTRA_BALL, 1
	setflag FLAG_TOPAZE_HID_TOWN_CELADONCITY
	release
	end

CeladonCity_EventScript_TopazeFind0_Done::
	release
	end

CeladonCity_EventScript_TopazeFind0_Full::
	msgbox CeladonCity_Text_TopazeFindFull
	release
	end


CeladonCity_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"

@ Topaze: tableau d'avis (ou trouver les rares)
CeladonCity_EventScript_NoticeBoard::
	msgbox CeladonCity_Text_NoticeBoard, MSGBOX_SIGN
	end

CeladonCity_Text_NoticeBoard::
	.string "WANTED: DITTO: REFLECTION MARSH.\n"
	.string "SABLEYE: EAST RESERVE, ASHEN MINE.\p"
	.string "MAWILE: EAST RESERVE, ASHEN MINE.$"
