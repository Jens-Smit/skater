"""Helle Verifikations-Renders fuer Remy-Clips (vorher/nachher Vergleiche)."""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
BASE = _os.path.dirname(_os.path.dirname(_HERE))  # Repo-Wurzel (tools/anims/..)

import sys, math
sys.path.insert(0, _HERE)
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from render_skin import skin_all, pose_for, PART_COLOR

HEAD = 6
HEAD_DY = 70.0
HEAD_DZ = -29.0
OLD_DY = 20.0  # Stufe 1 der Kopf-Anhebung (vorheriger Stand)

def pose_no_head_fix(clip, t):
    """Pose wie auf main vor der Kopf-Korrektur (Anhebung zurueckgerechnet)."""
    p = pose_for(clip, t)
    q = dict(p)
    if HEAD in q:
        q[HEAD] = (np.asarray(q[HEAD][0], np.float32) - np.array([0.0, HEAD_DY, HEAD_DZ], np.float32), q[HEAD][1])
    return q

def pose_prev_head_fix(clip, t):
    """Pose des letzten Stands (+20 Y) auf Basis der neuen Datei."""
    p = pose_for(clip, t)
    q = dict(p)
    if HEAD in q:
        q[HEAD] = (np.asarray(q[HEAD][0], np.float32) - np.array([0.0, HEAD_DY, HEAD_DZ], np.float32) + np.array([0.0, OLD_DY, 0.0], np.float32), q[HEAD][1])
    return q

def render_bright(pose, path_png, view='side', title=''):
    parts = skin_all(pose)
    allv = []; allc = []
    light = np.array([0.45, 0.75, 0.5]); light /= np.linalg.norm(light)
    for name, V, N in parts:
        tris = np.arange(len(V)).reshape(-1, 3)
        lam = np.clip(N @ light, 0, 1) * 0.5 + 0.5
        if view == 'side':
            pts = np.stack([V[:, 2], V[:, 1]], axis=1); depth = V[:, 0]
        else:
            pts = np.stack([-V[:, 0], V[:, 1]], axis=1); depth = V[:, 2]
        Tv = pts[tris]
        zmean = depth[tris].mean(axis=1)
        sign = 1 if view == 'back' else -1
        order = np.argsort(sign * zmean)
        base = np.array(matplotlib.colors.to_rgb(PART_COLOR.get(name.lower(), '#999999')))
        lam_tri = np.clip(lam[tris].mean(axis=1), 0, 1)
        allv.append(Tv[order]); allc.append(lam_tri[order][:, None] * base[None, :])
    allv = np.concatenate(allv); allc = np.concatenate(allc)
    pc = PolyCollection(allv, facecolors=np.clip(allc * 1.4, 0, 1), edgecolors='0.25', linewidths=0.15)
    fig, ax = plt.subplots(figsize=(3.6, 5.0), dpi=110)
    ax.add_collection(pc)
    ax.set_facecolor('#f4f6f8'); fig.patch.set_facecolor('#f4f6f8')
    xmin, ymin = allv[:, :, 0].min(), allv[:, :, 1].min()
    xmax, ymax = allv[:, :, 0].max(), allv[:, :, 1].max()
    w = max(xmax - xmin, (ymax - ymin) * 0.72); cx = (xmin + xmax) / 2
    ax.set_xlim(cx - w/2 - 6, cx + w/2 + 6); ax.set_ylim(ymin - 8, ymax + 12)
    ax.set_title(title, fontsize=9, pad=4)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect('equal')
    fig.savefig(path_png, bbox_inches='tight', facecolor='#f4f6f8'); plt.close(fig)
    return path_png
