Why?
==========
PGP has a big problem. Who can we trust? You can't easily trust keys because:

1. Impersonation: A key that claims to be Obama might actually not be Obama, although most people won't believe a key that doesn't have any signatures.
2. Anyone can sign any key. The Obama Impersonator Key may create fake keys to sign itself to make it more believable.

**Goal:** How to assign trust to each node to result in the least violation score (see Details)?

Files Explaination
=========
Look at the **presentation.pdf** for an overview of this project

Run **evolutionAlg.py** plots will be saved in "plots"

You should change the parameters in the code.

Read the "paper.pdf" for details (for more rigor).

**Requires <a href="http://matplotlib.sourceforge.net/">Matplotlib</a>**

Key concepts: PGP, Web of Trust.


Details
==========
(from "presentation.pdf")

**Input:** 
1. Directed Graph of trust where node = key, edge = certification
2. Source node/key

Use Evolutionary Algorithm-->

**Output:** Trust assigned to each node/key (1 = trustworthy, 0 = not trust worthy) with respect to that source node (trust is in the eye of the beholder).


Our Algorithm Specifications
-------
The Web of Trust is represented by a Directed graph where 

- Trust is boolean: 1 = trustworthy. 0 = not trustworthy. 
- Keys has inforamtion on the Name it belongs to, the children keys, and trust
    - Good Key = keys of real people, matching their Names. Trust should = 1
    - Impersonated Keys = keys pretending to be a Good Key's person. Trust should = 0
    - Madeup Keys = keys pretending to be people who don't exist in the Good Keys (like Santa Claus). It's made by the same people who made the impersonated keys to sign the impersonted keys (to make the Impersonted Obama key look credible). Trust should = 0
- Nodes = keys
- Edges = A -- signed --> B's Key
- Person Group: All keys' claiming to be their Name (e.g. the Obama Person group are all keys, fake or real, claiming to be Obama)
    - In our policy, we make the real person inter-sign all the keys s/he has, so all the keys become 1 supernode. So every person group should have at most 1 real node.
- Violation Score: 1 signing violation point for each edge going from a Trust 1 to a Trust 0 key

**Goal:** How to assign trust to each node to result in the least violation score?

Output Plots:
---------
- Score Plot: Violation Score through generations.
- Trust Plot: The black and white plots signify the trust across generation, each generation is a row.
    The order of the keys go from left to right as: Good Key, Impersonated Keys, Madeup Keys

How?
--------
Read the comments in **evolutionAlg.py**.  For Generation 0, we randomly assign 0s and 1s. At every generation, we pick the assignments that has the lowest Violation Scores and randomly mutate them (1% chance of switching trust score) to produce the next generation. Note that this is asexual.

About
--------
For 6.857 class final project, by haoqili and linfei. We worked with H. Yang who did part 1, making PGP key signing with Android phone barcode scanner.
