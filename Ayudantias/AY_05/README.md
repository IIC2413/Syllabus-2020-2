
# Ayundatia 5 - Heroku y Mapa

## Mapa

El archivo mapa.php contiene el ejemplo visto en la ayudantia. Este es parte de lo que pueden encontrar en leaflet[https://leafletjs.com/examples/quick-start/]

## Heroku

Para subir sus API a heroku deben utilizar un archivo que se debe llamar **Procfile**, el cual debe tener el siguiente contenido: ```web: gunicorn <nombre del archivo .py de su api>:app```. Osea si el el archivo es main.py su Procfile será: ```web: gunicorn main:app```. 
  
Ademas, es relevante que **gunicorn** debe estar en su pipfile, para esto lo pueden instalar con ```pip install gunicorn```
