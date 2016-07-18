import sys
sys.path.insert(0, '/Settings')

import mmap, Settings.settingsMT as st, random, Settings.settingsAN as settingsAN, numpy as np

def creaPersonas(S):
    N = len(S)
    for i in range(0, N):
        if i < N/7:
            S[i] = 'H'
        elif i > N*3/4:
            S[i] = 'R';
        else:
            S[i] = 'C';

    return S
    
def escribeTodo(propC, propH, propR, iRed):
    nombre = 'Resultados/Montecarlo/resu_r' + str(iRed) + '.txt'
    outfile = open(nombre, 'wt')
    for t in range(0, len(propC)):
        l = [str(t), str(propC[t]), str(propH[t]), str(propR[t])]
        data = '\t'.join("%s" % (x) for x in l)
        data = data + "\n"
        outfile.write(data)
    outfile.close()

def dameN(filename):
    maximo = 0
    f = open(filename, "rt")

    for linea in f:
        linea = linea.split()
        linea = map(int, linea)
        maxv = max(linea)
        if maxv > maximo:
            maximo = maxv

    return maximo +1

def montecarlo(S, red):
    Scopia = S
    for iPers in range(0, len(S)):
        producto = 1
        if Scopia[iPers] == 'R':
            if random.random() < st.lista['r']:
                Scopia[iPers] = 'H'
        elif Scopia[iPers] == 'H':
            if random.random() < st.lista['delta1']:
                Scopia[iPers] = 'C'
            else:
                for j in range(0, red.conec[iPers]):
                    indice = red.conex[iPers][j]
                    indice = indice.astype(int)
                    if S[indice] == 'C':
                        producto *= 1 - st.lista['alfa']

                prob = producto
                if random.random() > prob:
                    Scopia[iPers] = 'C'
        else:
            #Si es Corrupto puede pasar a Honesto con delta2:
            if random.random() < st.lista['delta2']:
                Scopia[iPers] = 'H'
            else:
                if random.random() < st.lista['b']:
                    Scopia[iPers] = 'R'
                else:
                    for j in range(0, red.conec[iPers]):
                        indice = red.conex[iPers][j]
                        indice = indice.astype(int)
                        if S[indice] == 'H':
                            producto *= (1 - st.lista['beta'])

                    prob = producto
                    if random.random() > prob:
                        Scopia[iPers] = 'R'

    S = Scopia
    return S

def montecarlo2(S, red):
    Scopia = S
    for iPers in range(0, len(S)):
        producto = 1
        if Scopia[iPers] == 'R':
            if random.random() < st.lista['r']:
                Scopia[iPers] = 'H'
        elif Scopia[iPers] == 'H':
            if random.random() < st.lista['delta1']:
                Scopia[iPers] = 'C'
        else:
            #Si es Corrupto puede pasar a Honesto con delta2:
            if random.random() < st.lista['delta2']:
                Scopia[iPers] = 'H'
            else:
                if random.random() < st.lista['b']:
                    Scopia[iPers] = 'R'

    S = Scopia
    return S


def importarDatos(cantidad):
    for i in range(0, cantidad):
        filename = settingsAN.lista['directorio'] + settingsAN.lista['nombre_archivo'] + str(i) + '.txt'
        if i == 0:
            lon = len(open(filename).readlines())
            propC = np.zeros((lon, 1))
            propH = np.zeros((lon, 1))
            propR = np.zeros((lon, 1))
        else:
            lon = len(open(filename).readlines())
            aprop = np.zeros((lon, 1))
            #De momento todos los archivos deben ser del mismo tamaño, si no salta la excepción y salta el archivo
            try:
                propC = np.hstack((propC, aprop))
            except ValueError:
                print('Los archivos no tienen la misma longitud')
                break

            propH = np.hstack((propH, aprop))
            propR = np.hstack((propR, aprop))

        with open(filename, 'rt') as f:
            for linea in f:
                if linea.startswith('#'):
                    continue
               
                linea = linea.split()
                t = int(linea[0])
                #Se entiende que el tiempo siempre va de uno en uno, así que:
                propC[t][i] = float(linea[1])
                propH[t][i] = float(linea[2])
                propR[t][i] = float(linea[3])
                #propC.append(float(linea[1]))

        f.close()
    return propC, propH, propR

def desvstaPesada(desv):
    aux = 1/(desv*desv)
    final = 1/sum(aux)
    return final