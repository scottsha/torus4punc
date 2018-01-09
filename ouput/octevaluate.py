import json
import tandard

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

oo = octogons[0]
for oo in octogons:
    print( [ pts_outside_3curve(foo) for ct,foo in enumerate(oo) if ct%2==0] )