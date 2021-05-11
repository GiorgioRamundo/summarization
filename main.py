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
            context.append(word)
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
    filtered_text = set()
    c = 0
    for p in text:
        p = p.lower()
        for w in context:
            print(w)
            if w in p:
                print('{} contains {}'.format(p,w))
                filtered_text.add(p)
    print('*****ORIGINAL TEXT*****')
    print(len(text))
    print(text)
    print('*****SUMMARISED TEXT*****')
    print(len(filtered_text))
    print(filtered_text)
text = read_document("Andy-Warhol")
summarize(text,10)