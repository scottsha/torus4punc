import os
import json
from tandard import curve_sort_key

known_intersections = set()

for filename in os.listdir('mergeums'):
    if filename.endswith('.txt'):
        print('Reading', filename)
        with open('mergeums/'+filename,'r') as file:
            lino = file.readline()
            while lino:
                ii = int(lino)
                pat3in = file.readline()
                pat3 = [int(foo) for foo in pat3in.split(',')]
                pat4in = file.readline()
                pat4 = [int(foo) for foo in pat4in.split(',')]
                iknow = tuple( [ii]+pat3+pat4 )
                known_intersections.add( iknow )
                lino = file.readline()
known_i = list(known_intersections)
known_i.sort(key=lambda x: (x[0],) + curve_sort_key(x[1:13]) + curve_sort_key(x[13::]))

print('listing knowns')
with open('knownintersections.json', 'w') as outfile:
    json.dump(known_i, outfile)

