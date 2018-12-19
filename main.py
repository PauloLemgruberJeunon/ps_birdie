import pickle
import spacy
import time
from nltk.tokenize import word_tokenize


class Taggers:
    '''
    Class responsible to load an handle the different POS Tagger used in this
    project. It has a static function used to convert different types of tags.
    '''
    conversion_dict = {'NOUN': 'N', 'NPROP': 'N', 'VERB': 'V'}

    def __init__(self):
        self.aubt_tagger, self.brill_tagger, self.nlp_tool = self.load_taggers()

    def load_taggers(self):
        try:
            aubt_tagger_mdl = open('./taggers/mac_morpho_aubt.pickle', 'rb')
            aubt_tagger = pickle.load(aubt_tagger_mdl)
        except FileNotFoundError as e:
            aubt_tagger = None
            print('[WARNING] Not able to load aubt_tagger')

        try:
            brill_tagger_mdl = open('./taggers/mac_morpho_brill_aubt.pickle', 'rb')
            brill_tagger = pickle.load(brill_tagger_mdl)
        except FileNotFoundError as e:
            brill_tagger = None
            print('[WARNING] Not able to load brill_tagger')

        try:
            nlp_tool = spacy.load('pt_core_news_sm')
        except Exception as e:
            nlp_tool = None
            print('[WARNING] Portuguse model not found...')
            print('Download it using ./venv/bin/python3 -m spacy download pt')

        print('POS Tagger\'s modules loaded')
        return aubt_tagger, brill_tagger, nlp_tool

    @staticmethod
    def normalize_tag(tag):
        # Convert all tags to the same tag pattern
        if tag in Taggers.conversion_dict:
            return Taggers.conversion_dict[tag]
        return tag

    def tag_with_aubt(self, text_string):
        # Function used to tokenize and tag a text string with the aubt tagger
        if self.aubt_tagger is None:
            print('[WARNING] aubt tagger could not be loaded')
            return None

        toks = word_tokenize(text_string)
        return self.aubt_tagger.tag(toks)

    def tag_with_brill(self, text_string):
        # Function used to tokenize and tag a text string with the brill tagger
        if self.brill_tagger is None:
            print('[WARNING] brill tagger could not be loaded')
            return None

        toks = word_tokenize(text_string)
        return self.brill_tagger.tag(toks)

    def tag_with_spacy(self, text_string):
        # Function used to tokenize and tag a text string with the spacy tagger
        if self.nlp_tool is None:
            print('[WARNING] brill tagger could not be loaded')
            return None

        tagged_text = self.nlp_tool(text_string)
        tagged_text_formated = []
        for tok in tagged_text:
            tag = self.normalize_tag(tok.pos_)
            tagged_text_formated.append((tok.text, tag))

        return tagged_text_formated


def load_reviews():
    try:
        data_file = open('./data/reviews_test_estag_nlp.txt', 'r')
        reviews = data_file.readlines()
    except FileNotFoundError as e:
        print('[WARNING] Not able to load reviews. Aborting ...')
        quit()

    return reviews


def process_reviews(reviews, tag_function):
    '''
    Function used to iterate over all reviews and extract the patterns if any
    present in the reviews.
    @param reviews: List of text strings each one containing one review/comment
    @param tag_function: Pointer of the postag function

    @return: Return a list of strings containing the patterns extracted from the
    reviews
    '''

    # Nested dictionaries to aid in the search for the wanted patterns
    patterns_tree = {'N': {'ADJ': None, 'V': {'ADJ': None}}}
    # Int number representing the highest number of pos tags in a pattern
    tree_max_depth = 3
    opinions = []
    for i, review in enumerate(reviews):
        tagged_review = tag_function(review)
        opinions.extend(extract_patterns(tagged_review, patterns_tree,
                                         tree_max_depth))

    return opinions


def extract_patterns(tagged_sent, patterns_tree, tree_max_depth):
    '''
    Function used to find and return patterns in a postagged sentence.

    @param tagged_sent: Is a list of tuples. Each tuple contain the word on the
    first position and it's postag on the second.
    @param patterns_tree: Nested dictionaries containing the wanted patterns.
    @param tree_max_depth: Int number representing the maximum number of postags
    a pattern has in the patterns_tree.

    @return: Returns a list of strings. Each string contains an extracted pattern
    '''
    opinions = []
    i = 0
    # The i represents a starting point for finding a pattern
    while i < len(tagged_sent) - 1:
        curr_tree_level = patterns_tree
        opinion = ''
        # The j is the offset while searching for a pattern that started on i
        for j in range(tree_max_depth):
            if j + i < len(tagged_sent):
                curr_tag = Taggers.normalize_tag(tagged_sent[i + j][1])
                if curr_tag in curr_tree_level:
                    if curr_tree_level[curr_tag] is None:
                        opinion += tagged_sent[i + j][0]
                        opinions.append(opinion)
                        i += j
                        break
                    else:
                        curr_tree_level = curr_tree_level[curr_tag]
                        opinion += tagged_sent[i + j][0] + ' '
                else:
                    break
            else:
                break
        i += 1

    return opinions


def save_results(opinions, file_name):
    with open('./results/' + file_name, 'w') as result_file:
        for opinion in opinions:
            result_file.write(opinion + '\n')


if __name__ == '__main__':
    reviews = load_reviews()
    taggers = Taggers()

    ini = time.time()
    opinions_with_aubt = process_reviews(reviews, taggers.tag_with_aubt)
    end = time.time()
    print('Time to process with aubt pos tagger:', str(end - ini), 's')

    ini = time.time()
    opinions_with_brill = process_reviews(reviews, taggers.tag_with_brill)
    end = time.time()
    print('Time to process with brill pos tagger:', str(end - ini), 's')

    ini = time.time()
    opinions_with_spacy = process_reviews(reviews, taggers.tag_with_spacy)
    end = time.time()
    print('Time to process with spacy pos tagger:', str(end - ini), 's')

    save_results(opinions_with_aubt, 'opinions_with_aubt.txt')
    save_results(opinions_with_brill, 'opinions_with_brill.txt')
    save_results(opinions_with_spacy, 'opinions_with_spacy.txt')
