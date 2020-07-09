#####_0_parámetros
#
#distancia máxima entre fragmentos de dos instrumentos distintos, por defecto 3
distancia_maxima=3
#
#tiempo medio que cada instrumentos toca cada fragmento, por defecto 60
tiempo_medio=30
varianza=11
#
#lista de sintes (o instrumentos) que participan en nuestro ensemble:    
lsi=[gong,charm,zap,karp,keys,blip,charm,zap,karp,keys,blip]#,gong]
#
#bpm para nuestro pulso básico (la corchea)
Clock.bpm = 222
#
#eleccion del metrónomo para la interpretación
metronomo = True
#
#respuesta indica en beats cada cuanto se actualizará la interpretación
respuesta=12
#

#####_1_constantes y funciones
#
#obtenemos el directorio de trabajo actual (cwd=current working directory)
import os
cwd = os.getcwd()
#
#dirigimos al directorio actual para obtener información de los otros archivos
import sys
sys.path.append(cwd)
#
#importamos desde el parser la representación interna de nuestra partitura,
import abcparser
from abcparser import fragmentos
#
#importamos los demás módulos que necesitaremos
from random import random,randint
import numpy
#
#cambiamos el compás a 1por4 por comodidad de trabajo con FoxDot
#así, identificamos pulso con compás y no tenemos dos "medidas" diferentes
Clock.meter=(1,4)
Clock.time_signature=(1,4)
#
#trabajamos con la escala cromática, ya que es la que hemos usado con el parser
#y es la que da mayor flexibilidad al incluir las 12 notas posibles
Scale.default="chromatic"
#
###
#
#extraemos la información por fragmento: alturas (notas) y ritmo (duraciones)
nF = len(fragmentos) #número total de fragmentos!!
#
fNotas = [elem[0] for elem in fragmentos] #notas en cada fragmento
#
def convDur(n):
    '''
    convierte las duraciones negativas en silencios
    n: duración a convertir
    '''
    if n<0:
        return rest(-n)
    else:
        return n
#
fDurPrima = [elem[1] for elem in fragmentos]
fDurs = [] #duraciones en cada fragmento
#
for elem in fDurPrima:
    aux=[]
    for x in elem:
        #vamos a trabajar con base de corcheas (de ahí el proporcion=2)
        proporcion=2.0
        aux.append(convDur(proporcion*x))
    fDurs.append(aux)
#
#en pats guardamos la información de alturas y ritmo de los fragmentos
#o patrones, que luego pasaremos a cada player.
pats=[] # lista con los pares ([notas],[duraciones]) de cada fragmento!!
#
for i in range(nF):
    pats.append( (fNotas[i],fDurs[i]) )
#
durs = [float(sum(elem[1])) for elem in pats] #duracion total por fragmento!!
#
###
#
#lp: lista de players, máximo 35
#están por parejas, por su posterior uso alternado
lpl=[ [p0,p1] , [p2,p3] , [p4,p5] , [p6,p7] , [p8,p9] ,
      [s0,s1] , [s2,s3] , [s4,s5] , [s6,s7] , [s8,s9] ,
      [t0,t1] , [t2,t3] , [t4,t5] , [t6,t7] , [t8,t9] ,
      [q0,q1] , [q2,q3] , [q4,q5] , [q6,q7] , [q8,q9] ,
      [r0,r1] , [r2,r3] , [r4,r5] , [r6,r7] , [r8,r9] ,
      [v0,v1] , [v2,v3] , [v4,v5] , [v6,v7] , [v8,v9] ,
      [w0,w1] , [w2,w3] , [w4,w5] , [w6,w7] , [w8,w9] ]
#
#lista de sintes predefinidos que responden bien: a partir de estos elegir
lsi_predefs=[gong,charm,zap,karp,keys,blip]\
    +[arpy,nylon,pluck,bell,bass]\
    +[pads,ambi,sinepad,razz]\
    +[viola,ripple,spark,star,saw,varsaw,swell,quin,pulse,orient]
