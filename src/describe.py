from collections import Counter
from janome.tokenizer import Tokenizer
import bs4
import re
import requests
import urllib3
import certifi

t = Tokenizer()


def get_word(query):
    word_list = []
    keys = []
    values = []

    http = urllib3.PoolManager(
        cert_reqs = 'CERT_REQUIRED',
        ca_certs = certifi.where()
    )
    r = http.request('GET', "https://www.google.co.jp/search?num=10&q=" + query + '&gl=jp&hl=ja')
    soup = bs4.BeautifulSoup(r.data, "html.parser")
    elems = soup.find_all("a")
    p = re.compile(r"<[^>]*?>")
    full_text = p.sub("", str(elems))
    p = re.compile(r'[!"“#$%&()\*\+\-\.,\/:;<=>?@\[\\\]^_`{|}~]')
    full_text = p.sub("", full_text)
    full_text = re.sub("年", "", full_text)
    full_text = re.sub("月", "", full_text)
    full_text = re.sub("日", "", full_text)

    query = query.split()
    for x in query:
        full_text = full_text.replace(x, "")

    tokens = t.tokenize(full_text)

    for token in tokens:
        word = token.surface
        partofspeech1 = token.part_of_speech.split(',')[0]
        partofspeech2 = token.part_of_speech.split(',')[1]

        if partofspeech1 == "名詞":
            if (partofspeech2 != "非自立") and (partofspeech2 != "代名詞") and (partofspeech2 != "数") and (partofspeech2 != "サ変接続"):
                word_list.append(word)

    counter = Counter(word_list)
    q = counter.most_common(10)

    for i in q:
        keys.append(i[0])
    for j in q:
        values.append(j[1])

    return keys, values
