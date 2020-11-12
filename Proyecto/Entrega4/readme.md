# Resultados Consultas de Prueba

https://docs.google.com/spreadsheets/d/1PwtaZ1sV77e7VReRNgXZY-3SZJn2jfKI4fSntLNQItg/edit?usp=sharing


# Rúbrica E4

## Puntajes (60 pts):

Los puntajes asignados son los siguientes:

- **(18 pts) GET básico:** el puntaje se divide de la siguiente manera:

  - (3 pts) En la ruta `/messages` se muestran todos los mensajes con todos sus atributos.

  - (3 pts) En la ruta `/users` se muestran todos los usuarios con todos sus atributos.

  - (4 pts) En la ruta `/messages/:id`, si el id de mensaje existe, se muestra el mensaje con todos sus atributos. Si el id de mensaje NO existe, la app no se cae.

  - (4 pts) En la ruta `/users/:id`, si el id de usuario existe, se muestra el usuario con todos sus atributos. Si el id de usuario NO existe, la app no se cae.

  - (4 pts) En la ruta `/messages?id1=x&id2=y`, si ambos id existen, se muestran los mensajes intercambiados entre los usuarios (en ambas direcciones). Si alguno de los id no existe, la app no se cae.

* **(24 pts) GET Búsqueda de texto:** el puntaje se divide de la siguiente manera:

  - (4 pts) Al realizar una búsqueda sin body o con diccionario vacío se retornan todos los mensajes.

  - (8 pts) La búsqueda funciona con cada uno de los 4 criterios por separado.

  - (8 pts) La búsqueda funciona con no todos los criterios e incluso con algunos como listas vacías.

  - (4 pts) La búsqueda funciona con los 4 criterios simultáneamente.

- **(12 pts) POST:** el puntaje se divide de la siguiente manera:

  - (12 pts) Si se entregan todos los atributos, es posible crear un nuevo mensaje. Si no se entregan todos los atributos, el mensaje no se crea y se muestra el atributo erróneo

* **(6 pts) DELETE:** el puntaje se divide de la siguiente manera:

  - (6 pts) Es posible eliminar un mensaje existente. Si el ID no existe, la app no se cae.

## Descuentos

- (1 pto) Por subir en carpeta incorrecta.

- (Hasta 1 pto) A juicio del corrector, por trabajos que no estén bien explicados, que cuenten con demasiadas faltas de ortografía o que se dificulte la corrección.
