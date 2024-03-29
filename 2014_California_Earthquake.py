
# Importing Libraries 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
import warnings 
warnings.filterwarnings("ignore", category=DeprecationWarning)

from google.colab import files
uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(name=fn, length=len(uploaded[fn])))

import pandas as pd
import io
df = pd.read_csv(io.StringIO(uploaded['2014_California_Earthquake.csv'].decode("ISO-8859-1")),skipinitialspace=True)
print(df)
df.head()
df['tweet_time']

df.describe()

for col in df.columns: 
    print(col)

!git clone https://github.com/imgarylai/bert-embedding.git

!pip install bert-embedding

df['tweet_text']

# Importing HTMLParser
from html.parser import HTMLParser
html_parser = HTMLParser()

# Created a new columns i.e. clean_tweet contains the same tweets but cleaned version
df['clean_tweet'] = df['tweet_text'].apply(lambda x: html_parser.unescape(x))
df.head(10)

df= df.drop(['tweet_lon','tweet_lat'], axis=1)

df.head()

##Removing @user
import re
import numpy as np

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt

# remove twitter handles (@user)
df['clean_tweet'] = np.vectorize(remove_pattern)(df['clean_tweet'], "@[\w]*")
df.head(10)

#all characters to lowercase

df['clean_tweet'] = df['clean_tweet'].apply(lambda x: x.lower())
df.head(10)

#Short Word Lookup

short_word_dict = {
"121": "one to one",
"a/s/l": "age, sex, location",
"adn": "any day now",
"afaik": "as far as I know",
"afk": "away from keyboard",
"aight": "alright",
"alol": "actually laughing out loud",
"b4": "before",
"b4n": "bye for now",
"bak": "back at the keyboard",
"bf": "boyfriend",
"bff": "best friends forever",
"bfn": "bye for now",
"bg": "big grin",
"bta": "but then again",
"btw": "by the way",
"cid": "crying in disgrace",
"cnp": "continued in my next post",
"cp": "chat post",
"cu": "see you",
"cul": "see you later",
"cul8r": "see you later",
"cya": "bye",
"cyo": "see you online",
"dbau": "doing business as usual",
"fud": "fear, uncertainty, and doubt",
"fwiw": "for what it's worth",
"fyi": "for your information",
"g": "grin",
"g2g": "got to go",
"ga": "go ahead",
"gal": "get a life",
"gf": "girlfriend",
"gfn": "gone for now",
"gmbo": "giggling my butt off",
"gmta": "great minds think alike",
"h8": "hate",
"hagn": "have a good night",
"hdop": "help delete online predators",
"hhis": "hanging head in shame",
"iac": "in any case",
"ianal": "I am not a lawyer",
"ic": "I see",
"idk": "I don't know",
"imao": "in my arrogant opinion",
"imnsho": "in my not so humble opinion",
"imo": "in my opinion",
"iow": "in other words",
"ipn": "I’m posting naked",
"irl": "in real life",
"jk": "just kidding",
"l8r": "later",
"ld": "later, dude",
"ldr": "long distance relationship",
"llta": "lots and lots of thunderous applause",
"lmao": "laugh my ass off",
"lmirl": "let's meet in real life",
"lol": "laugh out loud",
"ltr": "longterm relationship",
"lulab": "love you like a brother",
"lulas": "love you like a sister",
"luv": "love",
"m/f": "male or female",
"m8": "mate",
"milf": "mother I would like to fuck",
"oll": "online love",
"omg": "oh my god",
"otoh": "on the other hand",
"pir": "parent in room",
"ppl": "people",
"r": "are",
"rofl": "roll on the floor laughing",
"rpg": "role playing games",
"ru": "are you",
"shid": "slaps head in disgust",
"somy": "sick of me yet",
"sot": "short of time",
"thanx": "thanks",
"thx": "thanks",
"ttyl": "talk to you later",
"u": "you",
"ur": "you are",
"uw": "you’re welcome",
"wb": "welcome back",
"wfm": "works for me",
"wibni": "wouldn't it be nice if",
"wtf": "what the fuck",
"wtg": "way to go",
"wtgp": "want to go private",
"ym": "young man",
"gr8": "great"
}

def lookup_dict(text, dictionary):
    for word in text.split():
        if word.lower() in dictionary:
            if word.lower() in text.split():
                text = text.replace(word, dictionary[word.lower()])
    return text
  
  
df['clean_tweet'] = df['clean_tweet'].apply(lambda x: lookup_dict(x,short_word_dict))
df.head(10)

