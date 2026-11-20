"""glTF-Encoding: neue Clips als Animationen + Buffer f7 + Roundtrip-Validierung."""
import numpy as np, json, base64, pickle, sys, os, shutil, math
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
BASE = _os.path.dirname(_os.path.dirname(_HERE))  # Repo-Wurzel (tools/anims/..)


SRC = _os.path.join(_HERE, 'original') + _os.sep   # Original-gltf (4 Clips) + Puffer
OUT = _os.path.join(BASE, 'assets', 'remy')        # aktuelle Spiel-Assets
os.makedirs(OUT, exist_ok=True)

import gltf_lib
from gltf_lib import load_gltf, Rig, FK, quat_normalize
gltf_lib.ASSET = SRC   # Original-gltf als Basis laden

g, read_acc = load_gltf()
rig = Rig(g, read_acc)
HIPS = rig.idx_of['mixamorigHips']
JSET = sorted([n for n in rig.clips['jump'] if isinstance(n, int)])

frames = pickle.load(open(_os.path.join(_HERE, 'frames2.pkl'),'rb'))
FPS = 30.0
NEW_ORDER = ['ride','ride2','jump','flip','shove','grab','grind','manual','nmanual','land']

# Kopf-Anhebung: +10 cm Welt-Aufwaertshub gegenueber main (dy=70, dz=-29);
# aus dem Rueckenausschnitt (Unhohe Haar zu Kragen vorher nur ~1.3 cm).
HEAD = rig.idx_of['mixamorigHead']
HEAD_DY = 70.0   # Kopf weiter aus dem Hoodie-Kragen heben (Wunsch: mind. 10 cm mehr)
HEAD_DZ = -29.0  # leichte Gegenkomponente: verhindert zu starke Vorwaertsneigung
for name in NEW_ORDER:
    fr = frames[name]
    for f in fr:
        f[HEAD] = (np.asarray(f[HEAD][0], np.float32) + np.array([0.0, HEAD_DY, HEAD_DZ], np.float32), f[HEAD][1])

# ---- Binary-Packing --------------------------------------------------------
buf = bytearray()
bviews, accs = [], []
BV0 = len(g['bufferViews']); AC0 = len(g['accessors'])
def add_view(data):
    if len(buf) % 4: buf.extend(b'\x00' * (4 - len(buf) % 4))
    off = len(buf)
    buf.extend(data)
    bviews.append(dict(buffer=7, byteOffset=off, byteLength=len(data)))
    return BV0 + len(bviews)-1

def add_acc_times(a):
    v = add_view(np.ascontiguousarray(a, np.float32).tobytes())
    accs.append(dict(bufferView=v, componentType=5126, count=len(a), type="SCALAR"))
    return AC0 + len(accs)-1
def add_acc_vals(a, t):
    a2 = np.ascontiguousarray(a, np.float32)
    v = add_view(a2.tobytes())
    nc = a2.shape[1]
    accs.append(dict(bufferView=v, componentType=5126, count=a2.shape[0],
                     type={1:"SCALAR",3:"VEC3",4:"VEC4"}[nc]))
    return AC0 + len(accs)-1

new_anims = []
for name in NEW_ORDER:
    fr = frames[name]
    n = len(fr)
    times = np.arange(n, dtype=np.float32)/FPS
    t_acc = add_acc_times(times)
    channels, samplers = [], []
    # hips translation
    vals = np.stack([f[HIPS][0] for f in fr]).astype(np.float32)
    v_acc = add_acc_vals(vals, 'VEC3')
    samplers.append(dict(input=t_acc, output=v_acc, interpolation="LINEAR"))
    channels.append(dict(sampler=0, target=dict(node=HIPS, path="translation")))
    for si, nid in enumerate(JSET, start=1):
        q = np.stack([quat_normalize(f[nid][1]) for f in fr]).astype(np.float32)
        v_acc = add_acc_vals(q, 'VEC4')
        samplers.append(dict(input=t_acc, output=v_acc, interpolation="LINEAR"))
        channels.append(dict(sampler=si, target=dict(node=nid, path="rotation")))
    # Kopf-Anhebung: konstanter Translation-Kanal auf mixamorigHead
    hv = np.stack([np.asarray(f[HEAD][0], np.float32) for f in fr]).astype(np.float32)
    v_acc = add_acc_vals(hv, 'VEC3')
    samplers.append(dict(input=t_acc, output=v_acc, interpolation="LINEAR"))
    channels.append(dict(sampler=len(JSET)+1, target=dict(node=HEAD, path="translation")))
    new_anims.append(dict(channels=channels, samplers=samplers, name=name))

