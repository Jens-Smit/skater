"""Skinning-Renderer fuer Remy: echte Mesh-Silhouetten pro Clip/Zeit als PNG.
Reine numpy-Berechnung, matplotlib-Ausgabe, keine GPU noetig."""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
BASE = _os.path.dirname(_os.path.dirname(_HERE))  # Repo-Wurzel (tools/anims/..)

import sys, os, json, base64, math
sys.path.insert(0, _HERE)
import numpy as np

ASSET = _os.environ.get('REMY_ASSET', _os.path.join(BASE, 'assets', 'remy')) + _os.sep  # zu pruefende Asset-Version

def load_all():
    g = json.load(open(ASSET + 'remy.gltf.json'))
    bufs = {}
    for i, b in enumerate(g['buffers']):
        raw = open(ASSET + b['uri'], 'rb').read()
        bufs[i] = base64.b64decode(raw)
    accs = g['accessors']; bvs = g['bufferViews']
    def acc(ai):
        a = accs[ai]; bv = bvs[a['bufferView']]
        off = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
        ct = a['componentType']; n = a['count']
        tmap = {5120: (np.int8,1),5121: (np.uint8,1),5122: (np.int16,2),5123: (np.uint16,2),
                5125: (np.uint8,1),5126: (np.float32,4)}
        dtype, sz = tmap[ct]
        nc = {'SCALAR':1,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']]
        data = bufs[bv['buffer']][off: off + n*sz*nc]
        nfmt = np.dtype([('x', dtype, (nc,))])
        arr = np.frombuffer(data[:n*sz*nc], dtype=nfmt, count=n)['x']
        return arr.astype(np.float32)
    return g, acc

g, acc = load_all()
nodes = g['nodes']
children = {}
for i, n in enumerate(nodes):
    for c in n.get('children', []):
        children.setdefault(i, []).append(c)

def qmat(q):
    x,y,z,w = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
        [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
        [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]], np.float32)

def local_mat(n):
    if 'matrix' in n:
        m = np.array(n['matrix'], np.float32).reshape(4, 4).T  # glTF: spaltenmajor
        return m
    t = np.array(n.get('translation', [0,0,0]), np.float32)
    q = np.array(n.get('rotation', [0,0,0,1]), np.float32)
    s = np.array(n.get('scale', [1,1,1]), np.float32)
    M = np.eye(4, dtype=np.float32)
    M[:3,:3] = qmat(q) * s[None,:]
    M[:3,3] = t
    return M

def world_mats(pose):
    W = {}
    def rec(nid, P):
        if nid in pose:
            t, q = np.asarray(pose[nid][0], np.float32), np.asarray(pose[nid][1], np.float32)
            M = np.eye(4, dtype=np.float32)
            M[:3,:3] = qmat(q)
            M[:3,3] = t
        else:
            M = local_mat(nodes[nid])
        Wm = P @ M
        W[nid] = Wm
        for c in children.get(nid, []):
            rec(c, Wm)
    has_par = set()
    for n in nodes:
        for c in n.get('children', []):
            has_par.add(c)
    for r in [i for i in range(len(nodes)) if i not in has_par]:
        rec(r, np.eye(4, dtype=np.float32))
    return W

import gltf_lib
gltf_lib.ASSET = ASSET
from gltf_lib import load_gltf, Rig, FK, build_pose
g2, read_acc = load_gltf()
rig = Rig(g2, read_acc); fk = FK(rig)

skins = []
for mi, mesh in enumerate(g['meshes']):
    prim = mesh['primitives'][0]
    node_of_mesh = next(i for i, n in enumerate(nodes) if n.get('mesh') == mi)
    sk = g['skins'][nodes[node_of_mesh]['skin']]
    joints = sk['joints']
    ibm = acc(sk['inverseBindMatrices']).reshape(len(joints), 4, 4).transpose(0, 2, 1)  # spaltenmajor
    skins.append(dict(node=node_of_mesh, joints=joints, ibm=ibm,
                      pos=acc(prim['attributes']['POSITION']),
                      nrm=acc(prim['attributes']['NORMAL']),
                      jnt=acc(prim['attributes']['JOINTS_0']).astype(np.int64),
                      wgt=acc(prim['attributes']['WEIGHTS_0']) / 255.0,
                      mesh_name=nodes[node_of_mesh].get('name', f'mesh{mi}')))