# Apostrophe Dictionary
apostrophe_dict = {
"ain't": "am not / are not",
"aren't": "are not / am not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had / he would",
"he'd've": "he would have",
"he'll": "he shall / he will",
"he'll've": "he shall have / he will have",
"he's": "he has / he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how has / how is",
"i'd": "I had / I would",
"i'd've": "I would have",
"i'll": "I shall / I will",
"i'll've": "I shall have / I will have",
"i'm": "I am",
"i've": "I have",
"isn't": "is not",
"it'd": "it had / it would",
"it'd've": "it would have",
"it'll": "it shall / it will",
"it'll've": "it shall have / it will have",
"it's": "it has / it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had / she would",
"she'd've": "she would have",
"she'll": "she shall / she will",
"she'll've": "she shall have / she will have",
"she's": "she has / she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as / so is",
"that'd": "that would / that had",
"that'd've": "that would have",
"that's": "that has / that is",
"there'd": "there had / there would",
"there'd've": "there would have",
"there's": "there has / there is",
"they'd": "they had / they would",
"they'd've": "they would have",
"they'll": "they shall / they will",
"they'll've": "they shall have / they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we had / we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what shall / what will",
"what'll've": "what shall have / what will have",
"what're": "what are",
"what's": "what has / what is",
"what've": "what have",
"when's": "when has / when is",
"when've": "when have",
"where'd": "where did",
"where's": "where has / where is",
"where've": "where have",
"who'll": "who shall / who will",
"who'll've": "who shall have / who will have",
"who's": "who has / who is",
"who've": "who have",
"why's": "why has / why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you had / you would",
"you'd've": "you would have",
"you'll": "you shall / you will",
"you'll've": "you shall have / you will have",
"you're": "you are",
"you've": "you have"
}

df['clean_tweet'] = df['clean_tweet'].apply(lambda x: lookup_dict(x,apostrophe_dict))
df.head(10)

#Emoticon 


emoticon_dict = {
":)": "happy",
":‑)": "happy",
":-]": "happy",
":-3": "happy",
":->": "happy",
"8-)": "happy",
":-}": "happy",
":o)": "happy",
":c)": "happy",
":^)": "happy",
"=]": "happy",
"=)": "happy",
"<3": "happy",
":-(": "sad",
":(": "sad",
":c": "sad",
":<": "sad",
":[": "sad",
">:[": "sad",
":{": "sad",
">:(": "sad",
":-c": "sad",
":-< ": "sad",
":-[": "sad",
":-||": "sad"
}

df['clean_tweet'] = df['clean_tweet'].apply(lambda x: lookup_dict(x,emoticon_dict))
df.head(10)

#ReplacingPunctuations with space



df['clean_tweet'] = df['clean_tweet'].apply(lambda x: re.sub(r'[^\w\s]',' ',x))
df.head(10)

#Replacing Special Characters with space

df['clean_tweet'] = df['clean_tweet'].apply(lambda x: re.sub(r'[^a-zA-Z0-9]',' ',x))
df.head(10)

#Replacing Numbers (integers) with space

df['clean_tweet'] = df['clean_tweet'].apply(lambda x: re.sub(r'[^a-zA-Z]',' ',x))
df.head(10)

#Removing words whom length is 1

