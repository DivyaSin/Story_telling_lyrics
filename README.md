Goal: The goal is to generate lyrics based on the plot generation system. It involves integration of both cognitive and statistical models thus producing narrative-based emotional engaging lyrics with coherent plots. 

Implementation: MEXICA produces novel coherent plots of stories about the Mexicas (Gods), an indigenous people of what is today Mexico City. After generating a plot using MEXICA, MABLE utilizes a statistical model to expand the plot into lyrics. For each line in the plot, the statistical model is used to create a new, poetic phrase that, by rhyming with the original sentence and following its metric structure, leads to seamless integration of the narrative into the ballad.

Evaluation: To evaluate MABLE's artifacts, we compare them against poems and lyrics created by previous systems,
as well as human-made lyrics. 

Technologies/Languages Used: Python, Markov Model, NLTK, Markovify, CMUDict, Twinword Sentiment Analysis API, BeautifulSoup, Python Flask, jQuery/AJAX/HTML5/CSS3

Future: Working on speeding up the response time in web application. Using deep learning framework recurrent neural networks: Long Short Term Networks and keras (theano backend) to optimize algorithm and results.
