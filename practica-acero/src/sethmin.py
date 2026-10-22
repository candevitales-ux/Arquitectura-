# uso: python3 sethmin.py archivo.py clave valor  -> fija hmin en la llamada Sheet(NUM["clave"], ...)
import sys, re
f, k, val = sys.argv[1:4]
s = open(f).read()
i = s.index(f'Sheet(NUM["{k}"]')
depth = 0
for j in range(i, len(s)):
    if s[j] == '(': depth += 1
    elif s[j] == ')':
        depth -= 1
        if depth == 0: break
call = s[i:j]
call = re.sub(r', hmin=[\d.]+', '', call)
s = s[:i] + call + f', hmin={val}' + s[j:]
open(f, 'w').write(s)