# ---- Original-Animationen umbenennen (fallback) ------------------------------
ren = {'ride':'orig_ride','ride2':'orig_ride2','jump':'orig_jump'}
old_anims = []
for a in g['animations']:
    b = dict(a)
    b['name'] = ren.get(a['name'], a['name'])   # 'fall' bleibt
    if b['name'] == 'fall':
        # Kopf-Anhebung auch im Fall-Clip (konstanter Kanal)
        inp = b['samplers'][0]['input']
        n_keys = g['accessors'][inp]['count']
        hv = np.tile(np.array([0.0, HEAD_DY, HEAD_DZ], np.float32), (n_keys, 1))
        v_acc = add_acc_vals(hv, 'VEC3')
        samplers_f = b['samplers'] + [dict(input=inp, output=v_acc, interpolation="LINEAR")]
        channels_f = b['channels'] + [dict(sampler=len(samplers_f)-1,
                                           target=dict(node=HEAD, path="translation"))]
        b = dict(b, samplers=samplers_f, channels=channels_f)
    old_anims.append(b)

out = dict(g)
out['buffers'] = g['buffers'] + [dict(byteLength=int(math.ceil(len(buf)/4)*4), uri='f7.txt')]
out['bufferViews'] = g['bufferViews'] + bviews
out['accessors'] = g['accessors'] + accs
out['animations'] = new_anims + [a for a in old_anims if a['name'] != 'fall' or True]
# Reihenfolge: neue Clips zuerst, fall danach, orig_ am Ende
ordered = new_anims + [a for a in old_anims if a['name'] == 'fall'] + [a for a in old_anims if a['name'].startswith('orig_')]
out['animations'] = ordered

# pad buffer auf byteLength
if len(buf) % 4: buf.extend(b'\x00' * (4 - len(buf) % 4))

with open(os.path.join(OUT, 'remy.gltf.json'), 'w') as f:
    json.dump(out, f, separators=(',',':'))
with open(os.path.join(OUT, 'f7.txt'), 'wb') as f:
    f.write(base64.b64encode(bytes(buf)))
# Buffer/Dateien des Originals aus dem Spiel-Asset uebernehmen (f0..f6 identisch)
for fn in [f for f in os.listdir(OUT) if f != 'remy.gltf.json' and f != 'f7.txt']:
    pass  # f0..f6 liegen bereits in assets/remy (identisch mit dem Original)

print("geschrieben:", OUT)
print("f7 byteLength:", out['buffers'][-1]['byteLength'], "-> base64 f7.txt",
      os.path.getsize(OUT+'/f7.txt'), "Bytes")
print("Animationen:", [a['name'] for a in out['animations']])

# ---- Roundtrip: neue Datei laden und pruefen --------------------------------
gltf_lib.ASSET = OUT + '/'
g2, read2 = gltf_lib.load_gltf()
rig2 = Rig(g2, read2); fk2 = FK(rig2)
print("\n== Roundtrip-Metrik (aus der geschriebenen Datei):")
for name in NEW_ORDER + ['fall']:
    a = next(x for x in g2['animations'] if x['name'] == name)
    ch = rig2.clips[name]
    tr = ch[HIPS]['translation'][1]
    n_keys = len(tr)
    ok_norm = True
    for nid in JSET:
        if nid in ch and 'rotation' in ch[nid]:
            q = ch[nid]['rotation'][1]
            if not np.allclose(np.linalg.norm(q, axis=1), 1.0, atol=1e-4): ok_norm = False
    rot_cnt = sum(1 for nid in ch if isinstance(nid,int) and 'rotation' in ch[nid])
    hy = ch[HEAD]['translation'][1][:,1].mean() if (HEAD in ch and 'translation' in ch[HEAD]) else float('nan')
    hz = ch[HEAD]['translation'][1][:,2].mean() if (HEAD in ch and 'translation' in ch[HEAD]) else float('nan')
    print(f" {name:8s} keys={n_keys:3d} rot-channels={rot_cnt} quats-normiert={ok_norm} hipsY {tr[:,1].min():.1f}..{tr[:,1].max():.1f} hipsZ {np.abs(tr[:,2]).max():.1f} (Drift-Check) KopfY {hy:.1f} KopfZ {hz:.1f}")