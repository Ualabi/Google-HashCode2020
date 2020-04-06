#################################################
# Read the in-file
#################################################
basedir = __file__
for x in range(len(basedir)-1,-1,-1):
    if (basedir[x] == '/') :
        basedir = basedir[:x+1]
        break
indir = basedir + 'TestB.txt'
print(indir)

infile = open(indir,"r", encoding='utf-8')
text = infile.read()
infile.close()

text = text.split('\n')

biglist = []
for row in text:
    if row:
        aux = list (map (int, row.split (' ')))
        biglist.append(aux)

#################################################
# Build the dictionary of the libraries
#################################################
[nbooks,nlibs,ndays] = biglist[0]
vBooks = 100 # Value of the books
Amount = vBooks*1000

libraries = {}
order = {}
row = 2

for index in range(nlibs):
    [NBooks,Wait,Ship] = biglist[row]
    row += 1
    
    books = biglist[row]
    row += 1
    
    libraries[index] = [index,NBooks,Wait,Ship,Amount,books]
    order[Wait] = order.get(Wait,[]) + [index]

libs = []
for x in sorted(order,reverse = True):
    libs += order[x]

#################################################
# Simulation of the days
#################################################
past, actual = 0, 0 # Count and limit of the waiting days
queue   = set() # Queue of libraries where we are taking books
tlib    = []    # Libararies taken, it has order
mydict  = {}    # Dictionary where we write the libraries with the books taken
flag    = True  # The flag indicates if its time to pick up a new librarie
check   = None  # The selected librarie
total   = 0

for day in range(ndays): # Simulation of the days
    #############################################
    # Pick up a librarie or count the days
    #############################################
    if flag: # We pick up a new librarie and add the last one to the queue
        if check:
            queue.add(check)
            tlib.append(check)
            mydict[check] = []
        
        flag = False
        past = 1
        
        if libs:
            check = libs.pop()
            actual = libraries[check][2]
        else:
            actual = 10**8
    else: # We add 1 to the count of the waiting days
        if actual > 1: # Count the day
            past += 1
            if past == actual:
                flag = True
        elif actual == 1: # If the wait was of 1 day we add if to the queue
            queue.add(check)
            tlib.append(check)
            mydict[check] = []
            
            flag = False
            past = 1
            
            check = libs.pop()
            actual = libraries[check][2]

    #############################################
    # Pick up the books for each librarie
    #############################################
    if queue:
        for element in queue:
            total += vBooks
            x = libraries[element][5].pop()
            mydict[element] += [x]
    
    if day%10==0:
        print(day,total,len(tlib))

print(" - ",total)

#################################################
# Write the out-text
#################################################
mytext = ''
mytext += str(len(mydict)) + '\n'
for x in tlib:
    mytext += str(x) + ' ' + str(len(mydict[x])) + '\n'
    r = ''
    for y in mydict[x]:
        r += str(y) + ' '
    
    if r:
        mytext += r[:-1] + '\n'
    else:
        mytext += '\n'

#################################################
# Write the out-file
#################################################
stotal = str(total)
outdir = ''
while stotal:
    if len(stotal) > 3:
        outdir = ','+stotal[-3:] + outdir
        stotal = stotal[:-3]
    else:
        outdir = stotal + outdir
        stotal = None

outdir = basedir + 'B '+ outdir + '.txt'
outfile = open(outdir,"w+", encoding='utf-8')
outfile.write(mytext)
outfile.close()