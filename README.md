# openCore

Proyecto openCore. Taller de sistemas. UNAP 2023.

<!-- TOC -->
- [openCore](#opencore)
- [Primeros pasos](#primeros-pasos)
- [Comandos creados](#comandos-creados)
- [Tareas](#tareas)
<!-- TOC -->

## Primeros pasos

Una vez clonado el repositorio, insertar el archivo `.env` enviado en su respectiva carpeta.
Luego, ejecutar:

```python
pip install -r requirements.txt
```

No es necesario hacer migraciones, estas ya fueron realizadas con anterioridad.

## Comandos creados

```python
python manage.py loadnews
```

Pasa los datos extraídos desde el archivo json a la base de datos disponible en línea.

## Tareas

- Revisar y corregir archivo yml para el correcto dump de noticias del archivo json a la base de datos.

- Extender el script de web scraping para incluir más fuentes de noticias. Minimo 10 noticias por fuente:

  - **T13**
  - **La Tercera**
  - **Mega**
  - **CNN**
  - **Chilevision**
  - **El mostrador**
  - **El dínamo**
  - **ADN**
  - ~~Cooperativa~~
  - ~~24 horas~~
  - ~~Emol~~
  - ~~Ciper~~
  - ~~SoyChile~~
  - ~~El ciudadano~~
  - ~~TVN~~

- Escribir un comando que elimine noticias de la base de datos, en caso de tener 14 días o más de antigüedad y agregarlo al workflow.

_Los valores en negrita son cosas ya implementadas, los valores tachados fueron descartados._
