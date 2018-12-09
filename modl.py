import spacy
import textacy


print('loading en_coref_md...')
nlp = spacy.load('en_coref_sm')
print('done')



# for now assuming all names are unique identifiers
class Person:
    # statements = []
#     resolved_refs = []

    def __init__(self, name, refs=[]):
        self.name = name
#         self.gender = gender
        self.refs = refs
#         self.user = user




# UPGRADE AT SOME POINT TO EXTRACT GENDER, ACCOUNT FOR CLUSTERS WITHOUT NAMES
# UPGRADE TO INCLUDE I, USER

# assumes names are unique identifiers
# assumes misspellings are diff people

# MEMORYLESS FOR NOW; each change to text means a whole new model
# Set extensions later, for keeping track of which tokens are what
class Model:
    def __init__(self, text):
        self.raw = text
        preprocessed = textacy.preprocess.normalize_whitespace(text)
        preprocessed = textacy.preprocess.preprocess_text(preprocessed, fix_unicode=True, no_contractions=True, no_accents=True)
        self.doc = nlp(preprocessed)

        self.people = []
        self.extract_people()

        self.resolved = self.get_resolved()
        print([person.refs for person in self.people])

    def get_person_by_name(self, name):
        for person in self.people:
            if person.name == name:
                return person
        return None

    def extract_people(self, doc=None):
        if doc == None:
            doc = self.doc
        namedrops = [ent for ent in doc.ents if ent.label_ == 'PERSON']
        names = set([namedrop.text for namedrop in namedrops])

        # for clusters that include namedrops
        if doc._.coref_clusters != None:
            for cluster in doc._.coref_clusters:
                name = None

                for mention in cluster.mentions:
                    mention_text = mention.root.text
                    if mention_text in names:
                        name = mention_text

                if name != None:
                    person = self.get_person_by_name(name)
                    if person == None:
                        self.people += [Person(name, refs=cluster.mentions)]
                    else:
                        person.refs = list(set(person.refs + cluster.mentions))

        # for named entities without clusters (single mentions)
        for namedrop in namedrops:
            person = self.get_person_by_name(namedrop.text)
            if person == None:
                self.people += [Person(namedrop.text, refs=[namedrop])]
            else:
                person.refs = list(set(person.refs + [namedrop]))

        # for user (first person refs)
        refs = []
        for token in doc:
            pronoun = token.tag_ in ['PRP', 'PRP$']
            first_person = token.text.lower() in ['i', 'me', 'my', 'mine', 'myself']
            if pronoun and first_person:
                start = token.i - token.n_lefts
                end = token.i + token.n_rights + 1
                ref = doc[start:end]
                refs += [ref]
        self.people += [Person('User', refs)]

    def get_resolved(self, doc=None):
        if doc == None:
            doc = self.doc

        resolved_text = [token.text_with_ws for token in self.doc]
        for person in self.people:
            for ref in person.refs:

                # determine resolved value
                resolved_value = '[' + person.name.upper() + ']'
                if ref.root.tag_ == 'PRP$':
                    resolved_value += '\'s'
                if ref.text_with_ws[-1] == ' ':
                    resolved_value += ' '

                # set first token to value, remaining tokens to ''
                resolved_text[ref.start] = resolved_value
                for i in range(ref.start+1, ref.end):
                    resolved_text[i] = ''
        return ''.join(resolved_text)

    # def update_people_statements(self, doc):
    #     res = nlp(self.resolve_people(doc))
    #
    #     for person in model.people:
    #         statements = []
    #         for ref in person.refs:
    #             head = ref.root.head
    #             if head.pos_ == 'VERB':
    #                 for statement in textacy.extract.semistructured_statements(res, person.name, head.lemma_):
    #                     statements += [statement]
    #         person.statements = list(set(statements))
