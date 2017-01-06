# import unirest, json
# import re
# import words
# from itertools import groupby
# import json
import pprint

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
          val_array = [val for sublist in val_array for val in sublist]
          action_dictionary[new_key] = val_array
          action_dictionary.update(action_dictionary)
    if line == "END":
      break
pprint.pprint(actions_list)

    

# string = "A Child was standing on a street. He leaned with one shoulder. He swayed the other to and fro. He stood dreamily gazing"
# pat = ('\. +(?=[A-Z ])')
# text = re.sub(pat, '\n', string)
# print text

# text_file = open('story.txt', 'w')  
# text_file.write(text)
# text_file.close()




# client = words.Words("MPPiWZYJAhmshW2madDJsYEkXdClp1WdjRtjsniiWtmhiaLSDR")

# print 

# with open ("story.txt") as f:
#   lines = f.readlines()
#   close_sentences = []
  # count = 0
  # line_no = 0
  # count_index = []
  # for line in lines:
  #   print line
  #   response = unirest.get("https://twinword-sentiment-analysis.p.mashape.com/analyze/?text=" + line,
  #   headers={
  #   "X-Mashape-Key": "MPPiWZYJAhmshW2madDJsYEkXdClp1WdjRtjsniiWtmhiaLSDR",
  #   "Accept": "application/json"
  #     }
  #       )
  #   t = response.body
  #   keywords = t['keywords']
  #   score = 0
  #   for keyword in keywords:
  #     score = score + keyword['score']
  #     close_sentences.append((score, line))
  # print close_sentences
    # print score['score']
#       words = line.split()
#       for word in words:
#       	data = client.word(word)
#       	try:
#       		count += data['syllables']['count']
#       	except Exception as e:
#       		pass
#       count_index.insert(line_no, count)
#       line_no += 1
#       count = 0
# print count_index


      
        


