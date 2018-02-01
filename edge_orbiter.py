import tandard as tt
import time
# import json
timestr = time.strftime("%d%H%M%S")

eb3 = (1,2,4,5,7,8,-6,-7,-5,-4,-2,-1,-11,9)
base3 = tt.normal_coord( eb3 )
# print( base3 )
eb4 = (1,2,4,5,7,8,10,11,-9,-10,-8,-7,-5,-4,-2,-1,-11,9)
base4 = tt.normal_coord( eb4 )
# print( base4 )
a0=(1,0,1,0,0,0,0,0,0,0,0,0)
a9=tt.order4rotate(a0)
a6=tt.order4rotate(a9)
a3=tt.order4rotate(a6)
a1=(0,1,1,0,1,1,0,1,1,0,1,1)
nonsep=[a0,a9,a6,a3,a1]


que = [ base3+base4 ]
known = set(base3+base4)
N=10000
edgecount=1

try:
    fileis = open('edges'+timestr+'.txt','a')
    orbit = []
    for foo in range(N):
        cc = que.pop(0)
        print('working', cc)
        cc3 = cc[0:12]
        cd3 = cc[0:12]
        cc4 = cc[12::]
        cd4 = cc[12::]
        fresh_orbs = []
        cinv = tt.involution(cc3)+tt.involution(cc4)
        if cinv not in orbit:
            orbit.append(cinv)
            fresh_orbs.append(cinv)
            if cinv not in que:
                que.append(cinv)
        for bar in range(3):
            cd3 = tt.order4rotate(cd3)
            cd4 = tt.order4rotate(cd4)
            cd=cd3+cd4
            if cd not in orbit:
                orbit.append(cd)
                fresh_orbs.append(cd)
                if cd not in que:
                    que.append(cd)
        for g in nonsep:
            ct3 = tt.dehn_twist(g, cc3)
            ct4 = tt.dehn_twist(g, cc4)
            ct=ct3+ct4
            if ct not in orbit:
                orbit.append(ct)
                fresh_orbs.append(ct)
                if ct not in que:
                    que.append(ct)
        for g in nonsep:
            ct3 = tt.dehn_twist(g, cc3, -1)
            ct4 = tt.dehn_twist(g, cc4, -1)
            ct=ct3+ct4
            if ct not in orbit:
                orbit.append(ct)
                fresh_orbs.append(ct)
                if ct not in que:
                    que.append(ct)
        for e in [12, 3, 6, 9, 2, 5, 8, 11]:
            for powow in [-1, 1]:
                ct3 = tt.braid(cc3, e, powow)
                ct4 = tt.braid(cc4, e, powow)
                ct = ct3 +ct4
            if ct not in orbit:
                orbit.append(ct)
                fresh_orbs.append(ct)
                if ct not in que:
                    que.append(ct)
        for newbie in fresh_orbs:
            strguy = str(newbie)
            fileis.write(strguy[1:-1] + '\n')
        print(len(orbit))
except KeyboardInterrupt:
    fileis.close()
    print('No worries Ill jot this down.')
