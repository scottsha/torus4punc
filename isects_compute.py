import tandard as tt
import listermerger
import json
import time
timestr = time.strftime("%d%H%M%S")

#This octogon has pt type 0,0,1,1
x0 = (1,2,1,1,2,3,0,2,2,2,2,2)
y0 = (0,2,2,0,2,2,0,2,2,2,2,2)
x1 = (1,2,3,1,2,1,0,2,2,2,2,2)
y1 = (2,4,6,2,4,2,0,2,2,2,2,2)
x2 = (1,2,3,2,2,2,0,2,2,1,2,1)
y2 = (0,2,2,2,2,2,0,2,2,0,2,2)
x3 = (1,2,1,2,2,2,0,2,2,1,2,3)
y3 = (2,4,2,2,4,4,0,2,2,2,2,4)
thirdheat = [x0,y0,x1,y1,x2,y2,x3,y3]


eb3 = (1,2,4,5,7,8,-6,-7,-5,-4,-2,-1,-11,9)
base3 = tt.normal_coord( eb3 )
# print( base3 )
eb4 = (1,2,4,5,7,8,10,11,-9,-10,-8,-7,-5,-4,-2,-1,-11,9)
base4 = tt.normal_coord( eb4 )
# print( base4 )
cb3 = tt.curve(base3)
rcb3 = tt.curve( tt.order4rotate(base3) )
cb4 = tt.curve(base4)
# tt.curvesplot( [cb3, rcb3] )
# tt.curveplot( cb3 )

a0=(1,0,1,0,0,0,0,0,0,0,0,0)
a9=tt.order4rotate(a0)
a6=tt.order4rotate(a9)
a3=tt.order4rotate(a6)
a1=(0,1,1,0,1,1,0,1,1,0,1,1)

nonsep = [a1,a0,a3,a6,a9]


anice3 = (1,0,1,0,2,2,0,2,2,1,2,1)
wild = (6,4,8,0,4,4,1,4,5,3,4,1)

wild4 = (6,4,8,0,4,4,0,4,4,2,4,2)
buck4 = (6,4,8,0,4,4,2,4,6,4,4,0)
style4 = (6,4,8,0,6,6,2,6,8,4,6,2)
cryal4 = (6,6,8,0,4,4,2,4,6,4,6,2)
mile4 = (0,2,2,0,2,2,2,2,4,2,2,2)
bile4 = (0,2,2,0,2,2,2,2,2,2,2,0)
qile4 = (0,2,2,0,2,2,2,2,2,2,2,4)


buck = (3,2,5,0,4,4,2,4,6,3,4,1)
style = (5,2,7,0,4,4,2,4,6,3,4,1)
cryal = (3,4,3,0,2,2,2,2,4,3,4,1)
mile = (1,0,1,0,2,2,2,2,4,1,2,1)
bile = (1,2,3,0,2,2,2,2,2,3,2,1)
qile = (1,2,1,0,2,2,2,2,2,1,2,1)


print('Thinking of curves')
# threes = tt.mod_orbit( [wild,anice3,buck,style,cryal,mile,bile,qile], orbsize)
# dehn_gens=[], braid_gens=[12,3,6,9,2,5,8,11] )
# threes = tt.mod_orbit( [base3], orbsize)
orbsize = 4
threes = tt.subgroup_orbit([base3], 500*orbsize, dehn_gens=[], braid_gens=[12,3,6,9])
#  fours = tt.subgroup_orbit( [base4], orbsize, dehn_gens=[a1,a6,a9], braid_gens=[12,3])
fours = tt.mod_orbit([base4], orbsize)
print('Sort these loopy boys')
# threes.sort(key = lambda x: tt.curve_sort_key(x))
# fours.sort(key = lambda x: tt.curve_sort_key(x))

n3 = len(threes)
n4 = len(fours)

toat = n3*n4

# with open('threes.txt','a') as file:
#     for foo in range(n3):
#         file.write( str(foo)+'\n'+str(threes[foo])+'\n\n')
#
# with open('fours.txt','a') as file:
#     for foo in range(n4):
#         file.write( str(foo)+'\n'+str(fours[foo])+'\n\n')

with open('knownintersections.json') as knownfile:
    knownlist = json.load(knownfile)

known_intersections = set([tuple(foo[1::]) for foo in knownlist])

try:
    fileis = open('extraisects'+timestr+'.txt','a')
    for foo in range(n3):
        for bar in range(n4):
            a=threes[foo]
            b=fours[bar]
            if a+b not in known_intersections:
                if not tt.obvious_intersection(a, b):
                    print(foo, ' of ', n3, ' and ', bar, 'of', n4)
                    # it=tt.geo_intersect( a, b)
                    if tt.is_disjoint_curves(a,b):
                        it=0
                        fileis.write(str(it)+'\n')
                        stra = str(a)
                        fileis.write(stra[1:-1]+'\n')
                        strb = str(b)
                        fileis.write(strb[1:-1]+'\n')
    fileis.close()
except KeyboardInterrupt:
    fileis.close()
    print('No worries Ill jot this down.')

