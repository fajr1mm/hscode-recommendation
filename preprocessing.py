# Function for text cleaning & preprocessing
from nltk.corpus import stopwords
from lingua import Language, LanguageDetectorBuilder
import spacy
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
"""
karena pada teks terdapat campuran bahasa inggris dan indonesia,
fungsi ini untuk mendeteksi apakah kata termasuk bahasa inggris 
atau indonesia.
"""
languages = [Language.ENGLISH, Language.INDONESIAN]
detector_en_id = LanguageDetectorBuilder.from_languages(*languages).build()


def detect_lang(string, detector=detector_en_id):
    return detector.detect_language_of(string)


"""
mengubah teks menjadi huruf kecil
"""


def lowercase(text):
    return text.lower()


"""
menghapus semua non kata seperti simbol dan angka
"""


def remove_non_words_and_numeric(text):
    return re.sub(r'[\W\d]+', ' ', text)


"""
menghapus semua whitespace lebih dari 1
"""


def remove_whitespace(text):
    return re.sub(r'\s+', ' ', text)


"""
menghapus semua stopwords
"""


def remove_stopwords(text):
    list_stopwords_id = set(stopwords.words('indonesian'))
    list_stopwords_en = set(stopwords.words('english'))

    list_stopwords = list(list_stopwords_id)+list(list_stopwords_en)

    removed_stopwords = [word for word in text.split(
        ' ') if word not in list_stopwords]
    return ' '.join(removed_stopwords)


"""
mengubah kata ke menjadi bentuk kata dasar,
disable=['parser', 'ner'] agar dapat melakukan lemmatizer pada 1 kata
"""
model = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
factory = StemmerFactory()
stemmer = factory.create_stemmer()


def lemmatize(text, nlp=model, stemmer=stemmer):
    doc = nlp(text)
    lemmas = ''

    for word in doc:
        if str(detect_lang(str(word))) == 'Language.ENGLISH':
            #             print('en')
            #             print(word.lemma_)
            lemmas += word.lemma_ + ' '
        elif str(detect_lang(str(word))) == 'Language.INDONESIAN':
            #             print('id')
            #             print(stemmer.stem(str(word)))
            lemmas += stemmer.stem(str(word)) + ' '
        else:
            lemmas += str(word)+' '
    return lemmas


"""
menghapus kata berulang
"""


def remove_duplicate_word(text):
    word_list = text.split()
    unique_words = list(dict.fromkeys(word_list))
    return ' '.join(unique_words)


"""
menghapus kata yang terdiri dari hanya 1 atau 2 karakter
"""


def remove_1or2_strings(text):
    no_single_char = [string for string in list(
        text.split(' ')) if not re.match(r'^.{1,2}$', string)]
    return ' '.join(no_single_char)

# def tokenize(text):
#     tokens = nltk.word_tokenize(text)
#     return tokens


"""
pipeline preprocess
"""


def preprocess(text):
    lowered = lowercase(text)
    only_words = remove_non_words_and_numeric(lowered)
    whitespace_removed = remove_whitespace(only_words)
    no_stopwords = remove_stopwords(whitespace_removed)
    lemmatized = lemmatize(no_stopwords)
    duplicate_removed = remove_duplicate_word(lemmatized)
    single_char_string_removed = remove_1or2_strings(duplicate_removed)

    return single_char_string_removed

#testing lagi 2 coba lagi

# test a