#################################################
# Function that returns the next librarie to take
#################################################
def A(recents,libraries,whereBooks,ndays,day,setlib,vBooks,vFreq):
    for x in recents:
        for y in whereBooks[x]:
            if y in libraries and x in libraries[y][5]:
                libraries[y][6] -= vFreq[x]
                libraries[y][5].remove(x)
                libraries[y][1] -= 1

    if day < 99812:
        ID = -1
        m1 = 0
        m2 = 0
        for x in libraries:
            [index,NBooks,Wait,Ship,Amount,sBooks,Uniq] = libraries[x]
            if NBooks and index not in setlib:
                maxi = min(NBooks,Ship*(ndays-day-Wait))
                Amount = 0
                for y in range(maxi):
                    Amount += vBooks[sBooks[y]]
                z = Amount/(Wait+2)

                libraries[index][6] = z
                if m1 < z:
                    m1 = z
                    m2 = Uniq
                    ID = index
                elif m1 == z and m2 < Uniq:
                    m2 = Uniq
                    ID = index
        
        count = 0
        for x in libraries[ID][5]: 
            for y in whereBooks[x]:
                if y in libraries and y != ID and x in libraries[y][5]:
                    libraries[y][6] -= vFreq[x]
                    libraries[y][5].remove(x)
                    libraries[y][1] -= 1
            count += 1
            if count == maxi:
                break

        return [ID,libraries]
    else:
        print(day)
        ID = -1
        m1 = 0
        for x in libraries:
            [index,NBooks,Wait,Ship,Amount,sBooks,Uniq] = libraries[x]
            if NBooks and index not in setlib:
                maxi = min(NBooks,Ship*(ndays-day-Wait))
                Amount = 0
                for y in range(maxi):
                    Amount += vBooks[sBooks[y]]
                z = Amount

                libraries[index][6] = z
                if m1 < z:
                    m1 = z
                    ID = index
        return [ID,libraries]

#################################################
# Read the in-file
#################################################
basedir = __file__
for x in range(len(basedir)-1,-1,-1):
    if (basedir[x] == '/') :
        basedir = basedir[:x+1]
        break
indir = basedir + 'TestC.txt'
print(indir)

infile = open(indir,"r", encoding='utf-8')
text = infile.read()
infile.close()

text = text.split('\n')

biglist = []
for renglon in text:
    if renglon:
        aux = list (map (int, renglon.split (' ')))
        biglist.append(aux)

#################################################
# Build the dictionary of the libraries
#################################################
[nbooks,nlibs,ndays] = biglist[0]
vBooks = biglist[1] # Value of the books

whereBooks = {}
libraries = {}
vFreq = []
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
    
    libraries[index] = [index,NBooks,Wait,Ship,Amount,sBooks,0]

bfreq = {} #Books frequencies
for x in libraries:
    for y in libraries[x][5]:
        bfreq[y] = bfreq.get(y,0)+1

vFreq = {} #Inverse number
for x in sorted(bfreq):
    vFreq[x] = 1/bfreq[x]

for x in range(nlibs):
    Uniq = 0
    for y in libraries[x][5]:
        Uniq += vFreq[y]
    libraries[x][6] = Uniq

#################################################
# Simulation of the days
#################################################
past, actual = 0, 0 # Count and limit of the waiting days
setlib  = set() # Set libraries taken, it has O(1) to search in it
queue   = set() # Queue of libraries where we are taking books
taken   = set() # Books taken
tlib    = []    # Libararies taken, it has order
recents = []    # Books just taken
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
            setlib.add(check)
            mydict[check] = []
        
        flag = False
        past = 1
        
        [check,libraries] = A(recents,libraries,whereBooks,ndays,day,setlib,vBooks,vFreq)
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
            
            [check,libraries] = A(recents,libraries,whereBooks,ndays,day,setlib,vBooks,vFreq)
            actual = libraries[check][2] if check >= 0 else 10**8
            recents = []
    
    #############################################
    # Pick up the books for each librarie
    #############################################
    if queue:
        delete = []
        for element in queue:
            [index,NLibros,Wait,Ship,Amount,sBooks,Uniq] = libraries[element] 

            count = 0
            for x in sBooks:
                if x not in taken:
                    recents.append(x)
                    total += vBooks[x]
                    mydict[element] += [x]
                    taken.add(x)
                    count += 1
                if count == Ship:
                    break

            if x == sBooks[-1]:
                delete.append(index)

        for rr in delete:
            queue.remove(rr)
            del libraries[rr]
    
    if day%500==0:
        print(day,len(tlib),len(libraries),total)

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

outdir = basedir + 'C '+ outdir + '.txt'
outfile = open(outdir,"w+", encoding='utf-8')
outfile.write(mytext)
outfile.close()