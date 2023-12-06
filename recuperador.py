# -*- coding: cp1252 -*-
import random
import sys
import re
import time
try:
    import cPickle as pickle
except:
    import pickle

def load_object(file_name):
    with open(file_name, 'rb') as fh:
        obj = pickle.load(fh)
    return obj
# TO-DO ARREGLAR ERROR DE PALABRA PERU #
def separar(consulta):
    # OJO: se pide al usuario una sintaxis determinada  #
    # para los sintagmas. Ver el leeme.                 #
    partes = {u"text":0,u"headline":1,u"category":2,u"date":3}
    # Buscar y borrar sintagmas de la consulta #
    multis = re.findall("^.*\"",consulta,re.LOCALE|re.UNICODE)
    if multis!=[]:
        multis = [x for x in multis[0].split("\"") if x!=u'' and x!=u' ']
    consulta = re.sub("^.*\"","",consulta,re.LOCALE|re.UNICODE)
    # Buscar las palabras que tienen etiqueta (headline,etc) #
    # y luego quitarlas de la consulta                       #
    secciones = re.findall("\w+:",consulta,re.LOCALE|re.UNICODE)
    palabras_sec = re.findall(":\w+",consulta,re.LOCALE|re.UNICODE)
    consulta = re.sub(":\w+","",consulta,re.LOCALE|re.UNICODE)
    # Quitar dos puntos al inicio o final (":") #
    multis = [x.split(" ") for x in multis]
    palabras_sec = [re.split("\W+",x,re.LOCALE|re.UNICODE) for x in palabras_sec]
    palabras_sec = map(lambda x: [y for y in x if y!=u''][0],palabras_sec)
    secciones = [re.split("\W+",x,re.LOCALE|re.UNICODE) for x in secciones]
    secciones = map(lambda x: [y for y in x if y!=u''][0],secciones)
    # Guardar las palabras que no tienen etiqueta (las "text" por defecto) #
    resto = [x for x in consulta.split() if x not in partes]
    secciones += [u"text" for x in range(len(resto))]
    palabras_sec += resto
    # FIN #
    res = (multis,zip(secciones,palabras_sec))
    return res

def interseccion(p1,p2,texto):
    res = []
    i = j = 0
    while i<len(p1) and j<len(p2):
        if p1[i][0]==p2[j][0]:
            res.append([p1[i][0],p1[i][1]+p2[j][1] if texto else p1[i][1]])
            i,j = (i+1,j+1)
        elif p1[i][0]<p2[j][0]:
            i+=1
        else:
            j+=1
    return res


def procesar(ind, q):
    partes = {u"text":0,u"headline":1,u"category":2,u"date":3}
    resultados = ind.get((partes[q[1][0][0]],q[1][0][1]),[]) if len(q[1])>0 else []
    vacio_ini = True if resultados==[] else False
    # Palabras #
    if len(q[1])>0:
        for ap, pal in q[1][1:]:
            posting = ind.get((partes[ap],pal),[])
            resultados = interseccion(resultados,posting,ap==u"text")
            if resultados==[]: # Ley de absorcion #
                return []
    # Sintagmas #
    for k, sintagma in enumerate(q[0]):
        inter_pal = ind.get((0,sintagma[0]),[])
        for pal in sintagma[1:]:
            posting = ind.get((0,pal),[])
            inter_pal = interseccion(inter_pal,posting,True)
            if inter_pal==[]: # Absorcion #
                break
        post_local = []
        for docid, posting in inter_pal:
            noticia = docs[docid[0]][0][docid[1]]
            posiciones = []
            for pos in posting:
                if noticia[pos]==sintagma[0] and pos<len(noticia)-len(sintagma)+1:
                    n_grama = noticia[pos:pos+len(sintagma)]
                    if sintagma==n_grama:
                        posiciones.append(pos)
            if posiciones!=[]:
                post_local.append(([(docid[0],docid[1]),posiciones]))
        if vacio_ini:
            resultados = post_local
            vacio_ini = False
        elif resultados==[]:
            break
        else:
            resultados = interseccion(resultados,post_local,True)
    return resultados

def snippet(docs, docs_consulta):
    textos = []
    for docid, posting_list in docs_consulta:
        textos.append(" ".join(docs[docid[0]][1][docid[1]]).upper())
        for pos in [random.choice(posting_list) for x in range(5)]:
            noticia = docs[docid[0]][0][docid[1]]
            anterior = noticia[pos-10:pos] if pos>=10 else noticia[:pos]
            posterior = noticia[pos+1:pos+10] if pos+10<len(noticia) else noticia[pos:]
            textos.append(" ".join(anterior+[noticia[pos].upper()]+posterior))
    return textos
                
fichero = "indice.dat"
print(u"Cargando índice...")
docs, ind = load_object(fichero)
print(u"Índice cargado")
while True:
    print("Introduzca su consulta: ")
    consulta = unicode(raw_input().rstrip().lower(),sys.stdin.encoding)
    cons_limpia = separar(consulta)
    print(cons_limpia)
    resultado = procesar(ind, cons_limpia)
    print("Consulta finalizada")
    print(u"Se encontró/encontraron "+str(len(resultado))+" resultado/s")
    if len(resultado)==0:
        print("Su consulta no produjo resultados")
    elif len(resultado)<=2:
        for d in resultado:
            print(" ".join(docs[d[0][0]][1][d[0][1]]).upper())
            print(" ".join(docs[d[0][0]][0][d[0][1]]))
    elif len(resultado)<=5:
        print("\n\n".join(snippet(docs, resultado)))
    elif len(resultado)<=10:
        for d in resultado[:len(resultado)]:
            print(" ".join(docs[d[0][0]][1][d[0][1]]).upper())
    else:
        for d in resultado[:10]:
            print(" ".join(docs[d[0][0]][1][d[0][1]]).upper())
