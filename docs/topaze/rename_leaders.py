# Remplace les noms des champions d'origine par ceux de Topaze dans les textes (par emplacement de dresseur).
import re,glob,subprocess
M=[('BROCK','KAY'),('MISTY','SYLVESTRE'),('LT. SURGE','HERA'),('SURGE','HERA'),('ERIKA','GRIM'),
   ('KOGA','ACHLYS'),('SABRINA','NOX'),('BLAINE','EDDIE')]
files=glob.glob('data/maps/**/text.inc',recursive=True)+glob.glob('data/text/*.inc')+glob.glob('data/scripts/*.inc')
GIO=['data/maps/ViridianCity_Gym/text.inc','data/maps/ViridianCity/text.inc']
ch=0
for f in files:
    s=open(f).read(); o=s
    for a,b in M:
        s=re.sub(r'(?<![A-Za-z_])'+re.escape(a)+r"(?![A-Za-z_])",b,s) if False else re.sub(r'\b'+re.escape(a)+r'\b',b,s) if not re.search(r'LEADER_|FAMECHECKER|TRAINER_',a) else s
    if f in GIO: s=re.sub(r'\bGIOVANNI\b','HEPHA',s)
    if s!=o:
        # ne touche pas aux identifiants (lignes sans .string)
        out=[]
        for lo,ln in zip(o.split('\n'),s.split('\n')):
            out.append(ln if '.string' in lo else lo)
        s='\n'.join(out)
        if s!=o: open(f,'w').write(s); ch+=1
print(ch,'fichiers')
