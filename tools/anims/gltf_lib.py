import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
BASE = _os.path.dirname(_os.path.dirname(_HERE))  # Repo-Wurzel (tools/anims/..)

"""Loader + FK for the Remy glTF (Mixamo rig). Pure numpy."""
import json, base64, math
import numpy as np

ASSET = ''  # absoluter Pfad mit Endschraegstrich; wird von den Skripten gesetzt

def _read_buffer(uri):
    """Buffer-Datei lesen: erst ASSET, dann Repo assets/remy (gleiche Inhalte)."""
    for d in (ASSET, _os.path.join(BASE, 'assets', 'remy') + _os.sep):
        p = _os.path.join(d, uri)
        if _os.path.exists(p):
            return p
    raise FileNotFoundError(uri)


def load_gltf():
    g = json.load(open(ASSET + 'remy.gltf.json'))
    bufs = {}
    for i, b in enumerate(g['buffers']):
        raw = open(_read_buffer(b['uri']), 'rb').read()
        bufs[i] = base64.b64decode(raw)
    accs = g['accessors']; bvs = g['bufferViews']
    def read_acc(ai):
        a = accs[ai]
        bv = bvs[a['bufferView']]
        off = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
        ct = a['componentType']; n = a['count']
        tmap = {5120: (np.int8,1),5121: (np.uint8,1),5122: (np.int16,2),5123: (np.uint16,2),
                5125: (np.uint8,1),5126: (np.float32,4)}
        dtype, sz = tmap[ct]
        nc = {'SCALAR':1,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']]
        data = bufs[bv['buffer']][off: off + n*sz*nc]
        # pad to multiple of component size like glTF requires anyway
        nfmt = np.dtype([('x', dtype, (nc,))])
        arr = np.frombuffer(data[:n*sz*nc], dtype=nfmt, count=n)['x']
        if nc == 1: arr = arr.reshape(-1)
        if dtype in (np.int8, np.uint8, np.int16, np.uint16):
            arr = arr.astype(np.float32)
            if ct in (5121,): arr /= 255.0
            elif ct in (5123,): arr /= 65535.0
            elif ct in (5122,): np.maximum(arr/32767, -1, out=arr)
            elif ct in (5120,): np.maximum(arr/127, -1, out=arr)
        return arr
    return g, read_acc

class Rig:
    def __init__(self, g, read_acc):
        self.g = g; self.read_acc = read_acc
        self.nodes = g['nodes']
        self.name_of = {i: n.get('name','?') for i, n in enumerate(self.nodes)}
        self.idx_of = {n.get('name'): i for i, n in enumerate(self.nodes)}
        # animation tracks: clip -> node -> ('translation', arr[n,3]) / ('rotation', arr[n,4]) with times
        self.clips = {}
        for a in g['animations']:
            clip = {}
            shared_times = {}
            for ch in a['channels']:
                tgt = ch['target']; s = a['samplers'][ch['sampler']]
                path = tgt['path']
                times = read_acc(s['input']).astype(np.float32)
                vals = read_acc(s['output']).astype(np.float32)
                clip.setdefault(tgt['node'], {})[path] = (times, vals)
                shared_times.setdefault(len(times), times)
            self.clips[a['name']] = clip
            self.clips[a['name'] + '.__len_times'] = max(shared_times)  # store len only
        # run root (hips) default TRS
    def node_children(self):
        ch = {}
        for i, n in enumerate(self.nodes):
            for c in n.get('children', []):
                ch.setdefault(i, []).append(c)
        return ch
    def parents(self):
        ch = self.node_children()
        par = {c: p for p, cs in ch.items() for c in cs}
        return par

def quat_mul(a, b):
    """a, b: (...,4)_xyzw; returns a⊗b"""
    ax, ay, az, aw = a[...,0], a[...,1], a[...,2], a[...,3]
    bx, by, bz, bw = b[...,0], b[...,1], b[...,2], b[...,3]
    return np.stack([
        aw*bx + ax*bw + ay*bz - az*by,
        aw*by - ax*bz + ay*bw + az*bx,
        aw*bz + ax*by - ay*bx + az*bw,
        aw*bw - ax*bx - ay*by - az*bz], axis=-1)

def quat_normalize(q):
    return q / np.linalg.norm(q, axis=-1, keepdims=True)

def quat_slerp(a, b, t):
    """naive but vectorized slerp"""
    dot = np.sum(a*b, axis=-1, keepdims=True)
    b2 = np.where(dot < 0, -b, b)
    dot = np.abs(dot)
    omega = np.arccos(np.clip(dot, -1, 1))
    small = omega < 1e-4
    so = np.where(omega < 1e-6, 1.0, np.sin(omega))
    wa = np.sin((1-t)*omega)/so
    wb = np.sin(t*omega)/so
    lin = quat_normalize((1-t)*a + t*b2)
    return np.where(small, lin, quat_normalize(wa*a + wb*b2))

def quat_from_axis_angle(axis, angle):
    axis = np.asarray(axis, np.float32); axis = axis/np.linalg.norm(axis)
    half = angle/2
    return np.array([axis[0]*math.sin(half), axis[1]*math.sin(half), axis[2]*math.sin(half),
                     math.cos(half)], np.float32)

def quat_to_mat(q):
    x, y, z, w = q[...,0], q[...,1], q[...,2], q[...,3]
    m = np.empty(q.shape[:-1] + (3,3), np.float32)
    m[...,0,0] = 1-2*(y*y+z*z); m[...,0,1] = 2*(x*y-z*w); m[...,0,2] = 2*(x*z+y*w)
    m[...,1,0] = 2*(x*y+z*w); m[...,1,1] = 1-2*(x*x+z*z); m[...,1,2] = 2*(y*z-x*w)
    m[...,2,0] = 2*(x*z-y*w); m[...,2,1] = 2*(y*z+x*w); m[...,2,2] = 1-2*(x*x+y*y)
    return m

class FK:
    """Forward kinematics over the joint hierarchy."""
    def __init__(self, rig):
        self.rig = rig
        self.children = rig.node_children()
        self.root = rig.idx_of['mixamorigHips']
        self.ids = {}
    def local_trs(self, nid, rot=None, tr=None):
        n = self.rig.nodes[nid]
        r = rot if rot is not None else n.get('rotation', [0,0,0,1])
        t = tr if tr is not None else n.get('translation', [0,0,0])
        return np.array(t, np.float32), np.array(r, np.float32)
    def world(self, pose):
        """pose: dict nid -> (t3, q4). Returns dict nid -> (pos3, rot4) world."""
        out = {}
        def rec(nid, pt, pr):
            for c in self.children.get(nid, []):
                t, q = pose.get(c, self.local_trs(c))
                wr = quat_mul(pr, q); wr = quat_normalize(wr)
                wp = pt + quat_to_mat(pr).dot(t)
                out[c] = (wp, wr)
                rec(c, wp, wr)
        t, q = pose[self.root]
        out[self.root] = (np.array(t, np.float32), quat_normalize(np.array(q, np.float32)))
        rec(self.root, np.array(t, np.float32), out[self.root][1])
        return out

def pose_at(rig, clip, t_frame):
    """Sample the given clip at the time index (assumes all channels share times)."""
    ch = rig.clips[clip]
    times = ch[rig.idx_of['mixamorigHips']]['translation'][0]
    # find bracketing keys
    i1 = int(np.searchsorted(times, t_frame))
    i0 = max(0, i1-1); i1 = min(len(times)-1, i1)
    if i1 == i0: f = 0.0
    else:
        a, b = times[i0], times[i1]
        f = 0.0 if b <= a else (t_frame-a)/(b-a)
    pose = {}
    for nid, tracks in ch.items():
        if not isinstance(nid, int): continue
        if 'rotation' in tracks:
            tq, vq = tracks['rotation']
            q = quat_slerp(vq[i0], vq[i1], f)
            pose[nid] = ('r', q)
        if 'translation' in tracks:
            tt, vt = tracks['translation']
            pose[nid] = ('t', tt, (1-f)*vt[i0] + f*vt[i1])
    return pose

def build_pose(fk, rig, clip, t_frame, world=False, deltas=None):
    """Full TRS pose (every joint) sampled from clip, optional per-joint delta quats applied."""
    ch = rig.clips[clip]
    def sample(times, t_frame):
        i1 = int(np.searchsorted(times, t_frame, side='right')); i1 = min(max(i1, 1), len(times)-1); i0 = i1-1
        if len(times) == 1: return np.float32(0.0), 0, 0
        f = 0.0 if times[i1] <= times[i0] else max(0.0, min(1.0, (t_frame-times[i0])/(times[i1]-times[i0])))
        return f, i0, i1
    pose = {}
    for nid, tracks in ch.items():
        if not isinstance(nid, int): continue
        t = np.array(rig.nodes[nid].get('translation', [0,0,0]), np.float32)
        q = np.array(rig.nodes[nid].get('rotation', [0,0,0,1]), np.float32)
        if 'rotation' in tracks:
            tq, vq = tracks['rotation']
            f, i0, i1 = sample(tq, t_frame)
            q = quat_slerp(vq[i0], vq[i1], f)
        if 'translation' in tracks:
            tt, vt = tracks['translation']
            f, i0, i1 = sample(tt, t_frame)
            t = (1-f)*vt[i0] + f*vt[i1]
        pose[nid] = (t, q)
    if deltas:
        for nid, (dq, weight_dt) in deltas.items():
            if nid in pose:
                t, q = pose[nid]
                d = quat_from_axis_angle(dq[:3], dq[3]*weight_dt)
                pose[nid] = (t, quat_normalize(quat_mul(d, q)))
    return pose
