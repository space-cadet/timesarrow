#!/usr/bin/env python3
"""
Exact 3D Penrose-style pen-and-ink stippled tetrahedral chain renderer.

Generates two publication-grade figures (vector PDF + 300 dpi PNG):
  1. penrose-chain-minimal.{pdf,png}  -- Four spaced, distinctly rotated regular 3D
     tetrahedra threaded along a straight horizontal dual line with exact face-interior
     punctures, dashed interior segments, central node dots, and velvety Rapidograph stippling.
  2. penrose-chain-4valent.{pdf,png}  -- Same exact 3D Penrose style upgraded to the
     full 4-valent intertwiner chain (all 4 face-piercing magnetic legs per tetrahedron with
     true 3D front/back occlusion, sleek singlet epsilon blocks, and a warm-terracotta
     triplet block E with spin-1 leg M).
"""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon


OUT_DIR = Path(__file__).resolve().parent

# Regular tetrahedron centered at origin, unit circumradius
BASE_VERTS = np.array([
    [ 1.0,  1.0,  1.0],
    [ 1.0, -1.0, -1.0],
    [-1.0,  1.0, -1.0],
    [-1.0, -1.0,  1.0],
], dtype=float) / np.sqrt(3.0)

FACES = [
    (0, 2, 1),
    (0, 1, 3),
    (0, 3, 2),
    (1, 2, 3),
]

EDGES = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def rot_xyz(rx_deg: float, ry_deg: float, rz_deg: float) -> np.ndarray:
    rx, ry, rz = np.deg2rad([rx_deg, ry_deg, rz_deg])
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(rx), -np.sin(rx)],
                   [0, np.sin(rx),  np.cos(rx)]])
    Ry = np.array([[ np.cos(ry), 0, np.sin(ry)],
                   [ 0,          1, 0         ],
                   [-np.sin(ry), 0, np.cos(ry)]])
    Rz = np.array([[np.cos(rz), -np.sin(rz), 0],
                   [np.sin(rz),  np.cos(rz), 0],
                   [0,           0,          1]])
    return Rz @ Ry @ Rx


def face_normal(verts: np.ndarray, face: tuple[int, int, int]) -> np.ndarray:
    a, b, c = verts[face[0]], verts[face[1]], verts[face[2]]
    n = np.cross(b - a, c - a)
    n /= np.linalg.norm(n)
    if np.dot(n, (a + b + c) / 3.0) < 0:
        n = -n
    return n


def ray_intersect_tet(verts: np.ndarray, direction: np.ndarray):
    """Return (hit_point, face_idx, barycentric_coords, t) for ray from origin along direction."""
    d = direction / np.linalg.norm(direction)
    best = None
    for fi, f in enumerate(FACES):
        v0, v1, v2 = verts[f[0]], verts[f[1]], verts[f[2]]
        e1 = v1 - v0
        e2 = v2 - v0
        h = np.cross(d, e2)
        det = np.dot(e1, h)
        if abs(det) < 1e-12:
            continue
        inv_det = 1.0 / det
        s = -v0
        u = inv_det * np.dot(s, h)
        if u < -1e-9 or u > 1.0 + 1e-9:
            continue
        q = np.cross(s, e1)
        v = inv_det * np.dot(d, q)
        if v < -1e-9 or u + v > 1.0 + 1e-9:
            continue
        t = inv_det * np.dot(e2, q)
        if t > 1e-9:
            w = 1.0 - u - v
            if best is None or t < best[3]:
                best = (t * d, fi, (w, u, v), t)
    return best


def ray_exit_silhouette_2d(origin2d: np.ndarray, dir2d: np.ndarray, verts2d: np.ndarray) -> float:
    """Largest parameter t >= 0 where 2D ray origin2d + t*dir2d crosses any projected edge."""
    t_max = 0.0
    for a, b in EDGES:
        p = verts2d[a]
        s = verts2d[b] - p
        # Solve origin + t*dir = p + u*s
        denom = dir2d[0] * s[1] - dir2d[1] * s[0]
        if abs(denom) < 1e-10:
            continue
        diff = p - origin2d
        t = (diff[0] * s[1] - diff[1] * s[0]) / denom
        u = (diff[0] * dir2d[1] - diff[1] * dir2d[0]) / denom
        if t >= -1e-6 and -1e-6 <= u <= 1.0 + 1e-6:
            t_max = max(t_max, t)
    return t_max


