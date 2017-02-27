import copy
import nltk
from collections import defaultdict
import random
import cPickle
import gzip
import os
import re
import unirest
import string
from nltk.corpus import PlaintextCorpusReader, wordnet
import syllables
import pronouncing
import pprint
from nltk.tokenize import word_tokenize
from fuzzywuzzy import fuzz
import markov_lyrics
import unicodedata
# from nltk.tag import pos_tag
# from fnmatch import fnmatch
# from difflib import SequenceMatcher

rhyme_entries = nltk.corpus.cmudict.entries()
pronunciationDictionary = nltk.corpus.cmudict.dict() 

tension_dictionary = {}
tension_list = []
with open('/Users/divyasingh/Desktop/Story_telling_lyrics/words/corpus/ce_eg5.txt') as tension_file:
    flag = True
    same_value = True
    val = []
    for line in tension_file: 
        if not line.strip():
            if not tension_dictionary[key]:
                tension_dictionary[key] = []              
            else:
                tension_dictionary.update(tension_dictionary)
            same_value = True
        else:        
            if same_value:
                key = line.strip()
                same_value = False
                tension_dictionary[key] = []
            else:
                val = re.split("[ :,()\n ]", line.strip(" "))
                val = list(filter(None, val))
                if tension_dictionary[key]:
                    tension_dictionary[key].append(val)
                else:
                    tension_dictionary[key] = [val]
# pprint.pprint(tension_dictionary)

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
# flag = "False"
# output = ""
# if flag != "True":
#     file_name = "corpus/lyrics_batch.txt"
# # string_to_add = "."
#     with open(file_name, 'r') as f:
#         file_lines = [''.join([x.strip(), string_to_add, '\n']) for x in f.readlines() ]

#     with open(file_name, 'w') as f:
#         f.writelines(file_lines) 
#     false = "True"

def last_word(sentence):
    ss = [ word for word in sentence if len(word) > 1 ]
    if len(ss) > 0:
        return ss[-1]
    else:
        return "" 

def getMarkovBatch():
    last_word_sentences = defaultdict(list)
    markov_lyrics.markov()
    corpus_root = '/Users/divyasingh/Desktop/Story_telling_lyrics/words/corpus'
    wordlists = PlaintextCorpusReader(corpus_root, '.*')

# print wordlists.fileids()

# print wordlists.sents('lyrics1.txt')

# print wordlists.sents('lyrics.txt')

# li = [i.strip().split() for i in open("lyrics1.txt").readlines()]

# mega_sentences = ( wordlists.sents('taylor_lyrics.txt') ) 

    mega_sentences = (wordlists.sents('lyrics_batch.txt'))
    # print mega_sentences

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

    
    # if os.path.exists("sentences.gz"):
    #     with gzip.open("sentences.gz", "r") as cache_file:
    #         last_word_sentences = cPickle.load( cache_file )
    # else:
    for sentence in mega_sentences:
        lw = last_word(sentence)
        last_word_sentences[ lw ].append(sentence)
    # pprint.pprint(last_word_sentences)
    keys = last_word_sentences.keys()
    # print "\n"
    # print keys
    # with gzip.open("sentences.gz", "w") as cache_file:
    #     cPickle.dump(last_word_sentences, cache_file)
    return keys, last_word_sentences

def candidate_sentences(word):
    # print word
    # print "candidate_sentences"
    candidates = []
    word_pronunciation = pronunciationDictionary[word.lower()]
    word_pro = word_pronunciation[0]
    # print word_pro
    # print 
    # print "Markov chain again called"
    keys, last_word_sentences = getMarkovBatch()
    # print last_word_sentences
    for key in keys:
        try:
            key_pronunciation = pronunciationDictionary[key]
            key_pro = key_pronunciation[0]
            # print key_pro
            # print key_pronunciation
        except KeyError:
            # print "KeyError"
            # if key[-1].isdigit():
            #     continue
            # key_pro = pronunciationDictionary[key[-1].lower()]
            continue
        rhyme_quality = quality_of_rhyme(word_pro, key_pro)
        # print word_pronunciation, key_pronunciation
        # print rhyme_quality
        candidates.append( (rhyme_quality, key) )
    # print candidates
    candidates.sort()
    candidates.reverse()
    words = [ key for rhyme_quality, key in candidates if rhyme_quality >= 1 ]
    # print "words"
    # print words
    
    # print "last_word_sentences"
    # print last_word_sentences
    if words:
        good_word = random.choice(words)
        # print last_word_sentences[good_word.lower()]
        return last_word_sentences[good_word.lower()]  
    else:
        # candidate_sentences(word)
        return ''

