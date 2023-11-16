from typing import List, Optional


class FormRepresentation:
    def __init__(self, form: str, phonetic: str, dialect: str, audio: str):
        self.form = form
        self.phonetic = phonetic
        self.dialect = dialect
        self.audio = audio

class Lemma:
    def __init__(self, formRepresentations: List[FormRepresentation], type: str):
        self.formRepresentations = formRepresentations
        self.type = type

class Stem:
    def __init__(self, formRepresentations: List[FormRepresentation], type: str):
        self.formRepresentations = formRepresentations
        self.type = type

class WordForm:
    def __init__(
        self,
        formRepresentations: List[FormRepresentation],
        aspect: str,
        def_: str,
        gender: str,
        isNasab: bool,
        numberWordForm: str,
        person: str,
        isSmall: bool,
        voice: str
    ):
        self.formRepresentations = formRepresentations
        self.aspect = aspect
        self.def_ = def_
        self.gender = gender
        self.isNasab = isNasab
        self.numberWordForm = numberWordForm
        self.person = person
        self.isSmall = isSmall
        self.voice = voice

class Definition:
    def __init__(self, statement: str):
        self.statement = statement

class Translation:
    def __init__(self, language: str, form: str, phonetic: str, dialect: str, audio: str):
        self.language = language
        self.form = form
        self.phonetic = phonetic
        self.dialect = dialect
        self.audio = audio

class Context:
    def __init__(self, form: str, phonetic: str, dialect: str, audio: str):
        self.form = form
        self.phonetic = phonetic
        self.dialect = dialect
        self.audio = audio

class Example:
    def __init__(self, form: str, phonetic: str, dialect: str, audio: str, exampleType: str, source: str):
        self.form = form
        self.phonetic = phonetic
        self.dialect = dialect
        self.audio = audio
        self.exampleType = exampleType
        self.source = source

class Relation:
    def __init__(self, type: str, related: str):
        self.type = type
        self.related = related

class Sense:
    def __init__(
        self,
        _id: str,
        definition: Definition,
        translations: List[Translation],
        contexts: List[Context],
        domainIds: List[str],
        domains: List[str],
        examples: List[Example],
        relations: List[Relation],
        image: str
    ):
        self._id = _id
        self.definition = definition
        self.translations = translations
        self.contexts = contexts
        self.domainIds = domainIds
        self.domains = domains
        self.examples = examples
        self.relations = relations
        self.image = image

class CreateBody:
    def __init__(
        self,
        lemma: Lemma,
        stems: List[Stem],
        wordForms: List[WordForm],
        senses: List[Sense],
        morphologicalPatterns: str,
        pos: str,
        plain: str,
        verbOrigin: str,
        nounOrigin: str,
        originality: str,
        hasTanween: bool
    ):
        self.lemma = lemma
        self.stems = stems
        self.wordForms = wordForms
        self.senses = senses
        self.morphologicalPatterns = morphologicalPatterns
        self.pos = pos
        self.plain = plain
        self.verbOrigin = verbOrigin
        self.nounOrigin = nounOrigin
        self.originality = originality
        self.hasTanween = hasTanween