#lista de sintes que responden peor
lsi_predefs_peor=[dirt,lazer,dab,rave,dub,feel,sitar,pasha,twang,prophet]
#lsi: lista de sintes a usar lsi, pueden ser de FoxDot o importados!!
#pueden repetirse, tantas veces como se quiera,
#organización orientativa: [buenos]+[placados]+[pads]+[granulados]
'''
lsi=[gong,charm,zap,karp,keys,blip]
    +[arpy,nylon,pluck,bell,bass]
    +[pads,ambi,sinepad,razz]
    +[viola,ripple,spark,star,saw,varsaw,swell,quin,pulse,orient]
'''
#nota: lsi es uno de los parámetros, pues el usuario debe elegir su ensemble
#
#nsi: numero total de sintes, máximo 20
#para no sobrecargar el servidor de audio de SuperCollider
nsi = min(len(lsi),20)
#
#la lista actuales indica los datos actuales de cada instrumentos en cierto momento
actuales = [ [0,0,0] for i in range(nsi)] # [indice_fragmento, delay_acumulado, cuando_empieza] !!  .
#
###
#
def toca(fragmento_i,player_p,delay_d,sinte_s):
    '''
    fragmento_i: indice del fragmento a tocar (0 a nF-1)
    player_p: indice (0 a 1) del player que va a tocar
    sinte_s: indice del instrumento/sinte que va a tocar (0 a nsi-1)
    parámetros del player:
        notas: asociamos las notas del fragmento actual a las duraciones con una variable temporal:
        #degree = var(pats[fragmento_i][0],dur=pats[fragmento_i][1],start=now)
        dur: duraciones del fragmento actual
        #dur = pats[fragmento_i][1]
        delay: retraso en el inicio, indicado por delay_d
        amp: amplitud o volumen, para no sobrecargar la salida, "normalizamos" con nsi
        pan: panorama, elegimos un número aleatorio entre -1 (Left) y 1 (Right)
        #amp y pan para dar riqueza al resultado sonoro (espacio y dinámicas)
    '''
    lpl[sinte_s][player_p] >> lsi[sinte_s](var(pats[fragmento_i][0],dur=pats[fragmento_i][1],start=now),
                                           dur=pats[fragmento_i][1],
                                           delay=delay_d,
                                           amp=3*random()/nsi,
                                           pan=2*random()-1)
#
def para(player_p):
    '''
    detiene el player indicado
    player_p: player que se quiere detener
    '''
    player_p.stop()
#
def arranca(i,sinte_s):
    '''
    i: indice del fragmento desde el que se arranca (para pruebas se deja libre)
    sinte_s: indice del sinte (0 a nsi-1)
    todos los instrumentos empiezan a la vez, en el instante 0 (para la coordinación),
    luego establecemos el tiempo interno a 0 (-0.2 por la latencia)
    devuelve la lista [numero de fragmento, delay_acumulado, cuándo empieza]
    '''
    #Clock.set_time(-0.3)
    #
    lpl[sinte_s][i%2] >> lsi[sinte_s](var(pats[i][0],dur=pats[i][1],start=now),
                                      dur=pats[i][1], delay=0,
                                      amp=3*random()/nsi, pan=random()*2-1)
    #
    return [i,0,0] # [numero de fragmento, delay_acumulado, cuándo empieza]
#
def siguiente(actual,sinte_s):
    '''
    hace avanzar a cierto instrumento sinte_s al fragmento siguiente,
    coordinando el entrelazado o transición entre fragmentos
    actual: lista con [numero de fragmento, delay_acumulado, cuándo empieza] del
    fragmento que está sonando actualmente, del cual queremos salir
    sinte_s: indice del sinte que queremos que avance
    es la función más complicada, por la sincronización de FoxDot:
        tenemos que calcular cuándo lanzar el siguiente fragmento para que empiece 'en fase'
        calculamos el delay necesario para que se solape bien con el final
        del fragmento anterior, manejando las excepciones necesarias
        programamos (schedule) el fin del fragmento anterior con la función 'para'
        programamos (schedule) el comienzo del nuevo fragmento, con la función 'toca'
    devuelve la lista [numero de fragmento, delay_acumulado, cuándo empieza]
    '''
    i0=actual[0] #indice del fragmento que suena actualmente
    i1=i0+1 #indice del fragmento siguiente, al que queremos avanzar
    #
    dac=actual[1] #delay acumulado que lleva el fragmento que suena actualmente
    #
    d0=durs[i0] #duración total del fragmento que suena actualmente
    d1=durs[i1] #duración del siguiente fragmento
    #
    c=int(Clock.now()+0.5) #+1 #el pulso actual, con margen para la latencia
    c0=Clock.mod(d0)+dac #momento en el que acaba el fragmento actual
    c1=Clock.mod(d1) #momento en que debería empezar el fragmento siguiente para ir 'en fase'
    #
    #caso 1: la llamada a la función no deja tiempo a reacción
    while c>c1:
        c1=c1+d1
    #
    #caso 2: el fragmento actual acaba muy rápido (c>c0, quizá el fragmento actual es muy corto)
    #o no da tiempo a coordinar la entrada del siguiente (c1>c0, quizá porque sea muy largo)
    while c1>c0 or c>c0:
        c0=c0+d0
    #
    #caso 3: se solapan los dos fragmentos a causa del delay acumulado
    #luego hay que retrasar la entrada del siguiente
    while c0-dac-c1-d1>=0:
        c1=c1+d1
    #
    #ahora calculamos el delay que va a acumular el fragmento siguiente al actual
    if c0>c1:
        delay=c0-c1
    else:
        delay=0
    #
    #si quedan fragmentos, pasamos al siguiente
    if i1<len(durs):
        #teniendo en cuenta la latencia, programamos 'tocar' el siguiente
        Clock.schedule(toca, c1-0.1, args=[i1,i1%2,delay,sinte_s])
    #
    #teniendo en cuenta la latencia, programamos 'parar' el actual
    Clock.schedule(para,c0-dac-0.1,args=[lpl[sinte_s][i0%2]])
    #
    #devolvemos la lista con la info del siguiente: 
    return [i0+1,delay,c1+delay] # [indice del fragmento, delay_acumulado,cuándo empieza]
