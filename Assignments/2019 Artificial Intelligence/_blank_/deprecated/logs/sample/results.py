from collections import defaultdict, Counter
import pandas as pd
from IPython.display import display
import os
from pprint import pprint

directory = os.path.normpath("C:\\Users\\akira\\Documents\\GitHub\\COMP30024\\Chexers\\Part B\\code\\Chexers\\logs\\sample")

count = {'red': defaultdict(int), 'green': defaultdict(int), 'blue': defaultdict(int)}
losses = {'red': list(), 'green': list(), 'blue': list()}
draws = {'red': list(), 'green': list(), 'blue': list()}
time = {'red': list(), 'green': list(), 'blue': list()}
overtime = {'red': list(), 'green': list(), 'blue': list()}

for directory, subdirectories, files in os.walk('.'):
    for match in files:
        if match == 'results.py':
            continue
        colour = match.split('_')[0]
        agent = match.split('_')[1]
        try:
            f = pd.read_csv(os.path.join(directory, match),sep='\n')
        except:
            print(match,"empty file. game quit unexpectedly (usually a keyboard interrupt)")
            
        match_time = float(''.join(list(f.columns[0])[6:]))
        time[colour].append(match_time)
        if match_time >= 60:
            overtime[colour].append(agent)
        if 'game state occurred 4 times' in ''.join(f.values[0][0]):
            draws[colour].append(agent)
            count[colour]['draw'] += 1
        elif colour in f.values[0][0].casefold():
            count[colour]['win'] += 1
        else:
            losses[colour].append(agent)
            count[colour]['loss'] += 1

print("WIN DRAW LOSS")        
print(pd.DataFrame().from_dict(count).fillna(0))

# sort time for a nice graph :)
for i in time.keys():
    time[i].sort()

print("\nMATCH TIMES")
print(pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in time.items() ])))

print("\nAGENT DRAW RATE")
pprint(Counter([b for a in draws.values() for b in a]))
print("\nAGENT LOSS RATE")
pprint(Counter([b for a in losses.values() for b in a]))
print("\nGAME LOST AS COLOUR")
print("\nAGENT OVER 60 SECOND MATCHES")
pprint(Counter([b for a in overtime.values() for b in a]))
print("\nGAME OVERTIME AS COLOUR")