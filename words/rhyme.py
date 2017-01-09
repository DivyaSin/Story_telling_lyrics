import copy
import nltk
from collections import defaultdict
import random
import cPickle
import gzip
import os
import re
import unirest
from nltk.corpus import PlaintextCorpusReader, wordnet
import syllables
import pronouncing
import pprint
from nltk.tokenize import word_tokenize
# from nltk.tag import pos_tag
# from fnmatch import fnmatch
# from difflib import SequenceMatcher
from fuzzywuzzy import fuzz

rhyme_entries = nltk.corpus.cmudict.entries()
pronunciationDictionary = nltk.corpus.cmudict.dict() 

# dictionary of actions
action_keys = ['ACT', 'PRE', 'POS', 'TEN', 'TEXT']
action_dictionary = {}
actions_list = []

with open("actions.txt") as actions_file: 
  for line in actions_file:

    if line.strip() in action_keys:
        new_key = line.strip()
        action_dictionary[new_key] = []
    else:
      if not line.strip():
        # pprint.pprint(action_dictionary)
        l = action_dictionary["TEXT"]
        l = [val for sublist in l for val in sublist]
        action_dictionary["TEXT"] = l
        actions_list.append(action_dictionary)
        action_dictionary = {'ACT':[], 'PRE':[], 'POS':[], 'TEN':[], 'TEXT':[]}
        continue
      else:
        if new_key in ['PRE', 'POS', 'TEN']:
          val = line.strip().split(" ")
        else:
          val = line.strip().split(". ")
          # if new_key == "TEXT":
          #   val.pop()
        if new_key == "TEXT":
          if action_dictionary[new_key]:
            action_dictionary[new_key].append(val)
            # for string in action_dictionary[new_key]:
            #   val.append(string)
          else:
            val = [val]
            action_dictionary[new_key] = val
        else:
          val_array=[val]
          if action_dictionary[new_key]:
            for array in action_dictionary[new_key]:
              val_array.append(array)
          val_array.reverse()
          # val_array = [val for sublist in val_array for val in sublist]
          action_dictionary[new_key] = val_array
          action_dictionary.update(action_dictionary)
    if line == "END":
      break
# pprint.pprint(actions_list)

# output = ""
# file_name = "corpus/new_lyrics_reversed.txt"
# string_to_add = "."

# with open(file_name, 'r') as f:
#     file_lines = [''.join([x.strip(), string_to_add, '\n']) for x in f.readlines() ]

# with open(file_name, 'w') as f:
#     f.writelines(file_lines) 

corpus_root = '/Users/divyasingh/Desktop/Story_telling_lyrics/words/corpus'
wordlists = PlaintextCorpusReader(corpus_root, '.*')

# print wordlists.fileids()

# print wordlists.sents('lyrics1.txt')

# print wordlists.sents('lyrics.txt')

# li = [i.strip().split() for i in open("lyrics1.txt").readlines()]

# mega_sentences = ( wordlists.sents('taylor_lyrics.txt') ) 
mega_sentences = (wordlists.sents('new_lyrics_reversed.txt')) 

# mega_sentences = ( nltk.corpus.brown.sents() + 
#                 nltk.corpus.inaugural.sents() + 
#                 nltk.corpus.reuters.sents() + 
#                 nltk.corpus.webtext.sents() + 
#                 nltk.corpus.inaugural.sents() + 
#                 nltk.corpus.gutenberg.sents("carroll-alice.txt") +
#                 nltk.corpus.gutenberg.sents("austen-emma.txt") + 
#                 nltk.corpus.gutenberg.sents("austen-sense.txt") + 
#                 nltk.corpus.gutenberg.sents("blake-poems.txt") + 
#                 nltk.corpus.gutenberg.sents("bible-kjv.txt") + 
#                 nltk.corpus.gutenberg.sents("chesterton-ball.txt") + 
#                 nltk.corpus.gutenberg.sents("melville-moby_dick.txt") + 
#                 nltk.corpus.gutenberg.sents("milton-paradise.txt") + 
#                 nltk.corpus.gutenberg.sents("whitman-leaves.txt") + 
#                 nltk.corpus.gutenberg.sents("austen-persuasion.txt") + 
#                 nltk.corpus.gutenberg.sents("shakespeare-hamlet.txt") + 
#                 nltk.corpus.gutenberg.sents("shakespeare-macbeth.txt") ) 

last_word_sentences = defaultdict(list)

def last_word(sentence):
    ss = [ word for word in sentence if len(word) > 1 ]
    if len(ss) > 0:
        return ss[-1]
    else:
        return "" 

if os.path.exists("sentences.gz"):
    with gzip.open("sentences.gz", "r") as cache_file:
        last_word_sentences = cPickle.load( cache_file )
