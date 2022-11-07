# text in & text out
from collections import defaultdict
import json
import requests
import numpy as np
from numpy.linalg import norm


class ChatBot:
    def __init__(self, threshold):
        self.threshold = threshold
        with open("./files/menu.json", 'r', encoding='utf-8') as f:
            self.menu = json.load(f).keys()
        self.numberMap = dict(zip(
            ['一', '兩', '三', '四', '五', '六', '七', '八', '九', '十'], range(1, 11)
        ))
        self.base_vectors = np.load('./files/question.npy')
        self.answers = []
        with open('./files/A_format.txt', 'r', encoding='utf-8') as f:
            self.answers.extend(f.readlines())
        self.tfidf = TFIDF()

    def menuSearch(self, sentence):
        order_list = ""
        for order1 in self.menu:
            idx = sentence.find(order1)
            if idx != -1:
                order_list = order_list + order1
                sentence = sentence[:idx]+sentence[idx+len(order1):]
                for order2 in self.menu:
                    idx = sentence.find(order2)
                    if idx != -1:
                        order_list = order_list + ";" + order2
                        sentence = sentence[:idx]+sentence[idx+len(order2):]
        return order_list, sentence
    def tokenize(self, sent):
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJ2ZXIiOjAuMSwiaWF0IjoxNjYzMzIwNTQ0LCJ1c2VyX2lkIjoiNDQ0IiwiaWQiOjUwNSwic2NvcGVzIjoiMCIsInN1YiI6IiIsImlzcyI6IkpXVCIsInNlcnZpY2VfaWQiOiIxIiwiYXVkIjoid21ta3MuY3NpZS5lZHUudHciLCJuYmYiOjE2NjMzMjA1NDQsImV4cCI6MTY3ODg3MjU0NH0.aQmo2HD0fqF5J36jd-aa6wG4P8XLWQgwOyi-QY9yAEiYjebr8twa2K8cGbIpqPAIgX9fZC-Ac99jHzTaGFRA5Df_5Boh-75jfnf_4a80ic1ynm2_bWjX3Hz8dh2fdQYT7DTf7k_fIxI919kzXjxk3i7wV4Az3EQLe8razQMpSP4"
        res = requests.post("http://140.116.245.157:2001", data={"data":sent, "token":token})
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            return None

    def ask(self, question):
        result = {
            "order": None,  #菜名
            "number": None, #份數
            "alter": None,  #新增或刪除
            "reply": None
        }
        temp = self.tokenize(question)
        word, pos = temp['ws'][0], temp['pos'][0]
        idx, sim = self.find_similar(self.tfidf.getVector(word))
        if sim < self.threshold:
            result["reply"] = '我不知道你在說甚麼？'
        else:
            ans = self.answers[idx].rstrip().split()
            status, reply = int(ans[0]), ans[1]
            orderType, question = self.menuSearch(question)
            if status == 1:
                result["order"] = orderType
                result["number"] = 1
                result["alter"] = 1
                result["reply"] = reply
                for w, p in zip(word, pos):
                    if p == 'Neu':
                        result["number"] = self.numberMap[w]
                        break
            elif status == -1:
                result["order"] = orderType
                result["number"] = 1
                result["alter"] = -1
                result["reply"] = reply
                for w, p in zip(word, pos):
                    if p == 'Neu':
                        result["number"] = self.numberMap[w]
                        break
            elif status == 2:
                result["order"] = orderType.split(";")
                result["number"] = 1
                result["alter"] = 2
                result["reply"] = reply
            elif status == 0:
                result["reply"] = reply
            elif status == 200:
                result["reply"] = None
        return result
    def find_similar(self, vector):
        idx = -1
        max_idx = -1
        max_similar = 0
        length_v = norm(vector) + 10e-5 # smoothing
        for base_vector in self.base_vectors:
            similar = np.sum((vector * base_vector) / length_v / norm(base_vector))
            idx += 1
            if (similar > max_similar):
                max_similar = similar
                max_idx = idx
        return max_idx, max_similar

class TFIDF:
    def __init__(self, sentences=None, files=['./files/idf.npy', './files/wordmap.json']):
        if sentences is not None:
            idf = defaultdict(int)
            for sentence in sentences:
                sentence = set(sentence)
                for word in sentence:
                    idf[word] += 1
            self.wordmap = dict( zip(idf.keys(), range(len(idf.keys()))) )
            self.idf = np.array(list(idf.values()))
            self.idf = np.log(len(sentences) / (self.idf + 1))
        else:
            # load idf & wordmap
            self.idf = np.load(files[0])
            with open(files[1], 'r', encoding='utf-8') as f:
                self.wordmap = json.load(f)

    def getVector(self, sentence):
        vector = np.zeros((len(self.wordmap.keys()), ))
        for word in sentence:
            if word in self.wordmap.keys():
                vector[self.wordmap[word]] += 1
        return self.idf * vector

    def save(self, idf_file=None, wordmap_file=None):
        if idf_file is None or wordmap_file is None:
            print("Error! You need to have both file names :(")
        else:
            np.save(idf_file, self.idf)
            with open(wordmap_file, 'w', encoding='utf-8') as f:
                json.dump(self.wordmap, f, ensure_ascii=False)
