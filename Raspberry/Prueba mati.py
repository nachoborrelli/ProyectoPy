def ConsultarPalabraJson(palabra):
    '''devuelve la definicion de una palabra'''
    try:
        jsonfile = open('Definiciones.json', 'r')
    except FileNotFoundError:
        return False,False
    else:
        diccionario = json.load(jsonfile)
        if (palabra in diccionario.keys()):
            jsonfile.close()
            print(diccionario)
            return palabra,diccionario[palabra][0]
        else:
            jsonfile.close()
            return False,False

def AgregarJson(palabra, definicion,tipo):
    '''agrega una palabra con su definicion al json sin borrar los datos previos (actualiza)'''
    definiciones[palabra] = (tipo,definicion)
    try:
        jsonfile = open('Definiciones.json', 'x')
    except FileExistsError:
        with open('Definiciones.json', 'r') as jsonfile:
            antiguo = {}
            antiguo = json.load(jsonfile)
            definiciones.update(antiguo)
        jsonfile = open('Definiciones.json', 'w')
    finally:
        json.dump(definiciones, jsonfile)
        jsonfile.close()

    palabra,clasificacion = ConsultarPalabraJson(pal)
    if (palabra):
        ok = True
        dic[clasificacion].append(palabra)
        return ok,clasificacion