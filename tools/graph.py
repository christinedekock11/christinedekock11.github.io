import json, pathlib, collections, random
import networkx as nx
SC = pathlib.Path(__file__).resolve().parent
ME, BIG = "Christine de Kock", 8

papers = json.load(open(SC/"papers.json"))
count = collections.Counter(a for p in papers for a in p["authors"] if a != ME)

kept, folded = set(), 0
for p in papers:
    big = len(p["authors"]) > BIG
    for a in p["authors"]:
        if a == ME: continue
        if not big or count[a] >= 3: kept.add(a)
        else: folded += 1

G = nx.Graph()
G.add_node(ME, papers=len(papers))
for a in kept: G.add_node(a, papers=count[a])
for p in papers:
    big = len(p["authors"]) > BIG
    auth=[a for a in p["authors"] if a in kept]
    for a in auth:
        G.add_edge(ME, a, weight=G.get_edge_data(ME,a,{}).get("weight",0)+1)
    for i,x in enumerate(auth):
        for y in auth[i+1:]:
            G.add_edge(x, y, weight=G.get_edge_data(x,y,{}).get("weight",0)+1)

# Edges are drawn at their true co-authorship count, but a 48-author paper is a
# clique whose pull would collapse that whole group onto one point. For the
# layout only, damp author-to-author ties so the cluster stays legible.
for u, v, d in G.edges(data=True):
    d["lw"] = d["weight"] if ME in (u, v) else d["weight"] * 0.18

random.seed(11)
pos = nx.spring_layout(G, weight="lw", k=1.15, iterations=1800, seed=11)
cx, cy = pos[ME]
pos = {n:(x-cx, y-cy) for n,(x,y) in pos.items()}
m = max(max(abs(x),abs(y)) for x,y in pos.values())
pos = {n:(x/m, y/m) for n,(x,y) in pos.items()}
json.dump({"nodes":[{"id":n,"papers":G.nodes[n]["papers"],
                     "x":round(pos[n][0],4),"y":round(pos[n][1],4)} for n in G],
           "edges":[[u,v,d["weight"]] for u,v,d in G.edges(data=True)],
           "folded":folded,"n_total":len(count),"n_papers":len(papers)},
          open(SC/"graph.json","w"), indent=1, ensure_ascii=False)
print(f"nodes {len(G)} (of {len(count)} co-authors), edges {G.number_of_edges()}, folded {folded}")
