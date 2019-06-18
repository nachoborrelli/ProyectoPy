def Comparar (wordDic,palabras_encontradas):
    if(len(palabras_encontradas['__adjetivos__']) == len(wordDic['__adjetivos__'])):
        cantAdj = 0
    else:
        cantAdj = len(wordDic['__adjetivos__']) - len(palabras_encontradas['__adjetivos__'])
    if (len(palabras_encontradas['__verbos__']) == len(wordDic['__verbos__'])):
        cantVerbs = 0
    else:
        cantVerbs = len(wordDic['__verbos__']) - len(palabras_encontradas['__verbos__'])
    if (len(palabras_encontradas['__sustantivos__']) == len(wordDic['__sustantivos__'])):
        cantSust = 0
    else:
        cantSust = len(wordDic['__sustantivos__']) - len(palabras_encontradas['__sustantivos__'])
    return cantAdj,cantVerbs,cantSust

palabras_encontradas = {}
palabras_encontradas['__verbos__'] = ['correr', 'caminar', 'saltar' , 'dormir']  # dic de palabras encontradas por tipo
palabras_encontradas['__adjetivos__'] = ['lindo', 'feo', 'rojo']
palabras_encontradas['__sustantivos__'] = ['perro', 'gato']

wordDic= {}
wordDic['__adjetivos__']= ['lindo', 'feo', 'rojo', 'negro', 'oscuro']
wordDic['__verbos__'] = ['correr', 'caminar', 'saltar' , 'dormir', 'cojer']
wordDic['__sustantivos__'] = ['perro', 'gato', 'mesa' , 'celular', 'silla']

a,v,s=Comparar(wordDic,palabras_encontradas)
print('Te faltan encontrar {} adjetivos, {} verbos, {} sustantivos'.format(a,v,s))