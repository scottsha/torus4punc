import tandard as tt

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

def mod_orbit( base, N ):
    orbit = base[::]
    que = base[::]
    for foo in range(N):
        cc = que.pop(0)
        cd=cc[::]
        cinv = tt.involution(cc)
        if cinv not in orbit:
            orbit.append(cinv)
            if cd not in que:
                que.append(cinv)
        for foo in range(3):
            cd = tt.order4rotate(cd)
            if cd not in orbit:
                orbit.append( cd )
                if cd not in que:
                    que.append( cd )
        for g in nonsep:
            ct = tt.dehn_twist( g, cc )
            if ct not in orbit:
                orbit.append( ct )
                if ct not in que:
                    que.append( ct )
        for g in nonsep:
            ct = tt.dehn_twist(g, cc, -1)
            if ct not in orbit:
                orbit.append(ct)
                if ct not in que:
                    que.append(ct)
        for e in [12,3,6,9]:
            for pow in [-1,1]:
                ct = tt.braid( cc, e, pow)
            if ct not in orbit:
                orbit.append(ct)
                if ct not in que:
                    que.append(ct)
    return orbit

orbsize = 50



threes = mod_orbit( [base3,x0,x1,x2,x3], orbsize)
fours = mod_orbit( [base4,y0,y1,y2,y3], orbsize)

n3 = len(threes)
n4 = len(fours)
toat = n3*n4

with open('threes.txt','a') as file:
    for foo in range(n3):
        file.write( str(foo)+'\n'+str(threes[foo])+'\n\n')

with open('fours.txt','a') as file:
    for foo in range(n4):
        file.write( str(foo)+'\n'+str(fours[foo])+'\n\n')


with open('edges.txt','a') as file:
    edges=[]
    for foo in range(n3):
        for bar in range(n4):
            a=threes[foo]
            b=fours[bar]
            print(foo,' of ',n3, ' and ' , bar, 'of', n4)
            it=tt.geo_intersect( a, b)
            # jt=tt.geo_intersect( b, a)
            # if it!=jt: print(it,jt, 'CRISIS')
            if it == 0:
                edges.append((foo, bar))
                file.write(str(foo) + "," + str(bar) + "\n")
    print(len(edges))


