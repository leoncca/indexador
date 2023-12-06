# -*- coding: cp1252 -*-
import codecs
import sys
import re
import os
import time
try:
    import cPickle as pickle
except:
    import pickle
    
def save_object(object, file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh, pickle.HIGHEST_PROTOCOL)
        
def leerDocumentos(directorio,partes_doc):
    cortar = lambda st,ini,fin: st[st.find(ini)+len(ini):st.find(fin)]
    separar = lambda s,p,f: re.split("\W+", cortar(s,p,f),flags=re.LOCALE|re.UNICODE)
    docs_limpio = []
    for subds, ds, documentos in os.walk(directorio):
        for documento in documentos:
            docs_limpio.append([[] for elem in partes_doc])
            with codecs.open('/'.join([directorio,documento]),'r',encoding='UTF-8') as doc:
                articulos = doc.read().lower().split("<doc>")
                for i, separador in enumerate(partes_doc):
                    for j, art in enumerate(articulos):
                        if j>0: # j>0: porque al usar split() queda el primer elem vacio #
                            docs_limpio[-1][i].append([p for p in separar(art,separador[0],separador[1]) if p!=u''])
    return docs_limpio

def crearPostingLists(docs_limpio,partes_doc):
    posting_lists = {}
    for docid, doc in enumerate(docs_limpio):
        for ap, apartado in enumerate(doc):
            for i, articulo in enumerate(apartado):
                estaba_en_articulo = {}
                for pos, pal in enumerate(articulo):
                    if (ap,pal) not in posting_lists:
                        posting_lists[(ap,pal)] = []
                    if pal not in estaba_en_articulo:
                        posting_lists[(ap,pal)].append([(docid,i),[]])
                        estaba_en_articulo[pal] = True
                    posting_lists[(ap,pal)][-1][1].append(pos)
    return posting_lists 
                
directorio = "mini_enero" #sys.argv[1]
destino = "indice.dat" #sys.argv[2]
partes_doc = (("<text>","</text>"),
              ("<title>","</title>"),
              ("<category>","</category>"),
              ("<date>","</date>"))
print("Leyendo documentos...")
t_ini = time.time()
docs_limpio = leerDocumentos(directorio,partes_doc)
t_f = time.time() - t_ini
print("Finalizado. Tiempo aprox. consumido: "+str(round(t_f))+" segundos")
t_ini = time.time()
posting_lists = crearPostingLists(docs_limpio,partes_doc)
t_f = time.time() - t_ini
print("Finalizado. Tiempo aprox. consumido: "+str(round(t_f))+" segundos")
print("Guardando datos...")
t_ini = time.time()
save_object((docs_limpio,posting_lists),destino)
t_f = time.time() - t_ini
print("Finalizado. Tiempo aprox. consumido: "+str(round(t_f))+" segundos")