def verify_rotations(rotations):
    """Assert every rotation has strict front-face interior horizontal punctures."""
    for idx, (rx, ry, rz) in enumerate(rotations):
        V = BASE_VERTS @ rot_xyz(rx, ry, rz).T
        hit_l = ray_intersect_tet(V, np.array([-1.0, 0.0, 0.0]))
        hit_r = ray_intersect_tet(V, np.array([ 1.0, 0.0, 0.0]))
        assert hit_l is not None and hit_r is not None
        min_l = min(hit_l[2])
        min_r = min(hit_r[2])
        assert min_l > 0.14 and min_r > 0.14, (
            f"Tet {idx+1} puncture too close to edge: min_bary L={min_l:.3f}, R={min_r:.3f}"
        )


def sample_triangle_stipple(
    tri2d: np.ndarray,
    edge_weights: tuple[float, float, float],
    face_shade: float,
    rng: np.random.Generator,
    spacing: float = 0.0145,
):
    """
    Velvety Rapidograph 0.1mm Penrose stipple shading inside a 2D projected triangle:
    dense micro-dots hugging shadowed ridges and corners, fading rapidly into crisp
    luminous white paper in the center of each face.
    """
    A, B, C = tri2d[0], tri2d[1], tri2d[2]
    xmin, ymin = tri2d.min(axis=0)
    xmax, ymax = tri2d.max(axis=0)

    xs = np.arange(xmin, xmax + spacing, spacing)
    ys = np.arange(ymin, ymax + spacing, spacing)
    gx, gy = np.meshgrid(xs, ys)
    pts = np.column_stack([gx.ravel(), gy.ravel()])
    pts += rng.uniform(-0.47 * spacing, 0.47 * spacing, size=pts.shape)

    v0 = B - A
    v1 = C - A
    v2 = pts - A
    d00 = np.dot(v0, v0)
    d01 = np.dot(v0, v1)
    d11 = np.dot(v1, v1)
    denom = d00 * d11 - d01 * d01
    if abs(denom) < 1e-12:
        return np.empty((0, 2)), np.empty((0,))
    d20 = v2 @ v0
    d21 = v2 @ v1
    u = (d11 * d20 - d01 * d21) / denom
    v = (d00 * d21 - d01 * d20) / denom
    w = 1.0 - u - v
    inside = (u > 0.008) & (v > 0.008) & (w > 0.008)
    pts = pts[inside]
    if len(pts) == 0:
        return np.empty((0, 2)), np.empty((0,))

    def seg_dist(p, p1, p2):
        e = p2 - p1
        el = np.linalg.norm(e)
        if el < 1e-12:
            return np.linalg.norm(p - p1, axis=1)
        return np.abs((p[:, 0] - p1[0]) * e[1] - (p[:, 1] - p1[1]) * e[0]) / el

    d_ab = seg_dist(pts, A, B)
    d_bc = seg_dist(pts, B, C)
    d_ca = seg_dist(pts, C, A)
    dv = np.minimum(
        np.minimum(np.linalg.norm(pts - A, axis=1), np.linalg.norm(pts - B, axis=1)),
        np.linalg.norm(pts - C, axis=1),
    )

    w0, w1, w2 = edge_weights
    # Tight bevel falloff so face interiors stay bright luminous white
    sigma = 0.075 + 0.068 * face_shade
    prob = (
        w0 * np.exp(-((d_ab / sigma) ** 1.18))
        + w1 * np.exp(-((d_bc / sigma) ** 1.18))
        + w2 * np.exp(-((d_ca / sigma) ** 1.18))
        + 0.42 * np.exp(-((dv / 0.16) ** 1.35))
    )
    # Soft threshold floor so stray dots don't pepper the bright center
    prob = np.clip((prob - 0.035) * 0.78, 0.0, 0.96)

    keep = rng.random(len(pts)) < prob
    kept_pts = pts[keep]
    kept_prob = prob[keep]
    sizes = 0.08 + 0.34 * (kept_prob ** 1.35) + rng.uniform(-0.02, 0.05, size=len(kept_pts))
    sizes = np.clip(sizes, 0.06, 0.52)
    return kept_pts, sizes


