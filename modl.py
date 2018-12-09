import spacy
import textacy


print('loading en_coref_md...')
nlp = spacy.load('en_coref_sm')
print('done')



# for now assuming all names are unique identifiers
class Person:
    statements = []
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
    raw = None
    doc = None
    people = []
    resolved = None

    def __init__(self, text):
        raw = text
        preprocessed = textacy.preprocess.normalize_whitespace(text)
        preprocessed = textacy.preprocess.preprocess_text(preprocessed, fix_unicode=True, no_contractions=True, no_accents=True)
        self.doc = nlp(preprocessed)
        print(self.doc.text)
        self.extract_people()
        self.resolved = self.get_resolved()

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
                        person = Person(name, refs=cluster.mentions)
                        self.people += [person]
                    else:
                        person.refs = list(set(person.refs + cluster.mentions))

        # for named entities without clusters (single mentions)
        for namedrop in namedrops:
            person = self.get_person_by_name(namedrop.text)
            if person == None:
                person = Person(namedrop.text, refs=[namedrop])
                self.people += [person]
            else:
                person.refs = list(set(person.refs + [namedrop]))

#     def get_resolved_text(self, doc=None):
#         if doc == None:
#             doc = self.doc
#         tokens = [token.text for token in doc]
#         for person in self.people:
#             for ref in person.refs:

#                 # determine resolved value
#                 resolved_token = person.name
#                 if ref.root.pos_ == 'ADJ':
#                     resolved_token += '\'s'

#                 # set first token to resolved value
#                 tokens[ref.start] = resolved_token

#                 # set extra tokens in mention to blank
#                 for i in range(ref.start+1, ref.end):
#                     tokens[i] = ''
#         return ' '.join([token for token in tokens if token != ''])

#     def resolve(self):
#         self.resolved_text = self.get_resolved_text()
#         self.resolved_doc = nlp(self.resolved_text)

#         offset = 0;
#         for person in self.people:
#             for ref in person.refs:
#                 resolved_ref = self.resolved_doc[ref.start-offset:ref.start-offset+1]
#                 person.resolved_refs += [resolved_ref]

#                 # increase offset for each multi-word ref
#                 words_in_ref = (ref.end - ref.start)
#                 offset += words_in_ref - 1
#     def resolve(self):

#         # create resolved text
#         chars = list(self.doc.text)
#         chars_inserted_before = 0
#         for person in self.people:
#             for ref in person.refs:

#                 # determine resolved value
#                 resolved = person.name
#                 if ref.root.pos_ == 'ADJ':
#                     resolved += '\'s'
#                 if ref.text_with_ws[-1] = ' ':
#                     resolved += ' '


#                 # set appropriate chars to resolved value
#                 new_start = ref.start_char + chars_inserted_before
#                 new_end = ref.end_char + chars_inserted_before
#                 print(chars_inserted_before, new_start, new_end, chars[new_start:new_end], list(resolved))
#                 chars[new_start:new_end] = list(resolved)
#                 chars_inserted_before += len(resolved) - len(ref.text)

#         self.resolved_doc = nlp(''.join(chars))

#         # create list with original text but resolved token index
#         merged_copy = copy(self.doc)
#         for person in self.people:
#             for ref in person.refs:
#                 merged_copy.char_span(ref.start_char, ref.end_char).merge()

#         # use merged_copy to translate refs to resolved_refs
#         for person in self.people:
#             for ref in person.refs:
#                 resolved_i = merged_copy.char_span(ref.char_start, ref.char_end)
#                 resolved_ref = self.resolved_doc[resolved_i]
#                 person.resolved_refs = list(set(person.resolved_refs + resolved_ref))

    def get_resolved(self, doc=None):
        if doc == None:
            doc = self.doc

        resolved_text = [token.text_with_ws for token in self.doc]
        for person in self.people:
            for ref in person.refs:

                # determine resolved value
                resolved_value = person.name
                if ref.root.pos_ == 'ADJ':
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
