# Entrega 4 - Verificador de formato

¡Hola! A continuación se explica parte de cómo utilizar el programa, y algunas consideraciones.

¡Lo primero! Mover el archivo a la carpeta en donde estará nuestro `main.py` y nuestro `Pipfile`. Luego se puede utilizar cualquiera de los siguientes comandos (dependiendo de lo que queramos realizar!)

* `python formato_checker.py`

  Este comando nos permite abrir el script y realizar el funcionamento completo, esto es:
  * Instalar las librerías necesarias en el entorno virtual.
  * Correr la api en el entorno virtual.
  * Abrir las consultas de prueba.

  Para las consultas, primero se nos mostrarán todas las opciones cargadas, pera luego interactuar y elegir cuál queremos intentar a partir de los números del lado izquierdo.

  ![image](https://drive.google.com/uc?export=view&id=1k5tEznCkuabJXe504MDTRbwmkVQ-kdLc)

  Podemos notar que para salir del programa podemos escribir "0", sin embargo, esto no cerrará la api (aún no está disponible esta opción). ¡pero no deberían haber problemas! Con cerrar y volver a abrir la consola, la api debería dejar de ocupar el puerto :D

* `python formato_checker.py plantilla` o `python formato_checker.py template`

  Este comando nos permite guardar las consultas de prueba en un archivo (el que será preguntado luego). Una vez ingresado el nombre, se creará un `json` que tendrá estas consultas, estas podrán ser modificadas y cargadas con el comando de a continuación:

  ![image](https://drive.google.com/uc?export=view&id=1gnsplfZKgenPbLRtLv5tz5fnhhgDtkFQ)

  En la imagen no se instalan los paquetes en el entorno virtual, más abajo se explica esta opción!

* `python formato_checker.py archivo`

  Este comando nos permite cargar las consultas guardadas en este archivo. Es posible tener aún más consultas de las que tenía originalmente la plantilla, lo importante es que cumplan el formato de "GX.algo" (donde G podría ser P o D también, y X es el número respectivo de la ruta). De esta forma tendremos a:

  ```
  G0 => {"id1": id1, "id2": id2} => /messages?id1=1&id2=2
  G1 => "null" => /messages
     => id => /messages/id
  G2 => "null" => /users
     => id => /users/id
  G3 => "null" => /text-search (vacío)
     => diccionario => /text-search (enviando diccionario en el body)
  P1 => diccionario => /messages (enviando diccionario con los datos del usuario en el body)
  D1 => id => /message/id
  ```

Adicionalmente podemos agregar los parámetros `-pipenv`, `-api` que nos permitirán saltarnos los pasos de instalar las librerías en el entorno virtual, y correr la api en este, respectivamente. Ambos pueden ser incluidos, o de manera individual, de estas formas, las siguientes combinaciones son válidas:

* `python formato_checker.py -pipenv`
* `python formato_checker.py -api`
* `python formato_checker.py -pipenv -api`
* `python formato_checker.py archivo -pipenv -api`
* `python formato_checker.py archivo -api`
* `python formato_checker.py archivo -pipenv`


Otra forma es modificar los parámetros que están en el mismo archivo, `par_open_api` y `par_pip_env`.

Además es posible modificar `default_python`, `default_pipenv` y `default_route`.

En caso de querer realizar consultas "más rápido", es posible importar el archivo como módulo :D

De esta forma, lo siguiente es posible realizarlo:

```
> python
Python...
>>> from formato_checker import Consulta
>>> consulta = Consulta("localhost:5000")
>>> consulta.consulta_g_0({"id1": 1, "id2": 2})
>>> consulta.consulta_g_1(1)
>>> consulta.consulta_g_2(1)
>>> consulta.consulta_g_3({"required": [], "desired": [], "forbidden": []})
>>> consulta.consulta_p_1({
  "message": "¡hola! :D"
  "sender": 1,
  "receptant": 2,
  "lat": 38.0
  "long": 38.0
  "date": "2020-11-13"
})
>>> consulta.consulta_d_1(10000)
```

¡Eso!

Cualquier duda, o comentario, pueden enviar un correo a `ridiaz2@uc.cl`.

También pueden abrir una issue si lo prefieren! (idealmente indicando algo del estilo: "formato_checker" o "verificador de formato" en el asunto).

¡Con todo el ánimo y éxito para lo poquito que queda de semestre! ¡Estaremos atent-s! ¡Muchos saludos!