def draw_penrose_tetrahedron(
    ax,
    center_x: float,
    scale: float,
    rotation: tuple[float, float, float],
    rng: np.random.Generator,
    mode: str = "minimal",
):
    """Draw one exact 3D rotated regular tetrahedron with velvety Penrose stippling."""
    R = rot_xyz(*rotation)
    V = (BASE_VERTS @ R.T) * scale
    V_world = V + np.array([center_x, 0.0, 0.0])

    light = np.array([-0.50, 0.52, 0.69])
    light /= np.linalg.norm(light)

    normals = [face_normal(V, f) for f in FACES]
    front_faces = [fi for fi, n in enumerate(normals) if n[2] > 0.02]

    edge_adj = {e: [] for e in EDGES}
    for fi, f in enumerate(FACES):
        for a, b in [(f[0], f[1]), (f[1], f[2]), (f[2], f[0])]:
            e = (min(a, b), max(a, b))
            edge_adj[e].append(fi)

    # Hidden back edges: very delicate hairline hint
    for e in EDGES:
        adj = edge_adj[e]
        vis = any(fi in front_faces for fi in adj)
        if not vis:
            p1, p2 = V_world[e[0], :2], V_world[e[1], :2]
            ax.plot(
                [p1[0], p2[0]], [p1[1], p2[1]],
                color="#5B6570", lw=0.45, ls=(0, (2.5, 2.8)), alpha=0.28, zorder=2,
            )

    hit_l = ray_intersect_tet(V, np.array([-1.0, 0.0, 0.0]))
    hit_r = ray_intersect_tet(V, np.array([ 1.0, 0.0, 0.0]))
    p_l = hit_l[0] + np.array([center_x, 0.0, 0.0])
    p_r = hit_r[0] + np.array([center_x, 0.0, 0.0])
    f_l, f_r = hit_l[1], hit_r[1]

    # Front faces: luminous translucent white + velvety edge stippling
    for fi in front_faces:
        f = FACES[fi]
        tri2d = V_world[list(f), :2]
        n = normals[fi]
        ndotl = np.clip(np.dot(n, light), -1.0, 1.0)
        face_shade = float(np.clip(0.62 - 0.58 * ndotl, 0.06, 0.95))

        poly = Polygon(tri2d, closed=True, facecolor=(1.0, 1.0, 1.0, 0.78), edgecolor="none", zorder=3)
        ax.add_patch(poly)

        f_edges = [(f[0], f[1]), (f[1], f[2]), (f[2], f[0])]
        e_weights = []
        for a, b in f_edges:
            e = (min(a, b), max(a, b))
            other_faces = [of for of in edge_adj[e] if of != fi]
            is_ridge = other_faces and (other_faces[0] in front_faces)
            mid = 0.5 * (V[a, :2] + V[b, :2])
            dir_bias = np.clip(0.58 + 0.38 * (mid[0] - mid[1]) / scale, 0.20, 1.15)
            w_e = (0.95 if is_ridge else 0.72) * (0.36 + 0.92 * face_shade) * dir_bias
            e_weights.append(float(w_e))

        spts, ssizes = sample_triangle_stipple(tri2d, tuple(e_weights), face_shade, rng, spacing=0.0145)
        if len(spts) > 0:
            ax.scatter(
                spts[:, 0], spts[:, 1],
                s=ssizes, c="#12161A", marker="o", linewidths=0, alpha=0.88, zorder=4,
            )

    cx = center_x
    if mode == "minimal":
        ax.plot(
            [p_l[0], cx, p_r[0]], [0.0, 0.0, 0.0],
            color="#15191E", lw=0.85, ls=(0, (3.2, 2.5)), solid_capstyle="round", zorder=6,
        )
        for pt in (p_l, p_r):
            ax.scatter([pt[0]], [pt[1]], s=9.5, facecolor="white", edgecolor="#15191E", lw=0.72, zorder=9)
    else:
        other_faces = [fi for fi in range(4) if fi not in (f_l, f_r)]
        ax.plot([p_l[0], cx, p_r[0]], [0.0, 0.0, 0.0], color="#15191E", lw=0.82, ls=(0, (3.0, 2.4)), zorder=6)
        ax.scatter([p_l[0], p_r[0]], [0.0, 0.0], s=9.5, facecolor="white", edgecolor="#15191E", lw=0.72, zorder=9)

        # Remaining two faces: exact 3D centroid rays with true front/back silhouette occlusion!
        for fi in other_faces:
            f = FACES[fi]
            fc_local = V[list(f)].mean(axis=0)
            n = normals[fi]
            dir2d = n[:2].copy()
            norm2d = np.linalg.norm(dir2d)
            if norm2d < 0.16:
                dir2d = np.array([0.22, 1.0 if n[1] >= 0 else -1.0])
                dir2d /= np.linalg.norm(dir2d)
            else:
                dir2d /= norm2d

            p_face = np.array([cx + fc_local[0], fc_local[1]])
            if fi in front_faces:
                # Front-facing puncture: dashed inside (C -> p_face), solid outside (p_face -> p_ext)
                p_ext = p_face + dir2d * (0.64 * scale)
                ax.plot([cx, p_face[0]], [0.0, p_face[1]], color="#15191E", lw=0.80, ls=(0, (2.8, 2.3)), zorder=6)
                ax.plot([p_face[0], p_ext[0]], [p_face[1], p_ext[1]], color="white", lw=2.1, solid_capstyle="round", zorder=7)
                ax.plot([p_face[0], p_ext[0]], [p_face[1], p_ext[1]], color="#15191E", lw=0.94, solid_capstyle="round", zorder=8)
                ax.scatter([p_face[0]], [p_face[1]], s=9.5, facecolor="white", edgecolor="#15191E", lw=0.72, zorder=9)
            else:
                # Back-facing puncture: dashed behind the translucent crystal until exiting silhouette, then solid!
                t_exit = ray_exit_silhouette_2d(p_face, dir2d, V_world[:, :2])
                p_exit = p_face + dir2d * t_exit
                p_ext = p_exit + dir2d * (0.48 * scale)
                ax.plot([cx, p_face[0]], [0.0, p_face[1]], color="#15191E", lw=0.76, ls=(0, (2.6, 2.4)), alpha=0.85, zorder=5)
                ax.plot([p_face[0], p_exit[0]], [p_face[1], p_exit[1]], color="#242A30", lw=0.72, ls=(0, (2.0, 2.4)), alpha=0.68, zorder=5)
                ax.plot([p_exit[0], p_ext[0]], [p_exit[1], p_ext[1]], color="#15191E", lw=0.94, solid_capstyle="round", zorder=8)
                ax.scatter([p_face[0]], [p_face[1]], s=7.5, facecolor="white", edgecolor="#3A424B", lw=0.65, alpha=0.80, zorder=6)

    # Crisp front ink wireframe edges
    for e in EDGES:
        adj = edge_adj[e]
        vis = any(fi in front_faces for fi in adj)
        if not vis:
            continue
        is_silhouette = len([fi for fi in adj if fi in front_faces]) == 1
        p1, p2 = V_world[e[0], :2], V_world[e[1], :2]
        lw = 1.24 if is_silhouette else 1.04
        ax.plot(
            [p1[0], p2[0]], [p1[1], p2[1]],
            color="#101418", lw=lw, solid_capstyle="round", solid_joinstyle="round", zorder=7,
        )

    # Central black intertwiner dot
    ax.scatter([cx], [0.0], s=17, c="#101418", linewidths=0, zorder=10)
    return p_l[0], p_r[0]


