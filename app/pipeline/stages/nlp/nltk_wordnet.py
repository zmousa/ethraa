import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet

class NLTKWordnet:
     def get_synonyms_antonyms(self, word):
          definitions = []
          synonyms = []
          antonyms = []

          for syn in wordnet.synsets(word, lang='arb'):
               definitions.append(syn.definition())
               for l in syn.lemmas(lang='arb'):
                    synonyms.append(l.name())
                    if l.antonyms():
                         antonyms.append(l.antonyms()[0].name())
          
          return {
               'definitions': set(definitions),
               'synonyms': set(synonyms),
               'antonyms': set(antonyms)
          }


wn = NLTKWordnet()
result = wn.get_synonyms_antonyms('فرح')
print(result)
