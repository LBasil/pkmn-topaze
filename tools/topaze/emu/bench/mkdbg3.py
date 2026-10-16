#!/usr/bin/env python3
# Construit /tmp/gx/dbg3.gba : debug.patch + équipe forte + presets flags/vars + mode dieu ; restaure les sources.
import subprocess, re, os, shutil
os.chdir('/home/claude/pkmn-topaze')
sh = lambda c: subprocess.run(c, shell=True, check=True, capture_output=True, text=True)
sh('git checkout src/new_game.c src/trainer_see.c src/wild_encounter.c src/battle_script_commands.c src/battle_main.c src/battle_setup.c')
sh('git apply tools/topaze/emu/debug.patch')
p = 'src/new_game.c'; s = open(p).read()
marker = "    if (gTopazeDbg[0]) SetWarpDestination"
add = '''    if (gTopazeDbg[0] && gTopazeDbg[7] == 9)
    {
        u8 i;
        ScriptGiveMon(SPECIES_MEWTWO, 90, ITEM_NONE, 0, 0, 0);
        SetMonMoveSlot(&gPlayerParty[0], MOVE_PSYCHIC, 0);
        SetMonMoveSlot(&gPlayerParty[0], MOVE_RECOVER, 1);
        ScriptGiveMon(SPECIES_SNORLAX, 80, ITEM_NONE, 0, 0, 0);
        ScriptGiveMon(SPECIES_DRAGONITE, 80, ITEM_NONE, 0, 0, 0);
        ScriptGiveMon(SPECIES_GENGAR, 80, ITEM_NONE, 0, 0, 0);
        ScriptGiveMon(SPECIES_ALAKAZAM, 80, ITEM_NONE, 0, 0, 0);
        ScriptGiveMon(SPECIES_BLASTOISE, 80, ITEM_NONE, 0, 0, 0);
        FlagSet(FLAG_SYS_POKEMON_GET);
        FlagSet(FLAG_SYS_POKEDEX_GET);
        for (i = 0; i < 24; i++)
            if (gTopazeFlags[i]) FlagSet(gTopazeFlags[i]);
        for (i = 0; i < 8; i++)
            if (gTopazeVars[i * 2]) VarSet(gTopazeVars[i * 2], gTopazeVars[i * 2 + 1]);
    }
'''
assert marker in s
s = s.replace(marker, add + marker, 1)
s = s.replace('u8 gTopazeDbg[8];', 'u8 gTopazeDbg[8];\nu16 gTopazeFlags[24];\nu16 gTopazeVars[16];\nu8 gTopazeGod;', 1)
s = s.replace('#include "script_pokemon_util.h"', '#include "script_pokemon_util.h"\n#include "pokemon.h"\n#include "constants/moves.h"', 1)
open(p, 'w').write(s)
s2 = open('src/battle_script_commands.c').read()
old2 = 'static void Cmd_ppreduce(void)\n{\n    s32 ppToDeduct = 1;\n'
assert old2 in s2
s2 = s2.replace(old2, 'extern u8 gTopazeGod;\n' + old2 + '    if (gTopazeGod && GetBattlerSide(gBattlerAttacker) == B_SIDE_PLAYER) { gBattlescriptCurrInstr++; return; }\n', 1)
open('src/battle_script_commands.c','w').write(s2)
p = 'src/battle_script_commands.c'; s = open(p).read()
old_tc = 'static void Cmd_typecalc(void)\n{\n    s32 i = 0;\n    u8 moveType;\n\n'
assert old_tc in s
s = s.replace(old_tc, 'extern u8 gTopazeGod;\n' + old_tc + '    if (gTopazeGod && GetBattlerSide(gBattlerAttacker) == B_SIDE_PLAYER) { gBattlescriptCurrInstr++; return; }\n', 1)
old = 'static void Cmd_adjustnormaldamage(void)\n{\n    u8 holdEffect, param;\n\n    ApplyRandomDmgMultiplier();\n'
assert old in s
s = s.replace(old, old + '    if (gTopazeGod) { if (GetBattlerSide(gBattlerAttacker) == B_SIDE_PLAYER) { if (gBattleMoveDamage > 0) gBattleMoveDamage = 9999; } else gBattleMoveDamage = 1; }\n', 1)
assert 'gTopazeGod && GetBattlerSide' in s
open(p, 'w').write(s)
# mode dieu : les attaques de STATUT du joueur sont remplacees par METEORES (touche toujours, tue en un coup) ; sinon un partenaire dont
# la 1re attaque est un statut (ex. Vampigraine) ne finit jamais un combat pilote par A.
p = 'src/battle_main.c'; s = open(p).read()
old = '    gBattlescriptCurrInstr = gBattleScriptsForMoveEffects[gBattleMoves[gCurrentMove].effect];\n    gCurrentActionFuncId = B_ACTION_EXEC_SCRIPT;\n}\n\nstatic void HandleAction_Switch(void)'
assert old in s
new = '    if (gTopazeGod && GetBattlerSide(gBattlerAttacker) == B_SIDE_PLAYER && gBattleMoves[gCurrentMove].power == 0 && gCurrentMove != MOVE_NONE)\n    {\n        gCurrentMove = MOVE_SWIFT;\n        gBattlerTarget = GetBattlerAtPosition(B_POSITION_OPPONENT_LEFT);\n    }\n'
s = s.replace(old, new + old, 1)
s = s.replace('#include "constants/moves.h"', '#include "constants/moves.h"\nextern u8 gTopazeGod;', 1)
open(p, 'w').write(s)

