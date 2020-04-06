import os
#################################################
# Read the in-file
#################################################
basedir = __file__
for x in range(len(basedir)-1,-1,-1):
    if (basedir[x] == '/') :
        basedir = basedir[:x+1]
        break
entries = os.listdir(basedir)
print(entries,'\n')

for xfile in entries:
    if xfile[-3:] == 'txt':
        indir = basedir + xfile
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
        vBooks = biglist[1] # Value of the books

        libraries = {}
        order = {}
        row = 2

        for index in range(nlibs):
            [NBooks,Wait,Ship] = biglist[row]
            row += 1
            
            books = biglist[row]
            row += 1
            
            libraries[index] = [index,NBooks,Wait,Ship,books]

        minVL = min(vBooks)
        maxVL = max(vBooks)

        minL = float('inf')
        maxL = 0
        minE = float('inf')
        maxE = 0
        minP = float('inf')
        maxP = 0

        for x in libraries:
            [index,NBooks,Wait,Ship,books] = libraries[x]

            minL = min(minL,NBooks)
            maxL = max(maxL,NBooks)

            minE = min(minE,Wait)
            maxE = max(maxE,Wait)
            
            minP = min(minP,Ship)
            maxP = max(maxP,Ship)

        aux = {}
        for x in range(nbooks):
            aux[x] = 0

        for x in libraries:
            for y in libraries[x][4]:
                aux[y] += 1

        aux2 = {}
        for x in aux:
            aux2[aux[x]] = aux2.get(aux[x],0) + 1

        print("\n\n############################")
        print("File: ",xfile)
        print("There are ",nbooks," books")
        print("There are ",nlibs," libraries")
        print("There are ",ndays," days\n")

        print("min/max value of books:  ",minVL," / ",maxVL)
        print("min/max number of books: ",minL," / ",maxL)
        print("min/max waiting days:    ",minE," / ",maxE)
        print("min/max books shipped:   ",minP," / ",maxP,"\n")

        print("Frequencies of books overlap:")
        for x in sorted(aux2):
            print(x,' ',aux2[x])