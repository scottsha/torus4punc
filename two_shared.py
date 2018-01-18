import json
# import tandard as tt
import listermergetwosthrees
import networkx as nx
import time
timestr = time.strftime("%d%H%M%S")

with open('octagons.json', 'r') as infile:
    octagons = json.load(infile)

with open('bases.json','r') as infile:
    octabase = json.load(infile)

print(len(octagons), ' octagons coming in')

with open('knowntwosthrees.json') as knownfile:
    knownlist = json.load(knownfile)

disjoints = []
threes = set()
twos = set()

for foo in knownlist:
    if foo[0] == 0:
        atwo = tuple(foo[1:13])
        athree = tuple(foo[13::])
        threes.add( athree )
        twos.add( atwo )
        disjoints.append( (athree, atwo)  )

print(len(threes), 'Three')
print(len(twos), 'Twoin')

threes = sorted( list(threes), key = lambda x: tt.curve_sort_key(x) )
twos = sorted( list(twos), key = lambda x: tt.curve_sort_key(x) )
H23 = nx.Graph()
for foo in disjoints:
    i3 = threes.index(foo[0])
    i2 = twos.index(foo[1])
    H23.add_edge((3,i3),(2,i2))

print(H23.number_of_edges(), 'edges in 23graph')
print(H23.number_of_nodes(), 'nodes in 23graph')


abad = False
for oct in octagons:
    for foo in range(-2,6,2):
        xi = tuple(oct[foo])
        xip1 = tuple(oct[foo+2])
        vi = threes.index(xi)
        vj = threes.index(xip1)
        paths = [foo for foo in nx.all_simple_paths(H23, (3,vi), (3,vj), cutoff=2) ]
        ii = len(paths)
        if ii!=1:
            print(ii, xi, 'bad', xip1)
            print(oct)
            abad = True


if abad:
    print('I saw bads. ')
else:
    print('I saw no bads. Everyone has a unique 2-curve.')