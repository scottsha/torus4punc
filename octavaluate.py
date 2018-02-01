import json
import tandard as tt
from itertools import combinations
import matplotlib.pyplot as plt

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
with open('knowninocts.json', 'r') as infile:
    knowins = json.load(infile)

storedisects = dict()
for know_it in knowins:
    cc = tuple(know_it[0:12])
    cd = tuple(know_it[12:24])
    storedisects[(cc,cd)] = know_it[24]


def isect_pattern( octagon ):
    a=[]
    for foo, bar in [(0,2),(2,4),(4,6),(6,0),(0,4),(2,6)]:
        cc=octagon[foo]
        cd=octagon[bar]
        if tt.curve_sort_key(cc) < tt.curve_sort_key(cd):
            pair = (cc, cd)
        else:
            pair = (cd, cc)
        if pair in storedisects:
            ii=storedisects[pair]
        else:
            ii=tt.geo_intersect(*pair)
            storedisects[pair]=ii
        a.append( ii )
    for foo, bar in [(1,3),(3,5),(5,7),(7,1),(1,5),(3,7)]:
        cc=octagon[foo]
        cd=octagon[bar]
        if tt.curve_sort_key(cc) < tt.curve_sort_key(cd):
            pair = (cc, cd)
        else:
            pair = (cd, cc)
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
    if len(set(pttype))==2 and (ittype[4]>10 or ittype[5]>10):
        print(ittype, pttype)
        print(oct)
        print('')
    reped_pt = False
    for foo in range(4):
        if pttype[foo-1]==pttype[foo]:
            reped_pt=True
    if reped_pt:
        print('A repeater')
        print(ittype)
        print(oct)

for sawi in observe_itype:
    print( sawi )

for sawp in observe_ptype:
    print( sawp )


for foo in storedisects.keys():
    knownins.append( foo[0]+foo[1]+tuple([storedisects[foo]]) )

with open('knowninocts.json', 'w') as outfile:
    json.dump(knownins, outfile)