else:
    for sentence in mega_sentences:
        lw = last_word(sentence)
        last_word_sentences[ lw ].append(sentence)
    with gzip.open("sentences.gz", "w") as cache_file:
        cPickle.dump(last_word_sentences, cache_file)

def candidate_sentences(word):
    return last_word_sentences[ word.lower() ]

def quality_of_rhyme(p1, p2):
    p1 = copy.deepcopy(p1)
    # print p1
    p2 = copy.deepcopy(p2)
    # print p2
    p1.reverse()
    # print p1
    p2.reverse()
    # print p2
    if p1 == p2:
        return 0
    quality = 0
    for i, p in enumerate(p1):
        try:
            if p == p2[i] and p in ('a', 'e', 'i', 'o', 'u'):
                quality += 3
            else:
                quality += 1
            if p != p2[i]:
                break
        except IndexError:
            break
    return quality
    
def find_high_priority(candidates, word):
    p2 = list(copy.deepcopy(word))
    p2.reverse()
    new_candidates = []
    for candidate in candidates:
        p1 = list(copy.deepcopy(candidate))
        p1.reverse()
        # print "Words are:"
        # print p1
        # print p2
        if p1 == p2:
            return 0
        quality = 0
        sameVowelFound = False
        for i, p in enumerate(p1):
            try:
                if p == p2[i]:
                    # print p
                    # print p2[i]
                    quality += 1
                    if p not in ('a', 'e', 'i', 'o', 'u'):
                        quality -= 1
                    if p in ('a', 'e', 'i', 'o', 'u') and (not sameVowelFound):
                        quality += 1
                        sameVowelFound = True
                    # print quality
                else:
                    break  
            except IndexError:
                break
        if quality > 0:
            new_candidates.append( (quality, candidate) )
    new_candidates.sort()
    new_candidates.reverse()
    new_candidates = [ candidate for quality, candidate in new_candidates ]
    # print candidates
    return new_candidates

def word_rhyme_candidates(word):
    word = word.lower()
    candidates = []
    try:
        pronunciations = pronunciationDictionary[word]
    except KeyError:
        return word_rhyme_candidates(word[-1])
    if pronunciations == []:
        print "No pronunciations"
        return []
    for pronunciation in pronunciations:
        for rhyme_word, rhyme_pronunciation in rhyme_entries:
            quality = quality_of_rhyme(pronunciation, rhyme_pronunciation)
            if quality > 0:
                candidates.append( (quality, rhyme_word) )
    candidates.sort()
    candidates.reverse()
    # best_quality = candidates[0][0]
    # worst_quality = best_quality - 5
    # candidates = [ candidate for q, candidate in candidates if q >= worst_quality ]
    candidates = [ candidate for q, candidate in candidates ]
    # print candidates
    # print candidates
    new_candidates = find_high_priority(candidates, word)
    if not new_candidates:
        # print "Candidates taken"
        # print candidates
        return candidates
    else:
        # print "New_candidates taken"
        # print new_candidates
        return new_candidates

def get_pre_score(sentiment_dictionary):
    PRE_list = sentiment_dictionary.get('PRE')
    # get sentiment_score
    for list in PRE_list:
        for symbol in list:
            if symbol[0] == '-':
                return -1 * int(symbol[1])
            elif symbol[0] == '+':
                return int(symbol[1])
    return 0

def get_pos_score(sentiment_dictionary):
    POS_list = sentiment_dictionary.get('POS')
    # get sentiment_score
    for list in POS_list:
        for symbol in list:
            if symbol[0] == '-':
                return -1 * int(symbol[1])
            elif symbol[0] == '+':
                return int(symbol[1])
    return 0

def get_story_score(sentiment_dictionary):
    if not sentiment_dictionary.get('POS'):
        # print 'No pos'
        if not sentiment_dictionary.get('PRE'):
            story_score = 0
            return story_score
        else:
            story_score = get_pre_score(sentiment_dictionary)
            return story_score
    else:
        # print "pos"
        story_score = get_pos_score(sentiment_dictionary)
        if story_score == 0:
            story_score = get_pre_score(sentiment_dictionary)
        return story_score

def get_sentiment_dictionary(pattern, actions_list):
    max_similarity_score = 0
    sentiment_dictionary = []
    for dictionary in actions_list:
        for string in dictionary["TEXT"]:
            # print pattern
            # print string
            # m = SequenceMatcher(None, pattern, string)
            similarity_score = fuzz.partial_ratio(pattern, string)
            # print similarity_score
            # print "###########"
            if similarity_score > max_similarity_score:
                max_similarity_score = similarity_score
                sentiment_dictionary = dictionary
    return sentiment_dictionary

