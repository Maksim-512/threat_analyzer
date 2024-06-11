import nltk
import string
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from selecting_data_db import get_list_device_variation

stemmer_ru = SnowballStemmer('russian')
stemmer_en = SnowballStemmer('english')


# con, cur = connect()
#
# cur.execute('SELECT * FROM devices_variations;')
# rows = cur.fetchall()
#
# word_list = []
# for row in rows:
#     word_list.append(row[2])
# print(word_list)

# word_list = ['Принтер', 'Микрофон', 'Жесткий диск', 'USB-Микрофон']

# text_input = '''В нашем кабинете располагается несколько принтеров, три жёстких мамы, два монитора и миллион жестких дисков USB-микрофоны'''


def device_detection(con, text_input):
    '''Из введённого пользователем текста определяем какие устройства были введены'''

    word_list = get_list_device_variation(con)

    # text_input = text_input.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    text_input = text_input.translate(str.maketrans({char: ' ' for char in string.punctuation if char != '-'}))

    tokens = nltk.word_tokenize(text_input)

    stemmed_words = []

    for word in tokens:
        stemmed_words.append(stemmer_ru.stem(word.lower()))

    devices = []
    for w in word_list:
        # w_mix = w.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
        w_mix = w.translate(str.maketrans({char: ' ' for char in string.punctuation if char != '-'}))
        stemmed_w = []
        for word in w_mix.split():
            stemmed_w.append(stemmer_ru.stem(word.lower()))
        if all(word in stemmed_words for word in stemmed_w):
            devices.append(w)

    return devices
