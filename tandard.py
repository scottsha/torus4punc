import pylab as pl
from matplotlib import collections as mc
import random
from collections import Counter
# The chosen triangulation of S_{1,4}
#
# 0---1---2---3---0
# |0\1|2\3|4\5|6\7|
# 0---1---2---3---0
#

#  ___ ___ _________
# |\  |\  |\  |\    |
# 1 2 4 5 7 8 10 11
# |_0\|_3\|_6\|_9_\ |
#

tripts = {
    0: [(0, 1), (0, 0), (1, 0)],
    1: [(0, 1), (1, 0), (1, 1)],
    2: [(1, 1), (1, 0), (2, 0)],
    3: [(1, 1), (2, 0), (2, 1)],
    4: [(2, 1), (2, 0), (3, 0)],
    5: [(2, 1), (3, 0), (3, 1)],
    6: [(3, 1), (3, 0), (4, 0)],
    7: [(3, 1), (4, 0), (4, 1)],
}
triedge = {
    0: [0, 2, 1],
    1: [4, 0, 2],
    2: [3, 5, 4],
    3: [7, 3, 5],
    4: [6, 8, 7],
    5: [10, 6, 8],
    6: [9, 11, 10],
    7: [1, 9, 11]
}
#
# Normal coordinates on the edges
#
edgepts = {
    0: [ [(0, 0), (1, 0)], [(0, 1), (1, 1)] ],
    1: [ [(0, 0), (0, 1)], [(4, 0), (4, 1)] ],
    2: [ [(0, 1), (1, 0)] ],
    3: [[(1, 0), (2, 0)], [(1, 1), (2, 1)]],
    4: [[(1, 0), (1, 1)]],
    5: [ [(1, 1), (2, 0)] ],
    6: [[(2, 0), (3, 0)], [(2, 1), (3, 1)]],
    7: [[(2, 0), (2, 1)]],
    8: [ [(2, 1), (3, 0)] ],
    9: [[(3, 0), (4, 0)], [(3, 1), (4, 1)]],
    10: [[(3, 0), (3, 1)]],
    11: [[(3, 1), (4, 0)]],
}

#
# From intersection pattern on triangulation edges we can obtain the segments per angle
#
def seg_nums_by_angle( ipat ):
    segnums = [None]*24
    for foo in range(8):
        tri = triedge[foo]
        for bar in range(3):
            seghere =  ipat[ tri[(bar+1)%3] ] + ipat[ tri[(bar+2)%3] ] - ipat[ tri[bar] ]
            if ((seghere < 0) or (seghere%2!=0)):
                return False
            else:
                segnums[3*foo+bar] = seghere/2
    return segnums

#
#Example: here's a nonseparating curve: (1,0,1,0,0,0,0,0,0,0,0,0)
#
#
#print( seg_nums_by_angle( (1,0,1,0,0,0,0,0,0,0,0,0) ) )
#print( seg_nums_by_angle( (1,0,0,0,0,0,0,0,0,0,0,0) ) )

#
#
#
def midptw( a, b, t ):
    return ( ( (1-t)*a[0] + (t)*b[0], (1-t)*a[1] + (t)*b[1]) )

def tori_equal(a,b):
     c = ( abs( (a[0]-b[0])%4 ) <= 1e-8 ) or ( abs((4-(a[0]-b[0])%4)) <= 1e-8 )
     d= ( abs( (a[1]-b[1])%1 ) <= 1e-8 ) or ( abs(1- ((a[1]-b[1])%1) ) <= 1e-8 )
     return (c and d)
#    return ( abs( (a[0]-b[0])%4 )<=1e-8 ) and ( abs((a[1]-b[1])%1)<=1e-8)
#
#Produce an embedding of the curve/multicurve as an ordered list of points in [0,4] x [0,1]
def embed_curve( ipat ):
    segnums = seg_nums_by_angle(ipat)
    if not segnums: return False
    segments=[]
    for foo in range(8):
        pts = tripts[foo]
        tri = triedge[foo]
        for bar in range(3):
            i1 = ipat[ tri[(bar+1)%3] ]
            i2 = ipat[ tri[(bar+2)%3] ]
            seghere =  i1+i2 - ipat[ tri[bar] ]
            seghere = int(seghere/2)
            a=pts[bar]
            b=pts[(bar+1)%3]
            c=pts[(bar+2)%3]
            for qux in range(seghere):
                p1=midptw( a, b,  float(qux+1)/(i2 +1) ) #Fraction( (qux+1), (i2 +1)))
                p2=midptw( a, c, float(qux+1)/(i1 +1) )#Fraction( (qux+1), (i1 +1)))
                segments.append( (p1,p2) )
    return( segments )

