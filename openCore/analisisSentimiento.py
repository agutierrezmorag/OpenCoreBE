import json
import os
from collections import Counter

from transformers import pipeline


def initialize_sentiment_analyzer():
    """
    Initializes the sentiment analyzer by loading the pre-trained model.

    Returns:
        A sentiment analysis pipeline object.
    """
    return pipeline(
        model="lxyuan/distilbert-base-multilingual-cased-sentiments-student"
    )


def analizar_sentimientos_transformers(texto, clasificador_sentimientos):
    """
    Analyzes the sentiment of a given text using a sentiment classifier.

    Args:
        texto (str): The text to be analyzed.
        clasificador_sentimientos: The sentiment classifier.

    Returns:
        list: A list of sentiment labels for each fragment of the text.
    """
    resultado = []
    for fragmento in texto.split("."):
        if len(fragmento) != 0:
            try:
                resultado_fragmento = clasificador_sentimientos(fragmento)
                resultado.append(resultado_fragmento[0]["label"])
            except Exception as e:
                print(f"Error analyzing sentiment: {e}")

    return resultado


def most_common(lst):
    """
    Returns the most common sentiment in a list.

    Parameters:
    lst (list): A list of sentiments.

    Returns:
    str: The most common sentiment. Returns "Positivo" if the most common sentiment is "positive",
        "Negativo" if the most common sentiment is "negative", and "Neutro" otherwise.
    """
    data = Counter(lst)
    sentiment = data.most_common(1)[0][0]
    if sentiment == "positive":
        return "Positivo"
    elif sentiment == "negative":
        return "Negativo"
    else:
        return "Neutro"


def main():
    with open("newsdb.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    clasificador_sentimientos = initialize_sentiment_analyzer()

    for item in data:
        print("------------------------------")
        print(f"Titulo: {item['title']} ")
        texto = item["content"]
        resultado_sentimientos_transformers = analizar_sentimientos_transformers(
            texto, clasificador_sentimientos
        )
        item["sentiment"] = most_common(resultado_sentimientos_transformers)
        print(f"Sentimiento: {item['sentiment']} ")

    with open("newsdb.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
