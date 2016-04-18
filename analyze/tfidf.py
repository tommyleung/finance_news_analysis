# encoding=utf-8

import codecs
import math
import word_segment
import json
import sys

class TFIDFTransformer(object):
    def __init__(self):
        self.word_idf = {}
        self.doc_count = 0
        self.has_idf = False

    def addDocument(self, raw_doc, use_stop_words=False):
        doc_word_list = word_segment.word_segment(raw_doc, use_stop_words)
        self.addDocumentWordList(doc_word_list)
        pass

    def addDocumentWordList(self, doc_word_list):
        self.doc_count += 1
        for w in set(doc_word_list):
            if w in self.word_idf:
                self.word_idf[w] += 1
            else:
                self.word_idf[w] = 1
        pass

    def calculateIDF(self):
        if self.doc_count == 0:
            return
        for w in self.word_idf:
            self.word_idf[w] = math.log(
                self.doc_count / (self.word_idf[w] + 1.0))
        self.has_idf = True
        pass

    def dumpIDFDict(self, filename=r"idf.dat"):
        if not self.has_idf:
            return
        output = codecs.open(filename, 'wb', 'utf-8')
        for w in self.word_idf:
            output.write(w + '\t' + str(w) + '\n')
        pass

    def clear(self):
        self.word_idf.clear()
        self.doc_count = 0
        pass


def main():
    doc_file = r'C:\Users\s_pankh\news_data\crawl_news\EastMoneyNewsSpider-bak.json'
    idf_file = r'C:\Users\s_pankh\news_data\analyze\data\idf.txt'
    file = codecs.open(doc_file, 'r', 'utf-8')
    tfidf = TFIDFTransformer()
    i = 0
    for line in file:
        i = i+1
        print i
        try:
            data = json.loads(line.strip())
            content = data.get('content')
            if content is not None:
                tfidf.addDocument(content)
        except:
            '''
            try:
                sys.stderr.write(line+'\n')
            except:
                pass
            '''
            pass
    tfidf.calculateIDF()
    tfidf.dumpIDFDict(idf_file)
    tfidf.clear()
    pass


if __name__ == '__main__':
    main()