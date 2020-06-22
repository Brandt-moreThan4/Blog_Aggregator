import re
import string
from collections import Counter


def main():
    with open('moby_dick.txt') as f:
        text = f.read()

    grammy = get_ngrams_from_text(text)
    # new_file = open('new.txt', 'w')
    # new_file.write(str(grammy))
    print(grammy)


def load_text_file(file_name):
    """Put moby dick text """
    with open(file_name) as f:
        text = f.read()
    return text


def clean_sentence(sentence):
    """Cleans the sentence by stripping out anything that's not a word"""

    sentence = sentence.split(' ')
    sentence = [word.strip(string.punctuation + string.whitespace) for word in sentence]
    sentence = [word for word in sentence if len(word) > 1 or word.lower() == 'a' or word.lower == 'i']
    return sentence


def clean_input(content):
    content = content.upper()
    content = re.sub('\n', ' ', content)
    sentences = re.split('\.|\?|!', content)
    # sentences = content.split('. ')
    cleaned_sentences = [clean_sentence(sentence) for sentence in sentences]
    return cleaned_sentences


def get_ngrams_from_sentence(sentence_list, n=2):
    """Returns list of ngrams from the sentence"""
    all_grams = []
    for i in range(len(sentence_list) - n + 1):
        all_grams.append(sentence_list[i:i + n])
    return all_grams


def get_ngrams_from_text(text, n=2):
    """gets list of ngrams from the whole text"""

    text = clean_input(text)
    ngrams_list = []
    ngrams = Counter()
    for sentence in text:
        new_grams = [' '.join(ngrams) for ngrams in get_ngrams_from_sentence(sentence)]
        ngrams_list.extend(new_grams)
        ngrams.update(new_grams)
    return ngrams


if __name__ == '__main__':
    main()
