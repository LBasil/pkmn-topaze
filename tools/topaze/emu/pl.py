from play import run
import os
S='/tmp/claude-0/-home-claude-pkmn-topaze/4707c200-259e-5dc8-ac11-6c931ed74d2a/scratchpad/emu/'
def walk(d,n): return ['key %s %d'%(d,16*n-2),'run 4']
def pos(): return 'readp 03005008 0 6'
def fromstate(name,L,**k): return run(['run 2','ls '+S+name+'.ss','run 2']+L,**k)
