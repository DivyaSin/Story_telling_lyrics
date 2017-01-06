#from nltk.sentiment import SentimentIntensityAnalyzer
#text = "ambitious"
##you have to use _arg1 to reference the data column you're analyzing, in this case [Word]. It gets word further down after the ,
#scores = [] #this is a python list where the scores will get stored
#sid = SentimentIntensityAnalyzer() #this is a class from the nltk (Natural Language Toolkit) library. We'll pass our words through this to return the score
#for word in text: # this loops through each row in the column you pass via _arg1; in this case [Word]
#    ss = sid.polarity_scores(word) #passes the word through the sentiment analyzer to get the score
#    scores.append(ss['compound']) #appends the score to the list of scores
#print scores #returns the scores
from textblob import TextBlob

text="Artist was an ambitious person. Artist wanted power and money in an easy way. Artist kidnapped Hunter and went to Chapultepec forest. Artist's plan was to ask for an important amount of cacauatl (cacao beans) and quetzalli (quetzal) feathers. Artist wanted to liberate Hunter. Artist thoroughly observed Hunter. Then, Artist took a dagger. Jumped towards Hunter. Hunter was attacked. Artist's frame of mind was very volatile. Without thinking, Hunter was charged against. Hunter thoroughly observed Artist. Then, Hunter took a dagger. Jumped towards Artist. Artist was attacked. Hunter's frame of mind was very volatile. Without thinking, Artist was charged against. Artist felt panic. Artist ran away from Hunter to hide in the Popocateptl."

blob = TextBlob(text)
blob.tags

for sentence in blob.sentences:
    print(sentence.sentiment.polarity)
