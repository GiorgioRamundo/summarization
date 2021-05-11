from operator import itemgetter
import collections

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


def _nasari():
    file = open("dd-small-nasari-15.txt","r")
    nasari = {}
    for line in file:
        data = line.split(";")
        babel_synset = data[0]
        name = data[1]
        data.remove(name)
        data.remove(babel_synset)
        key = name.lower()
        for i in range(len(data)):
            data[i] = data[i].replace("\n","")
        nasari[key] = (babel_synset,data)
    file.close()
    return nasari


def read_document(name):
    file = open(name+".txt","r")
    doc = []
    for line in file:
        doc.append(line)
    _doc = []
    for i in range(len(doc)):
        if doc[i] != "\n":
            _doc.append(doc[i].replace("\n",""))
    return _doc


def read_words(topic):
    context = []
    for v in topic:
        words = v[1]
        for w in words:
            word = w.split('_')[0]
            score = (float)(w.split('_')[1])
            context.append((word,score))
    return context

def _print(text):
    for t in text:
        print(t)


def search_value(_t, nasari):
    for v in nasari:
        (x,l) = nasari[v]
        for w in l:
            _w = w.split('_')[0]
            if _w == _t:
                return v
    return ""


def __print(filtered_text):
    for key in filtered_text:
        print(str(key) + ' *** ' + filtered_text[key])


def summarize(text,ratio):
    nasari = _nasari()
    _title = text[0]
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    title_tokens = word_tokenize(_title)
    title = [w for w in title_tokens if not w in stop_words]
    topic = []
    for t in title:
        _t = lemmatizer.lemmatize(t.lower())
        _v = nasari.get(_t)
        if _v is None:
            _w = search_value(_t, nasari)
            if _w != '':
                _v = nasari.get(_w)
                topic.append(_v)
        else:
            topic.append(_v)

    context = read_words(topic)
    filtered_text = {}
    c = 0
    for p in text:
        score = 0.0
        insert = False
        p = p.lower()
        for w in context:
            if w[0] in p:
                insert = True
                print('{} contains {}'.format(p,w[0]))
                score = score + w[1]
        if insert:
            filtered_text[score] = p
    lines = len(text)
    output_lines = lines - int((lines*ratio)/100)
    _output = {}
    c = 0
    for key in collections.OrderedDict(sorted(filtered_text.items(),reverse=True)):
        c = c + 1
        if c > output_lines:
            break
        _output[key] = filtered_text[key]
    return _output

text = read_document("Life-indoors")
summarized = summarize(text,30)
print('*****ORIGINAL TEXT*****')
print('Length: ' + str(len(text)))
_print(text)
print('*****SUMMARIZED TEXT*****')
print('Length: ' + str(len(summarized)))
__print(summarized)