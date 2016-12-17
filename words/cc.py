import unirest
import re
import words

string = "A Child was standing on a street. He leaned with one shoulder. He swayed the other to and fro. He stood dreamily gazing"
pat = ('\. +(?=[A-Z ])')
text = re.sub(pat, '\n', string)
print text

text_file = open('story.txt', 'w')  
text_file.write(text)
text_file.close()

client = words.Words("MPPiWZYJAhmshW2madDJsYEkXdClp1WdjRtjsniiWtmhiaLSDR")

print 

with open ("story.txt") as f:
  lines = f.readlines()
  count = 0
  line_no = 0
  count_index = []
  for line in lines:
      words = line.split()
      for word in words:
      	data = client.word(word)
      	try:
      		count += data['syllables']['count']
      	except Exception as e:
      		pass
      count_index.insert(line_no, count)
      line_no += 1
      count = 0
print count_index


      
        


