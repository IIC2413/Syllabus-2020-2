import sys, os, subprocess
import json
import requests
###########################################################################
default_python = "python"         # Comando predeterminado de python
default_pipenv = "pipenv"         # Comando predeterminado de pipenv
default_route = "http://localhost:5000"  # Ruta predeterminada api
############################################################################
par_pip_env = True      # Instala paquetes en entorno virtual
par_open_api = True     # Corre api en el entorno virtual
par_interactive = True  # Comienza el programa de manera interactiva
############################################################################
default_query = '''
G0:{id1:306/id2:262};{id1:38/id2:3700}|G1:;262;50000|G2:;1;10000|G3:{};;{desired:Anacleto,destino,solo,resignarme,P y NP,Pokemon};{required:quiero jugar Megaman,Bai};{forbidden:Pokemon,Megaman,Espero,Buena,Hola,Cambio,despido,Feliz,tiempo,cancion,hablar,cuento,bases,bai,respecto,completo,tal,algo,estas,viste,Konnichiwa,mal,ayuda,niño,tarea,profe,destino,saludos,extinguieron,día,nuevo,pez,aburría,123,magikarp,shrek,mar,maldad,venir,futuro,pintura,silver,hacerlo,grunge,dinosaurio,postulo,olvida,prefiero,creo,copia,sueño,tierra,pared,Kudo,hacer,vida,situación,jugar};{userId:130};{required:Turing/userId:215};{required:Hola/forbidden:venir,como,viste,Bai,pronto,camino,fifa,Cambio y fuera,restaurant,partido,equipo};{userId:212/forbidden:no,mala};{desired:};{userId:212/forbidden:magikarp,se/desired:shrek/required:que}|P1:{message:Mensaje para probar el POST/sender:1/receptant:2/lat:-46.059365/long:-72.201691/date:2018-10-16};{message:Mensaje para probar el POST/receptant:2/lat:-46.059365/long:-72.201691/date:2018-10-16}|D1:1;10000
'''
#############################################################################

def descifrar(codigo):
    codigo = codigo.strip().replace("\n", "")
    diccionario = {}
    for i in codigo.split("|"):
        i_ = i.find(":")
        llave, valores, valores_diccionario = i[:i_], (i + " ")[i_+1:][:-1], []
        for j in valores.split(";"):
            if j == "" or j == "null":
                valor = None
            elif j[0] == "{":
                if j[1] == "}":
                    valor = {}
                else:
                    mini_valores = {}
                    for mini_valor in j[1:-1].split("/"):
                        i__ = mini_valor.find(":")
                        mini_llave = mini_valor[:i__]
                        mini_mini_valores = (mini_valor + " ")[i__+1:][:-1]
                        if mini_mini_valores.isnumeric():
                            mini_mini_valores = int(mini_mini_valores)
                        elif mini_mini_valores.replace(".", "")[
                            0 if "-" not in mini_mini_valores else 1:
                            ].isnumeric():
                            mini_mini_valores = float(mini_mini_valores)
                        elif mini_llave in "forbiddenrequireddesired":
                            mini_mini_valores = mini_mini_valores.split(
                            ",") if mini_mini_valores != "" else []
                        else:
                            mini_mini_valores = mini_mini_valores
                        mini_valores[mini_llave] =  mini_mini_valores
                    valor = mini_valores
            elif j.isnumeric():
                valor = int(j)
            valores_diccionario.append(valor)
        for valor in range(len(valores_diccionario) ):
            diccionario[llave + "." + f"{valor+1}"] = valores_diccionario[valor]
    return diccionario

def imprimir_retornar(valor, mensaje=""):
    print(mensaje, valor) if mensaje != "" else print(valor)
    return valor

def input_(opciones, mensaje=None, simbolo=">> ") :
    if mensaje is None:
        mensaje = """Lo sentimos, este input no lo entendimos.
Puedes intentarlo de nuevo"""
    in_ = input(simbolo).strip()
    while in_ not in opciones:
        print(mensaje)
        in_ = input(simbolo).strip()
    return in_

def os_(something):
    print(">>", something)
    subprocess.call(something)

def pip_env():
    imprimir = f"""{default_pipenv} install"""
    os_(imprimir)

