import re
import string
from collections import Counter
import random as rd
from nlp import load_text_file


def main():
    text = load_text_file('moby_dick.txt')
    word_dictionary = build_word_dictionary(text)
    new_text_word_length = 100
    new_text = ['I']

    for i in range(new_text_word_length):
        next_word = retrieve_random_word(word_dictionary[new_text[-1]])
        new_text.append(next_word)

    new_text = ' '.join(new_text)
    new_text = new_text.replace(' . ', '. ')
    new_text = new_text.replace(' , ', ', ')
    print(new_text)


def build_word_dictionary(text):
    # Remove newlines and quotes. should i remove other things?
    text = text.replace('\n', ' ')
    text = text.replace('"', '')
    text = text.upper()

    # Make sure punctuation is treated as its own word
    punctuation = [',', '.', ',', ';', ':']
    for symbol in punctuation:
        text = text.replace(symbol, f' {symbol} ')

    words = text.split(' ')
    words = [word for word in words if word != '']

    word_dict = {}  # Dictionary of dictionaries
    for i in range(1, len(words)):
        if words[i - 1] not in word_dict:
            word_dict[words[i - 1]] = {}
        if words[i] not in word_dict[words[i - 1]]:
            word_dict[words[i - 1]][words[i]] = 0
        word_dict[words[i - 1]][words[i]] += 1

    return word_dict


def retrieve_random_word(word_dict):
    """Get a random word weighted by it's frequency"""
    """Better method for doing this?"""
    total_list = []
    for word, count in word_dict.items():
        total_list.extend([word] * count)
    return rd.choice(total_list)


if __name__ == '__main__':
    main()
