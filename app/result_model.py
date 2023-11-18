from pipeline.stages.nlp.nlp import LemmaItem

class ResultItem:
    def __init__(self, word: LemmaItem, enrichment: str, translation: str, nltk: str, ner: str, found: bool):
        self.word = word
        self.enrichment = enrichment
        self.translation = translation
        self.nltk = nltk
        self.ner = ner,
        self.found = found
