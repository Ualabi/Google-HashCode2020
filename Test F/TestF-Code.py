#################################################
# Function that returns the next librarie to take
#################################################
def A(libraries,whereBooks,ndays,day,setlib,vBooks):
    ID = -1
    m1 = 0
    for x in range(len(libraries)):
        if x not in setlib:
            [Index,NBooks,Wait,Ship,Amount] = libraries[x][:5]
            maxi = min(NBooks,Ship*(ndays-day-Wait))
            maxi = max(1,maxi)
            Amount = 0
            for y in range(maxi):
                Amount += vBooks[libraries[x][5][y]]
            aux = Amount/(Wait+30)
            libraries[x][4] = aux
            if m1 < aux:
                ID = Index
                m1 = aux
    
    if ID >= 0:
        delete = []
        count = 0
        for x in libraries[ID][5]:
            delete.append(x)
            count += 1
            if count == maxi:
                break
        
        for x in delete:
            for y in whereBooks[x]:
                if y != ID and x in libraries[y][5]:
                    libraries[y][5].remove(x)
                    libraries[y][4] -= vBooks[x]
                    libraries[y][1] -= 1

    return [ID,libraries]

#################################################
# Read the in-file
#################################################
basedir = __file__
for x in range(len(basedir)-1,-1,-1):
    if (basedir[x] == '/') :
        basedir = basedir[:x+1]
        break
indir = basedir + 'TestF.txt'
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
    
    libraries[index] = [index,NBooks,Wait,Ship,Amount,sBooks]

#################################################
# Simulation of the days
#################################################
past, actual = 0, 0 # Count and limit of the waiting days
setlib  = set() # Set libraries taken, it has O(1) to search in it
queue   = set() # Queue of libraries where we are taking books
taken   = set() # Books taken
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
            setlib.add(check)
            mydict[check] = []
        
        flag = False
        past = 1
        
        [check,libraries] = A(libraries,whereBooks,ndays,day,setlib,vBooks)
        actual = libraries[check][2] if check >= 0 else 10**8
    else: # We add 1 to the count of the waiting days
        if actual > 1: # Count the day
            past += 1
            if past == actual:
                flag = True
        elif actual == 1:
            queue.add(check)
            tlib.append(check)
            setlib.add(check)
            mydict[check] = []
            
            flag = False
            past = 1
            
            [check,libraries] = A(libraries,whereBooks,ndays,day,setlib,vBooks)
            actual = libraries[check][2] if check >= 0 else 10**8
    
    #############################################
    # Pick up the books for each librarie
    #############################################
    if queue:
        delete = []
        for element in queue:
            [ID,NLibros,Wait,Ship,Amount,sBooks] = libraries[element] 

            count = 0
            for x in sBooks:
                if x not in taken:
                    total += vBooks[x]
                    mydict[element] += [x]
                    taken.add(x)
                    count += 1
                if count == Ship:
                    break

            if x == sBooks[-1]:
                delete.append(ID)

        for rr in delete:
            queue.remove(rr)
    
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

outdir = basedir + 'F '+ outdir + '.txt'
outfile = open(outdir,"w+", encoding='utf-8')
outfile.write(mytext)
outfile.close()