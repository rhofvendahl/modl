import spacy
import textacy

print('loading en_coref_md...')
nlp = spacy.load('en_coref_med')
print('...done')



# for now assuming all names are unique identifiers
class Person:
    statements = []

    def __init__(self, name, pronouns=None, refs=[], user=False):
        self.name = name
#         self.gender = gender
        self.refs = refs
        self.user = user




# UPGRADE AT SOME POINT TO EXTRACT GENDER, ACCOUNT FOR CLUSTERS WITHOUT NAMES
# UPGRADE TO INCLUDE I, USER

# assumes names are unique identifiers
# assumes misspellings are diff people

# MEMORYLESS FOR NOW; each change to text means a whole new model
# Set extensions later, for keeping track of which tokens are what
class Model:
    text = None
    doc = None
    people = []

    def __init__(self, text):
        self.text = text
        self.doc = self.get_doc()
        self.people = self.get_people()

    def get_doc(self, text=self.text):
        preprocessed = textacy.preprocess.normalize_whitespace(text)
        preprocessed = textacy.preprocess.preprocess_text(preprocessed, fix_unicode=True, no_contractions=True, no_accents=True)
        doc = nlp(preprocessed)

        # merge mentions into tokens for easy coref tracking, resolution
        for cluster in doc._.coref_clusters:
            for mention in cluster.mentions:
                mention.merge()
        return doc

    def get_people(self, doc=self.doc):
        namedrops = [ent for ent in doc.ents if ent.label_ == 'PERSON']
        names = set([namedrop.text for namedrop in namedrops])
        people = []

        # for clusters that include namedrops
        for cluster in doc._.coref_clusters:
            name = None

            for mention in cluster.mentions:
                mention_text = mention.root.text
                if mention_text in names:
                    name = mention_text

            if name != None:
                person = self.get_person_by_name(name)
                refs = [mention.head.i for mention in cluster.mentions]
                if person == None:
                    person = Person(name, refs=refs)
                    people += [person]
                else:
                    person.refs += refs

            # for named entities without clusters (single mentions)
            for name_mention in name_mentions:
                person = self.get_person_by_name(name_mention.text)
                if person == None:
                    person = Person(name_mention.text, refs=[name_mention.head.i])
                    people += [person]
        return people

    def get_person_by_name(self, name):
        for person in self.people:
            if person.name == name:
                return person
                return None

    def get_resolved(self, doc=self.doc):
        tokens = [token.text for token in doc]

        for person in self.people:
            for ref in person.refs:

                # determine resolved value
                resolved = person.name
                if ref.root.pos == 'ADJ':
                    resolved += '\'s'

                # set first token to resolved value
                tokens[ref.start] = resolved

                # set extra tokens in ref to blank
                for i in range(ref.start+1, ref.end):
                    tokens[i] = ''
        return ' '.join([token for token in tokens if token != ''])

    def update_people_statements(self, doc):
        res = nlp(self.resolve_people(doc))

        for person in model.people:
            statements = []
            for ref in person.refss:
                head = ref.root.head
                if head.pos_ == 'VERB':
                    for statement in textacy.extract.semistructured_statements(res, person.name, head.lemma_):
                        statements += [statement]
            person.statements = list(set(statements))
