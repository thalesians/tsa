import itertools
import math
import numpy as np
import pandas as pd

def words_of_length(alphabet_size, word_length):
    return tuple(itertools.product(range(1, alphabet_size+1), repeat=word_length))

def words(alphabet_size, max_word_length=None):
    if max_word_length is None: max_word_length = alphabet_size
    return sum((words_of_length(alphabet_size, i) for i in range(1, max_word_length+1)), ())

def signature_element(df, word):
    if len(word) == 0:
        return 1.
    elif len(df) == 2:
        result = 1./math.factorial(len(word))
        for letter in word:
            result *= df.iloc[1,letter-1] - df.iloc[0,letter-1]
        return result
    else:
        result = 0.
        for i in range(0, len(word)+1):
            result += signature_element(df[:2], word[0:i]) * signature_element(df[1:], word[i:])
        return result

def signature(df, max_word_length=None):
    return {w: signature_element(df, w) for w in words(len(df.columns), max_word_length)}