#
def quiza_siguiente(actual,sinte_s):
    '''
    función que introduce una pequeña irregularidad en el avance de fragmentos
    dependiendo aleatoriamente de cierta probabilidad
    '''
    ra=random()
    probabilidad=0.0
    if ra>probabilidad and actuales[sinte_s][2]<int(Clock.now()) and actuales[sinte_s][0]<len(durs):
        #pasamos al siguiente fragmento
        return siguiente(actual,sinte_s)
    else:
        #nos mantenemos en el fragmento actual
        print("NO se avanza aún",ra)
        return actual
#
def avanza(iii):
    '''
    iii: indice del sinte que tiene que avanzar al siguiente fragmento
    '''
    actuales[iii]=quiza_siguiente(actuales[iii],iii)
    print(iii)
#
def volumen(iii,v):
    '''
    función para regular el volumen de un sinte, es decir, de sus dos players asociados
    en caso de necesitarlo por desequilibrios
    iii: el indice del sinte
    v: el volumen que queremos asignar
    '''
    (lpl[iii][0]).amp=v
    (lpl[iii][1]).amp=v
#

#
#####_2_normas y PLAY
#
#numpy.random.normal(media,varianza,num)
#devuelve una lista de num valores según una distribución normal N(media,varianza)
teb=int(tiempo_medio*Clock.bpm/60) #tiempo_medio en beats (donde tiempo_medio es un parámetro)
veb=int(varianza*Clock.bpm/60) #varianza en beats (donde varianza es un parámetro)
#
def normas(actuales):
    #norma 1: respetar la distancia
    fragmentos_actuales=[actuales[i][0] for i in range(len(actuales))]
    maximo=max(fragmentos_actuales)
    minimo=min(fragmentos_actuales)
    distancia_actual=maximo-minimo
    if distancia_actual>distancia_maxima:
        for ik in range(len(actuales)):
            if actuales[ik][0]==minimo:
                #print("obligado:distancia")
                avanza(ik)
    #norma 2: mantenerse cierto tiempo, distribución Normal
    cuanto_cada_uno = [int(Clock.now())-actuales[iii][2]-actuales[iii][1] for iii in range(len(actuales))]
    probabilidades_normales=numpy.random.normal(teb,veb,len(actuales))
    for ik in range(len(actuales)):
        if (cuanto_cada_uno[ik] > probabilidades_normales[ik]) and fragmentos_actuales[ik]<(nF-1):
            #print("obligado:normal")
            avanza(ik)
    #norma 3: sincronización final
    final = all([fragmentos_actuales[ik]==(nF-1) for ik in range(len(actuales))])
    if final:
        print("FINAL")
        finc(actuales)
    else:
        Clock.future(respuesta,dami,args=[lambda x : x])
    #return 0
#
def finc(actuales):
    '''
    maneja la sincronización final de la obra
    '''
    teb1=teb/2.0
    for iii in range(nsi):
        ra=random()*10
        ppp=random()
        vvv=expvar([2.0/nsi,ppp/nsi],[teb1+ra,teb1-ra,0.5*teb1+ra,1.5*teb1-ra])
        Clock.schedule(volumen,args=(iii,vvv))
        Clock.future(4*teb1+2,volumen,args=(iii,2.0/nsi))
    Clock.future(4*teb1,lambda:Clock.clear())
#
#
###_main
#
#
def dami(f):
    aux=normas(actuales)
    e = f(actuales)
    print(e)
#
Clock.set_time(-0.15)
#
for ik in range(nsi):
    actuales[ik]=arranca(0,ik)
#
if metronomo:
    #el instrumento marimba hace de "metrónomo" a corcheas
    m1 >> marimba(12,dur=[0.5,rest(0.5)],amp=0.4)
#
print(actuales)
#
Clock.future(respuesta,dami,args=[lambda x : x])

###
