import networkx as nx
import json


threelist=[]
threedict={}
f=open('threes.txt','r')
liney = f.readline()
while liney:
    v = 't'+str(int( liney ))
    threelist.append( v )
    liney=f.readline()
    lin = liney[1:-2]
    ipat = tuple( [int(foo) for foo in lin.split(', ')] )
    threedict[ v ] = ipat
    liney=f.readline()
    liney=f.readline()
f.close()


fourlist=[]
fourdict={}
f=open('fours.txt','r')
liney = f.readline()
while liney:
    v = 'f'+str(int( liney ))
    fourlist.append( v )
    liney=f.readline()
    lin = liney[1:-2]
    ipat = tuple( [int(foo) for foo in lin.split(', ')] )
    fourdict[ v ] = ipat
    liney=f.readline()
    liney=f.readline()
f.close()

usedthrees=[]
edges=[]
f=open('edges.txt','r')
for line in f:
    x=line.split(',')
    v = 't'+str(int(x[0]))
    w = 'f'+str(int(x[1]))
    edges.append( (v,w) )
    usedthrees.append(v)
f.close()

G = nx.Graph()
Gno0 = nx.Graph()

for e in edges:
    G.add_edge(*e)
    Gno0.add_edge(*e)

Gno0.remove_node('t0')


def neighs_at_dist(graph,  vertex, distance):
    dist_from = nx.shortest_path_length( graph, source = vertex)
    neighs = [foo for (foo,bar) in dist_from.items() if bar==distance]
    return neighs


def lexigraphic_less( ipat0, ipat1 ):
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


octogons=[]

for x0 in usedthrees:
    d4t0 = neighs_at_dist(G, x0, 4)
    for x2 in d4t0:
        d2x0 = neighs_at_dist(G, 't0', 2)
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
                    for o in oct:
                        try:
                            ipat = threedict[o]
                        except KeyError:
                            ipat = fourdict[o]
                        octo.append(ipat)
                    octo = cannoctagon(octo)
                    if (octo not in octogons):
                        octogons.append(octo)

print(len(octogons))

with open('octogons.json', 'w') as outfile:
    json.dump(octogons, outfile)
