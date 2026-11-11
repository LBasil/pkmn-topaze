import json,sys,re
off=int(open('/tmp/gx/rev.off').read()) if len(sys.argv)<2 else int(sys.argv[1])
L=[json.loads(l) for l in open('/tmp/gx/texts.jsonl')]
skip=re.compile(r"(utilise|gagne|passe au|veut se battre|envoie|est K\.O|^Que doit|^¥|^\W*$|^TYPE|^[0-9.]+x|× \d+|Vas-y|Reviens|^[A-ZÉÈ'♂♀ -]+[♂♀]$|capturé|AAAA|/ÓÔ|oublie|apprend|a battu|Touché|gagne)")
for d in L[off:]:
    t=d['text']
    if skip.search(t): continue
    print(d['map'][:22],'|',t[:200])
open('/tmp/gx/rev.off','w').write(str(len(L)))
