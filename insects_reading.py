import networkx as nx
import json
f=open('isects11Jan.txt','r')

disjoints=[]
threes=[]
fours=[]
lino=True
while lino:
    lino = f.readline()
    try:
        ii = int(lino)
        pat3in = f.readline()
        pat3 = tuple([int(foo) for foo in pat3in.split(',')])
        pat4in = f.readline()
        pat4 = tuple([int(foo) for foo in pat4in.split(',')])
        if ii == 0:
            disjoints.append( (pat3, pat4) )
            if pat3 not in threes:
                threes.append(pat3)
            if pat4 not in fours:
                fours.append(pat4)
    except ValueError:
        continue
f.close()
print(len(threes), 'Three')
print(len(fours),'Fourin')

threes.sort()
fours.sort()
G = nx.Graph()
for foo in disjoints:
    ti = threes.index(foo[0])
    fi = fours.index(foo[1])
    G.add_edge((0,ti),(1,fi))

print(G.number_of_edges())
print(G.number_of_nodes())


def neighs_at_dist(graph,  vertex, distance):
    dist_from = nx.shortest_path_length( graph, source = vertex)
    neighs = [foo for (foo,bar) in dist_from.items() if bar==distance]
    return neighs


def lexigraphic_less( ipat0, ipat1 ):
    s0 = sum(ipat0)
    s1 = sum(ipat1)
    if s0<s1:
        return True
    elif s0>s1:
        return False
    else:
        for foo, bar in zip(ipat0,ipat1):
            if foo>bar:
                return False
            elif foo<bar:
                return True
        return False


def cannoctagon ( oct ):
    oo = oct[::]
    leastat = 0
    for foo in range(2,8,2):
        if lexigraphic_less( oct[foo], oct[leastat] ):
            leastat = foo
    if lexigraphic_less( oct[(leastat +2)%8], oct[(leastat +6)%8] ):
        return [ oct[(leastat+foo)%8] for foo in range(8) ]
    else:
        return [oct[(leastat + foo) % 8] for foo in range(8,0,-1)]



# octogons=[]
#
# for x0 in usedthrees:
#     d4t0 = neighs_at_dist(G, x0, 4)
#     for x2 in d4t0:
#         d2x0 = neighs_at_dist(G, x0, 2)
#         d2x3 = neighs_at_dist(G, x2, 2)
#         x13s = [foo for foo in d2x0 if foo in d2x3]
#         for x1 in x13s:
#             p = nx.shortest_path(G, source=x0, target=x1)
#             y0 = p[1]
#             p = nx.shortest_path(G, source=x1, target=x2)
#             y1 = p[1]
#             H=G.copy()
#             H.remove_node(y0)
#             H.remove_node(x1)
#             H.remove_node(y1)
#             for x3 in x13s:
#                 if x3!=x1:
#                     try:
#                         p=nx.shortest_path(H, source=x0, target=x3)
#                         y3 = p[1]
#                         p=nx.shortest_path(H, source=x3, target=x2)
#                         y2 = p[1]
#                     except:
#                         continue
#                     oct = [x0,y0,x1,y1,x2,y2,x3,y3]
#                     octo = []
#                     for o in oct:
#                         try:
#                             ipat = threedict[o]
#                         except KeyError:
#                             ipat = fourdict[o]
#                         octo.append(ipat)
#                     octo = cannoctagon(octo)
#                     if (octo not in octogons):
#                         octogons.append(octo)

max3deg = 0
max3 = False
for foo, doo in G.degree():
    if doo>max3deg:
        max3 = foo
        max3deg = doo

x0=max3

octogons=[]

for x0 in [(0,0),(0,1),(0,7),(0,61),(0,78),(0,95),(0,137)]:
    d4t0 = neighs_at_dist(G, x0, 4)
    for x2 in d4t0:
        d2x0 = neighs_at_dist(G, x0, 2)
        d2x3 = neighs_at_dist(G, x2, 2)
        x13s = [foo for foo in d2x0 if foo in d2x3]
        for x1 in x13s:
            p = nx.shortest_path(G, source=x0, target=x1)
            y0 = p[1]
            p = nx.shortest_path(G, source=x1, target=x2)
            y1 = p[1]
            H=G.copy()
            H.remove_node(y0)
            H.remove_node(x1)
            H.remove_node(y1)
            for x3 in x13s:
                if x3!=x1:
                    try:
                        p=nx.shortest_path(H, source=x0, target=x3)
                        y3 = p[1]
                        p=nx.shortest_path(H, source=x3, target=x2)
                        y2 = p[1]
                    except:
                        continue
                    oct = [x0,y0,x1,y1,x2,y2,x3,y3]
                    octo = []
                    for foo in range(8):
                        o = oct[foo]
                        if foo%2==0:
                            ipat = threes[o[1]]
                        else:
                            ipat = fours[o[1]]
                        octo.append(ipat)
                    octo = cannoctagon(octo)
                    if (octo not in octogons):
                        octogons.append(octo)

print(len(octogons))

with open('octogons.json', 'w') as outfile:
    json.dump(octogons, outfile)