# declencheur de combat de dresseur (banc d'equilibrage) : gTopazeBattleReq = id du dresseur ; lance un combat simple/double comme un vrai dresseur
p = 'src/battle_setup.c'; s = open(p).read()
anchor = 'static void CB2_EndTrainerBattle(void);\n'
assert anchor in s
s = s.replace(anchor, anchor + 'u16 gTopazeBattleReq;\nstatic const u8 sTopazeDbgScript[] = {0x69, 0x5d, 0x6b, 0x02};\nvoid TopazeDbgBattle(void)\n{\n    gTrainerBattleOpponent_A = gTopazeBattleReq;\n    gTopazeBattleReq = 0;\n    sTrainerBattleMode = 0;\n    ScriptContext_SetupScript(sTopazeDbgScript);\n}\n', 1)
# sTrainerBattleMode / gTrainerBattleOpponent_A sont declares apres : on deplace la definition de TopazeDbgBattle apres leur declaration
s = s.replace('u16 gTopazeBattleReq;', 'u16 gTopazeBattleReq;\nvoid TopazeDbgBattle(void);', 1)
i = s.index('void TopazeDbgBattle(void)\n{'); j = s.index('}\n', i) + 2; fn = s[i:j]; s = s[:i] + s[j:]
k = s.index('void StartTrainerBattle(void)'); s = s[:k] + fn + '\n' + s[k:]
open(p, 'w').write(s)
p = 'src/trainer_see.c'; s = open(p).read()
old = 'bool8 CheckForTrainersWantingBattle(void) { if (gTopazeDbg[5]) return FALSE;'
assert old in s
s = s.replace(old, 'extern u16 gTopazeBattleReq;\nvoid TopazeDbgBattle(void);\nbool8 CheckForTrainersWantingBattle(void) { if (gTopazeBattleReq) { TopazeDbgBattle(); return TRUE; } if (gTopazeDbg[5]) return FALSE;', 1)
open(p, 'w').write(s)
r = subprocess.run('make -j8 firered 2>&1 | tail -4', shell=True, capture_output=True, text=True); print(r.stdout)
assert 'Error' not in r.stdout, 'BUILD FAIL'
shutil.copy('pokefirered.gba', '/tmp/gx/dbg3.gba'); shutil.copy('pokefirered.map', '/tmp/gx/dbg3.map'); shutil.copy('pokefirered.elf', '/tmp/gx/dbg3.elf')
sh('git checkout src/new_game.c src/trainer_see.c src/wild_encounter.c src/battle_script_commands.c src/battle_main.c src/battle_setup.c')
print(sh('git status --short').stdout)
m = open('/tmp/gx/dbg3.map').read()
for n in ('gTopazeVars', 'gTopazeFlags', 'gTopazeDbg', 'gTopazeGod', 'gTopazeBattleReq'):
    print(n, re.search(r'0x([0-9a-f]{8})\s+' + n + r'\b', m).group(1))
