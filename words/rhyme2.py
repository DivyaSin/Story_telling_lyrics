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

rhyme_entries = nltk.corpus.cmudict.entries()
pronunciationDictionary = nltk.corpus.cmudict.dict() 

# tension_dictionary = {}
# tension_list = []

# with open('/Users/divyasingh/Desktop/Story_telling_lyrics/words/corpus/ce_eg5.txt') as tension_file:
#     flag = True
#     same_value = True
#     val = []
#     for line in tension_file: 
#         if not line.strip():
#             if not tension_dictionary[key]:
#                 tension_dictionary[key] = []              
#             else:
#                 tension_dictionary.update(tension_dictionary)
#             same_value = True
#         else:        
#             if same_value:
#                 key = line.strip()
#                 same_value = False
#                 tension_dictionary[key] = []
#             else:
#                 val = re.split("[ :,()\n ]", line.strip(" "))
#                 val = list(filter(None, val))
#                 if tension_dictionary[key]:
#                     tension_dictionary[key].append(val)
#                 else:
#                     tension_dictionary[key] = [val]

# action_keys = ['ACT', 'PRE', 'POS', 'TEN', 'TEXT']
# action_dictionary = {}
# actions_list = []

# with open("actions.txt") as actions_file: 
#   for line in actions_file:
#     if line.strip() in action_keys:
#         new_key = line.strip()
#         action_dictionary[new_key] = []
#     else:
#       if not line.strip():
#         l = action_dictionary["TEXT"]
#         l = [val for sublist in l for val in sublist]
#         action_dictionary["TEXT"] = l
#         actions_list.append(action_dictionary)
#         action_dictionary = {'ACT':[], 'PRE':[], 'POS':[], 'TEN':[], 'TEXT':[]}
#         continue
#       else:
#         if new_key in ['PRE', 'POS', 'TEN']:
#           val = line.strip().split(" ")
#         else:
#           val = line.strip().split(". ")
#         if new_key == "TEXT":
#           if action_dictionary[new_key]:
#             action_dictionary[new_key].append(val)
#           else:
#             val = [val]
#             action_dictionary[new_key] = val
#         else:
#           val_array=[val]
#           if action_dictionary[new_key]:
#             for array in action_dictionary[new_key]:
#               val_array.append(array)
#           val_array.reverse()
#           action_dictionary[new_key] = val_array
#           action_dictionary.update(action_dictionary)
#     if line == "END":
#       break

def last_word(sentence):
    ss = [ word for word in sentence if len(word) > 1 ]
    if len(ss) > 0:
        return ss[-1]
    else:
        return "" 

def getMarkovBatch():
    last_word_sentences = defaultdict(list)
    markov_lyrics.markov()
    corpus_root = '/Users/divyasingh/Documents/MABLE'
    wordlists = PlaintextCorpusReader(corpus_root, '.*')
    mega_sentences = (wordlists.sents('rape_corpus.txt'))
    if mega_sentences:
        for sentence in mega_sentences:
            lw = last_word(sentence)
            last_word_sentences[ lw ].append(sentence)
        keys = last_word_sentences.keys()
    else:
        getMarkovBatch()
    # print "#############################################"
    # print "#############################################"
    # print keys, last_word_sentences
    return keys, last_word_sentences

def candidate_sentences(word):
    candidates = []
    word_pronunciation = pronunciationDictionary[word.lower()]
    word_pro = word_pronunciation[0]
    keys, last_word_sentences = getMarkovBatch()
    for key in keys:
        try:
            key_pronunciation = pronunciationDictionary[key]
            key_pro = key_pronunciation[0]
        except KeyError:
            continue
        rhyme_quality = quality_of_rhyme(word_pro, key_pro)
        candidates.append( (rhyme_quality, key) )
    candidates.sort()
    candidates.reverse()
    words = [ key for rhyme_quality, key in candidates if rhyme_quality >= 1 ]
    if words:
        good_word = random.choice(words)
        return last_word_sentences[good_word.lower()]  
    else:
        return ''

def quality_of_rhyme(p1, p2):
    p1 = copy.deepcopy(p1)
    p2 = copy.deepcopy(p2)
    p1.reverse()
    p2.reverse()
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
    return quality
    
