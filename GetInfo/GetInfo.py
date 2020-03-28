archivo = open("C:\\Users\\Xps 9350\\OneDrive\\Google\\Pruebas\\C.txt","r", encoding='utf-8') #Leemos con UTF-8 para que detecte los caracteres especiales
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

bibliotecas = []
count = 2
valor = 0
for index in range(nl):
    [NLibros,Espera,Prestar] = biglist[count]
    count += 1
    
    libros = biglist[count]
    count += 1

    bibliotecas.append([index,NLibros,Espera,Prestar,libros,valor])

minVL = min(valorLibros)
maxVL = max(valorLibros)

minL = 100000
maxL = 0
minE = 100000
maxE = 0
minP = 100000
maxP = 0
minV = 100000
maxV = 0
minR = 100000
maxR = 0


tomados = set()
suma = 0

for x in bibliotecas:
    [index,NLibros,Espera,Prestar,myarr,valor] = x
    for y in myarr:
        valor += valorLibros[y]
        if y not in tomados:
            tomados.add(y)
            suma += valorLibros[y]
    x[5] = valor

    minL = min(minL,NLibros)
    maxL = max(maxL,NLibros)

    minE = min(minE,Espera)
    maxE = max(maxE,Espera)
    
    minP = min(minP,Prestar)
    maxP = max(maxP,Prestar)

    minV = min(minV, valor)
    maxV = max(maxV, valor)

    ratio = valor/(Espera+NLibros/Prestar)
    minR = min(minR, ratio)
    maxR = max(maxR, ratio)

aux = {}
for x in range(nb):
    aux[x] = 0

for x in range(nl):
    for y in bibliotecas[x][4]:
        aux[y] += 1

aux2 = {}
for x in aux:
    aux2[aux[x]] = aux2.get(aux[x],0) + 1

print("#Hay ",nb," libros")
print("#Hay ",nl," librerias")
print("#Tienes ",nd," días\n")

print("#Lo máximo alcanzable es ",suma,"\n")

print("#min/max valor de libros: ",minVL," / ",maxVL)
print("#min/max número de libros: ",minL," / ",maxL)
print("#min/max espera: ",minE," / ",maxE)
print("#min/max prestar: ",minP," / ",maxP,"\n")

print("#min/max valor de librerias: ",minV," / ",maxV,)
print("#min/max ratio: ",minR," / ",maxR,"\n")

print("Frecuencias:")
for x in sorted(aux2):
    print(x,' ',aux2[x])