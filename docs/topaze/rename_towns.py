"""Renomme les villes de Kanto selon le plan Topaze (idempotent). Usage : python3 docs/topaze/rename_towns.py (depuis la racine du dépôt)"""
import re,glob
full={'VIRIDIAN CITY':'OPANIHRUM','PEWTER CITY':'PYROPIA','CERULEAN CITY':'TOURMALIA','VERMILION CITY':'APATIA','CELADON CITY':'BOURG QUARTZ','FUCHSIA CITY':'AMETHIOLITE','SAFFRON CITY':'HEMATOWN','CINNABAR ISLAND':'CHRONDROLIA','LAVENDER TOWN':'SPINELLIA'}
bare={'VIRIDIAN':'OPANIHRUM','PEWTER':'PYROPIA','CERULEAN':'TOURMALIA','VERMILION':'APATIA','CELADON':'BOURG QUARTZ','FUCHSIA':'AMETHIOLITE','SAFFRON':'HEMATOWN','CINNABAR':'CHRONDROLIA','LAVENDER':'SPINELLIA'}
files=[f for pat in ('data/**/*.inc','data/**/*.json','src/data/**/*.h','src/data/**/*.json','src/strings.c') for f in glob.glob(pat,recursive=True)]
skip=('region_map_entry_strings.h',)
n=0
for f in files:
    if f.endswith(skip): continue
    try: s=open(f).read()
    except: continue
    o=s
    for table in (full,bare):
        for k,v in table.items():
            s=re.sub(r'(?<![A-Za-z_])'+k+r'(?![A-Za-z_])',v,s)
    if s!=o: open(f,'w').write(s); n+=1
print('fichiers modifiés',n)
