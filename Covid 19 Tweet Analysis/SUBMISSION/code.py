#!/usr/bin/env python
# coding: utf-8

# # Extract rows from file

# In[60]:


import csv
rows = []

with open('raw_data1.csv') as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        rows.append(row)

rows = rows[1:]


# # Extract domain names from url

# In[61]:


import tldextract
tweets_src = []
srcs = []

for r in range(len(rows)):
    cur = rows[r]
    for i in range(-2,-5,-1):
        src = cur[i]
        if (src!=''):
            ext = tldextract.extract(src)
            domain = ext.domain
            if (domain=='t'):
                domain = 'telegram'
            if domain == 'tn':
                domain = 'stopcorona'
            print(domain)
            if (domain!=''):
                srcs.append(domain)
            if (domain=='twitter'):
                tweets_src.append([r, src])


# In[62]:


print(len(srcs))
print(len(tweets_src))


# # Store source names and their count in dictionary

# In[63]:


src_dict = {}

for s in srcs:
    if (s in src_dict):
        src_dict[s] += 1
    else:
        src_dict[s] = 1

import operator
sorted_dict = sorted(src_dict.items(), key=operator.itemgetter(1), reverse=True)
src_names = []
src_values = []
for s in sorted_dict:
    src_names.append(s[0])
    src_values.append(s[1])
print(src_names)
print(src_values)


# # Bar Graph of Sources

# In[64]:


import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

y_pos = np.arange(20)

plt.barh(y_pos, src_values[:20], align='center', alpha=0.5)
plt.yticks(y_pos, src_names[:20])
plt.xlabel('Frequency')
plt.title('Sources Frequency')

plt.show()


# # Tweepy Authentication

# In[65]:


import tweepy

auth = tweepy.OAuthHandler('6qy9kQiAvBz4HwIPrxfmV56wt',
                           'hTJOPSVfb99XDpa90tV8LbUrJ7a3E4gODHl5wXTEWDdzCwTbvf')

auth.set_access_token('2283540210-cwjhz5RnkER9m7yzKX3JEY1e8Xz5lKuammfoYjM',
                      'bsuKRgWewyUnegDk4f4fi68wBznD1uRPDIMMg4lg3FdUw')

api = tweepy.API(auth)
if (not api):
    print("Authentication failed :(")
else:
    print("Authentication successfull!")


# # Extract Tweets (Do not run this, all tweets already stored)

# In[66]:


# tweets = []
# count = 0
# for t in tweets_src:
#     count+=1
#     t_id = t[1].split('/')[-1].split('?')[0]
#     try:
#         cur_tweet = api.get_status(int(t_id))
#         tweets.append([t[0], cur_tweet])
#         print(count)
#     except:
#         print(t[1])


# # Store tweets in pickle file (Do not run)

# In[67]:


# import pickle
# with open('tweets.txt', 'wb') as fp:
#     pickle.dump(tweets, fp)


# # Extract tweets from pickle file

# In[68]:


import pickle
tweets = []
with open('tweets.txt', 'rb') as fp:
    tweets = pickle.load(fp)


# In[69]:


print(len(tweets))


# # Latest 10 Tweets

# In[70]:


sorted_tweets = []
for i in range (len(tweets)) :
    sorted_tweets.append([tweets[i][1].created_at,tweets[i][1].text])
sorted_tweets.sort(reverse = True)

for i in range(10):
    print (i+1,sorted_tweets[i][1])


# # Extracting full tweets using unique id's (do not run, already extracted)

# In[71]:


# dict = {}
# count = 1
# for t in tweets:
    
#     id = t[1].id
#     tweet = None
    
#     if(id not in dict):
#         tweet = api.get_status(t[1].id,tweet_mode='extended')
#         dict[id] = tweet
#     else:
#         tweet = dict[id]
#     count+=1

# print(count)


# # Pickle files for storing

# In[72]:


# import pickle
# with open('tweets_fullText.txt', 'wb') as fp:
#     pickle.dump(dict, fp)


# In[73]:


