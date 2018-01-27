import tandard as tt
import listermerger
import json
import time
timestr = time.strftime("%d%H%M%S")



print('Reading old curves')



with open('knownintersections.json','r') as knownfile:
    knownlist = json.load(knownfile)

disjoints = []
threes = set()
fours = set()

for foo in knownlist:
    if foo[0] == 0:
        athree = tuple(foo[1:13])
        afour = tuple(foo[13::])
        threes.add( athree )
        fours.add( afour )
        disjoints.append( (athree, afour)  )

known_intersections = set([tuple(foo[1::]) for foo in knownlist])



print('Sort these loopy boys')
threes=list(threes)
fours=list(fours)
threes.sort(key = lambda x: tt.curve_sort_key(x))
fours.sort(key = lambda x: tt.curve_sort_key(x))

n3 = len(threes)
n4 = len(fours)

toat = n3*n4
print('Where do I begin!?')
try:
    try:
        with open('wasat.json','r') as filewasat:
            iwasat = json.load(filewasat)
    except FileNotFoundError:
        iwasat=0
    fileis = open('disjsquare'+timestr+'.txt','a')
    for bar in range(iwasat,n4):
        for foo in range(n3):
            if (bar*n3+foo)%1000 == 0:
                print('amille')
            a=threes[foo]
            b=fours[bar]
            if a+b not in known_intersections:
                if not tt.obvious_intersection(a,b):
                    print('try', foo, ' of ', n3, ' and ', bar, 'of', n4)
                    if tt.is_disjoint_curves(a,b):
                        print('cashmoney')
                        it=0
                        fileis.write(str(it)+'\n')
                        stra = str(a)
                        fileis.write(stra[1:-1]+'\n')
                        strb = str(b)
                        fileis.write(strb[1:-1]+'\n')
    fileis.close()
except KeyboardInterrupt:
    with open('wasat.json', 'w') as filewasat:
        iwasat = json.dump(bar,filewasat)
    fileis.close()
    print('No worries Ill jot this down.')


