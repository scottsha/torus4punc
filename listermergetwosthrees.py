import os
import json
from tandard import curve_sort_key

known_intersections = set()

for filename in os.listdir('mergetwosthrees'):
    if filename.endswith('.txt'):
        print('Reading', filename)
        with open('mergetwosthrees/'+filename,'r') as file:
            lino = file.readline()
            while lino:
                ii = int(lino)
                pat2in = file.readline()
                pat2 = [int(foo) for foo in pat2in.split(',')]
                pat3in = file.readline()
                pat3 = [int(foo) for foo in pat3in.split(',')]
                iknow = tuple( [ii]+pat2+pat3 )
                known_intersections.add( iknow )
                lino = file.readline()
known_i = list(known_intersections)
known_i.sort(key=lambda x: (x[0],) + curve_sort_key(x[1:13]) + curve_sort_key(x[13::]))

print('listing knowns')
with open('knowntwosthrees.json', 'w') as outfile:
    json.dump(known_i, outfile)

