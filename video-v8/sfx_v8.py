import numpy as np, wave, sys, json, os
SR = 48000
DUR = 57.3
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

def trans(d=0.0, lo=0.0, hi=0.0):
    # soft tonal transition: woodblock tap + short rising blip (replaces noise whoosh)
    n = int(0.35 * SR); t = np.arange(n) / SR
    wood = np.sin(2 * np.pi * 1250 * t) * np.exp(-t / 0.018) + 0.5 * np.sin(2 * np.pi * 2150 * t) * np.exp(-t / 0.01)
    f = 700 + 700 * np.clip(t / 0.11, 0, 1)
    blip = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-np.maximum(0, t - 0.03) / 0.07) * np.minimum(1, t / 0.01)
    blip = np.concatenate([np.zeros(int(0.04 * SR)), blip[:n - int(0.04 * SR)]])
    return (wood * 0.35 + blip * 0.22) * 0.9

N = int(DUR * SR)
mix = np.zeros(N)
def add(t, x, g=1.0):
    s = int(t * SR)
    if s < 0: x = x[-s:]; s = 0
    e = min(N, s + len(x))
    if s < N: mix[s:e] += x[:e - s] * g

# transitions (tonal, no whoosh)
for t, g in [(0.0, .6), (3.9, .5), (7.8, .5), (13.1, .5), (16.9, .5), (19.9, .5), (23.14, .6), (28.14, .6),
             (33.5, .5), (40.4, .5), (42.86, .6), (47.6, .6), (50.9, .5), (54.3, .5), (56.15, .6)]:
    add(t, trans(), g)
for t, g in [(0.85, .6), (5.5, .5), (8.7, .7), (10.72, .6), (11.86, .6), (12.46, .6), (15.62, .5), (24.3, .6),
             (25.7, .7), (32.55, .6), (36.3, .5), (41.9, .6), (44.02, .7), (48.6, .7), (49.0, .7), (49.45, .7),
             (52.05, .6), (52.88, .6)]:
    add(t, pop(), g)
add(8.95, chime(1318.5, 1.2), .6)
add(17.0, sparkle(), .5)
add(19.9, shutter(), .8); add(29.58, shutter(), .8)
add(28.14, chime(784, 1.6), .7); add(28.16, chime(1175, 1.4), .4)
add(24.95, thud(0.3), .5); add(36.32, thud(0.3), .6); add(5.6, thud(0.25), .4); add(41.6, thud(0.25), .4)
add(32.6, chime(1568, 1.0), .5)
for i, t in enumerate((44.95, 45.5, 45.9, 46.75)):
    add(t, chime(1046.5 * (1.12 ** i), 0.6, ((1, 1), (2, .2))), .45)
for t in (50.92, 54.32):
    add(t, chime(1568, 0.9, ((1, 1), (2.0, .3))), .6); add(t + 0.09, chime(2093, 1.1, ((1, 1), (2.0, .3))), .5)
add(56.55, chime(1318.5, 1.0), .5)
# subtle tick on each caption group start
for t in json.load(open(sys.argv[2])):
    add(t, tick(), .5)

mix = np.tanh(mix * 1.1) * 0.9
st = np.stack([mix, mix], 1)
pcm = (st * 32767 * 0.5).astype(np.int16)
w = wave.open(sys.argv[1], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(pcm.tobytes()); w.close()
print('ok', np.abs(mix).max())