import pickle
dict = {}
with open('tweets_fullText.txt', 'rb') as fp:
    dict = pickle.load(fp)


# # Word Cloud from tweets

# In[74]:


from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Here tt is the ditionary Aarish gave earlier


# Reference - https://github.com/precog-iiitd/social-computing-18/blob/master/Lab%201B%20--%20Building%20basic%20graphs%20from%20the%20data.ipynb
def make_word_cloud(tweet_text, stopwords):        
    ball_mask = np.array(Image.open('cloud_background.jpg'))

    # Generate a word cloud image
    wordcloud = WordCloud(background_color="white", mask=ball_mask, stopwords=stopwords).generate(tweet_text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.show()

tweet_text = ''
ppp = 0
for tweet in tweets:
    tweet_id = tweet[1].id
    
    try :
        tweet_text += dict[tweet_id].full_text + " "
    except :
        pass
stopwords = set(STOPWORDS)
stopwords.add('https')
stopwords.add('BCwn8xx039RT')

make_word_cloud(tweet_text, stopwords)


# # Count verified and non-verified profiles

# In[75]:


verified = 0
non_verified = 0
for t in tweets:
    case = t[0]
    tweet = t[1]
    screen_name = tweet.user.screen_name
    name = tweet.user.name
    if(tweet.user.verified):
        verified+=1
    else:
        non_verified+=1

print(verified)
print(non_verified)


# # Credibility Score for non-verified sources

# In[76]:


ratio = []
posts = []
description = []
age = []

from datetime import datetime
from datetime import date
today = datetime.today()
date = datetime(2020,1,30)

for t in tweets:
    
    tweet = t[1]
    if(not tweet.user.verified):
        
        user = tweet.user
        
        if(user.statuses_count>200):
            posts.append(1)
        else:
            posts.append(0)
        
        if(user.followers_count / user.friends_count > 20):
            ratio.append(1)
        else:
            ratio.append(0)
        
        if(user.description is not None and user.description!=""):
            description.append(1)
        else:
            description.append(0)
            
        days = (date-user.created_at).days
        
        if(days>=30):
            age.append(1)
        else:
            age.append(0)
    


# In[77]:


c=0
c3=0
c4=0
c2=0
c1=0
users_4 = []
users_3 = []
users_1 = []
users_2 = []
for t in range(len(tweets)):
    if(not tweets[t][1].user.verified):
        score = posts[c]+description[c]+age[c]+ratio[c]
        c+=1
        if(score==4):
            users_4.append(tweets[t][1].user.screen_name)
            c4+=1
        if(score==3):
            users_3.append(tweets[t][1].user.screen_name)
            c3+=1
        if(score==2):
            users_2.append(tweets[t][1].user.screen_name)
            c2+=1
        if(score==1):
            users_1.append(tweets[t][1].user.screen_name)
            c1+=1
        


# In[78]:


print(c4,c3,c2,c1)
print()
print(users_4)
print()
print(users_3)
print()
print(users_2)
print()
print(users_1)


# # Loading the pre-trained text matching model

# In[79]:


import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()


# # Extracting locations from text using NER Spacy

# In[80]:


locs = {}
for t in tweets:
    id = t[1].id
    case = t[0]
    locs[case] = []
    if(id in dict):
        doc = nlp(dict[id].full_text)
        for ent in doc.ents:
            text = ent.text
            label = ent.label_
            if(label=="GPE" or label=="ORG" or label=="NORP" or label=="LOC"):
                locs[case].append(text)
        
print(len(locs))


# # Matching text using NER Spacy 

# In[81]:


pii = {}
for t in tweets:
    id = t[1].id
    case = t[0]
    pii[case] = []
    if(id in dict):
        doc = nlp(dict[id].full_text)
        for ent in doc.ents:
            text = ent.text
            label = ent.label_
            pii[case].append((text,label))


# # Person Names

# In[82]:


temp = []
for t in tweets:
    id = t[1].id
    if (id in dict):
        case = t[0]
        temp = []
        for match in pii[case]:
            if(match[1]=="PERSON"):
                temp.append(match)
        print(temp)
        print(dict[id].full_text)
        print()


# # Nationality matching Information

# In[83]:


temp = []
for t in tweets:
    id = t[1].id
    if(id in dict):
        case = t[0]
        temp = []
        for match in pii[case]:
            if(match[1]=="NORP"):
                temp.append(match)
        if(len(temp)>0):
            print(temp)
            print(dict[id].full_text)
            print()


# # Location Information

# In[84]:


temp = []
for t in tweets:
    id = t[1].id
    case = t[0]
    temp = []
    for match in pii[case]:
        if(match[1]=="GPE"):
            temp.append(match)
    if(len(temp)==1):
        print(temp)
        print(dict[id].full_text)
        print()


# # Travel History

# In[85]:


import re

# here tt is the dictionary which aarish gave containing the full text of tweets

for tweet in tweets :
	try :
		tweet_text = dict[tweet[1].id].full_text
		a = re.findall(r"(\btravel history to [a-zA-Z]*\b)|(\btravel history to the [a-zA-Z]*\b)|(\breturned from [#a-zA-Z]*\b)|(\bvisited [#a-zA-Z]*\b)",tweet_text)
		if (len(a) > 0) :
			print (tweet_text)
			print ()
	except :
		pass


# # Age Information

# In[86]:


for tweet in tweets :
	try :
		tweet_text = dict[tweet[1].id].full_text
		a = re.findall(r"(\b\d*-year-old\b)|(\b\d*-yr-old\b)|(\b\d*-year old\b)|(\b\d* year old\b)|(\b\d*-yr old\b)|(\b\d* yr old\b)",tweet_text)
		if (len(a) > 0) :
			print (tweet_text)
			print ()
	except :
		pass


# # Gender Information

# In[87]:


for tweet in tweets :
	try :
		tweet_text = dict[tweet[1].id].full_text
		a = re.findall(r"(\bman\b)|(\bwoman\b)|(\bboy\b)|(\bgirl\b)|(\bfemale\b)|(\bmale\b)|(\bson\b)|(\bdaughter\b)|(\bmother\b)|(\bfather\b)",tweet_text)
		if (len(a) > 0) :
			print (tweet_text)
			print ()
	except :
		pass


# # Location Matching with dataset columns

# In[88]:


#6,7,8,11
count_1=0
count_4=0
count = 0
for row in rows:
    check1=False
    check2=False
    if(count in locs):
        s1 = row[6].lower()
        s2 = row[7].lower()
        s3 = row[8].lower()
        a = [s1,s2,s3]
        b=[]
        s4 = row[11].split(" ")
        s5 = row[-1].split(" ")
        
        for i in range(len(s4)):
            s4[i] = s4[i].lower()
            b.append(s4[i])
        for i in range(len(s5)):
            s5[i] = s5[i].lower()
            b.append(s5[i])
            
        locations = locs[count]
        if(len(locations)>0):
            for i in range(len(locations)):
                locations[i]= locations[i].lower()
        
        for loc1 in locations:
            for loc2 in a:
                if(loc1==loc2):
                    count_1+=1
                    check1=True
                    break
            if(check1):
                break
        
        for loc1 in locations:
            for loc2 in b:
                if(loc1==loc2):
                    count_4+=1
                    check2=True
                    break
            if(check2):
                break
    
    count+=1
print(count_1,count_4)


# # Tweets having locations

# In[89]:


count_2 = len(locs)
count_3 = 0
for case in locs:
    if(len(locs[case])>0):
        count_3+=1
print(count_2,count_3)


# # Required Percentage

# In[90]:


print(count_1/count_3)
print(count_4/count_3)


# # Profile with most COVID19 Posts

# In[91]:


user_dic = {}
max_user = None
max_count = 0

for t in tweets:
    cur_user = t[1].user.name
    if (cur_user in user_dic):
        user_dic[cur_user] += 1
    else:
        user_dic[cur_user] = 1
    if (user_dic[cur_user] > max_count):
        max_count = user_dic[cur_user]
        max_user = t[1].user

print(max_user.screen_name)
print(max_user.verified)
print(max_count)

