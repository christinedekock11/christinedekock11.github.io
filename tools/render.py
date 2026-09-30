import json, pathlib, math, html
SC = pathlib.Path(__file__).resolve().parent
d = json.load(open(SC/"graph.json"))
ME = "Christine de Kock"

W, H = 1080, 760
PADX, PADY = 150, 58          # room for labels at the edges
N = {n["id"]: n for n in d["nodes"]}
xs = [v["x"] for v in N.values()]; ys = [v["y"] for v in N.values()]
x0, x1 = min(xs), max(xs); y0, y1 = min(ys), max(ys)
sx = lambda x: PADX + (x - x0) / (x1 - x0) * (W - 2 * PADX)
sy = lambda y: PADY + (y - y0) / (y1 - y0) * (H - 2 * PADY)
P = {k: (sx(v["x"]), sy(v["y"])) for k, v in N.items()}
rad = lambda n: 13 if n == ME else 3.4 + 2.9 * math.sqrt(N[n]["papers"] - 1)

out = [f'<svg class="coauthors" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
       f'role="img" aria-labelledby="cg-title"><title id="cg-title">Co-authorship network: '
       f'{d["n_papers"]} papers, {d["n_total"]} co-authors</title>']

# edges, heaviest last
out.append('<g class="edges">')
for u, v, w in sorted(d["edges"], key=lambda e: e[2]):
    x1, y1 = P[u]; x2, y2 = P[v]
    cls = "e-me" if ME in (u, v) else "e-co"
    out.append(f'<line class="{cls}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
               f'stroke-width="{min(0.5 + 0.55 * w, 3.2):.2f}"/>')
out.append('</g>')

# labels: push apart vertically within each half
labels = []
for n in N:
    if n == ME: continue
    x, y = P[n]
    right = x >= W / 2
    labels.append({"n": n, "x": x + (rad(n) + 6) * (1 if right else -1), "y": y, "right": right})
for side in (True, False):
    grp = sorted([l for l in labels if l["right"] == side], key=lambda l: l["y"])
    for _ in range(400):
        moved = False
        for i in range(len(grp) - 1):
            a, b = grp[i], grp[i + 1]
            gap = b["y"] - a["y"]
            if gap < 13.5 and abs(a["x"] - b["x"]) < 150:
                shift = (13.5 - gap) / 2
                a["y"] -= shift; b["y"] += shift; moved = True
        if not moved: break

out.append('<g class="nodes">')
for n in N:
    if n == ME: continue
    x, y = P[n]
    out.append(f'<circle class="node" cx="{x:.1f}" cy="{y:.1f}" r="{rad(n):.1f}">'
               f'<title>{html.escape(n)} — {N[n]["papers"]} paper'
               f'{"s" if N[n]["papers"] > 1 else ""}</title></circle>')
for l in labels:
    n = l["n"]
    cls = "lbl strong" if N[n]["papers"] >= 2 else "lbl"
    out.append(f'<text class="{cls}" x="{l["x"]:.1f}" y="{l["y"]:.1f}" '
               f'text-anchor="{"start" if l["right"] else "end"}" dominant-baseline="middle">'
               f'{html.escape(n)}</text>')
mx, my = P[ME]
out.append(f'<circle class="me" cx="{mx:.1f}" cy="{my:.1f}" r="{rad(ME)}"><title>{ME}</title></circle>')
out.append(f'<text class="lbl me-lbl" x="{mx:.1f}" y="{my - rad(ME) - 9:.1f}" text-anchor="middle">Christine de Kock</text>')
out.append('</g></svg>')

(SC/"coauthors.svg").write_text("\n".join(out), encoding="utf-8")
print("nodes:", len(N), "edges:", len(d["edges"]), "| bytes:", len("\n".join(out)))
