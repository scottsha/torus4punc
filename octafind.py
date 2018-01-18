import networkx as nx
import json
import os
from itertools import combinations


with open('knownintersections.json','r') as knownfile:
    knownlist = json.load(knownfile)

disjoints = []
threes = set()
fours = set()

for foo in knownlist:
    if foo[0] == 0:
        athree = tuple(foo[1:13])
        afour = tuple(foo[13::])
        threes.add( athree )
        fours.add( afour )
        disjoints.append( (athree, afour)  )

# lino=True
# while lino:
#     lino = f.readline()
#     try:
#         ii = int(lino)
#         pat3in = f.readline()
#         pat3 = tuple([int(foo) for foo in pat3in.split(',')])
#         pat4in = f.readline()
#         pat4 = tuple([int(foo) for foo in pat4in.split(',')])
#         if ii == 0:
#             disjoints.append( (pat3, pat4) )
#             if pat3 not in threes:
#                 threes.append(pat3)
#             if pat4 not in fours:
#                 fours.append(pat4)
#     except ValueError:
#         continue
# f.close()
print(len(threes), 'Three')
print(len(fours),'Fourin')

threes = sorted( list(threes), key = lambda x: tuple([sum(x)])+x )
fours = sorted( list(fours), key = lambda x: tuple([sum(x)])+x )
G = nx.Graph()
for foo in disjoints:
    ti = threes.index(foo[0])
    fi = fours.index(foo[1])
    G.add_edge((0,ti),(1,fi))

print(G.number_of_edges(), 'edges in G')
print(G.number_of_nodes(), 'nodes in G')


def neighs_at_dist(graph,  vertex, distance):
    dist_from = nx.shortest_path_length( graph, source = vertex)
    neighs = [foo for (foo,bar) in dist_from.items() if bar==distance]
    return neighs


def octagon_wrapper( oct ):
    a = ()
    for pat in oct:
        a+=tt.curve_sort_key(ipat)
    b = (sum(a),)+a
    return tuple(b)

def cannoctagon ( oct ):
    sameocts = []
    for foo in range(4):
        sameocts.append( oct[2*foo:]+oct[:2*foo] )
    reved = []
    for foo in sameocts:
        reved.append( foo[::-1] )
    sameocts+=reved
    low = min(sameocts, key = lambda x: octagon_wrapper(x) )
    return tuple(low)

max3deg = 0
max3 = False
for foo, doo in G.degree():
    if doo>max3deg:
        max3 = foo
        max3deg = doo

x0=max3

octogons=[]

bases = [max3]

for x0 in bases:
    d4t0 = neighs_at_dist(G, x0, 4)
    print('considering', len(d4t0), 'possible x2')
    for x2 in d4t0:
        d2x0 = neighs_at_dist(G, x0, 2)
        d2x3 = neighs_at_dist(G, x2, 2)
        x13s = [foo for foo in d2x0 if foo in d2x3]
        for x1,x3 in combinations(x13s,2):
            p = nx.shortest_path(G, source=x0, target=x1)
            y0 = p[1]
            p = nx.shortest_path(G, source=x1, target=x2)
            y1 = p[1]
            H=G.copy()
            H.remove_node(y0)
            H.remove_node(x1)
            H.remove_node(y1)
            try:
                p=nx.shortest_path(H, source=x0, target=x3)
                y3 = p[1]
                p=nx.shortest_path(H, source=x3, target=x2)
                y2 = p[1]
            except:
                continue
            oct = (x0,y0,x1,y1,x2,y2,x3,y3)
            octo = []
            for foo in range(8):
                o = oct[foo]
                if foo%2==0:
                    ipat = threes[o[1]]
                else:
                    ipat = fours[o[1]]
                octo.append(ipat)
            octo = cannoctagon(tuple(octo))
            if (octo not in octogons):
                octogons.append(octo)

print(len(octogons), 'octagons found based at', x0, threes[x0[1]])

octogons.sort(key = lambda x: octagon_wrapper(x))

with open('octagons.json', 'w') as outfile:
    json.dump(octogons, outfile)

with open('bases.json','w') as outfile:
    json.dump([threes[foo[1]] for foo in bases], outfile)