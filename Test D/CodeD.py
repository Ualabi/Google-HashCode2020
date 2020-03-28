#import copy

def A(recent,bibliotecas,dondeLibros,nd,dia,setlib,valorLibros,pasado,valorFrecuencia,i):
    #bibliotecas.append([index,NLibros,Espera,Prestar,suma,valortop,myarr,uniq])
    for x in recent:
        for y in dondeLibros[x]:
            if y in bibliotecas and x in bibliotecas[y][6]:
                bibliotecas[y][7] -= valorFrecuencia[x]
                bibliotecas[y][6].remove(x)
                bibliotecas[y][4] -= valorLibros[x]
                bibliotecas[y][1] -= 1
    
    #aux = {}
    m1 = 0
    m2 = 0
    m3 = 0
    for x in bibliotecas:
        [index,NLibros,Espera,Prestar,suma,valortop,myarr,uniq] = bibliotecas[x]
        if NLibros and index not in setlib:
            maxi = min(NLibros,Prestar*(nd-dia))
            suma = 0
            for y in range(maxi):
                suma += valorLibros[bibliotecas[index][6][y]]
            z = suma/(Espera+i)

            bibliotecas[index][5] = z
            if m1 < z:
                m1 = z
                m2 = NLibros
                m3 = uniq
                ID = index
            elif m1 == z and m2 < NLibros:
                m2 = NLibros
                m3 = uniq
                ID = index
            elif m2 == NLibros and m3 < uniq:
                m3 = uniq
                ID = index
            #aux[bibliotecas[x][5]] = [bibliotecas[x][0],suma,Espera,Prestar]
    
    #print(bibliotecas[ID])
    
    count = 0
    for x in bibliotecas[ID][6]: 
        for y in dondeLibros[x]:
            if y in bibliotecas and y != ID and x in bibliotecas[y][6]:
                bibliotecas[y][7] -= valorFrecuencia[x]
                bibliotecas[y][6].remove(x)
                bibliotecas[y][4] -= valorLibros[x]
                bibliotecas[y][1] -= 1
        
        count += 1
        if count == maxi:
            break

    #print(ID)
    return [ID,bibliotecas]

def Solution(bibliotecas, valorLibros, valorFrecuencias, dondeLibros, i):
    ######################
    # Codigo
    ######################
    past, actual = 0, 0
    flag = True
    queue = set()
    tomados = set()
    recent = []
    libraries = []
    setlib = set()
    mydict = {}
    check = None
    total = 0

    for x in range(nd):
        if flag:
            if check:
                queue.add(check)
                libraries.append(check)
                setlib.add(check)
                mydict[check] = []
            
            flag = False
            past = 1
            
            [check,bibliotecas] = A(recent,bibliotecas,dondeLibros,nd,x,setlib,valorLibros,check,valorFrecuencia,i)
            actual = bibliotecas[check][2]
            recent = []
        else:
            if actual == 1:
                queue.add(check)
                libraries.append(check)
                setlib.add(check)
                mydict[check] = []
                
                flag = False
                past = 1
                
                [check,bibliotecas] = A(recent,bibliotecas,dondeLibros,nd,x,setlib,valorLibros,check,valorFrecuencia,i)
                actual = bibliotecas[check][2]
                recent = []
            else:
                past += 1
                if past == actual:
                    flag = True
        
        if queue:
            borrar = []
            for element in queue:
                ID = bibliotecas[element][0]
                Prestar = bibliotecas[element][3]
                myarr = bibliotecas[element][6]
                #print(len(myarr),' , ',Prestar,' ; ',end='')

                llevo = 0
                for voy in myarr:
                    if voy not in tomados:
                        total += valorLibros[voy]
                        mydict[element] += [voy]
                        tomados.add(voy)
                        recent.append(voy)
                        llevo += 1
                    if llevo == Prestar:
                        break

                if voy == myarr[-1]:
                    borrar.append(ID)

            for rr in borrar:
                queue.remove(rr)
                del bibliotecas[rr]
        
        #if x%1000 == 0:
        #    print(x,total)
        #if x%10==0:
        #    print(x,len(libraries),len(mydict),len(bibliotecas),len(dondeLibros),total,queue,check,Prestar,past,actual)
            #print(len(dondeLibros))

    print(i,x,total,len(libraries))
    return[total,mydict,libraries]

##############################
#Lectura del archivo
##############################
archivo = open("C:\\Users\\Xps 9350\\OneDrive\\Google\\Hashcode2020\\5E.txt","r", encoding='utf-8') #Leemos con UTF-8 para que detecte los caracteres especiales
text = archivo.read()
archivo.close()

text = text.split('\n')

biglist = []
for renglon in text:
    if renglon:
        aux = list (map (int, renglon.split (' ')))
        biglist.append(aux)

[nb,nl,nd] = biglist[0]
valorLibros = biglist[1]
valorFrecuencia = []

dondeLibros = {}

bibliotecas = {}
count = 2

valortop = 0
uniq = 0

for index in range(nl):
    [NLibros,Espera,Prestar] = biglist[count]
    count += 1
    
    libros = biglist[count]
    count += 1

    aux = {}
    for ID in libros:
        aux[valorLibros[ID]] = aux.get(valorLibros[ID],[])+[ID]
    
    suma = 0
    myarr = []
    for x in sorted(aux,reverse=True):
        myarr += aux[x]
        for y in aux[x]:
            dondeLibros[y] = dondeLibros.get(y,[])+[index]
            suma += valorLibros[y]
    
    bibliotecas[index] = [index,NLibros,Espera,Prestar,suma,valortop,myarr,uniq]

aux = {}
for x in range(nl):
    for y in bibliotecas[x][6]:
        aux[y] = aux.get(y,0)+1

valorFrecuencia = {}
for x in sorted(aux):
    valorFrecuencia[x] = 1/aux[x]

for x in range(nl):
    count = 0
    for y in bibliotecas[x][6]:
        count += valorFrecuencia[y]
    bibliotecas[x][7] = count 

[total,mydict,libraries] = Solution(bibliotecas,valorLibros,valorFrecuencia,dondeLibros,2)

##############################
#Convertir variables texto
##############################
mytext = ''
mytext += str(len(mydict)) + '\n'
for x in libraries:
    mytext += str(x) + ' ' + str(len(mydict[x])) + '\n'
    r = ''
    for y in mydict[x]:
        r += str(y) + ' '
    
    if r:
        mytext += r[:-1] + '\n'
    else:
        mytext += '\n'

archivo = open("C:\\Users\\Xps 9350\\OneDrive\\Google\\Hashcode2020\\pruebas.txt","w+", encoding='utf-8') #Escribimos con UTF-8 para escribir los caracteres especiales
archivo.write(mytext)
archivo.close()