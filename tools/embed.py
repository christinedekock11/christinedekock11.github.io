"""Drop the freshly rendered SVG and its counts into ../index.html."""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
svg = (HERE/"coauthors.svg").read_text(encoding="utf-8")
g = json.load(open(HERE/"graph.json"))
idx = HERE.parent/"index.html"
t = idx.read_text(encoding="utf-8")

t2, n = re.subn(r'<svg class="coauthors".*?</svg>', lambda _: svg, t, count=1, flags=re.S)
assert n == 1, "could not find the <svg class=\"coauthors\"> block"

caption = (f'Co-authorship across {g["n_papers"]} papers. Point size shows the number\n'
           f'  of joint papers; hover a point for the name and count. {g["n_total"]} people appear on\n'
           f'  those papers in total &mdash; the {g["folded"]} who appear only once, and only on a large\n'
           f'  multi-author collaboration, are left out to keep the picture readable.')
t2, n = re.subn(r'<figcaption>.*?</figcaption>', lambda _: f'<figcaption>{caption}</figcaption>',
                t2, count=1, flags=re.S)
assert n == 1, "could not find the figcaption"
idx.write_text(t2, encoding="utf-8")
print(f"embedded: {len(g['nodes'])} nodes, {len(g['edges'])} edges, {g['folded']} folded")
