"""Fix-Runde 2: jump (sofortiges Abfeden, kein Klampfen), grab (weniger Tiefe, Kopf aufrecht).
Basierend auf author_full.py;gruende geaendert: jump, flip, shove, grab."""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
BASE = _os.path.dirname(_os.path.dirname(_HERE))  # Repo-Wurzel (tools/anims/..)

import numpy as np, math, sys, pickle, json, base64, struct
sys.path.insert(0, _HERE)
import gltf_lib
from gltf_lib import *
gltf_lib.ASSET = _os.path.join(_HERE, 'original') + _os.sep   # Original-Clips als Basis
from scipy.optimize import minimize

out_dir = _HERE   # frames2.pkl bleibt neben den Skripten
import os, shutil
os.makedirs(out_dir, exist_ok=True)

g, read_acc = load_gltf()
rig = Rig(g, read_acc); fk = FK(rig)
HIPS = rig.idx_of['mixamorigHips']

def sample(clip, t): return build_pose(fk, rig, clip, t)
def blend(pA, pB, w):
    out = {}
    for nid in pA:
        qa = pA.get(nid, (None, np.array([0,0,0,1],np.float32)))[1]
        qb = pB.get(nid, qa)[1]
        out[nid] = (pA[nid][0], quat_slerp(qa, qb, w))
    return out
def with_xz(pose, x, z):
    p = dict(pose); t = np.array(pose[HIPS][0], np.float32); t[0]=x; t[2]=z
    p[HIPS] = (t, p[HIPS][1]); return p
def feet_rel_mean(pose):
    p = dict(pose); t = np.array(pose[HIPS][0], np.float32); t[1]=0.0; p[HIPS]=(t,p[HIPS][1])
    w = fk.world(p)
    lf = w[rig.idx_of['mixamorigLeftFoot']][0]; rf = w[rig.idx_of['mixamorigRightFoot']][0]
    return (lf[1]+rf[1])/2.0
FEET_Y = 53.05
def glue(pose, x=None, z=0.0, lo=40.0, hi=215.0):
    y = FEET_Y - feet_rel_mean(pose)
    y = max(lo, min(hi, y))
    p = dict(pose); t = np.array(pose[HIPS][0], np.float32)
    t[0] = t[0] if x is None else x; t[1] = y; t[2] = z
    p[HIPS] = (t, p[HIPS][1]); return p
def post(nm, pose, axis, ang):
    p = dict(pose); i = rig.idx_of[nm]
    d = quat_from_axis_angle(axis, ang)
    p[i] = (p[i][0], quat_normalize(quat_mul(d, p[i][1])))
    return p

RIDE0 = sample('ride', 0.0)
CROUCH = sample('jump', 0.30)
FALLBAL = sample('fall', 1.067)
AX = {'LUpLeg': (np.array([-0.86,0.33,0.38]), 0.892),
      'LLeg':  (np.array([-0.75,-0.22,-0.63]), 0.354),
      'RUpLeg':(np.array([-0.90,0.20,-0.39]), 0.857),
      'RLeg':  (np.array([-0.73,0.21,0.65]), 0.312)}
def more_tuck(pose, tuck):
    p = pose
    for k, nm in [('LUpLeg','mixamorigLeftUpLeg'), ('RUpLeg','mixamorigRightUpLeg')]:
        ax, base = AX[k]; p = post(nm, p, ax, base*0.55*tuck)
    for k, nm in [('LLeg','mixamorigLeftLeg'), ('RLeg','mixamorigRightLeg')]:
        ax, base = AX[k]; p = post(nm, p, ax, base*1.6*tuck)
    return p
def bend_fwd(pose, ang, neck=-0.55, head=-0.30):
    p = pose
    for nm, w in [('mixamorigSpine',0.4),('mixamorigSpine1',0.33),('mixamorigSpine2',0.27)]:
        p = post(nm, p, (1,0,0), ang*w)
    p = post('mixamorigNeck', p, (1,0,0), -ang*neck)
    p = post('mixamorigHead', p, (1,0,0), -ang*head)
    return p

ARMJ = ['mixamorigLeftShoulder','mixamorigLeftArm','mixamorigLeftForeArm','mixamorigLeftHand',
        'mixamorigRightShoulder','mixamorigRightArm','mixamorigRightForeArm','mixamorigRightHand']
def arms_from(pose, src_pose, w):
    p = dict(pose)
    for nm in ARMJ:
        nid = rig.idx_of[nm]
        p[nid] = (p[nid][0], quat_slerp(p[nid][1], src_pose[nid][1], w))
    return p

def ease(x): x = min(max(x,0.0),1.0); return x*x*(3-2*x)

