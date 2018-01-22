import json
import tandard as tt
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


badds = []

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
            badds.append(xi)
            badds.append(xip1)


if abad:
    print('I saw bads. ')
    base2 = (0, 0, 0, 1, 0, 1, 0, 2, 2, 1, 2, 1)
    twos_orb_size = 3000
    twos = tt.mod_orbit([base2], twos_orb_size)
    twos.sort(key=lambda x: tt.curve_sort_key(x))
    num_twos = len(twos)
    num_threes = len(badds)
    print(num_twos, 'two-curves check against')

    known_twosthrees = set([tuple(foo[1::]) for foo in knownlist])

    try:
        fileis = open('twothreebads' + timestr + '.txt', 'a')
        for foo, atwo in enumerate(twos):
            for bar, athree in enumerate(badds):
                if atwo + athree not in known_twosthrees:
                    if not tt.obvious_intersection(atwo, athree):
                        print(foo, ' of ', num_twos, ' and ', bar, 'of', num_threes)
                        it = tt.geo_intersect(atwo, athree)
                        fileis.write(str(it) + '\n')
                        stra = str(atwo)
                        fileis.write(stra[1:-1] + '\n')
                        strb = str(athree)
                        fileis.write(strb[1:-1] + '\n')
        fileis.close()
    except KeyboardInterrupt:
        fileis.close()
        print('No worries Ill jot this down.')

else:
    print('I saw no bads. Everyone has a unique 2-curve.')