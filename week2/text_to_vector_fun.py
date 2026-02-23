import numpy as np
from collections import Counter

def text_to_vector(text, bag_of_words):
    words = text.lower().split()
    word_count = Counter(words)
    
    vector = np.array([word_count[word] for word in bag_of_words])
    
    return vector

bag_of_words = ["i", "love", "machine", "learning", "python"]

text1 = "I love machine learning"
text2 = "I love python"

vec1 = text_to_vector(text1, bag_of_words)
vec2 = text_to_vector(text2, bag_of_words)

print("Vector 1:", vec1)
print("Vector 2:", vec2)