import subprocess,sys,os
from PIL import Image
ROM='/home/claude/pkmn-topaze/pokefirered.gba'
def run(lines,show=True):
    open('s.txt','w').write('\n'.join(lines)+'\n')
    r=subprocess.run(['./h',ROM,'s.txt'],capture_output=True,text=True)
    out=[l for l in r.stdout.splitlines() if l.startswith('R:')]
    if show:
        for l in out: print(l)
    for f in os.listdir('.'):
        if f.endswith('.ppm'):
            d=open(f,'rb').read().split(b'\n',3)
            Image.frombytes('RGB',(240,160),d[3]).resize((480,320),Image.NEAREST).save(f[:-4]+'.png'); os.remove(f)
    return out
