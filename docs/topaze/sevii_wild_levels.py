#!/usr/bin/env python3
"""Niveaux sauvages de Sevii : coherents avec les dresseurs (plancher de l'ile - 5, mini plancher - 18). Idempotent."""
import json,re
EV={}
for m in re.finditer(r'\[(SPECIES_\w+)\]\s*=\s*\{\{EVO_LEVEL,\s*(\d+),\s*(SPECIES_\w+)\}',open('src/data/pokemon/evolution.h').read()): EV[m.group(1)]=(int(m.group(2)),m.group(3))
NOEVO={'SPECIES_LEDYBA','SPECIES_MAGBY','SPECIES_WOOPER'}
def evolve(sp,l):
    if sp in NOEVO: return sp
    while sp in EV and l>=EV[sp][0]: sp=EV[sp][1]
    return sp
FLOOR=[('ONE_ISLAND',58),('MT_EMBER',60),('TWO_ISLAND',60),('THREE_ISLAND',61),('FOUR_ISLAND',62),('FIVE_ISLAND',64),('SIX_ISLAND',65),('SEVEN_ISLAND',66)]
SKIP=('ALTERING','MEMORIAL','TANOBY_RUINS','THREE_ISLAND_PORT','ONE_ISLAND_PORT','TREASURE_BEACH_DUMMY')
F='src/data/wild_encounters.json'; wj=json.load(open(F)); n=0
for g in wj['wild_encounter_groups']:
    for e in g['encounters']:
        if 'FireRed' not in e['base_label']: continue
        mp=e['map'][4:]
        if any(s in mp for s in SKIP): continue
        fl=next((v for k,v in FLOOR if mp.startswith(k)),None)
        if not fl: continue
        for k in ('land_mons','water_mons','rock_smash_mons'):
            if k not in e: continue
            mons=e[k]['mons']; mx=max(m['max_level'] for m in mons); d=max(0,(fl-5)-mx)
            for m in mons:
                lo=max(m['min_level']+d,fl-18); hi=max(m['max_level']+d,lo)
                if (lo,hi)!=(m['min_level'],m['max_level']): n+=1
                m['min_level'],m['max_level']=lo,hi; m['species']=evolve(m['species'],hi)
json.dump(wj,open(F,'w'),indent=2); print(n,'creneaux')
