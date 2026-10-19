import subprocess, os
_ELF = os.environ.get('TZ_ELF', '/tmp/gx/dbg2.elf')
_T = {}
for l in subprocess.run(['arm-none-eabi-nm', _ELF], capture_output=True, text=True).stdout.splitlines():
    a = l.split()
    if len(a) == 3: _T[a[2]] = int(a[0], 16)
def S(n, off=0): return _T[n] + off