def open_api():
    imprimir = f"""{default_pipenv} run {default_python} main.py """
    print(">>", imprimir)
    return subprocess.Popen(imprimir, stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

def pre_consultas(api):
    out_ = ""
    while "http" not in out_:
        out_ = f"{api.stdout.readline()}"
    return out_[out_.find("http"):].split(" ")[0]

class Consulta:
    def __init__(self, ruta=default_route, rango=10):
        self.ruta, self.lista, self.rango = ruta, [], rango
        self.llaves = {"mensajes": ["mid", "sender", "receptant", "date", "lat",
        "long", "message"], "usuarios": ["uid", "name", "description", "age"]}
        self.ids = {"mensajes": "mid", "usuarios": "uid"}
        self.funciones = {"G0": self.consulta_g_0, "G1": self.consulta_g_1,
        "G2": self.consulta_g_2, "G3": self.consulta_g_3,
        "P1": self.consulta_p_1, "D1": self.consulta_d_1}

    def obtener(self, respuesta, tipo, ruta, filtro=7):
        for i in range(len(ruta)):
            respuesta = respuesta[ruta[i]]
            if i == len(ruta) - 2:
                super_contador = 0
                for key in respuesta:
                    contador = 0
                    for llave in self.llaves[tipo]:
                        if llave in respuesta[key]:
                            contador += 1
                    if contador >= filtro:
                        super_contador += 1
                if super_contador == len(respuesta):
                    return list(respuesta.values())
        if type(respuesta) != list:
            return [respuesta]
        return respuesta

    def encontrar(self, respuesta, tipo="mensajes", llaves=None, filtro=7):
        primero = False
        if llaves is None:
            llaves, primero = [], True
        if type(respuesta) == dict:
            contador = 0
            for i in self.llaves[tipo]:
                if i in respuesta:
                    contador += 1
            if contador >= filtro:
                if len(llaves) >= 1:
                    if type(llaves[-1]) == int or str(llaves[-1]).isnumeric():
                        llaves.pop(len(llaves)-1)
                if primero:
                    return self.obtener(respuesta, tipo, llaves, filtro)
                else:
                    return llaves
            retorno = False
            for key in respuesta:
                retorno = self.encontrar(respuesta[key], tipo,
                                            llaves.copy() + [key], filtro)
                if retorno is not False:
                    if primero:
                        return self.obtener(respuesta, tipo, retorno, filtro)
                    else:
                        return retorno
        elif type(respuesta) == list:
            retorno = 0
            for key in range(len(respuesta)):
                retorno = self.encontrar(respuesta[key], tipo,
                                            llaves.copy() + [key], filtro)
                if retorno is not False:
                    if primero:
                        return self.obtener(respuesta, tipo, retorno, filtro)
                    else:
                        return retorno
        if primero and filtro != 2:
            return self.encontrar(respuesta, tipo, None, 2)
        return False

    def _esperar(self, funcion, *args, **kwargs):
        for i in range(self.rango):
            a = funcion(*args, **kwargs)
            if a.status_code != 503:
                return a
            time.sleep(1)
        return a

    def _get(self, *args, **kwargs):
        return self._esperar(requests.get, *args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._esperar(requests.delete, *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._esperar(requests.post, *args, **kwargs)

    def cargar(self, diccionario={}):
        self.diccionario = diccionario
        self.lista = []
        if diccionario is None or diccionario == {}:
            self.diccionario = descifrar(default_query)
        for i in self.diccionario:
            mini_diccionario = { "tipo": i[:i.find(".")], "nombre": i,
               "valores": self.diccionario[i] }
            self.lista.append(mini_diccionario)

    def atributos_e_id(self, respuesta, tipo):
        _id = self.ids[tipo]
        if respuesta is False:
            print("No se encontraron mensajes o se recibió un error amigable")
            return
        ids_encontradas, max_encontrado = [], []
        todo_mensaje, no_mensaje, max_contador, max_ = 0, 0, 0, 0
        for i in respuesta:
            todo, contador, encontrados = True, 0, []
            for a in self.llaves[tipo]:
                if a in i:
                    contador += 1
                    encontrados.append(a)
            if _id in i:
                if type(i[_id]) in [float, int] or i[_id].isnumeric():
                    ids_encontradas.append( int( i[_id]) )
            if contador > max_contador:
                max_contador, max_encontrado, max_ = contador, encontrados, 1
            else:
                max_ += 1
        if max_contador == len(self.llaves[tipo]):
            largo = len(respuesta)
            if largo == max_:
                print("Se encontraron todos los atributos en todos los datos:",
                ", ".join( max_encontrado ) )
            else:
                print("Se encontraron todos los atributos en", max_,
                "de los", largo, "valores retornados.")
        else:
            print(f"En {max_} de los valores,",
                "se encontraron los atributos", max_encontrado)
            print("Falta retornar los atributos:",
            ", ".join( list(set(self.llaves[tipo]) - set( max_encontrado )) ) )
        return imprimir_retornar(ids_encontradas, tipo + " encontrados:")

    def obtener_json(self, respuesta):
        try:
            return respuesta.json()
        except:
            print("Error: No se recibió ningún json, puede que esté retornando un html, string o algo por el estilo")

    def consulta_get(self, ruta, tipo, llave, *args, imprimir=True, **kwargs):
        if imprimir:
            print("GET =>", ruta)
        respuesta = self._get(ruta, *args, **kwargs)
        respuesta_ = self.obtener_json(respuesta)
        if respuesta_ is None:
            return
        respuesta = self.encontrar(respuesta_, tipo)
        if llave is not None:
            self.respuestas[llave] = respuesta
        ids = self.atributos_e_id(respuesta, tipo) if imprimir else [
            i[self.ids[tipo]] for i in respuesta]
        return sorted(ids) if type(ids) == list else ids

    def consulta_g_0(self, valores, llave=None):
        ruta = self.ruta+f"/messages?id1={valores['id1']}&id2={valores['id2']}"
        return self.consulta_get(ruta, "mensajes", llave)

    def consulta_g_1(self, valores=None, llave=None, imprimir=True):
        ruta = self.ruta + f"/messages" + ("" if valores in [None,
                                            "null"] else f"/{valores}")
        return self.consulta_get(ruta, "mensajes", llave, imprimir=imprimir)

    def consulta_g_2(self, valores=None, llave=None):
        ruta = self.ruta + f"/users" + ("" if valores in [None,
                                            "null"] else f"/{valores}")
        return self.consulta_get(ruta, "usuarios", llave)

    def consulta_g_3(self, valores, llave=None):
        ruta = self.ruta + "/text-search"
        return self.consulta_get(ruta, "mensajes", llave, json=valores)

    def consulta_p_1(self, valores):
        ruta = self.ruta + f"/messages"
        print("POST =>", ruta)
        ids_previas = set(self.consulta_g_1(imprimir=False))
        respuesta = self.obtener_json(self._post(ruta, json=valores))
        if respuesta is None:
            return
        ids_nuevas = set(self.consulta_g_1(imprimir=False)) - ids_previas
        print("Se encontraron los siguientes nuevos mensajes:",
                ids_nuevas) if len(ids_nuevas) >= 1 else print(
                "No se encontraron nuevos mensajes")

    def consulta_d_1(self, valores):
        ruta = self.ruta + f"/message/{valores}"
        print("DELETE =>", ruta)
        ids_previas = set(self.consulta_g_1(imprimir=False))
        respuesta = self.obtener_json(self._delete(ruta, json=valores))
        if respuesta is None:
            return
        ids_nuevas =  ids_previas - set(self.consulta_g_1(imprimir=False))
        print("Se eliminaron los siguientes mensajes:",
            ids_nuevas) if len(ids_nuevas) >= 1 else print(
            "No se encontraron mensajes eliminados")

def plantilla(nombre="collection.json"):
    nombre = "collection.json" if nombre in [None, ""] else nombre
    json.dump(descifrar(default_query), open(nombre, "w"), indent=2)

def consultas(ruta=default_route, diccionario=None, par=[]):
    consulta = Consulta(ruta)
    consulta.cargar(diccionario)
    in_, add, diccionario = "", "-1" if len(par)-1 else "", consulta.diccionario
    mensaje = f"""¡Hola! A continuación puedes ingresar a algunas de las consultas:\n"""
    mensaje += f"[Enter]" + " Imprimir opciones nuevamente" + "\n"
    mensaje += f"   [-1]" + " Para recargar el archivo\n" if len(par) > 1 else ""
    mensaje += "{:>7}".format(f"[0]") + " Salir :D" + "\n"
    for i in range( len (  consulta.lista  ) ):
        mensaje += "{:>7}".format(f"[{i+1}]") + " " + consulta.lista[i]["nombre"] + "\n"
    print(mensaje)
    while in_ != "0":
        in_ = input_([f"{i}" for i in range(len(consulta.lista) + 1)] + ["", add])
        if in_ == "-1":
            (consulta.cargar(json.load(open(par[1]))), print("¡Actualizado!"), print())
        elif in_ == "":
            print(mensaje)
        elif in_ != "0":
            elegido = consulta.lista[int(in_) - 1]
            print("\n" + elegido["nombre"])
            (consulta.funciones[elegido["tipo"]](elegido["valores"]), print())
    return 0

if __name__ == "__main__":
    diccionario, par = {}, [j for j in sys.argv if j not in "-api-pipenv"]
    if "plantilla" in sys.argv or "template" in sys.argv:
        plantilla(input("""Nombre del archivo a guardar (Enter para guardar por defecto):
>> """).strip())
        exit()
    elif len(par) > 1:
        diccionario = json.load(open(par[1]))
    pip_env() if not "-pipenv" in sys.argv and par_pip_env else None
    if par_open_api and "-api" not in sys.argv:
        api = open_api()
        ruta = pre_consultas(api)
    else:
        ruta = default_route
    consultas(ruta, diccionario, par) # if par_interactive else consulta_i(ruta)
    # api.communicate(b"\x03")
    api.stdout.close() if par_open_api and "-api" not in sys.argv else None
    print("¡Muchas energías y éxitos! ¡Vamooooo!")
