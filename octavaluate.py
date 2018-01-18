import json
import tandard as tt
from itertools import combinations

with open('octagons.json', 'r') as infile:
    octagons = json.load(infile)

with open('bases.json','r') as infile:
    octabase = json.load(infile)

octagons = [ tuple([ tuple(ipat) for ipat in oct]) for oct in octagons]
print(len(octagons), ' octagons coming in')



def pts_outside_3curve( ipat ):
    with0 = []
    if ipat[0]%2 == 0:
        with0.append(1)
    if (ipat[0]+ipat[3])%2 == 0:
        with0.append(2)
    if ipat[9]%2 == 0:
        with0.append(3)
    if with0 == []:
        return 0
    else:
        for foo in range(1,4):
            if foo not in with0:
                return foo

knownins = []
storedisects = dict()


def isect_pattern( octagon ):
    a=[]
    for foo, bar in combinations([0,2,4,6],2):
        pair = tuple((octagon[foo], octagon[bar]))
        if pair in storedisects:
            ii=storedisects[pair]
        else:
            ii=tt.geo_intersect(*pair)
            storedisects[pair]=ii
        a.append( ii )
    for foo, bar in combinations([1,3,5,7],2):
        pair = (octagon[foo], octagon[bar])
        if pair in storedisects:
            ii=storedisects[pair]
        else:
            ii=tt.geo_intersect(*pair)
            storedisects[pair]=ii
        a.append( ii )
    return tuple(a)



observe_ptype = set()
observe_itype = set()
numo = len(octagons)
for foo,oct in enumerate(octagons):
    if (foo%10==0): print((100*foo)//numo, '% complete')
    pttype = tuple([pts_outside_3curve(foo) for ct, foo in enumerate(oct) if ct % 2 == 0])
    ittype = isect_pattern(oct)
    observe_ptype.add(pttype)
    if ittype not in observe_itype:
        observe_itype.add(ittype)
        print('oct number', foo)
        print(ittype, pttype)
        print(oct)
        print('/n')

for sawi in observe_itype:
    print( sawi )

for sawp in observe_ptype:
    print( sawp )


for foo in storedisects.keys():
    knownins.append( foo[0]+foo[1]+tuple([storedisects[foo]]) )

with open('knowninocts.json', 'w') as outfile:
    json.dump(knownins, outfile)
