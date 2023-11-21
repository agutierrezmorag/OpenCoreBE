from math import log

data = [    # Conectar aqui la salida del json que tiene las palabras y sus datos correspondientes
]           # Data debe ser una lista de diccionarios que contienen las palabras como en el json entregado

def calculate_tfidf(data):
    total_articles = len(data[0]['importance_scores'])
    
    for word_data in data:
        word = word_data['word']
        word_frequency_global = word_data['frequency_global']
        
        for score in word_data['importance_scores']:
            article_frequency = score['frequency']
            article_word_count = score['article_info']['word_count']
            
            tf = article_frequency / article_word_count
            
            idf = log(1 + (total_articles / word_frequency_global))
            
            tf_idf = tf * idf
            
            score['tf_idf'] = tf_idf

            word_data['importance_scores'] = sorted(word_data['importance_scores'], key=lambda x: x['tf_idf'], reverse=True)

calculate_tfidf(data)

for word_data in data:
    print(f"Word: {word_data['word']}")
    for score in word_data['importance_scores']:
        print(f"Article {score['article_info']['article_id']} - TF-IDF: {score['tf_idf']}")
    print()