def skin_all(pose):
    W = world_mats(pose)
    out = []
    for s in skins:
        Wj = np.stack([W[j] for j in s['joints']])
        B = Wj @ s['ibm']
        v, n, jj, ww = s['pos'], s['nrm'], s['jnt'], s['wgt']
        vh = np.concatenate([v, np.ones((len(v),1), np.float32)], axis=1)
        skinned = np.zeros((len(v), 3), np.float32)
        skinned_n = np.zeros((len(v), 3), np.float32)
        for k in range(4):
            Mk = B[jj[:, k]]
            skinned += np.einsum('nkj,nj->nk', Mk, vh)[:, :3] * ww[:, k][:, None]
            skinned_n += np.einsum('njk,nj->nk', Mk[:, :3, :3], n) * ww[:, k][:, None]
        nl = np.linalg.norm(skinned_n, axis=1, keepdims=True); nl[nl == 0] = 1
        out.append((s['mesh_name'], skinned, skinned_n / nl))
    return out

PART_COLOR = {'body': '#d8a67e', 'shoes': '#20242c', 'eyes': '#ffffff', 'tops': '#2c8577',
              'bottoms': '#3a4a5c', 'hair': '#4a3018', 'eyelashes': '#1a1a1a'}

def render(pose, path_png, view='side', title=''):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    parts = skin_all(pose)
    allv = []; allc = []
    light = np.array([0.45, 0.75, 0.5]); light /= np.linalg.norm(light)
    for name, V, N in parts:
        tris = np.arange(len(V)).reshape(-1, 3)
        lam = np.clip(N @ light, 0, 1) * 0.7 + 0.3
        if view == 'side':
            pts = np.stack([V[:, 2], V[:, 1]], axis=1); depth = V[:, 0]
        elif view == 'front':
            pts = np.stack([V[:, 0], V[:, 1]], axis=1); depth = V[:, 2]
        elif view == 'back':
            pts = np.stack([-V[:, 0], V[:, 1]], axis=1); depth = V[:, 2]
        elif view == 'iso':
            a = math.radians(35)
            pts = np.stack([V[:, 2]*math.cos(a) - V[:, 0]*math.sin(a)*0.5, V[:, 1]], axis=1)
            depth = V[:, 0]
        Tv = pts[tris]
        zmean = depth[tris].mean(axis=1)
        sign = 1 if view == 'back' else -1
        order = np.argsort(sign * zmean)
        base = np.array(matplotlib.colors.to_rgb(PART_COLOR.get(name.lower(), '#999999')))
        lam_tri = np.clip(lam[tris].mean(axis=1), 0, 1)
        allv.append(Tv[order])
        allc.append(lam_tri[order][:, None] * base[None, :])
    allv = np.concatenate(allv); allc = np.concatenate(allc)
    pc = PolyCollection(allv, facecolors=allc, edgecolors='none')
    fig, ax = plt.subplots(figsize=(4.6, 6.4), dpi=110)
    ax.add_collection(pc)
    ax.set_facecolor('#101822'); fig.patch.set_facecolor('#101822')
    xmin, ymin = allv[:, :, 0].min(), allv[:, :, 1].min()
    xmax, ymax = allv[:, :, 0].max(), allv[:, :, 1].max()
    w = max(xmax - xmin, (ymax - ymin) * 0.62)
    cx = (xmin + xmax) / 2
    ax.set_xlim(cx - w/2 - 6, cx + w/2 + 6)
    ax.set_ylim(ymin - 8, ymax + 14)
    ax.set_title(title, color='w', fontsize=9, pad=4)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect('equal')
    fig.savefig(path_png, bbox_inches='tight', facecolor='#101822')
    plt.close(fig)
    return path_png

def pose_for(clip, t):
    return build_pose(fk, rig, clip, t)

if __name__ == '__main__':
    # CLI: python3 render_skin.py <clip> [t=0] [view=side|back] [out.png]
    import matplotlib
    matplotlib.use('Agg')
    clip = sys.argv[1] if len(sys.argv) > 1 else 'ride'
    t = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    view = sys.argv[3] if len(sys.argv) > 3 else 'side'
    out = sys.argv[4] if len(sys.argv) > 4 else f'{clip}_{view}_t{t:g}.png'
    render(pose_for(clip, t), out, view=view, title=f'{clip} t={t:g} ({view})')
    print('geschrieben:', out)
