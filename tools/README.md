# Co-authorship graph

`papers.json` is the data: one entry per paper with its full author list.
Author lists came from Semantic Scholar, arXiv and the ACL Anthology.

To regenerate the figure after adding a paper to `papers.json`:

    python3 graph.py     # trims, builds the network, runs the spring layout -> graph.json
    python3 render.py    # writes coauthors.svg

Then paste the contents of `coauthors.svg` into the `<figure class="graph">`
block in `../index.html`, replacing the previous `<svg>`, and update the counts
in the figcaption (printed by `graph.py`).

Trimming: a paper with more than 8 authors counts as a large collaboration.
From those, only people appearing on 3+ papers get a node, and no
author-to-author edges are drawn — otherwise the SemEval and BRIGHTER
consortia bury everyone else. Requires networkx.
