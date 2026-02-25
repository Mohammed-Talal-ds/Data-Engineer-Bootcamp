import csv
import numpy as np
import pickle
import re


def read_articles(file_name):
    articles = []
    
    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            articles.append({
                "id": row["id"],
                "title": row["title"],
                "content": row["content"]
            })
    
    return articles



def clean_text(text):
    text = text.lower()
    
    text = re.sub(r'[^a-z\s]', '', text)
    
    words = text.split()
    
    return words



def build_vocabulary(articles):
    vocabulary = set()
    
    for article in articles:
        words = clean_text(article["content"])
        vocabulary.update(words)
    
    return sorted(list(vocabulary))



def build_vectors(articles, vocabulary):
    vectors = []
    
    for article in articles:
        words = clean_text(article["content"])
        word_set = set(words)
        
        vector = []
        for word in vocabulary:
            if word in word_set:
                vector.append(1)
            else:
                vector.append(0)
        
        vectors.append(vector)
    
    return np.array(vectors)



def compute_similarity_matrix(vectors):
    n = len(vectors)
    similarity_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            dot_product = np.dot(vectors[i], vectors[j])
            norm_i = np.linalg.norm(vectors[i])
            norm_j = np.linalg.norm(vectors[j])
            
            if norm_i == 0 or norm_j == 0:
                similarity = 0
            else:
                similarity = dot_product / (norm_i * norm_j)
            
            similarity_matrix[i][j] = similarity
    
    return similarity_matrix



def save_similarity_matrix(matrix, file_name="similarities.pkl"):
    with open(file_name, "wb") as f:
        pickle.dump(matrix, f)



def get_top_3_similar(article_id, articles, similarity_matrix):
    index = None
    
    for i, article in enumerate(articles):
        if article["id"] == str(article_id):
            index = i
            break
    
    if index is None:
        return "Article ID not found."
    
    similarities = similarity_matrix[index]
    
    indexed_similarities = list(enumerate(similarities))
    
    indexed_similarities = [x for x in indexed_similarities if x[0] != index]
    
    indexed_similarities.sort(key=lambda x: x[1], reverse=True)
    
    top_3 = indexed_similarities[:3]
    
    return [articles[i]["title"] for i, _ in top_3]


if __name__ == "__main__":
    
    articles = read_articles("articles.csv")
    
    vocabulary = build_vocabulary(articles)
    
    vectors = build_vectors(articles, vocabulary)
    
    similarity_matrix = compute_similarity_matrix(vectors)
    
    save_similarity_matrix(similarity_matrix)
    
    print("Top 3 similar articles to article 1:")
    print(get_top_3_similar(1, articles, similarity_matrix))