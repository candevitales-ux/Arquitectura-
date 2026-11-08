import numpy as np, wave, sys, json, os
SR = 48000
DUR = 34.3
rng = np.random.default_rng(1)

def env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)
    return e

def lp(x, k):
    # simple one-pole lowpass, k in (0,1)
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += k * (v - acc); y[i] = acc
    return y

def whoosh(d=0.45, lo=0.03, hi=0.25):
    n = int(d * SR)
    x = rng.normal(0, 1, n)
    ks = np.linspace(lo, hi, n // 2).tolist() + np.linspace(hi, lo, n - n // 2).tolist()
    y = np.empty(n); acc = 0.0
    for i in range(n):
        acc += ks[i] * (x[i] - acc); y[i] = acc
    t = np.linspace(0, 1, n)
    e = np.sin(np.pi * t) ** 1.6
    return y * e / (np.abs(y).max() + 1e-9) * 0.5

def pop(f0=820, f1=420, d=0.09):
    n = int(d * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.015)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(n, 0.002, 0.03) * 0.55

def tick():
    n = int(0.03 * SR)
    x = rng.normal(0, 1, n) * env(n, 0.0005, 0.004)
    return np.diff(np.concatenate([[0], x])) * 0.25

def chime(f=1046.5, d=1.4, parts=((1, 1), (2.01, .35), (3.0, .15), (4.2, .08))):
    n = int(d * SR); t = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t / (0.5 / k ** .5)) for k, a in parts)
    return y * np.minimum(1, t / 0.003) * 0.28

def thud(d=0.4):
    n = int(d * SR); t = np.arange(n) / SR
    f = 55 + 70 * np.exp(-t / 0.04)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12)
    y += lp(rng.normal(0, 1, n), 0.15) * np.exp(-t / 0.03) * 0.6
    return y * 0.7

def sizzle(d=2.4):
    n = int(d * SR)
    x = rng.normal(0, 1, n)
    hp = x - lp(x, 0.25)
    crack = (rng.random(n) > 0.9993) * rng.normal(0, 3, n)
    y = (hp * 0.5 + crack) * (rng.random(n) * 0.5 + 0.5)
    t = np.linspace(0, 1, n)
    e = np.minimum(1, t / 0.15) * np.minimum(1, (1 - t) / 0.3)
    return y * e * 0.12

def shutter():
    a = tick() * 3
    gap = np.zeros(int(0.07 * SR))
    return np.concatenate([a, gap, a * 0.8])

def sparkle():
    out = np.zeros(int(1.6 * SR))
    for i, f in enumerate([1568, 2093, 2637, 3136]):
        c = chime(f, 1.0) * 0.5
        s = int(i * 0.07 * SR)
        out[s:s + len(c)] += c[:len(out) - s]
    return out

N = int(DUR * SR)
mix = np.zeros(N)
def add(t, x, g=1.0):
    s = int(t * SR)
    if s < 0: x = x[-s:]; s = 0
    e = min(N, s + len(x))
    if s < N: mix[s:e] += x[:e - s] * g

# soft whooshes / transitions
for t, g in [(0.0, .6), (2.72, .7), (4.98, .8), (15.15, .6), (20.12, .8), (25.35, .6), (29.9, .6), (31.5, .5)]:
    add(t - 0.12, whoosh(), g)
# brand reveal
add(5.6, chime(784, 1.8), .9); add(5.62, chime(1175, 1.6), .5)
# pins / pops
for t, g in [(0.12, .6), (3.55, .5), (4.32, .7), (8.77, .7), (9.4, .7), (9.8, .7), (13.32, .5), (16.57, .6),
             (17.92, .7), (18.47, .7), (26.42, .7), (27.97, .6), (28.77, .6), (30.62, .5), (31.12, .7),
             (31.64, .8), (32.72, .8)]:
    add(t, pop(), g)
# dings / highlights
for t, f, g in [(15.0, 1318.5, .6), (19.32, 1568, .7), (27.14, 1046.5, .6), (31.2, 1318.5, .55), (21.1, 659.3, .5)]:
    add(t, chime(f, 1.2), g)
add(22.42, sparkle(), .8)
add(6.12, shutter(), .9)
add(7.32, thud(), .9); add(24.2, thud(), .7); add(1.02, thud(0.25), .4)
add(10.4, sizzle(2.5), 1.0); add(24.2, sizzle(1.3), .8)
add(11.4, whoosh(0.6, 0.02, 0.1), .5)
# subtle tick on each caption group start
for t in json.load(open(sys.argv[2])):
    add(t, tick(), .5)

mix = np.tanh(mix * 1.1) * 0.9
st = np.stack([mix, mix], 1)
pcm = (st * 32767 * 0.5).astype(np.int16)
w = wave.open(sys.argv[1], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(pcm.tobytes()); w.close()
print('ok', np.abs(mix).max())