def quality_of_rhyme(p1, p2):
    p1 = copy.deepcopy(p1)
    # print p1
    p2 = copy.deepcopy(p2)
    # print p2
    p1.reverse()
    # print "p1 reverse"
    # print p1
    p2.reverse()
    # print "p2 reverse"
    # print p2
    if p1 == p2:
        return 0
    quality = 0
    try:
        if p1[0]==p2[0]:
            quality += 1
            if p1[1]==p2[1] and p1[1] in ['a','e','i','o','u']:
                quality += 2
    except IndexError:
        pass
    # for i, p in enumerate(p1):    
    #     try:
    #         if p == p2[i+1]:
    #             quality += 1
    #     except IndexError:
    #         break
    # print quality
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
    print word
    word = word.lower()
    candidates = []
    pronunciations = []
    try:
        pronunciations = pronunciationDictionary[word]
    except KeyError:
        pass
    if pronunciations == []:
        print "No pronunciations"
        pronunciations = word[-1]
    for pronunciation in pronunciations:
        for rhyme_word, rhyme_pronunciation in rhyme_entries:
            # print pronunciation, rhyme_pronunciation
            if rhyme_word[-1].isdigit():
                continue
            quality = quality_of_rhyme(pronunciation, rhyme_pronunciation)
            if quality > 0:
                candidates.append( (quality, rhyme_word) )
    # print
    # print candidates
    candidates.sort()
    candidates.reverse()
    # print
    # print candidates
    # best_quality = candidates[0][0]
    # worst_quality = best_quality -1
    candidates = [ candidate for q, candidate in candidates ]
    # candidates = [ candidate for q, candidate in candidates ]
    top_candidates = candidates[:50]
    # candidates_random = random.choice(candidates, 50)
    # print candidates_random
    # print top_candidates
    high_priority_candidates = find_high_priority(candidates, word)
    if not high_priority_candidates:
        # print "Candidates taken"
        # print candidates
        return candidates
    else:
        # print "New_candidates taken"
        # print new_candidates
        return high_priority_candidates

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

def get_sentiment_value(pattern, tension_dictionary):
    print pattern
    max_similarity_score = 0
    sentiment_value = []
    lc_found = False
    ce_found = False
    for key, list in tension_dictionary.items():
        similarity_score = fuzz.partial_ratio(pattern, key)
        # print key, list, similarity_score
        if similarity_score >= max_similarity_score:
                max_similarity_score = similarity_score
                sentiment_list = list
    if not sentiment_list:
        return 0
    else:
        for list in sentiment_list:
            print list
            print list
            if list:
                for symbol in list:
                    if symbol[0] == '-':
                        score = -1 * int(symbol[1])
                    if symbol[0] == '+':
                        score =  int(symbol[1])
                    if symbol == 'lc':
                        lc_found = True
                    if symbol == 'ce2':
                        ce_found = True

    if lc_found:
        return -1 * (score)
    elif ce_found:
        return score
    else:
        return score

def get_corpus_score(close_sentences):
    closest_sentences = []
    print close_sentences
    for line in close_sentences:
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
            continue
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
    # for syn in wordnet.sysnsets(last_word(tokens)):
    #     for l in syn.lemmas():
    #         synonyms.append(l.name())
    # print(set(synonyms))
    candidate_sentence = []
    # if len(tokens) == 1:
    #     return ", ".join(rhymes[:12])
    # print "rhymes"
    # print rhymes
    for rhyme in rhymes:
        candidate_sentence += candidate_sentences(rhyme)
    # print sentence
    # print candidate_sentence

    # if candidate_sentence == []:
    #     generate_lyrics(sentence)

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
    close_sentences = [ sentence for n, sentence in syllable_sentences if close_number-1<=n <= close_number+1] 
    close_sentences_set = set(close_sentences)
    close_sentences_list = list(close_sentences_set)
    closest_sentences = get_corpus_score(close_sentences_list)
    # sentiment_dictionary = get_sentiment_dictionary(pattern, actions_list)
    # story_score = get_story_score(sentiment_dictionary)
    # pprint.pprint(tension_dictionary)
    story_score = get_sentiment_value(pattern, tension_dictionary)
    # print "sentiment value"
    # print story_score

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
    print "rhyme_sentences"
    # print rhyme_sentences 
    if not rhyme_sentences:
        rhyme_sentences = close_sentences_list
    return random.choice(rhyme_sentences) # need to fix this

