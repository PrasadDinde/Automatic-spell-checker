import streamlit as st
import string
import re
import numpy as np
from collections import Counter


def read_corpus(filename):
    with open(filename,'r',encoding='utf-8') as file:
        lines = file.readlines()

        words = []
        for word in lines:
            words += re.findall(r'\w+',word.lower())
    return words

corpus = read_corpus(r'https://github.com/PrasadDinde/Automatic-spell-checker/blob/2040836d638b78212fd1ec6e492ffada77633958/big.txt')

vocab = set(corpus)
len(vocab)

words_count = Counter(corpus)
total_count = float(sum(words_count.values()))
word_prob = {word : words_count[word]/total_count for word in words_count.keys()}

def split(word):
    return [(word[:i],word[i:])for i in range(len(word) + 1)]

def delete(word):
    return [left + right[1:] for left,right in split(word) if right]

def swap(word):
    return [left + right[1] + right[0] + right[2:] for left,right in split(word) if len(right)>1]

def replace(word):
    return [left + center + right[1:]for left,right in split(word) if right for center in string.ascii_lowercase]

def insert(word):
    return [left + center + right[1:]for left,right in split(word) for center in string.ascii_lowercase]

def level_one(word):
    return set((delete(word) + swap(word) + replace(word) + insert(word)))

def level_two(word):
    return set( e2 for e1 in level_one(word) for e2 in  level_one(e1))

def correct(word,vocab,word_prob):
    if word in vocab:
        return(f"{word} is already correctly spelled")

    suggestion = level_one(word) or level_two(word) or [word]
    best_guass = [w for w in suggestion if w in vocab]
    if not best_guass:
        return f'Sorry.no suggestion found for {word}'
    suggest_with_prob = [(w,word_prob[w]) for w in best_guass]
    suggest_with_prob.sort(key = lambda x: x[1],reverse=True)
    return f"suggestion for {word}: " + ', '.join([f"{w} ({prob:2%})" for w,prob in suggest_with_prob[:10]])

# GUI or Web App
st.title('AutoCorrect Mis-Spelled Word Search Engine System')
word = st.text_input('Search here')

if st.button('Check'):
    result = correct(word,vocab,word_prob)
    st.write(result)