def find_high_priority(candidates, word):
    p2 = list(copy.deepcopy(word))
    p2.reverse()
    new_candidates = []
    for candidate in candidates:
        p1 = list(copy.deepcopy(candidate))
        p1.reverse()
        if p1 == p2:
            return 0
        quality = 0
        sameVowelFound = False
        for i, p in enumerate(p1):
            try:
                if p == p2[i]:
                    quality += 1
                    if p not in ('a', 'e', 'i', 'o', 'u'):
                        quality -= 1
                    if p in ('a', 'e', 'i', 'o', 'u') and (not sameVowelFound):
                        quality += 1
                        sameVowelFound = True
                else:
                    break  
            except IndexError:
                break
        if quality > 0:
            new_candidates.append( (quality, candidate) )
    new_candidates.sort()
    new_candidates.reverse()
    new_candidates = [ candidate for quality, candidate in new_candidates ]
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
            if rhyme_word[-1].isdigit():
                continue
            quality = quality_of_rhyme(pronunciation, rhyme_pronunciation)
            if quality > 0:
                candidates.append( (quality, rhyme_word) )
    candidates.sort()
    candidates.reverse()
    candidates = [ candidate for q, candidate in candidates ]
    top_candidates = candidates[:50]
    high_priority_candidates = find_high_priority(candidates, word)
    if not high_priority_candidates:
        return candidates
    else:
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
        if not sentiment_dictionary.get('PRE'):
            story_score = 0
            return story_score
        else:
            story_score = get_pre_score(sentiment_dictionary)
            return story_score
    else:
        story_score = get_pos_score(sentiment_dictionary)
        if story_score == 0:
            story_score = get_pre_score(sentiment_dictionary)
        return story_score

def get_sentiment_dictionary(pattern, actions_list):
    max_similarity_score = 0
    sentiment_dictionary = []
    for dictionary in actions_list:
        for string in dictionary["TEXT"]:
            similarity_score = fuzz.partial_ratio(pattern, string)
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
        score = t['score']
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
    return closest_sentences

def get_rhyme(sentence):
    pattern = sentence
    target_syllables = syllables.sentence_syllables(sentence)
    tokens = nltk.word_tokenize(sentence)
    rhymes = word_rhyme_candidates(last_word(tokens))
    candidate_sentence = []
    for rhyme in rhymes:
        candidate_sentence += candidate_sentences(rhyme)
    syllable_sentences = []
    for sentence in candidate_sentence:
        sumOfSyllables = sum( [ syllables.syllables(word) for word in sentence ] )
        syllable_sentences.append( (sumOfSyllables, " ".join(sentence)) )
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
    close_sentences = [ sentence for n, sentence in syllable_sentences if close_number-1 <= n <= close_number] 
    close_sentences_set = set(close_sentences)
    close_sentences_list = list(close_sentences_set)
    closest_sentences = get_corpus_score(close_sentences_list)
    # story_score = get_sentiment_value(pattern, tension_dictionary)
    story_score = get_corpus_score(pattern)
    rhyme_sentences = []
    if story_score > 0:
        rhyme_sentences = [ sentence for score, sentence in closest_sentences if score == story_score] 
        rhyme_sentences.sort()
    elif story_score < 0:
        rhyme_sentences = [ sentence for score, sentence in closest_sentences if score == story_score] 
        rhyme_sentences.sort()
    else:
        rhyme_sentences = [ sentence for score, sentence in closest_sentences if score == 0] 
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
            if word in ['Prince', 'Eagle', 'He', 'his', 'him', 'priest', ' He']:
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

def get_new_line():
    candidates = []
    keys, last_word_sentences = getMarkovBatch()
    candidates.append(keys)
    # for sentence in last_word_sentences:
    #     sumOfSyllables = sum( [ syllables.syllables(word) for word in sentence ] )
    words = [ key for key in candidates ]
    words = [item for sublist in words for item in sublist]
    # print words
    select_random_word = random.choice(words)
    print select_random_word
    return last_word_sentences[select_random_word.lower()] 

lines = []
rhyme_lines = []


def generate_lyrics(numOfLines):
    numOfLines -= 1
    new_line = get_new_line()
    new_line =  [ item for sublist in new_line for item in sublist ]
    new_line = " ".join(new_line)
    print new_line
    lines.append(new_line)
    rhyme_line = get_rhyme(new_line)
    rhyme_lines.append(rhyme_line)
    if numOfLines!= 0:
        generate_lyrics(numOfLines)
    else:
        print_lyrics(lines, rhyme_lines)

    # for c in string.punctuation:
    #     if c == "\'":
    #         continue
    #     story = story.replace(c, "\n")

    # print ""
    # print ""
    # print "##### STORY #####"
    # print ""
    # print story
    # print ""
    # print "#################"
    # print 

    # text_file = open('story.txt', 'w') 
    # text_file.write(story)
    # text_file.close()

    # with open ("story.txt") as f:
    #     lines = f.readlines()
    #     line_no = 0
    #     rhyme_lines = []
    #     for line in lines:
    #         print line

    #         rhyme_line = get_rhyme(line)
    #         print rhyme_line
    #         # connected_line = connect_sentences(line, rhyme_line)
    #         # print connected_line
    #         rhyme_lines.insert(line_no, rhyme_line)
    #         line_no += 1



def print_lyrics(lines, rhyme_lines):
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

numOfLines = 4
generate_lyrics(numOfLines)
# generate_lyrics()
