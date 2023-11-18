import qalsadi.lemmatizer
from lang_trans.arabic import buckwalter
import sqlite3
from itertools import chain


class LemmaItem:
    def __init__(self, word, type, senses):
        self.word = word
        self.type = type
        self.senses = senses

class NLP_Lemmatizer:
    def __init__(self):
        self.lemmer = qalsadi.lemmatizer.Lemmatizer()
        self.lemmer.set_vocalized_lemma()
        con = sqlite3.connect("app/pipeline/stages/nlp/ontology/arabicwordnet.sqlite")
        self.cur = con.cursor()

    def not_stopword(self, str):
        return (str[1] != "stopword" and str[1] != "pounct" and str[1] != "all")

    def lemmatize(self, sections):
        all_lemmas = []
        for text in sections:
            lemmas = self.lemmer.lemmatize_text(text, return_pos=True)
            filtered_lemmas = filter(self.not_stopword, lemmas)
            all_lemmas.append(set(filtered_lemmas))

        result = list(set(chain(*all_lemmas)))
        lemma_items = []
        for t in result:
            item = LemmaItem(t[0], t[1], self.wordnet_lookup(t[0]))
            lemma_items.append(item)
        return lemma_items

    def wordnet_lookup(self, word):
        res = self.cur.execute("select type, LINK2 from LINK where LINK1 like ? and LINK2 not like ? and type in ('related_to','near_synonym','near_antonym','pertainym','hyponym','has_hyponym') LIMIT 50", (buckwalter.transliterate(word[0:-1])+'%','%EN',))
        return res.fetchall()