# Four lively, distinct, mathematically verified 3D poses (zero flat-bottom repetition)
ROTATIONS = [
    ( 18.0, -14.0,  32.0),   # Tilted upright 2-face crystal
    ( 48.0, -28.0, 162.0),   # Dramatic inverted 3-face apex-down pyramid
    (-26.0,  68.0, -62.0),   # Sweeping diagonal 2-face crystal
    (-42.0,  26.0,  18.0),   # Tilted asymmetric 3-face crystal
]


def render_minimal():
    verify_rotations(ROTATIONS)

    fig, ax = plt.subplots(figsize=(11.6, 3.55), dpi=300)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    centers = [-4.05, -1.35, 1.35, 4.05]
    scale = 1.02
    rng = np.random.default_rng(20261128)

    punctures = []
    for cx, rot in zip(centers, ROTATIONS):
        plx, prx = draw_penrose_tetrahedron(ax, cx, scale, rot, rng, mode="minimal")
        punctures.append((plx, prx))

    segments = [(-5.55, punctures[0][0])]
    for i in range(len(punctures) - 1):
        segments.append((punctures[i][1], punctures[i + 1][0]))
    segments.append((punctures[-1][1], 5.55))

    for x0, x1 in segments:
        ax.plot([x0, x1], [0.0, 0.0], color="#101418", lw=1.06, solid_capstyle="round", zorder=8)

    ax.set_xlim(-5.85, 5.85)
    ax.set_ylim(-1.60, 1.60)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)

    pdf_path = OUT_DIR / "penrose-chain-minimal.pdf"
    png_path = OUT_DIR / "penrose-chain-minimal.png"
    fig.savefig(pdf_path, facecolor="white")
    fig.savefig(png_path, dpi=300, facecolor="white")
    plt.close(fig)
    print(f"Saved {pdf_path.name} and {png_path.name}")