# ---------- Neue Basis-Poesen ----------------------------------------------
ANT  = arms_from(blend(RIDE0, CROUCH, 0.32), FALLBAL, 0.20)          # kurze Antizipation
EXT  = glue(sample('jump', 0.500), lo=100.0, hi=260.0)               # Abstoss-Streckung
AIR  = arms_from(blend(RIDE0, CROUCH, 0.16), FALLBAL, 0.35)          # Flugpose
LND  = arms_from(blend(RIDE0, CROUCH, 0.50), FALLBAL, 0.15)          # Landung
for P in (ANT, EXT, AIR, LND):
    pass
EXT  = arms_from(EXT, FALLBAL, 0.25)

JDUR = 0.6333
def jump_pose(t):
    """t in 0..JDUR: sofortige Reaktion, Streckung bei 0.20, Flug, Landevorbereitung."""
    if t < 0.08:
        p = blend(RIDE0, ANT, ease(t/0.08))
    elif t < 0.20:
        p = blend(ANT, EXT, ease((t-0.08)/0.12))
    elif t < 0.34:
        p = blend(EXT, AIR, ease((t-0.20)/0.14))
    elif t < 0.44:
        p = dict(AIR)
    else:
        p = blend(AIR, LND, ease((t-0.44)/(JDUR-0.44)))
    return glue(p, lo=150.0, hi=230.0)

FPS = 30.0
def plateau(t, t0, t1, rise=0.25):
    if t < t0-rise or t > t1+rise: return 0.0
    if t < t0: return (t-(t0-rise))/rise
    if t > t1: return 1.0-(t-t1)/rise
    return 1.0

# ---------- Grab: tiefe Indy-Hocke (Hand erreicht Board), Kopf aufrecht ------
GRAB_TUCK, GRAB_BEND = 1.8, 0.52
def grab_frame(arm_params, tuck=GRAB_TUCK, bend=GRAB_BEND):
    p = more_tuck(CROUCH, tuck)
    p = bend_fwd(p, bend, neck=1.00, head=0.60)    # Kopf aufrecht halten (starke Gegenkompensation)
    p = glue(p, lo=60.0, hi=200.0)
    ax_, ay, az, fx, fz = arm_params
    p = post('mixamorigRightArm', p, (0,0,1), az)
    p = post('mixamorigRightArm', p, (1,0,0), ax_)
    p = post('mixamorigRightForeArm', p, (0,0,1), fz)
    p = post('mixamorigRightForeArm', p, (1,0,0), fx)
    return p
def grab_dist(params):
    p = grab_frame(params)
    w = fk.world(p)
    hand = w[rig.idx_of['mixamorigRightHand']][0]
    lf = w[rig.idx_of['mixamorigLeftFoot']][0]; rf = w[rig.idx_of['mixamorigRightFoot']][0]
    tgt = (lf+rf)/2.0; tgt[1] -= 3.0
    return float(np.linalg.norm(hand-tgt))
res = minimize(grab_dist, np.array([0.85,0,-0.9,-0.6,0.4]), method='Powell',
               options=dict(maxiter=6000, xtol=1e-5, ftol=1e-8))
ARM = res.x
print("Grab-IK: dist=%.2f cm, params=%s" % (grab_dist(ARM), np.round(ARM,3).tolist()))
GRABt = grab_frame(ARM)

def pose_delta(a, b):
    s = 0.0
    for nid in a:
        qa = a[nid][1]; qb = b[nid][1]
        d = abs(float(np.dot(qa, qb)))
        s += 2*math.degrees(math.acos(min(1.0,d)))
    return s

CLIPS = {}
# ride in-place (unveraendert)
CLIPS['ride']     = dict(dur=1.0, gen=lambda t: with_xz(sample('ride', t % 1.0), sample('ride', t % 1.0)[HIPS][0][0], 0.0))
def ride2_gen(t):
    frac = min(t, 2.1666667)
    p = sample('ride2', frac); tr = np.array(p[HIPS][0], np.float32)
    tr[2] -= (frac/2.1666667)*(987.9-7.4)
    p = dict(p); p[HIPS] = (tr, p[HIPS][1]); return p
CLIPS['ride2']    = dict(dur=2.1666667, gen=ride2_gen)
# jump: sofortige Reaktion
CLIPS['jump']     = dict(dur=JDUR, gen=lambda t: jump_pose(min(t, JDUR)))
# flip: Tuck-Fenster auf neuer Sprungbasis
def flip_gen(t):
    t = min(t, JDUR)
    base = jump_pose(t)
    w = plateau(t, 0.20, 0.34, 0.10)*0.8
    if w > 0: base = more_tuck(base, w*0.9)
    return glue(base, lo=142.0, hi=215.0)
CLIPS['flip']     = dict(dur=JDUR, gen=flip_gen)
# shove: Hueft-Yaw + Schultergegendreh auf neuer Sprungbasis
def shove_gen(t):
    t = min(t, JDUR)
    pose = jump_pose(t)
    s = math.sin(min(max((t-0.10)/0.30,0),1)*math.pi)
    a = 0.42*s
    pose = post('mixamorigHips', pose, (0,-1,0), a)
    pose = post('mixamorigSpine2', pose, (0,1,0), a*0.7)
    pose = post('mixamorigSpine1', pose, (0,1,0), a*0.4)
    return pose
