# gunicorn-flask-pipenv-sample

## Para correr

### Windows con una sola version de python, Ubuntu 18.04+

```bash
pip install pipenv
```

### Otros

```bash
pip3 install pipenv
```

Abrimos nuevamente la consola

#### Crear entorno

```bash
pipenv install
```


### Entrar al entorno virtual
```bash
pipenv shell
```
Si estas en windows 
```
python main.py
```

Cualquier otro sistema operativo
```
gunicorn main:app --workers=3 --reload
```