def get_corpus_score(close_sentences):
    closest_sentences = []
    for line in close_sentences:
        # print line
        unirest.timeout(10)
        try:
            response = unirest.get("https://twinword-sentiment-analysis.p.mashape.com/analyze/?text=%s" % line,
            headers={
            "X-Mashape-Key": "ur8eDH4fVCmshtOozaz1zoWSjS79p1U8IGljsnA2aJAoTuh4Fc",
            "Accept": "application/json"
            }
            )
        except Exception, e:
            print "exception thrown"
            print e

        if response.code != 200:
            continue
        t = response.body
        # print line
        # print t
        # keywords = t['keywords']
        score = t['score']
        # for keyword in keywords:
        #     score = score + keyword['score']
        # if len(keywords) != 0:
        #     score = score / len(keywords)
        # else:
        #     score = 0
        if 0.05 < score < 0.5:
            score = 1
        elif 0.5 < score < 2.0:
            score = 2
        elif score > 2.0:
            score = 3
        elif -0.05 < score < 0.5:
            score = 0
        elif -0.5 < score < -0.05:
            score = -1
        elif -0.5 < score < -2.0:
            score = -2
        else:
            score = -3
        closest_sentences.append((score, line))
    # print closest_sentences 
    return closest_sentences

def get_rhyme(sentence):
    pattern = sentence
    # post_tag_list = nltk.pos_tag(sentence.split())
    target_syllables = syllables.sentence_syllables(sentence)
    tokens = nltk.word_tokenize(sentence) 
    rhymes = word_rhyme_candidates(last_word(tokens))
    candidate_sentence = []
    # if len(tokens) == 1:
    #     return ", ".join(rhymes[:12])
    for rhyme in rhymes:
        candidate_sentence += candidate_sentences( rhyme )
    syllable_sentences = []
    for sentence in candidate_sentence:
        sumOfSyllables = sum( [ syllables.syllables(word) for word in sentence ] )
        syllable_sentences.append( (sumOfSyllables, " ".join(sentence)) )
    # print syllable_sentences
    syllable_sentences.sort()
    syllable_sentences.reverse()
    if len( syllable_sentences ) == 0:
        if len( rhymes ) > 0: 
            # get synonyms of rhyme
            return " "
            return ", ".join(rhymes[:12])
        else:
            return "Oho ho ho ho ho"
    syllable_numbers = [ n for n, sentence in syllable_sentences ] 
    close_number = min( syllable_numbers, key=lambda x:abs(x-target_syllables) )
    close_sentences = [ sentence for n, sentence in syllable_sentences if close_number-1 <= n ] 
    closest_sentences = get_corpus_score(close_sentences)
    sentiment_dictionary = get_sentiment_dictionary(pattern, actions_list)
    story_score = get_story_score(sentiment_dictionary)
    # for score, sentence in closest_sentences:
    #     print score, sentence, story_score
    #     if score == story_score:
    #         print sentence
    rhyme_sentences = []
    # mapping of sentiments 
    if story_score > 0:
        rhyme_sentences = [ sentence for score, sentence in closest_sentences if score == story_score] 
        rhyme_sentences.sort()
        # pprint.pprint(rhyme_sentences)
    elif story_score < 0:
        rhyme_sentences = [ sentence for score, sentence in closest_sentences if score == story_score] 
        rhyme_sentences.sort()
        # pprint.pprint(rhyme_sentences)
    else:
        rhyme_sentences = [ sentence for score, sentence in closest_sentences if score == 0] 
        # print rhyme_sentences 
    if not rhyme_sentences:
        rhyme_sentences = close_sentences
    return random.choice(rhyme_sentences) # need to fix this

def generate_lyrics(string):
    pat = ('\. +(?=[A-Z ])')
    text = re.sub(pat, '\n', string)
    print ""
    print ""
    print "##### STORY #####"
    print ""
    print text
    print ""
    print "#################"
    print 

    text_file = open('story.txt', 'w')  
    text_file.write(text)
    text_file.close()

    with open ("story.txt") as f:
        lines = f.readlines()
        line_no = 0
        rhyme_lines = []
        for line in lines:
            rhyme_line = get_rhyme(line)
            rhyme_lines.insert(line_no, rhyme_line)
            line_no += 1

    print "#### LYRICS ####"
    print ""

    for i, v in enumerate(rhyme_lines):
        lines.insert(2*i+1, v)
    for i,j in enumerate(lines):
        print j.strip("\n")
        if (i in [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47]):
            print ''
        else:
            pass
    print "################"

generate_lyrics("Tlaloc -the God of the rain- was angry. He sent a storm. The heavy rain damaged the old wooden bridge. Princess tried to cross the river. The bridge collapsed injuring badly Princess's head. Princess's life was at risk. Princess was not cured. In this way, Trader expected Princess's dead. Trader thoroughly observed Princess. Then, Trader took a dagger. Jumped towards Princess. Princess was attacked.")
