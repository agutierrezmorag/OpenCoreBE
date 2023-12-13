from transformers import pipeline
import json
import os

with open('newsdb.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def analizar_sentimientos_transformers(texto):
    clasificador_sentimientos = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')
    
    resultado = []
    for fragmento in texto.split("."):
        if len(fragmento) != 0:
            resultado_fragmento = clasificador_sentimientos(fragmento)
            resultado.append(resultado_fragmento[0]['label'])
    
    return resultado

def valorar(etiqueta_estrellas):
    
    cincoStars = etiqueta_estrellas.count('5 stars')
    cuatroStars = etiqueta_estrellas.count('4 stars')
    tresStars = etiqueta_estrellas.count('3 stars')
    dosStars = etiqueta_estrellas.count('2 stars')
    unoStars = etiqueta_estrellas.count('1 star')
    """print(cincoStars)
    print(cuatroStars)
    print(tresStars)
    print(dosStars)
    print(unoStars)
    """
    print(f"Tamaño: {len(etiqueta_estrellas)}")
    promedio = (float(cincoStars*5.0+cuatroStars*4.0+tresStars*3.0+dosStars*2.0+unoStars*1.0))/len(etiqueta_estrellas)
    print(promedio)
    print(round(promedio))
    promedio = round(promedio)
    return promedio
    
def determinarValor(valor):
    if(valor == 1):
        return "NEGATIVE"
    elif(valor == 2):
        return "NEUTRAL"
    elif(valor == 3):
        return "NEUTRAL"
    elif(valor == 4):
        return "POSITIVE"
    elif(valor == 5):
        return "POSITIVE"

for item in data:
    print("------------------------------")
    print(f"Titulo: {item['title']} ")
    texto = item['content']
    # Tu texto
    #texto = "Durante la mañana de este sábado, 84 familias de la comuna de Santiago recibieron las llaves de sus nuevas viviendas, otorgadas gracias al Fondo Solidario para la Elección de Vivienda del Ministerio de Vivienda y Urbanismo. El complejo “Patios de Copiapó” está ubicado en el corazón del barrio 10 de Julio, en el polígono industrial Matta-Carmen, con departamentos de 3 dormitorios, entre 56 y 70 m2. Incluyen tipologías dúplex y triplex, así como viviendas de una planta con accesibilidad universal, para personas con movilidad reducida y/o discapacidad."

    # Analizar sentimientos
    resultado_sentimientos_transformers = analizar_sentimientos_transformers(texto)
    promedio = valorar(resultado_sentimientos_transformers)
    
    item['sentiment'] = determinarValor(promedio)
    print(f"El análisis de sentimientos es: {determinarValor(promedio)}")
    
with open('newsdb.json', 'w') as f:
    json.dump(data, f)
