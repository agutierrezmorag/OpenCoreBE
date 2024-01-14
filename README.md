# OpenCoreBE

openCore es un proyecto basado en Python diseñado para la extracción y gestión de datos de noticias de politica chilena. Proporciona funcionalidades como cargar datos de noticias desde un archivo JSON a una base de datos en línea, ejecutar un servidor web, y más.

## Primeros Pasos

Para ejecutar OpenCoreBE en tu máquina, sigue estos pasos:

1. Clona el repositorio en tu máquina local.

2. Crea un entorno virtual para el proyecto. Si no tienes `virtualenv` instalado, puedes instalarlo con `pip install virtualenv`. Luego, en la carpeta del proyecto, ejecuta:

    ```sh
    virtualenv venv
    ```

    Esto creará un nuevo entorno virtual en una carpeta llamada venv.

3. Activa el entorno virtual. En Windows, usa:

   ```sh
   venv\Scripts\activate
   ```

    En Unix o MacOS, usa:

    ```sh
    source venv/bin/activate
    ```

4. Coloca el archivo `.env` proporcionado en la carpeta raíz de tu copia local del repositorio.

5. Instala los paquetes de Python requeridos ejecutando el siguiente comando en tu terminal:

    ```python
    pip install -r requirements.txt
    ```

    Estos pasos aseguran que todas las dependencias del proyecto se instalen en un entorno aislado, en lugar de en tu instalación global de Python. Esto puede ayudar a evitar conflictos entre las dependencias de diferentes proyectos

## Ejecutando el servidor

Después de la configuración, navega al directorio openCore e inicia el servidor ejecutando:

```python
python manage.py runserver
```

## Comandos clave

OpenCoreBE proporciona un comando personalizado para cargar datos de noticias:

```python
python manage.py loadnews
```

Este comando lee datos de un archivo JSON `newsdb.json` (generado por el scraper) y los carga en la base de datos en línea.

## Dependencias

OpenCoreBE utiliza varias bibliotecas de Python y servicios, incluyendo:

- **Django**: Un framework web de alto nivel en Python que permite un desarrollo rápido y un diseño limpio y pragmático.
- **PyMongo**: Un driver de Python para MongoDB que proporciona herramientas para trabajar con MongoDB como datos de Python.
- **MongoDB Atlas**: Un servicio de base de datos en la nube para MongoDB, que se utiliza para almacenar los datos de las noticias.
- **python-decouple**: Una biblioteca que separa la configuración que contiene información sensible de tu código fuente.

Para obtener una lista completa de las dependencias, consultar el archivo `requirements.txt`.

## Flujo de Trabajo

El flujo de trabajo de openCore consta de dos partes principales: la extracción de noticias y la carga de estas noticias en la base de datos de MongoDB Atlas.

### Extracción de Noticias

El primer paso en el flujo de trabajo es la extracción de noticias. Esto se realiza mediante un script de web scraping que recopila noticias de varias fuentes en línea. El script utiliza varias bibliotecas de Python, incluyendo BeautifulSoup y requests, para extraer los datos de las páginas web.

El script de scraping recorre cada fuente de noticias, accede a las páginas web de las noticias, extrae los datos relevantes (como el título, la fecha de publicación, el contenido, etc.) y los almacena en un archivo JSON `newsdb.json`.

### Carga de Noticias en la Base de Datos

Una vez que los datos de las noticias se han extraído y almacenado en el archivo JSON, el siguiente paso es cargar estos datos en la base de datos de MongoDB Atlas.

Esto se realiza mediante el comando personalizado `loadnews`:

```python
python manage.py loadnews
```

Este comando lee los datos del archivo JSON newsdb.json y los carga en la base de datos en línea. Para cada noticia, se crea un documento en la base de datos con los datos de la noticia.

El comando `loadnews` utiliza la biblioteca PyMongo para interactuar con la base de datos de MongoDB. Antes de insertar una noticia en la base de datos, el comando verifica si la noticia ya existe en la base de datos para evitar duplicados.

### Automatizacion

Los pasos mencionados anteriormente son ejecutados de manera automatica todos los dias a las 08:00, 11:00 y 21:00 hrs. mediante [Github Actions](https://github.com/features/actions).

## Deployment

Este proyecto fue desplegado en el tier gratuito del servicio [Render](https://render.com/). Render lee directamente desde este repositorio, por ende, cada vez que se haga un push se vuelve a hacer el deploy.

## Screenshots

![imagen](https://github.com/agutierrezmorag/OpenCoreBE/assets/84687977/a4a5ce27-5207-4e22-9ce8-1df8a6ed9866)
