from transformers import pipeline
import json
import os

def initialize_sentiment_analyzer():
    return pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')

def analizar_sentimientos_transformers(texto, clasificador_sentimientos):
    resultado = []
    for fragmento in texto.split("."):
        if len(fragmento) != 0:
            try:
                resultado_fragmento = clasificador_sentimientos(fragmento)
                resultado.append(resultado_fragmento[0]['label'])
            except Exception as e:
                print(f"Error analyzing sentiment: {e}")
    
    return resultado

def valorar(etiqueta_estrellas):
    estrellas = {'5 stars': 5, '4 stars': 4, '3 stars': 3, '2 stars': 2, '1 star': 1}
    total_estrellas = sum(estrellas.get(etiqueta, 0) for etiqueta in etiqueta_estrellas)
    promedio = total_estrellas / len(etiqueta_estrellas)
    promedio_redondeado = round(promedio)
    
    return promedio_redondeado
    
def determinarValor(valor):
    if valor == 1:
        return "Negativo"
    elif valor == 4 or valor == 5:
        return "Positivo"
    else:
        return "Neutro"

def main():
    with open('newsdb.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    clasificador_sentimientos = initialize_sentiment_analyzer()
    
    for item in data:
        print("------------------------------")
        print(f"Titulo: {item['title']} ")
        texto = item['content']
        # Analizar sentimientos
        resultado_sentimientos_transformers = analizar_sentimientos_transformers(texto, clasificador_sentimientos)
        promedio = valorar(resultado_sentimientos_transformers)
        
        item['sentiment'] = determinarValor(promedio)
        print(f"El análisis de sentimientos es: {determinarValor(promedio)}")
        
    with open('newsdb.json', 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()