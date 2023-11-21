import qalsadi.lemmatizer
from lang_trans.arabic import buckwalter
import sqlite3
from itertools import chain


class LemmaItem:
    def __init__(self, word, type, senses, meaning):
        self.word = word
        self.type = type
        self.senses = senses
        self.meaning = meaning

class NLP_Lemmatizer:

    ar_relations = {'related_to' : "متعلق بـ",'near_synonym': "مرادف",'near_antonym': "تضاد",'pertainym':"تختص بـ",'hyponym' : "فرعي",'has_hyponym': "ذو معنى فرعي"}
    ar_types = {'noun' : "اسم",'verb': "فعل"}

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
            item = LemmaItem(t[0], self.ar_types.get(t[1], t[1]), self.wordnet_lookup(t[0]), self.get_meaning(t[0]))
            lemma_items.append(item)
        return lemma_items

    def wordnet_lookup(self, word):
        res = self.cur.execute("select type, LINK2 from LINK where LINK1 like ? and LINK2 not like ? and type in ('related_to','near_synonym','near_antonym','pertainym','hyponym','has_hyponym') LIMIT 50", (buckwalter.transliterate(word[0:-1])+'%','%EN',))
        untransliterated_words = [(self.ar_relations.get(rel, rel), buckwalter.untransliterate(word.split("_")[0])) for rel, word in res]

        return untransliterated_words

    def get_meaning(self, text):
        transliterate_word = buckwalter.transliterate(text[0:-1])
        res = self.cur.execute("SELECT i.GLOSS FROM link l INNER JOIN item i ON i.ITEMID = l.LINK2 WHERE l.link1 LIKE ? AND l.TYPE = 'equivalent'",(transliterate_word+"%",))
        word = res.fetchone()
        if word:
            return word[0]
        else:
            ""