df['clean_tweet'] = df['clean_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>1]))
df.head(10)

df['clean_tweet'] = df['clean_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>2]))
df.head(10)

!pip install nltk

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
stopwords

stop_words = set(stopwords.words('english'))
stop_words.add('http')
stop_words.add('https')
stop_words.add('are')
stop_words.add('were')

stop_words.add('has')
stop_words.add('had')
stop_words.add('is')
stop_words.add('you')
stop_words.add('was')
stop_words.add('wa')
stop_words.add('may')
stop_words.add('shall')
stop_words.add('could')
stop_words.add('what')
stop_words.add('could')
stop_words.add('where')
stop_words.add('how')
stop_words.add('which')
stop_words.add("what's")

stop_words

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

# Creating token for the clean tweets
df['tweet_token'] = df['clean_tweet'].apply(lambda x: word_tokenize(x))

## Fully formated tweets & there tokens
df.head(10)

# Created new columns of tokens - where stop words are being removed
df['tweet_token_filtered'] = df['tweet_token'].apply(lambda x: [word for word in x if not word in stop_words])

## Tokens columns with stop words and without stop words
df[['tweet_token', 'tweet_token_filtered']].head(10)

import nltk
nltk.download('words')
words = set(nltk.corpus.words.words())

# Created new columns of tokens - where stop words are being removed
df['tweet_token_filtered'] = df['tweet_token_filtered'].apply(lambda x: [word for word in x if word in words])

## Tokens columns with stop words and without stop words
df[['tweet_token', 'tweet_token_filtered']].head(10)

# Importing library for lemmatizing
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizing = WordNetLemmatizer()

import nltk
nltk.download('wordnet')
# Created one more columns tweet_lemmatized it shows tweets' lemmatized version
df['tweet_lemmatized'] = df['tweet_token_filtered'].apply(lambda x: ' '.join([lemmatizing.lemmatize(i) for i in x]))
df[['clean_tweet','tweet_lemmatized']].head(10)

df.head(10)

# f = lambda x: len(x["tweet_lemmatized"].split("\n")) 
# df["\n"] = df.apply(f, axis=1)

# s= pd.Series(df['tweet_lemmatized'])

# res=s.str.split('\n')

df['tweet_lemmatized']

len(df['tweet_lemmatized'])

df1 = pd.DataFrame(df['tweet_lemmatized'])
msk = np.random.rand(len(df1)) < 0.8
train = df1[msk]
test = df1[~msk]

# length=len(test['tweet_lemmatized'])
# type(test['tweet_lemmatized'][0])


# test['tweet_lemmatized'][7]
# df2= (test['tweet_lemmatized'].to_string(index= False))
r= train['tweet_lemmatized'].tolist()

len(r)

r

final = '.'.join(map(str, r))

len(final)

# final= ' '.join(r)

final

len(final)

#to get unique words

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

final=' '.join(unique_list(final.split()))

len(final)

from bert_embedding import BertEmbedding


sentences = final.split('.')
bert_embedding = BertEmbedding()
result = bert_embedding(sentences)

len(result)

result

n=[]
for i in range(len(result)):
  l= result[i]
  n.append(l[0])

flat1=[]
import itertools
flat1=itertools.chain.from_iterable(n)
flat1=list(flat1)
flat1

len(flat1)

m=[]
for i in range(len(result)):
  l= result[i]
  m.append(l[1])

flat2=[]
import itertools
flat2=itertools.chain.from_iterable(m)
flat2=list(flat2)



dict2={}
dict2=dict(zip(flat1,flat2))

len(dict2)

l1= list(dict2.keys())
l2= list(dict2.values())

!pip install kmodes

import numpy as np
from kmodes.kmodes import KModes

# random categorical data
data = np.array(l2)

km = KModes(n_clusters=5, init='Huang', n_init=1, verbose=1)

clusters = km.fit_predict(data)

# Print the cluster centroids
clust= km.cluster_centroids_

clust

len(clust)

#getting the centroids

f1= l1
f2= l2

answer1=[]
answer2=[]
new2= l2
new1= list(clust)
for i in range(len(new1)):
  n1= new1[i]
  for j in range(len(new2)):
    n2= new2[j]
    if(n1[0]==n2[0]):
      ans=j
      break
  answer1.append(f1[ans])
  #answer2.append(f2[ans])

len(answer1)

from google.colab import files
uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(name=fn, length=len(uploaded[fn])))

import pandas as pd
import io
df1 = pd.read_csv(io.StringIO(uploaded['2014_California_Earthquake.csv'].decode("ISO-8859-1")),skipinitialspace=True)
print(df1)
df1.head()

from google.colab import files

uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(name=fn, length=len(uploaded[fn])))

import pandas as pd
import io
df2 = pd.read_csv(io.StringIO(uploaded['2014_california_eq.csv'].decode("ISO-8859-1")),skipinitialspace=True)
print(df2)
df2.head()

affected_individuals={}
Donations_and_volunteering={}
Infrastructure_and_utilies={}
Not_related_or_relevant={}
Sympathy_and_Support={}
Other_useful_information={}
for i,j in zip(df1['label'],df1['tweet_text']):
    if i=='Missing, trapped, or found people' or i=='Displaced people' or i=='Injured or dead people':
        affected_individuals[j]=1
    elif i=='Volunteer or professional services' or i=='Money' or i=='Shelter and supplies':
        Donations_and_volunteering[j]=2
    elif i=='Infrastructure and utilities' or i=='Infrastructure Damage':
        Infrastructure_and_utilies[j]=3
    elif i=='Not related or irrelevant' or i=='Not relevant': 
        Not_related_or_relevant[j]=6
    elif i=='Sympathy and emotional support':
        Sympathy_and_Support[j]=4
    else:
        Other_useful_information[j]=5

