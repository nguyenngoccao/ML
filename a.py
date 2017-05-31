import collections
import re
from os import listdir


def read_doc(name):
    f = open(name, 'r')
    doc = f.read()
    f.close()

    doc = doc.lower()
    sents = doc.split('. ')

    for i in range(len(sents)):
        sents[i] = re.sub(r'(\<br \/>)+', ' ', sents[i])

    sents = map(lambda x: x.split(), sents)

    for i in range(len(sents)):
        temp = []
        for word in sents[i]:
            if re.match(r'^[a-z]+$', word):
                temp.append(word)
        sents[i] = temp

    return sents

def build_word_dataset(words, vocabulary_size=50000):
    count = [['UNK', -1]]
    count.extend(collections.Counter(words).most_common(vocabulary_size - 1))
    dictionary = dict() # {word: index}
    for word, _ in count:
        dictionary[word] = len(dictionary)
        data = list() # collect index
        unk_count = 0
    for word in words:
        if word in dictionary:
            index = dictionary[word]
        else:
            index = 0  # dictionary['UNK']
            unk_count += 1
        data.append(index)
    count[0][1] = unk_count # list of tuples (word, count)
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return data, count, dictionary, reverse_dictionary

def build_doc_dataset(docs, vocabulary_size=50000):
    print('building doc dataset...')
    count = [['UNK', -1]]
	# words = reduce(lambda x,y: x+y, docs)
    words = []
    doc_ids = [] # collect document(sentence) indices
    sent_ids = []
    sent_num = 0
    for i, doc in enumerate(docs):
        for j, sent in enumerate(doc):
            doc_ids.extend([i] * len(sent))
            words.extend(sent)
            sent_ids.extend([sent_num] * len(sent))
            sent_num += 1

    word_ids, count, dictionary, reverse_dictionary = build_word_dataset(words, vocabulary_size=vocabulary_size)

    word_id_groups = docs[:]

    index = 0
    for i in range(len(docs)):
        for j in range(len(docs[i])):
            for k in range(len(docs[i][j])):
                word_id_groups[i][j][k] = word_ids[index]
                index += 1

    return doc_ids, sent_ids, word_ids, count, dictionary, reverse_dictionary, word_id_groups

###################################################################################################

docs = []

path = 'aclImdb/train/pos/'
filenames = listdir(path)

print('preprocessing...')

for filename in filenames:
    name = path + filename
    docs.append(read_doc(name))

doc_ids, sent_ids, word_ids, count, dictionary, reverse_dictionary, word_id_groups = build_doc_dataset(docs)
