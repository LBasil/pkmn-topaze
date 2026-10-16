#!/usr/bin/env python3
"""Remet en forme (36 car/ligne) les textes signales 'ligne N car' par textlint. Usage : textlint.py | reflow.py"""
import re, sys, subprocess
W = 36
out = subprocess.run(['python3', 'tools/topaze/lint/textlint.py'], capture_output=True, text=True).stdout
targets = {}
for l in out.splitlines():
    m = re.match(r'avert\s+(\S+?):\d+ (\S+?):: : ligne \d+ car', l)
    if m: targets.setdefault(m.group(1), set()).add(m.group(2))
def wrap(words):
    lines = []; cur = ''
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= W: cur = (cur + ' ' + w) if cur else w
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines
for f, labs in targets.items():
    s = open(f).read()
    for lab in labs:
        m = re.search(r'(^' + re.escape(lab) + r'::\n)((?:[ \t]+\.string "[^\n]*\n)+)', s, re.M)
        raw = ''.join(re.findall(r'\.string "(.*)"\n', m.group(2)))
        raw = raw[:-1] if raw.endswith('$') else raw
        paras = re.split(r'\\p', raw); res = []
        for p in paras:
            p = re.sub(r'\\[nl]', ' ', p); words = p.split()
            ls = wrap(words); txt = ''
            for i, l in enumerate(ls):
                txt += l + ('' if i == len(ls) - 1 else ('\\n' if i % 2 == 0 else '\\l'))
            res.append(txt)
        flat = '\\p'.join(res) + '$'
        # decoupe en .string de <= 1 ligne logique : on coupe apres chaque \n, \l, \p
        parts = re.split(r'(?<=\\n)|(?<=\\l)|(?<=\\p)', flat)
        body = ''.join('    .string "' + p + '"\n' for p in parts if p)
        s = s[:m.start(2)] + body + s[m.end(2):]
    open(f, 'w').write(s)
print({f: len(v) for f, v in targets.items()})