def connect_sentences(line, rhyme_line):
    sub_list = ['Virgin', 'Eagle', 'Princess', 'Prince', 'He', 'She', 'Virgin\'s', 'Lady', 'he', 'she', 'her', 'his', 'priest', 'princess', 'lady', 'him']

    story_line, replaceable_line = line, rhyme_line

    def replace_all(text, dic):
        flag = True
        list_of_words = text.split()
        for i, j in dic.iteritems():
            for k, word in enumerate(list_of_words):
                if word == i:
                    list_of_words[k] = word.replace(word, j)        

        return ' '.join(list_of_words)

    dic_M = {'Id': 'hed', 'I': 'he', 'your': 'his', 'Shes': 'hes', 'Shes': 'hes', 'you' :'he', 'Im': 'hes', 'theyre': 'hes', 'my': 'his', 'Ill': 'he\'ll', 'am':'is', 'dont': 'doesnt', 'yours': 'his', 'me': 'him', 'mine': 'his', 'we': 'He', 'us': 'him', 'are': 'is', 'youre': 'hes', 'Ive': 'He has', 'Youve':'he has', 'We': 'he', 'weve': 'he has', 'have': 'has'}
    dic_F = {'Id': 'shed', 'I': 'she', 'your': 'her', 'Hes': 'shes', 'Hes': 'shes', 'you' :'she', 'Im': 'shes', 'theyre': 'shes', 'my': 'her', 'Ill': 'she\'ll', 'am' :'is', 'dont': 'doesnt', 'yours': 'hers', 'me': 'her', 'mine': 'her', 'we': 'she', 'us': 'her', 'are': 'is', 'youre': 'shes', 'Ive': 'she has', 'Ive':'she has', 'Youve':'she has', 'We': 'she', 'weve': 'she has', 'have':'has'}
    dic_T = {'Id': 'theyd', 'I': 'they', 'you': 'they', 'your': 'their', 'he': 'they', 'He': 'they ', 'She': 'they', 'she': 'they', 'shes':'theyre', 'hes': 'theyre', 'Im': 'theyre', 'my': 'their', 'Ill': 'theyll', 'am': 'are', 'me': 'them', 'mine': 'their', 'we': 'they', 'We': 'They', 'us': 'them', 'youre': 'they are', 'doesnt': 'dont', 'Ive': 'they\'ve', 'youve' : 'they have', 'weve': 'theyve', 'is' : 'are', 'has': 'have', 'was': 'were'}


    count = 0
    for word in story_line.split(): 
        if word in sub_list:
            count +=1

    if count == 1:
        for word in story_line.split(): 
                # print subject
            if word in ['Prince', 'Eagle', 'He', 'his', 'him', 'priest']:
                replaceable_word = 'he'
            else:
                replaceable_word = 'she'
    if count > 1:
        replaceable_word = 'they'
        subject = 'them'

    if replaceable_word == 'he':
        text = replace_all(replaceable_line, dic_M)
    if replaceable_word == 'she':
        text = replace_all(replaceable_line, dic_F)
    if replaceable_word == 'they':
        text = replace_all(replaceable_line, dic_T)

    return text

def generate_lyrics(story):
    # pat = ('\. +(?=[A-Z ])')
    # text = re.sub(pat, '\n', string)
    for c in string.punctuation:
        if c == "\'":
            continue
        story = story.replace(c, "\n")

    print ""
    print ""
    print "##### STORY #####"
    print ""
    print story
    print ""
    print "#################"
    print 

    text_file = open('story.txt', 'w') 
    text_file.write(story)
    text_file.close()

    with open ("story.txt") as f:
        lines = f.readlines()
        line_no = 0
        rhyme_lines = []
        for line in lines:
            print line
            rhyme_line = get_rhyme(line)
            print rhyme_line
            connected_line = connect_sentences(line, rhyme_line)
            print connected_line
            rhyme_lines.insert(line_no, connected_line)
            line_no += 1

    print "#### LYRICS ####"
    print ""

    for i, v in enumerate(rhyme_lines):
        lines.insert(2*i+1, v)
    for i,j in enumerate(lines):
        j = j.replace(j.split()[0], j.split()[0].title())
        print j.strip("\n")
        if (i in [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63, 67, 71, 75, 79, 83, 87]):
            print ''
        else:
            pass
    print "################"

story = "The lady wanted him from the start. The lady hid her love for the priest. But she fell in love with him. The princess was in love with the priest."
generate_lyrics(story)
