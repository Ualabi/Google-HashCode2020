#################################################
# Function that returns the next librarie to take
#################################################
def A(recents,libraries,whereBooks,ndays,day,setlib,vBooks,bfreq):
    for x in recents:
        for y in whereBooks[x]:
            if y in libraries and x in libraries[y][5]:
                libraries[y][5].remove(x)
                libraries[y][4] -= vBooks[x]
                libraries[y][1] -= 1
    
    ID = -1
    m1 = 0
    for x in libraries:
        if x not in setlib:
            [Index,NBooks,Wait,Ship,Amount] = libraries[x][:5]
            maxi = min(NBooks,1.8*Ship*(ndays-day-Wait))
            maxi = int(max(1,maxi))
            Amount = 0
            for y in range(maxi):
                book = libraries[x][5][y]
                Amount += vBooks[book]/bfreq[book]
            aux = Amount/(Wait)
            libraries[x][4] = aux
            if m1 < aux:
                ID = Index
                m1 = aux

    return [ID,libraries]

#################################################
# Read the in-file
#################################################
basedir = __file__
for x in range(len(basedir)-1,-1,-1):
    if (basedir[x] == '/') :
        basedir = basedir[:x+1]
        break
indir = basedir + 'TestE.txt'
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

[nbooks,nlibs,ndays] = biglist[0]
vBooks = biglist[1] # Value of the books

#################################################
# Build the dictionary of the libraries
#################################################
whereBooks = {}
libraries = {}
row = 2

for index in range(nlibs):
    [NBooks,Wait,Ship] = biglist[row]
    row += 1
    
    books = biglist[row]
    row += 1

    aux = {}
    for ID in books:
        aux[vBooks[ID]] = aux.get(vBooks[ID],[])+[ID]
    
    Amount = 0
    sBooks = [] #Sorted Books
    for x in sorted(aux,reverse=True):
        sBooks += aux[x]
        for y in aux[x]:
            whereBooks[y] = whereBooks.get(y,[])+[index]
            Amount += vBooks[y]
    
    if Wait < 3:
        libraries[index] = [index,NBooks,Wait,Ship,Amount,sBooks]

bfreq = {} #Books frequencies
for x in libraries:
    for y in libraries[x][5]:
        bfreq[y] = bfreq.get(y,0)+1

#################################################
# Simulation of the days
#################################################
past, actual = 0, 0 # Count and limit of the waiting days
setlib  = set() # Set libraries taken, it has O(1) to search in it
queue   = set() # Queue of libraries where we are taking books
taken   = set() # Books taken
tlib    = [] # Libararies taken, it has order
recents = [] # Books just taken
mydict  = {} # Dictionary where we write the libraries with the books taken
flag    = True # The flag indicates if its time to pick up a new librarie
check   = None # The selected librarie
total   = 0

for day in range(ndays): # Simulation of the days
    #############################################
    # Pick up a librarie or count the days
    #############################################
    if flag: # We pick up a new librarie and add the last one to the queue
        if check:
            queue.add(check)
            tlib.append(check)
            setlib.add(check)
            mydict[check] = []
        
        flag = False
        past = 1
        
        [check,libraries] = A(recents,libraries,whereBooks,ndays,day,setlib,vBooks,bfreq)
        actual = libraries[check][2] if check >= 0 else 10**8
        recents = []
    else: # We add 1 to the count of the waiting days
        if actual > 1: # Count the day
            past += 1
            if past == actual:
                flag = True
        elif actual == 1: # If the wait was of 1 day we add if to the queue
            queue.add(check)
            tlib.append(check)
            setlib.add(check)
            mydict[check] = []
            
            flag = False
            past = 1
            
            [check,libraries] = A(recents,libraries,whereBooks,ndays,day,setlib,vBooks,bfreq)
            actual = libraries[check][2] if check >= 0 else 10**8
            recents = []

    #############################################
    # Pick up the books for each librarie
    #############################################
    if queue:
        delete = []
        for element in queue:
            [index,NLibros,Wait,Ship,Amount,sBooks] = libraries[element] 

            llevo = 0
            for x in sBooks:
                if x not in taken:
                    recents.append(x)
                    total += vBooks[x]
                    mydict[element] += [x]
                    taken.add(x)
                    llevo += 1
                if llevo == Ship:
                    break

            if len(sBooks) == 0 or x == sBooks[-1]:
                delete.append(index)

        for rr in delete:
            if rr in queue:
                queue.remove(rr)
            if rr in libraries:
                del libraries[rr]
    
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

outdir = basedir + 'E '+ outdir + '.txt'
outfile = open(outdir,"w+", encoding='utf-8')
outfile.write(mytext)
outfile.close()
