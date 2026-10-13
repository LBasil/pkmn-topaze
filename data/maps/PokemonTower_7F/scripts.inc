PokemonTower_7F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PokemonTower_7F_OnTransition
	.byte 0

PokemonTower_7F_OnTransition::
	setflag FLAG_TEMP_5
	end

PokemonTower_7F_EventScript_MrFuji::
	lock
	faceplayer
	msgbox PokemonTower_7F_Text_MrFujiAfter
	release
	end

PokemonTower_7F_EventScript_Stone::
	msgbox PokemonTower_7F_Text_StoneGlows, MSGBOX_SIGN
	end

PokemonTower_7F_EventScript_Admin::
	end

PokemonTower_7F_EventScript_AdminScene::
	lockall
	goto_if_set FLAG_RESCUED_MR_FUJI, PokemonTower_7F_EventScript_SceneDone
	textcolor NPC_TEXT_COLOR_MALE
	msgbox PokemonTower_7F_Text_MrFujiCrypt
	closemessage
	playse SE_EXIT
	addobject LOCALID_POKEMON_TOWER_ADMIN
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
	applymovement LOCALID_POKEMON_TOWER_ADMIN, PokemonTower_7F_Movement_AdminApproach
	waitmovement 0
	msgbox PokemonTower_7F_Text_AdminThanks
	closemessage
	playse SE_M_SELF_DESTRUCT
	fadescreen FADE_TO_WHITE
	delay 30
	fadescreen FADE_FROM_WHITE
	msgbox PokemonTower_7F_Text_AdminBeatsYou
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_POKEMON_TOWER_STONE
	removeobject LOCALID_POKEMON_TOWER_ADMIN
	delay 30
	fadescreen FADE_FROM_BLACK
	msgbox PokemonTower_7F_Text_MrFujiAdmin
	special HealPlayerParty
	msgbox PokemonTower_7F_Text_FujiHeals
	setflag FLAG_RESCUED_MR_FUJI
	setflag FLAG_HIDE_TOWER_ROCKET_1
	releaseall
	end

PokemonTower_7F_EventScript_SceneDone::
	releaseall
	end

PokemonTower_7F_Movement_AdminApproach::
	walk_up
	walk_up
	walk_up
	walk_up
	step_end