affected_individuals={}
Donations_and_volunteering={}
Infrastructure_and_utilies={}
Not_related_or_relevant={}
Sympathy_and_Support={}
Other_useful_information={}
for i,j in zip(df2['choose_one_category'],df2['tweet_text']):
    if i=='displaced_people_and_evacuations' or i=='injured_or_dead_people' or i=='missing_trapped_or_found_people' :
        affected_individuals[j]=1
    elif i=='donation_needs_or_offers_or_volunteering_services':
        Donations_and_volunteering[j]=2
    elif i=='infrastructure_and_utilities_damage':
        Infrastructure_and_utilies[j]=3
    elif i=='not_related_or_irrelevant': 
        Not_related_or_relevant[j]=6
    elif i=='sympathy_and_emotional_support':
        Sympathy_and_Support[j]=4
    else:
        Other_useful_information[j]=5

print(len(Not_related_or_relevant))

frames=[affected_individuals,Donations_and_volunteering,Infrastructure_and_utilies,Not_related_or_relevant,Sympathy_and_Support,Other_useful_information]
dall = {}
dall.update(affected_individuals)
dall.update(Donations_and_volunteering)
dall.update(Infrastructure_and_utilies)
dall.update(Not_related_or_relevant)
dall.update(Sympathy_and_Support)
dall.update(Other_useful_information)

import numpy as np
X= list(dall.keys())
y= list(dall.values())
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=0,test_size=0.2)

import sys
import string 
import json 
from collections import Counter 
from nltk.tokenize import TweetTokenizer 
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
wnl = WordNetLemmatizer()
from sklearn.metrics import confusion_matrix
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn import svm
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.feature_extraction import text 

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm


from sklearn import metrics

def process(text, tokenizer=TweetTokenizer(), stopwords=[]): 
  """Process the text of a tweet: 
  - Lowercase 
  - Tokenize 
  - Stopword removal 
  - Digits removal 
 
  Return: list of strings 
  """ 
  
  text = text.lower()
  tokens = tokenizer.tokenize(text)
  return [tok for tok in tokens if tok not in stopwords and not any(i.isdigit() for i in tok)  and len(tok)>2 and tok is tok.strip('#') and tok is tok.strip('@')  and tok not in (tok for tok in tokens if re.search('http', tok)) ]

my_additional_stop_words=['amp','https','ud83d','nhttps','rieti','u2026','rt','http','37','10','38','di','24','36','...','the']
stop_words = text.ENGLISH_STOP_WORDS.union(my_additional_stop_words)

CHI= answer1


vectorizer=CountVectorizer(tokenizer=process,min_df=1,ngram_range=(1,1),stop_words=stop_words,vocabulary=CHI)
#vectorizer1=CountVectorizer(tokenizer=process,min_df=1,ngram_range=(1,1),stop_words=stop_words,vocabulary=CHI)
#X2=vectorizer1.fit_transform(X_train)
X1 = vectorizer.fit_transform(X_train)
#print vectorizer.get_feature_names()
X1 = X1.toarray()
#X2=X2.toarray()
X_test1 = vectorizer.transform(X_test)
#X_test2=vectorizer1.transform(X_test)
X_test1=X_test1.toarray()
#X_test2=X_test2.toarray()
#from sklearn.naive_bayes import MultinomialNB
#clf1=MultinomialNB()
#from sklearn.neighbors import KNeighborsClassifier
#clf1 = KNeighborsClassifier(n_neighbors=5)
#clf1 =SVC(kernel="rbf",probability=True)


#clf1=SVC(kernel="rbf")
#clf1 = RandomForestClassifier(n_estimators=100, max_depth=2,random_state=0)
#clf1 = LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial')
clf1 = svm.SVC(gamma='scale')

#from sklearn.tree import DecisionTreeClassifier
#clf1 = DecisionTreeClassifier(random_state=0)
clf1.fit(X1, y_train)
#clf2.fit(X1, y_train)
y_pred_class=clf1.predict(X_test1)
#y_pred_class=clf1.predict_proba(X1)
#y_pred_class1=clf2.predict(X_test1)
#y_pred_class1=clf1.predict_proba(X_test1)

#clf3 =SVC(kernel="rbf",probability=True)
#clf4=SVC(kernel="rbf")
#from sklearn.tree import DecisionTreeClassifier%time clf3.fit(X2, y_train)
#clf4.fit(X2, y_train)
#y_pred_class=clf1.predict(X1)
#y_pred_class2=clf3.predict_proba(X2)
#y_pred_class3=clf4.predict(X2)
print(metrics.accuracy_score(y_test,y_pred_class))
print(metrics.classification_report(y_test, y_pred_class))

confusion_matrix = metrics.confusion_matrix(y_test, y_pred_class)
print(confusion_matrix)






