def render_four_valent():
    verify_rotations(ROTATIONS)

    fig, ax = plt.subplots(figsize=(12.2, 4.05), dpi=300)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    centers = [-4.35, -1.45, 1.45, 4.35]
    scale = 0.94
    rng = np.random.default_rng(20261129)

    punctures = []
    for cx, rot in zip(centers, ROTATIONS):
        plx, prx = draw_penrose_tetrahedron(ax, cx, scale, rot, rng, mode="4valent")
        punctures.append((plx, prx))

    segments = [(-5.85, punctures[0][0])]
    for i in range(len(punctures) - 1):
        segments.append((punctures[i][1], punctures[i + 1][0]))
    segments.append((punctures[-1][1], 5.85))

    for x0, x1 in segments:
        ax.plot([x0, x1], [0.0, 0.0], color="#101418", lw=1.04, solid_capstyle="round", zorder=8)

    # Sleek, small Penrose-ink edge blocks on the 3 shared links
    link_mids = [0.5 * (punctures[i][1] + punctures[i + 1][0]) for i in range(3)]
    bw, bh = 0.36, 0.28

    for idx, mx in enumerate(link_mids):
        if idx == 1:
            halo = FancyBboxPatch(
                (mx - bw / 2 - 0.09, -bh / 2 - 0.09), bw + 0.18, bh + 0.18,
                boxstyle="round,pad=0.02,rounding_size=0.09",
                facecolor="#F5C99A", edgecolor="none", alpha=0.35, zorder=9,
            )
            ax.add_patch(halo)
            ax.plot([mx, mx], [bh / 2, 1.28], color="#A84C12", lw=1.55, solid_capstyle="round", zorder=10)
            ax.scatter([mx], [1.28], s=17, c="#A84C12", linewidths=0, zorder=11)
            ax.text(mx, 1.38, r"$M$", fontsize=10.5, color="#8A3B0A", ha="center", va="bottom", zorder=11)

            box = FancyBboxPatch(
                (mx - bw / 2, -bh / 2), bw, bh,
                boxstyle="round,pad=0.0,rounding_size=0.06",
                facecolor="#FFF3E3", edgecolor="#A84C12", lw=1.08, zorder=11,
            )
            ax.add_patch(box)
            ax.text(mx, -0.01, r"$E$", fontsize=9.8, color="#8A3B0A", ha="center", va="center", zorder=12)
            ax.text(mx, -bh / 2 - 0.12, r"$e$", fontsize=9.0, color="#8A3B0A", ha="center", va="top", zorder=12)
        else:
            box = FancyBboxPatch(
                (mx - bw / 2, -bh / 2), bw, bh,
                boxstyle="round,pad=0.0,rounding_size=0.06",
                facecolor="#EDF7F6", edgecolor="#1B6663", lw=0.96, zorder=11,
            )
            ax.add_patch(box)
            ax.text(mx, -0.01, r"$\epsilon$", fontsize=9.8, color="#124A47", ha="center", va="center", zorder=12)

    ax.text(-6.05, 0.0, r"$\cdots$", fontsize=11.5, color="#4A5560", ha="right", va="center")
    ax.text( 6.05, 0.0, r"$\cdots$", fontsize=11.5, color="#4A5560", ha="left",  va="center")

    ax.set_xlim(-6.55, 6.55)
    ax.set_ylim(-1.76, 1.78)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)

    pdf_path = OUT_DIR / "penrose-chain-4valent.pdf"
    png_path = OUT_DIR / "penrose-chain-4valent.png"
    fig.savefig(pdf_path, facecolor="white")
    fig.savefig(png_path, dpi=300, facecolor="white")
    plt.close(fig)
    print(f"Saved {pdf_path.name} and {png_path.name}")


if __name__ == "__main__":
    render_minimal()
    render_four_valent()
