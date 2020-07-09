from pyabc import * #importamos el paquete auxiliar completo
#
import os
cwd = os.getcwd() #cwd=current working directory, el directorio actual

#seleccionamos el archivo que queremos parsear, lo leemos y guardamos en txt
archivo='inC.abc'
path = cwd+'/'+archivo
file = open(path,'r')
txt = file.read()

#Tune es una clase de pyabc que se encargará de extraer los tokens
n = Tune(txt)

#creamos una cadena de notas y otra de alteraciones
#para reconocerlas luego más fácilmente
sNotas = "C.D.EF.G.A.Bc.d.ef.g.a.bc."
sAlteraciones = "_=^"

#fragmentos será la lista definitiva en la que guardamos la información
#relativa a cada fragmento con el formato [notas,duraciones]
fragmentos=[]
parentesis=False
llave=False
llaveS=False

for n in n.tokens:
    if isinstance(n,Note): #Note tiene métodos: note, duration,octave y accidental
        a=0 #alteración, por defecto, 0
        nota = sNotas.index(n.note)
        if n.accidental is not None:
            a = sAlteraciones.index(n.accidental)-1
        nota = (nota+a)%12 + 12*n.octave #ya tenemos la nota como número
        #
        if parentesis: #caso para las notas ligadas (más duración)
            if (pNot==[]):
                pNot.append(nota)
                pDur.append(n.duration)
            else:
                if (nota==pNot[-1]):
                    pDur[-1] += n.duration
        elif llave: #caso para las "grace notes", nota de partida
            lNot.append(nota)
            lDur.append(n.duration)
        elif llaveS: #caso para las "grace notes", nota de llegada
            proporcion=1.0/8
            lNot.append(nota)
            lDur.append(n.duration)
            lDur[-2] = lDur[-1]*proporcion
            lDur[-1] *= (1-proporcion)            
            for elem in lNot:
                fragmentNot.append(elem)
            for elem in lDur:
                fragmentDur.append(elem)
            llaveS=False
        else:
            fragmentNot.append(nota)
            fragmentDur.append(n.duration)
    #
    elif isinstance(n,Beam): #caso para los fragmentos
        if (n._text=="|:"): #se inicia el fragmento nuevo
            fragmentAux = []
            fragmentNot = []
            fragmentDur = []
        elif (n._text==":|"): #se acaba un fragmento
            fragmentAux.append(fragmentNot)
            fragmentAux.append(fragmentDur)
            fragmentos.append(fragmentAux)
    #
    elif isinstance(n,Rest): #caso para tratar los silencios
        #codificamos los silencios con duraciones negativas
        if (n._text=="z"):
            fragmentNot.append(0)
            fragmentDur.append(-1)
        elif (n._text=="z/"):
            fragmentNot.append(0)
            fragmentDur.append(-0.5)
        elif (n.length[0]==None):
            fragmentNot.append(0)
            duracionS=1.0/int(n.length[1])
            fragmentDur.append(-duracionS)
        elif (n.length[1]==None):
            fragmentNot.append(0)
            duracionS=int(n.length[0])
            fragmentDur.append(-duracionS)   
        else:
            fragmentNot.append(0)
            duracionS=float(n.length[0])/float(n.length[1])
            fragmentDur.append(-duracionS)
    #
    elif isinstance(n,Slur):#caso para las ( notas ligadas )
        if (n._text=="("):
            parentesis=True
            pNot = []
            pDur = []
        elif (n._text==")"):
            for elem in pNot:
                fragmentNot.append(elem)
            for elem in pDur:
                fragmentDur.append(elem)
            parentesis=False
    elif isinstance(n,GracenoteBrace): #caso para las {"grace notes"}
        if (n._text=="{"):
            llave=True
            lNot = []
            lDur = []
        elif (n._text=="}"):
            llave=False
            llaveS=True

#print(fragmentos)