CLIPS['shove']    = dict(dur=JDUR, gen=shove_gen)
# grab: Pingpong um Apex, moderat
def grab_gen(t):
    ph = (t % 0.9)/0.9
    tri = 1-2*abs(ph-0.5)          # 0..1..0 pingpong
    p = blend(AIR, GRABt, 0.30 + 0.70*tri)
    return glue(p, lo=85.0, hi=200.0)
CLIPS['grab']     = dict(dur=0.9, gen=grab_gen)
# grind: crouch halten (unveraendert)
def grind_gen(t):
    tt = t % 1.0
    ride = sample('ride', tt)
    c = blend(CROUCH, sample('jump', 0.12), 0.12)
    pose = blend(c, ride, 0.05 + 0.04*math.sin(tt*2*math.pi))
    pose = more_tuck(pose, 0.30)
    pose = post('mixamorigHips', pose, (0,0,1), 0.045*math.sin(tt*2*math.pi))
    return glue(pose, lo=130.0, hi=200.0)
CLIPS['grind']    = dict(dur=1.0, gen=grind_gen)
# manual (tail)/nmanual(nose) (unveraendert)
def manual_gen(t, nose):
    tt = t % 1.0
    pose = sample('ride', tt)
    d = -1.0 if nose else 1.0
    for nm, w in [('mixamorigSpine',1.1),('mixamorigSpine1',0.8),('mixamorigSpine2',0.5)]:
        pose = post(nm, pose, (1.15,0,0), -d*0.30*w)
    pose = post('mixamorigHips', pose, (1.15,0,0), -d*0.10)
    pose = post('mixamorigNeck', pose, (1.15,0,0), d*0.30)
    pose = post('mixamorigHead', pose, (1.15,0,0), d*0.18)
    pose = more_tuck(pose, 0.22)
    pose = arms_from(pose, FALLBAL, 0.55)
    return glue(pose, lo=150.0, hi=200.0)
CLIPS['manual']   = dict(dur=1.0, gen=lambda t: manual_gen(t, False))
CLIPS['nmanual']  = dict(dur=1.0, gen=lambda t: manual_gen(t, True))
# land: crouch -> ride (unveraendert)
def land_gen(t):
    w = ease(min(t/0.5, 1.0))
    pose = blend(CROUCH, RIDE0, w)
    return glue(pose)
CLIPS['land']     = dict(dur=0.5, gen=land_gen)

# ---------- Frames ziehen + Metriken --------------------------------------
JSET = sorted([n for n in rig.clips['jump'] if isinstance(n, int)])
frames = {}
metrics = {}
for name, cd in CLIPS.items():
    n = int(round(cd['dur']*FPS)) + 1
    fr = []
    for k in range(n):
        t = min(k/FPS, cd['dur'])
        fr.append(cd['gen'](t))
    frames[name] = fr
    w0 = fk.world(glue(fr[0])); w1 = fk.world(glue(fr[-1]))
    seam = pose_delta(fr[0], fr[-1])
    hips = [fk.world(glue(p))[HIPS][0][1] for p in fr]
    lf = [fk.world(glue(p))[rig.idx_of['mixamorigLeftFoot']][0][1] for p in fr]
    hd_up = []
    for p in fr:
        w = fk.world(glue(p))
        M = quat_to_mat(w[rig.idx_of['mixamorigHead']][1])
        hd_up.append((M[:3,1]/np.linalg.norm(M[:3,1]))[1])
    metrics[name] = dict(seam=seam, hips=(min(hips),max(hips)), lf=(min(lf),max(lf)), headUp=min(hd_up))
    print(f"{name:8s} keys={n:3d}  Naht={seam:6.1f} deg  hipsY {min(hips):6.1f}..{max(hips):6.1f}  LfootY {min(lf):6.1f}..{max(lf):6.1f}  minKopfYachse={min(hd_up):.2f}")

with open(_os.path.join(_HERE, 'frames2.pkl'),'wb') as f:
    pickle.dump(frames, f)
print("frames2.pkl gespeichert:", {name: len(frames[name]) for name in frames})

# Grab-Handkontrolle am tiefsten Punkt
best = min(frames['grab'], key=lambda p: fk.world(glue(p))[HIPS][0][1])
gw = fk.world(glue(best))
hand = gw[rig.idx_of['mixamorigRightHand']][0]
lf = gw[rig.idx_of['mixamorigLeftFoot']][0]; rf = gw[rig.idx_of['mixamorigRightFoot']][0]
tgt = (lf+rf)/2.0
print("Grab: Hand y=%.1f  Deck y=%.1f  Abstand %.1f cm  hipsY=%.1f" % (
    hand[1], tgt[1]-3, np.linalg.norm(hand-(tgt-[0,3,0])), gw[HIPS][0][1]))