def curve( ipat ):
    #determine if a collection of segments is a curve or just
    insegs = embed_curve(ipat)
    if not insegs: return False
    segments = insegs[:]
    s = segments.pop(0)
    c=[s]
    tail = s[1]
    done = False
    while not done:
        if segments==[]:
            done=True
        for foo in range(len(segments)):
            s=segments[foo]
            if tori_equal(s[0], tail):
                tail=s[1]
                c.append(s)
                segments.pop(foo)
                break
            elif tori_equal(s[1], tail):
                tail=s[0]
                c.append(s)
                segments.pop(foo)
                break
            if foo == len(segments)-1:
                done=True
    if len(c)==len(insegs):
        return c
    else:
        return False

def is_separating( ipat ):
    #Not sure if this is correct though
    it_is = (ipat[1]%2==0) and (ipat[4]%2==0) and (ipat[7]%2==0) and (ipat[10]%2==0)
    it_is = it_is and ( (ipat[0]+ipat[3]+ipat[6]+ipat[9])%2==0)
    return it_is


def curveplot( curve ):
    segments =[]
    for foo in range(4):
        segments.append([(foo,0), (foo,1)])
        segments.append([(foo, 0), (foo+1, 0)])
        segments.append([(foo, 1), (foo+1, 1)])
        segments.append([(foo,1), (foo+1,0)])
    segments.append([(4,0), (4,1)])
    ccc=mc.LineCollection( curve, colors='r', linewidths=2)
    lc = mc.LineCollection( segments, linewidths=1)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.add_collection(ccc)
    ax.autoscale()
    pl.axis('off')
    pl.show()

def randcolor():
    r = lambda: random.uniform(0.5, 1.0)
    c0=r()
    c1=r()
    c2=r()
    return (c0,c1,c2)

