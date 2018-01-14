import json
import tandard as tt
import time
import listermergetwosthrees
timestr = time.strftime("%d%H%M%S")

with open('octagons.json', 'r') as infile:
    octagons = json.load(infile)

with open('bases.json','r') as infile:
    octabase = json.load(infile)

print(len(octagons), ' octagons coming in')

octathrees = []
for oct in octagons:
    for foo in range(0,8,2):
        athree = tuple(oct[foo])
        if athree not in octathrees:
            octathrees.append(athree)

num_threes = len(octathrees)
print(num_threes, 'three-curves in these octagons')

base2 = (0,0,0,1,0,1,0,2,2,1,2,1)
twos_orb_size = 500

twos = tt.mod_orbit([base2], twos_orb_size)
twos.sort(key = lambda x: tuple([sum(x)])+x)
num_twos = len(twos)
print( num_twos, 'two-curves check against')


with open('knowntwosthrees.json') as knownfile:
    knownlist = json.load(knownfile)

known_twosthrees = set([tuple(foo[1::]) for foo in knownlist])

try:
    fileis = open('twothreeisects'+timestr+'.txt','a')
    for foo, atwo in enumerate(twos):
        for bar, athree in enumerate(octathrees):
            if atwo+athree not in known_twosthrees:
                if not tt.obvious_intersection(atwo, athree):
                    print(foo, ' of ', num_twos, ' and ', bar, 'of', num_threes)
                    it=tt.geo_intersect( atwo, athree)
                    fileis.write(str(it)+'\n')
                    stra = str(atwo)
                    fileis.write(stra[1:-1]+'\n')
                    strb = str(athree)
                    fileis.write(strb[1:-1]+'\n')
    fileis.close()
    print(len(edges))
except KeyboardInterrupt:
    fileis.close()
    print('No worries Ill jot this down.')

