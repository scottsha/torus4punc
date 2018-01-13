import json
import tandard as tt
from itertools import permutations

with open('octogons.json', 'r') as infile:
    octogons = json.load(infile)

print(len(octogons))

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

# oo = octogons[0]
# for octnum, oo in enumerate(octogons):
#     pttype = [ pts_outside_3curve(foo) for ct,foo in enumerate(oo) if ct%2==0]
#     print(pttype)
    # if pttype==[2,0,3,0]:
    #     print(octnum)
    #     for count,o in enumerate(oo):
    #         print(o)
    #     print('')

# odd_oct = octogons[37]
# for foo in range(0,8,2):
#     print( odd_oct[foo] )
#     tt.curveplot( tt.curve(odd_oct[foo]) )
# for foo in range(8):
#     print( tt.geo_intersect( odd_oct[foo-1], odd_oct[foo] ) )


# #This octogon has pt type 0,0,1,1
# x0 = (1,2,1,1,2,3,0,2,2,2,2,2)
# y0 = (0,2,2,0,2,2,0,2,2,2,2,2)
# x1 = (1,2,3,1,2,1,0,2,2,2,2,2)
# y1 = (2,4,6,2,4,2,0,2,2,2,2,2)
# x2 = (1,2,3,2,2,2,0,2,2,1,2,1)
# y2 = (0,2,2,2,2,2,0,2,2,0,2,2)
# x3 = (1,2,1,2,2,2,0,2,2,1,2,3)
# y3 = (2,4,2,2,4,4,0,2,2,2,2,4)
# thirdheat = [x0,y0,x1,y1,x2,y2,x3,y3]
#
# for foo, a in enumerate(thirdheat):
#     # c0=tt.middle_embedding( a )
#     # c1=tt.curve( thirdheat[foo-1] )
#     # # tt.curvesplot([c0,c1])
#     # print( tt.geo_intersect( thirdheat[foo-1], a) )

observed_ptype = [foo for foo in permutations(range(4),4)]
observed_ptype+= [(3,2,3,2), (3,0,3,0), (3,1,3,1), (2,0,2,0), (2,1,2,1), (2,3,2,3), (0,1,0,1), (0,3,0,3), (0,2,0,2),(1,0,1,0),(1,2,1,2),(1,3,1,3)]

for oct in octogons:
    a=[]
    for foo in range(-2,6,2):
        a.append( tt.geo_intersect(oct[foo], oct[foo+2]) )
    a=tuple(a)
    pttype = tuple([pts_outside_3curve(foo) for ct, foo in enumerate(oct) if ct % 2 == 0])
    if a!=(2,2,2,2):
        print('Intersection pattern is novel')
        print(oct)
        print(a)
        print('ptype', pttype)
    if pttype not in observed_ptype:
        print('Point compliment pattern is novel')
        print(oct)
        print(pttype)