somecols=["#d62728", "#1f77b4", "#2ca02c",  "#ff7f0e",   "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

def curvesplot( curves ):
    segments =[]
    for foo in range(4):
        segments.append([(foo,0), (foo,1)])
        segments.append([(foo, 0), (foo+1, 0)])
        segments.append([(foo, 1), (foo+1, 1)])
        segments.append([(foo,1), (foo+1,0)])
    segments.append([(4,0), (4,1)])
    lc = mc.LineCollection( segments, colors='k', linewidths=1)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    cnum=0
    for curve in curves:
        # col = randcolor()
        ccc=mc.LineCollection( curve, colors=somecols[cnum], linewidths=2)
        ax.add_collection(ccc)
        cnum=cnum+1
    ax.autoscale()
    pl.axis('off')
    pl.show()

def middle_embedding( ipat ):
    #embed the curve in the middle fifth of triangulation
    segnums = seg_nums_by_angle(ipat)
    if not segnums: return False
    segments=[]
    for foo in range(8):
        pts = tripts[foo]
        tri = triedge[foo]
        for bar in range(3):
            i1 = ipat[ tri[(bar+1)%3] ]
            i2 = ipat[ tri[(bar+2)%3] ]
            seghere =  i1+i2 - ipat[ tri[bar] ]
            seghere = int(seghere/2)
            a=pts[bar]
            b=pts[(bar+1)%3]
            c=pts[(bar+2)%3]
            right0=midptw( a, b ,0.4)
            right1=midptw( a, b ,0.6)
            left0=midptw( a, c ,0.4)
            left1=midptw( a, c ,0.6)
            for qux in range(seghere):
                p1=midptw( right0, right1,  float(qux+1)/(i2 +1) ) #Fraction( (qux+1), (i2 +1)))
                p2=midptw( left0, left1, float(qux+1)/(i1 +1) )#Fraction( (qux+1), (i1 +1)))
                segments.append((p1, p2))
    return( segments )

# triedge = {
#     0: [0, 2, 1],
#     1: [4, 0, 2],
#     2: [3, 5, 4],
#     3: [7, 3, 5],
#     4: [6, 8, 7],
#     5: [10, 6, 8],
#     6: [9, 11, 10],
#     7: [1, 9, 11]
# }
startarcs = {
    0:[ [(0,0), (0.2,0)], [(1,0), (0.8,.2)], [(0,0.2), (0,0)]],
    1:[ [(1,0), (1,0.2)], [(0.2,1),(0,1)], [(0.8,0.2), (1,0)]],
    2: [[(1, 0), (1.2, 0)], [(2, 0), (1.8, .2)], [(1, 0.2), (1, 0)]],
    3: [[(2, 0), (2, 0.2)], [(1.2, 1), (1, 1)], [(1.8, 0.2), (2, 0)]],
    4: [[(2, 0), (2.2, 0)], [(3, 0), (2.8, .2)], [(2, 0.2), (2, 0)]],
    5: [[(3, 0), (3, 0.2)], [(2.2, 1), (2, 1)], [(2.8, 0.2), (3, 0)]],
    6: [[(3, 0), (3.2, 0)], [(4, 0), (3.8, .2)], [(3, 0.2), (3, 0)]],
    7: [[(4, 0), (4, 0.2)], [(3.2, 1), (3, 1)], [(3.8, 0.2), (4, 0)]],
}

def near_point_embedding( ipat ):
    #embed the curve crossing traingaulation edges in the fifths nearest the marked points
    #uses triangulation specifics
    segnums = seg_nums_by_angle(ipat)
    if not segnums: return False
    segments=[]
    for foo in range(8):
        pts = tripts[foo]
        tri = triedge[foo]
        arcs = startarcs[foo]
        for bar in range(3):
            i1 = ipat[ tri[(bar+1)%3] ]
            i2 = ipat[ tri[(bar+2)%3] ]
            seghere =  i1+i2 - ipat[ tri[bar] ]
            seghere = int(seghere/2)
            right0=arcs[(bar+2)%3][0]
            right1=arcs[(bar+2)%3][1]
            left0=arcs[(bar+1)%3][1]
            left1=arcs[(bar+1)%3][0]
            for qux in range(seghere):
                p1=midptw( right0, right1,  float(qux+1)/(i2 +1) ) #Fraction( (qux+1), (i2 +1)))
                p2=midptw( left0, left1, float(qux+1)/(i1 +1) )#Fraction( (qux+1), (i1 +1)))
                segments.append( (p1,p2) )
    return( segments )


#     0: [0, 2, 1],
#     1: [4, 0, 2],
#     2: [3, 5, 4],
#     3: [7, 3, 5],
#     4: [6, 8, 7],
#     5: [10, 6, 8],
#     6: [9, 11, 10],
#     7: [1, 9, 11]

def mid_near_isect( ip, jp):
    #number of intersection points for a midembedded of intersection pattern ip
    # and a nearpoint-embedded intersection pattern jp
    # for foo in range(8):
    #     if foo%2==0:
    #         print(ip[triedge[foo][0]], jp[triedge[foo][1]])
    #     else:
    #         print(ip[triedge[foo][2]], jp[triedge[foo][1]])
    return ip[0]*jp[2]\
           +ip[2]*jp[0]\
           +ip[3]*jp[5]\
           +ip[5]*jp[3]\
           +ip[6]*jp[8]\
           +ip[8]*jp[6]\
           +ip[9]*jp[11]\
           +ip[11]*jp[9]

#The triangles on the left, right of the oriented edges are:
#
#   <--1--^
#   |\    |
#   2 e\< 0
#   |   \ |
#   v--3-->
edge_sqs={
    12: [-2,4],
    -12: [2,-1],
    1: [12, 2],
    -1:[-9, -11],
    2: [4, -12],
    -2: [-1, 12],
    3: [-5,7],
    -3:[ 5,-4],
    4: [3,5],
    -4: [-12,-2],
    5: [7,-3],
    -5: [-4,3],
    6: [-8,10],
    -6: [8,-7],
    7: [6,8],
    -7: [-3,-5],
    8: [10,-6],
    -8: [-7,6],
    9: [-11,1],
    -9: [11,-10],
    10: [9,11],
    -10: [-6,-8],
    11: [1,-9],
    -11: [-10,9]
}
# triedge = {
#     0: [0, 2, 1],
#     1: [4, 0, 2],
#     2: [3, 5, 4],
#     3: [7, 3, 5],
#     4: [6, 8, 7],
#     5: [10, 6, 8],
#     6: [9, 11, 10],
#     7: [1, 9, 11]
# }
def trisequence_curve( ipat , start=False):
    #Determine a triangulation edge sequence for a curve
    seg_nums = seg_nums_by_angle(ipat)
    if not seg_nums:
        return False
    crossings = [(foo, bar) for foo in range(1,13) for bar in range(ipat[foo%12])]
    # print(crossings)
    if not start: start = crossings[0]
    startop = ( -start[0], ipat[start[0]]-start[1]-1 )
    num_arcs=len(crossings)
    e0 = start[0]
    if e0==0: e0=12
    edgeseq=[e0]
    at = start
    for foo in range(num_arcs):
        e1,e2 = edge_sqs[e0]
        i1 = ipat[abs(e1)%12]
        i2 = ipat[abs(e2)%12]
        i0 = ipat[abs(e0)%12]
        segs01= int((i0+i1-i2)/2)
        # segs02 = int((i0 + i2 - i1) / 2)
        if at[1] < segs01:
            edgeseq.append(e1)
            at = (e1, at[1])
            e0=e1
        else:
            edgeseq.append(e2)
            at = (e2, i2-i0+at[1])
            e0=e2
        if (foo<num_arcs-1) and ( at==start or at==startop):
            return False
    edgeseq.pop()
    return tuple(edgeseq)

def tri_pt_seq_curve( ipat , start=False):
    #Determine a triangulation edge sequence for a curve
    seg_nums = seg_nums_by_angle(ipat)
    if not seg_nums:
        return False
    crossings = [(foo, bar) for foo in range(1,13) for bar in range(ipat[foo%12])]
    # print(crossings)
    if not start: start = crossings[0]
    startop = ( -start[0], ipat[start[0]]-start[1]-1 )
    num_arcs=len(crossings)
    e0 = start[0]
    if e0==0: e0=12
    ptseq=[start]
    at = start
    for foo in range(num_arcs):
        e1,e2 = edge_sqs[e0]
        i1 = ipat[abs(e1)%12]
        i2 = ipat[abs(e2)%12]
        i0 = ipat[abs(e0)%12]
        segs01= int((i0+i1-i2)/2)
        # segs02 = int((i0 + i2 - i1) / 2)
        if at[1] < segs01:
            at = (e1, at[1])
            ptseq.append(at)
            e0=e1
        else:
            at = (e2, i2-i0+at[1])
            ptseq.append(at)
            e0=e2
        if (foo<num_arcs-1) and ( at==start or at==startop):
            return False
    ptseq.pop()
    return tuple(ptseq)


# Homology dual basis
#  Up and left
# ___ ___ _________
# |\  |\  |\  |\  |
# 0 \ | \ | \ | \ |
# |_1\|_2\|_3\|_4\|
#

def homology_class( ipat ):
    edgeseq = trisequence_curve(ipat)
    a = Counter(edgeseq)
    # a[edgeseq[0]] -=1
    h0=a[1]-a[-1]
    h1=a[12]-a[-12]
    h2=a[3]-a[-3]
    h3=a[6]-a[-6]
    h4=a[9]-a[-9]
    return (h0,h1,h2,h3,h4)

def alg_intersection( c0, c1):
    v=homology_class(c0)
    w=homology_class(c1)
    return v[0]*(w[1]+w[2]+w[3]+w[4])+w[0]*(v[1]+v[2]+v[3]+v[4])


# def arc_insert2(c,  start, stop , power=1):
#     cpat = normal_coord(c)
#     if stop<0: a=(stop, cpat[abs(stop)%12]-1 )
#     else: a=(stop,0 )
#     arcseq = trisequence_curve( cpat, a )
#     if not arcseq:
#         return []
#     else:
#         return arcseq

def arc_insert(c,  start, stop , power=1):
    # cpat = normal_coord(c)
    # if stop<0: a=(stop, cpat[abs(stop)%12]-1 )
    # else: a=(stop,0 )
    # arcseq = trisequence_curve( cpat, a )
    # if not arcseq:
    #     return []
    # else:
    #     return arcseq
    ll = len(c)
    arcseq=[]
    nrevc = [-c[foo] for foo in range(-1,-ll-1,-1)]
    for foo in range(-1,ll-1):
        if (c[foo]==start and c[foo+1]==stop):
            arcseq+= power*(c[foo+1: ll]+c[0:foo+1])
        elif nrevc[foo]==start and nrevc[foo+1]==stop:
        #     bar=ll-foo
        #     # print(nrevc[bar+1: ll])
        #     # print(nrevc[0:bar+1])
             arcseq+= power*(nrevc[foo+1: ll]+nrevc[0:foo+1])
    # print('insert arc', arcseq)
    return arcseq

# edge_sqs={
#     12: [-2,4],
#     -12: [2,-1],
#     1: [12, 2],
#     -1:[-9, -11],
#     2: [4, -12],
#     -2: [-1, 12],
#     3: [-5,7],
#     -3:[ 5,-4],
#     4: [3,5],
#     -4: [-12,-2],
#     5: [7,-3],
#     -5: [-4,3],
#     6: [-8,10],
#     -6: [8,-7],
#     7: [6,8],
#     -7: [-3,-5],
#     8: [10,-6],
#     -8: [-7,6],
#     9: [-11,1],
#     -9: [11,-10],
#     10: [9,11],
#     -10: [-6,-8],
#     11: [1,-9],
#     -11: [-10,9]
# }

def fuse_arcs( alpha0, alpha1):
    if alpha0!=[] and alpha1!=[]:
        while alpha0[-1]==-alpha1[0]:
            alpha0.pop(-1)
            alpha1.pop(0)
            if alpha0 == [] or alpha1 == []: break
    return alpha0+alpha1

def cyclic_simplify( a ):
    ll=len(a)
    b=a[:]
    at=-1
    while at < ll-1:
        if ll<2: break
        if b[at]==-b[at+1]:
            while b[at]==-b[at+1]:
                if at==-1:
                    b.pop(-1)
                    b.pop(0)
                else:
                    b.pop(at)
                    b.pop(at)
                ll=ll-2
                if ll<2 or at>ll-2: break
            at=-1
        else: at=at+1
    return b

def twist_arc( c, a0 , a1, power=1):
    #Dehn twist the arc a0a1 edge embedded about c middle embedded
    seq=[a0]
    # nrevc = [-c[foo] for foo in range(-1, -ll - 1, -1)]
    #T0
    if (a0==1 and a1==2) or (a0==-12 and a1==2):
        seq+=arc_insert(c, -12, -1, power)
        seq+=arc_insert(c, -12, 2, power)
    elif (a0==-2 and a1==-1) or (a0==-2 and a1==12):
        seq+=arc_insert(c, -2, 12, power)
        seq+=arc_insert(c, 1, 12, power)
    #T1
    elif (a0==2 and a1==-12) or (a0==-4 and a1==-12):
        seq+=arc_insert(c, -4, -2, power)
        seq +=arc_insert(c, 12, -2, power)
    elif (a0==12 and a1==-2) or (a0==12 and a1==4):
        seq+=arc_insert(c, 2, -12, power)
        seq+=arc_insert(c, 2, 4, power)
    #T2
    elif (a0==4 and a1==5) or (a0==-3 and a1==5):
        seq+=arc_insert(c, -3, -4, power)
        seq+=arc_insert(c, -3, 5, power)
    elif (a0==-5 and a1==-4) or (a0==-5 and a1==3):
        seq+=arc_insert(c, -5, 3, power)
        seq+=arc_insert(c, 4, 3, power)
    #T3
    elif (a0==5 and a1==-3) or (a0==-7 and a1==-3):
        seq+=arc_insert(c, -7, -5, power)
        seq+=arc_insert(c, 3, -5, power)
    elif (a0==3 and a1==-5) or (a0==3 and a1==7):
        seq+=arc_insert(c, 5, -3, power)
        seq+=arc_insert(c, 5, 7, power)
    #T4
    elif (a0==7 and a1==8) or (a0==-6 and a1==8):
        seq+=arc_insert(c, -6, -7, power)
        seq+=arc_insert(c, -6, 8, power)
    elif (a0==-8 and a1==-7) or (a0==-8 and a1==6):
        seq+=arc_insert(c, -8, 6, power)
        seq+=arc_insert(c, 7, 6, power)
    #T5
    elif (a0==8 and a1==-6) or (a0==-10 and a1==-6):
        seq+=arc_insert(c, -10, -8, power)
        seq+=arc_insert(c, 6, -8, power)
    elif (a0==6 and a1==-8) or (a0==6 and a1==10):
        seq+=arc_insert(c, 8, -6, power)
        seq+=arc_insert(c, 8, 10, power)
    #T6
    elif (a0==10 and a1==11) or (a0==-9 and a1==11):
        seq+=arc_insert(c, -9, -10, power)
        seq+=arc_insert(c, -9, 11, power)
    elif (a0==-11 and a1==-10) or (a0==-11 and a1==9):
        seq+=arc_insert(c, -11, 9, power)
        seq+=arc_insert(c, 10, 9, power)
    #T7
    elif (a0==11 and a1==-9) or (a0==-1 and a1==-9):
        seq+=arc_insert(c, -1, -11, power)
        seq+=arc_insert(c, 9, -11, power)
    elif (a0==9 and a1==-11) or (a0==9 and a1==1):
        seq+=arc_insert(c, 11, -9, power)
        seq+=arc_insert(c, 11, 1, power)
    seq.append(a1)
    return seq

# def twist( c, a, power=1 ):
#     #Compute the power-th dehn twist of a about c    T_c(a)
#     #with c middle embeddec and a side embedded
#     seq=[]
#     for foo in range(len(a)-1):
#         tarc=twist_arc(c, a[foo], a[foo+1], power)
#         seq+=tarc[:-1]
#     tarc=twist_arc(c, a[-1], a[0], power)
#     seq+=tarc[:-1]
#     seq=cyclic_simplify(seq)
#     return tuple(seq)

def normal_coord( edgeseq ):
    #Compute the normal coordinates of a curve from the edge sequence
    a=Counter(edgeseq)
    e0=[a[12]+a[-12]]
    e=[a[foo]+a[-foo] for foo in range(1,12) ]
    return tuple(e0+e)

# def geometric_intersection( ipat, jpat):
#     #Compute geomtric intersection pattern
#     #from triangulation intersection patterns
#     #BAD
#     a=trisequence_curve(ipat)
#     b=trisequence_curve(jpat)
#     e = b[0]
#     cb = Counter(b)
#     ibe = cb[e]+cb[-e]
#     sufhigh = 2*ibe
#     tb_a = a
#     for foo in range(sufhigh): tb_a = twist(b, tb_a)
#     tn_b_a = tb_a
#     tnp1_b_a = twist(b, tn_b_a)
#     # tn_b_a = twist(b, a, sufhigh)
#     # tnp1_b_a = twist(b, a, sufhigh+1)
#     cbn = Counter(tn_b_a)
#     cbnp = Counter(tnp1_b_a)
#     q =  cbnp[e]+cbnp[-e]  - ( cbn[e] +cbn[-e])
#     return int(q / ibe)

def order4rotate( ipat ):
    #Apply an order 4 rotation sending each triangle T_i |-> T_i+2
    a =tuple( ipat[ (foo+3)%12 ] for foo in range(12))
    return a

def involution( ipat ):
    #Apply a hyperbolic involution that keeps the triangulation.
    i0=ipat[9]
    i1=ipat[1]
    i2=ipat[11]
    i3=ipat[6]
    i4=ipat[10]
    i5=ipat[8]
    i6=ipat[3]
    i7=ipat[7]
    i8=ipat[5]
    i9=ipat[0]
    i10=ipat[4]
    i11=ipat[2]
    return (i0,i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11)
hug_edge={
    #start from a0 hug edge on the signed side
    -12:(12, -1),
    12:(-2, -1),
    1:(12, -1),
    -1:(11,1),
    2:(2,1),
    -2:(-12, 1),
    -3:(3, -1),
    3: (-5, -1),
    -4: (2, 1),
    4: (3, -1),
    -5: (-3, 1),
    5: (5,1),
    -6: (6,-1),
    6: (-8, -1),
    -7:(5,1),
    7:(6,-1),
    -8:(-6,1),
    8:(8,1),
    -9:(9,-1),
    9:(-11,-1),
    -10:(8,1),
    10:(9,-1),
    -11:(-9,1),
    11:(11,1)
}

uncrossable = ((1,12),(2,4),(4,3),(5,7),(7,6),(8,10),(10,9),(11,1))

def arctwist( cpat, a0, a1, power=1, cpts=False ):
    #Dehn twist of an arc about the curve described by cpat
    if (a0,a1) in uncrossable or (-a1,-a0) in uncrossable:
        return [a0,a1]
    if not cpts: cpts = tri_pt_seq_curve(cpat)
    hug = hug_edge[a0]
    follows= hug[0]
    to_the_right = hug[1]
    c = [bar[0] for bar in cpts]
    revcpts = [ (-bar[0], cpat[abs(bar[0])%12]-bar[1]-1 ) for bar in cpts[::-1]]
    revc =[ bar[0] for bar in revcpts ]
    seq=[]
    ise = cpat[abs(follows)%12]
    for foo in range( ise ):
        if to_the_right ==1:
            pt = (-follows, ise - 1 - foo)
            try:
                ii = cpts.index(pt)
                seq += abs(power)*( c[ii:] + c[:ii] )
            except ValueError:
                ii = revcpts.index(pt)
                seq += abs(power)*( revc[ii:] + revc[:ii] )
        if to_the_right == -1:
            pt = (-follows, ise - 1 - foo)
            try:
                ii = cpts.index(pt)
                seq += abs(power)*(c[ii+1:] + c[:ii+1])
            except ValueError:
                ii = revcpts.index(pt)
                seq += abs(power)*(revc[ii+1:] + revc[:ii+1])
    if power<0:
        seq = [ -foo for foo in seq[::-1] ]
    return [a0]+seq+[a1]


def dehn_twist( cpat,  bpat, power=1 ):
    #Compute the power-th dehn twist of b about c    T_c(b)
    #with c middle embeddec and b side embedded
    seq=[]
    curve_pts = tri_pt_seq_curve(cpat)
    a = trisequence_curve(bpat)
    for foo in range(len(a)-1):
        tarc=arctwist(cpat, a[foo], a[foo+1], power, curve_pts)
        # print('arc', a[foo], 'to', a[foo+1], 'is', tarc)
        seq+=tarc[:-1]
    tarc=arctwist(cpat, a[-1], a[0], power, curve_pts)
    # print('arc', a[-1], 'to', a[0], 'is', tarc)
    seq+=tarc[:-1]
    seq=cyclic_simplify(seq)
    return normal_coord(seq)


def geo_intersect( ipat, jpat):
    #Compute geomtric intersection pattern
    #from triangulation intersection patterns
    es = [foo for foo in ipat if foo!=0]
    ibe = min(es)
    e = ipat.index(ibe)
    sufhigh = 2*ibe
    dn = dehn_twist( ipat, jpat, sufhigh )
    # dnp1 = dehn_twist( ipat, dn )
    dnp1 = dehn_twist(ipat, jpat, sufhigh + 1)
    dnp1 = dehn_twist(ipat, jpat, sufhigh + 1)
    q = dnp1[e] - dn[e]
    return q // ibe

def braid(ipat, e, power=1):
    #only do 1 or -1 power
    curve_seq = trisequence_curve( ipat )
    # top loop
    n3 = edge_sqs[-e][0]
    nn=n3
    s_top = [nn]
    for foo in range(4):
        nn = edge_sqs[nn][0]
        s_top.append(nn)
    #bottom loop
    n4 = edge_sqs[-e][1]
    nn = n4
    s_bot = [nn]
    for foo in range(4):
        nn = edge_sqs[nn][1]
        s_bot.append(nn)
    #
    if power>0:
        sbend = s_top+[-e]+s_bot
    else:
        sbend = s_bot+[-e]+s_top
    #
    # sbend = abs(power)*sbend
    sbendback = [-foo for foo in sbend[::-1]]
    braided = []
    for cross in curve_seq:
        if cross == e:
            braided+=sbend
        elif cross==-e:
            braided+=sbendback
        else:
            braided.append(cross)
    seq=cyclic_simplify(braided)
    return normal_coord(seq)


a0=(1,0,1,0,0,0,0,0,0,0,0,0)
a9=order4rotate(a0)
a6=order4rotate(a9)
a3=order4rotate(a6)
a1=(0,1,1,0,1,1,0,1,1,0,1,1)
nonsep = [a1,a0,a3,a6,a9]


def mod_orbit( base, iterations ):
    orbit = base[::]
    que = base[::]
    for foo in range( iterations ):
        cc = que.pop(0)
        cd=cc[::]
        cinv = involution(cc)
        if cinv not in orbit:
            orbit.append(cinv)
            if cd not in que:
                que.append(cinv)
        for bar in range(3):
            cd = order4rotate(cd)
            if cd not in orbit:
                orbit.append( cd )
                if cd not in que:
                    que.append( cd )
        for g in nonsep:
            ct = dehn_twist( g, cc )
            if ct not in orbit:
                orbit.append( ct )
                if ct not in que:
                    que.append( ct )
        for g in nonsep:
            ct = dehn_twist(g, cc, -1)
            if ct not in orbit:
                orbit.append(ct)
                if ct not in que:
                    que.append(ct)
        for e in [12,3,6,9,2,5,8,11]:
            for powow in [-1,1]:
                ct = braid( cc, e, powow)
            if ct not in orbit:
                orbit.append(ct)
                if ct not in que:
                    que.append(ct)
    return orbit

def euler_char_sides( ipat ):
    #Compute the euler characteristic of the components of S_1,4 cut along the curve
    slope0 = ipat[0]+ipat[3]+ipat[6]+ipat[9]
    slope1 = ipat[1]
    if (slope0%2 != 0) or (slope1%2 != 0):
        return False
    with0 = [0]
    without0 = []
    if ipat[0]%2 == 0:
        with0.append(1)
    else:
        without0.append(1)
    if (ipat[0]+ipat[3])%2 == 0:
        with0.append(2)
    else:
        without0.append(2)
    if ipat[9]%2 == 0:
        with0.append(3)
    else:
        without0.append(3)
    region = [0,0]
    edges = [0,0]
    si=sum(ipat)
    verts = [si,si]
    for pt in range(4):
        color = int(pt not in with0)
        verts[color] += 1
        for sign in [-1,1]:
            e=sign*(3*pt+1)
            i0 = ipat[ abs(e)%12 ]
            i1 = ipat[ abs(edge_sqs[e][0])%12 ]
            i2 = ipat[ abs(edge_sqs[e][1])%12 ]
            t0=(i1+i2-i0)//2
            t1=(i0+i2-i1)//2
            t2=(i0+i1-i2)//2
            #####
            color = int( pt not in with0 )
            region[color] +=1
            region[color] += t1//2
            region[(color+1)%2] += (t1+1)//2
            edges[color] += (i0 + i1 + i2) / 2
            edges[color] += ( i0/2 + 1 + (i1+1)//2+1 + (i2+1)//2+1 )/2
            edges[(color+1)%2] += (i0 + i1 + i2) / 2
            edges[(color+1)%2] += ( i0/2 + i1-(i1+1)//2 + i2-(i2+1)//2 )/2
            ####
            color = (color + t1)%2
            region[color] += t0//2 + t2//2
            region[(color+1)%2] += (t0+1)//2 + (t2+1)//2
    print(verts[0], edges[0], region[0])
    eul0 = int( verts[0] - edges[0] + region[0] )
    print(verts[1], edges[1], region[1])
    eul1 = int( verts[1] - edges[1] + region[1] )
    return (eul0, with0, eul1, without0)

obv_isect_pairs=[]
for midsq in range(1,13):
    dwn = (-edge_sqs[-midsq][0], midsq, edge_sqs[midsq][0])
    upp = (-edge_sqs[-midsq][1], midsq, edge_sqs[midsq][1])
    obv_isect_pairs.append((dwn,upp))

def arc_find( sub, a):
    x=sub[0]
    y=sub[1]
    z=sub[2]
    ll=len(a)
    for foo, v in enumerate(a):
        if v==y:
            if a[foo-1]==x and a[(foo+1)%ll]==z:
                return True
        elif v==-y:
            if a[foo-1]==-z and a[(foo+1)%ll]==-x:
                return True
    return False


def obvious_intersection( ipat, jpat ):
    c0 = trisequence_curve(ipat)
    c1 = trisequence_curve(jpat)
    for pair in obv_isect_pairs:
        if ( arc_find(pair[0],c0) and arc_find(pair[1],c1) ) or arc_find(pair[1],c0) and arc_find(pair[0],c1):
            return True
    return False
