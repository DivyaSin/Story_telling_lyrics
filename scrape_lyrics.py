#import urllib2
#from bs4 import BeautifulSoup
#import re
#html = urllib2.urlopen("http://www.azlyrics.com/")
#content = html.read()
#bsObj = BeautifulSoup(content, "lxml")
#for link in bsObj.find_all("div", attrs={'class':'btn-group text-center'}):
#    print link.find('a')['href']
with open("new_lyrics copy.txt") as f:
    with open("new_lyrics.txt", 'w') as g:
        lines = f.readlines()
        for line in lines:
            words = line.split()
            print line
            sentence_rev = " ".join(reversed(words))
            print sentence_rev
            g.writelines(sentence_rev+'\n')
f.close()
g.close()
