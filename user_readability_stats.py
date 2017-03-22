#!/usr/bin/env python
""" Tweet Readability Processor

Summary:
    Utility to parse and save a users most recent tweets and calculate readaibility


User options:
    username: User must enter Twitter handle of user
    tweet_file: Output text file containing all recent tweets of user
    letters: Specify characters that indicate a tweet should be ignored

    python tweet_reader.py


Twitter API Keys and Tokens:
    You must generate these using your twitter account.
    Instructions: https://python-twitter.readthedocs.io/en/latest/getting_started.html

    consumer_key = '',
    consumer_secret = '',
    access_token = '',
    access_token_secret = ''


"""
import math
import os
import re
from TwitterSearch import *
from textstat.textstat import textstat
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Display plots in GUI on Mac OS X
import matplotlib.pyplot as plt

# ~~~~ USER OPTIONS ~~~~ #

# Twitter API Credentials
# Don't know how to get these? Look no further than...
# http://stackoverflow.com/questions/1808855/getting-new-twitter-api-consumer-and-secret-keys

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Twitter handle of user you want to query
username = 'BarackObama'

# Number of top words to count
top_n_words = 20

# Character filter. Ignore tweets containing the following characters
char_ignore = set('@:#^&;/~`\|1234567890')

# ~~~~ END USER OPTIONS ~~~~ #


def loadTweets(username, consumer_key, consumer_secret, access_token, access_token_secret):
    """Use the Twitter API to load all recent tweets by the user

    :param username: Username of user we are querying
    :return: An array of tweets

    """
    try:

        # Create object based on username
        user = TwitterUserOrder(username)

        # API credentials
        ts = TwitterSearch(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
        )

        user_tweets = []
        # Load tweets into array
        for tweet in ts.search_tweets_iterable(user):
            user_tweets.append((tweet['text'] + "."))


    except TwitterSearchException as e:
        print("ERROR: Bad credentials, username, or related issue...")
        print(e)

    return user_tweets


def saveTweets(user_tweets, tweet_file):
    """ Filter tweets and save  to output text file

    Before saving tweets, we filter out any tweets containing characters in the
    char_ignore list

    :param user_tweets: Array of user's recent tweets
    :param tweet_file: textfile to save tweets to
    :return: Text file with tweets

    """
    # Check if old output text file exists, delete if it does
    try:
        os.remove(tweet_file)
    except OSError:
        pass

    # For each tweet, check if forbidden characters exist and ignore it if it contains them
    # else write the tweet to the text file
    for n in user_tweets:
        if char_ignore & set(n):
            pass
        else:
            with open(tweet_file, "a") as text_file:
                text_file.write(n.encode('utf8'))

def stop_words():
    # Ignore stop words and some extras to ignore when counting user's most used words
    filter_list = ['a', 'about', 'above', 'across', 'after', 'again', 'against', 'all', 'almost', 'alone', 'along',
                   'already', 'also', 'although', 'always', 'am', 'among', 'an', 'and', 'another', 'any', 'anybody', 'anyone',
                   'anything', 'anywhere', 'are', 'area', 'areas', 'around', 'as', 'ask', 'asked', 'asking', 'asks', 'at',
                   'away', 'b', 'back', 'backed', 'backing', 'backs', 'be', 'became', 'because', 'become', 'becomes',
                   'been', 'before', 'began', 'behind', 'being', 'beings', 'best', 'better', 'between', 'big', 'both',
                   'but', 'by', 'c', 'came', 'can', 'cannot', 'case', 'cases', 'certain', 'certainly', 'clear', 'clearly',
                   'come', 'could', 'd', 'did', 'differ', 'different', 'differently', 'do', 'does', 'done', 'down', 'down',
                   'downed', 'downing', 'downs', 'during', 'e', 'each', 'early', 'either', 'end', 'ended', 'ending', 'ends',
                   'enough', 'even', 'evenly', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'f',
                   'face', 'faces', 'fact', 'facts', 'far', 'felt', 'few', 'find', 'finds', 'first', 'for', 'four', 'from',
                   'full', 'fully', 'further', 'furthered', 'furthering', 'furthers', 'g', 'gave', 'general', 'generally',
                   'get', 'gets', 'give', 'given', 'gives', 'go', 'going', 'good', 'goods', 'got', 'great', 'greater',
                   'greatest', 'group', 'grouped', 'grouping', 'groups', 'h', 'had', 'has', 'have', 'having', 'he', 'her',
                   'here', 'herself', 'high', 'high', 'high', 'higher', 'highest', 'him', 'himself', 'his', 'how',
                   'however', 'i', 'if', 'important', 'in', 'interest', 'interested', 'interesting', 'interests', 'into',
                   'is', 'it', 'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kind', 'knew', 'know', 'known', 'knows',
                   'l', 'large', 'largely', 'last', 'later', 'latest', 'least', 'less', 'let', 'lets', 'like', 'likely',
                   'long', 'longer', 'longest', 'm', 'made', 'make', 'making', 'man', 'many', 'may', 'me', 'member',
                   'members', 'men', 'might', 'more', 'most', 'mostly', 'mr', 'mrs', 'much', 'must', 'my', 'myself',
                   'n', 'necessary', 'need', 'needed', 'needing', 'needs', 'never', 'new', 'new', 'newer', 'newest',
                   'next', 'no', 'nobody', 'non', 'noone', 'not', 'nothing', 'now', 'nowhere', 'number', 'numbers', 'o',
                   'of', 'off', 'often', 'old', 'older', 'oldest', 'on', 'once', 'one', 'only', 'open', 'opened', 'opening',
                   'opens', 'or', 'order', 'ordered', 'ordering', 'orders', 'other', 'others', 'our', 'out', 'over', 'p',
                   'part', 'parted', 'parting', 'parts', 'per', 'perhaps', 'place', 'places', 'point', 'pointed',
                   'pointing', 'points', 'possible', 'present', 'presented', 'presenting', 'presents', 'problem',
                   'problems', 'put', 'puts', 'q', 'quite', 'r', 'rather', 'really', 'right', 'right', 'room', 'rooms',
                   's', 'said', 'same', 'saw', 'say', 'says', 'second', 'seconds', 'see', 'seem', 'seemed', 'seeming',
                   'seems', 'sees', 'several', 'shall', 'she', 'should', 'show', 'showed', 'showing', 'shows', 'side',
                   'sides', 'since', 'small', 'smaller', 'smallest', 'so', 'some', 'somebody', 'someone', 'something',
                   'somewhere', 'state', 'states', 'still', 'still', 'such', 'sure', 't', 'take', 'taken', 'than', 'that',
                   'the', 'their', 'them', 'then', 'there', 'therefore', 'these', 'they', 'thing', 'things', 'think',
                   'thinks', 'this', 'those', 'though', 'thought', 'thoughts', 'three', 'through', 'thus', 'to', 'today',
                   'together', 'too', 'took', 'toward', 'turn', 'turned', 'turning', 'turns', 'two', 'u', 'under', 'until',
                   'up', 'upon', 'us', 'use', 'used', 'uses', 'v', 'very', 'w', 'want', 'wanted', 'wanting', 'wants', 'was',
                   'way', 'ways', 'we', 'well', 'wells', 'went', 'were', 'what', 'when', 'where', 'whether', 'which',
                   'while', 'who', 'whole', 'whose', 'why', 'will', 'with', 'within', 'without', 'work', 'worked',
                   'working', 'works', 'would', 'x', 'y', 'year', 'years', 'yet', 'you', 'young', 'younger', 'youngest',
                   'your', 'yours', 'z',
                   # extra words/letters because the parser I have now isnt actually that great
                   'is', 's', 'r', 'was', 't', 'were', 'c', 'v', 'u', 'i', 've', 're',
                   'm', 'll', 'don', 'd', 'didn', 'shouldn','couldn','wouldn']

    return filter_list


def readability(tweet_file, top_n_words, username):
    """Calculate readability

    :param tweet_file:
    :param top_n_words:
    :param username:
    :return:
    """
    with open(tweet_file, 'r') as myfile:
        data = myfile.read().replace('\n', '')

    print "\n Running Twitter Readability for: %s \n" % username

    # Use regex to parse for all words in text file
    words = re.findall(r'\w+', data)

    # make everything lower case to avoid case sensitivity issues
    cap_words = [word.lower() for word in words]

    # Filter out common words or things my parser isnt smart enough to catch
    wordlist1 = [word for word in cap_words if word not in stop_words()]

    # Count the number of times a word appears
    word_counts = Counter(wordlist1)
    top_words = word_counts.most_common(top_n_words)

    # Begin plotting stuff. You can figure it out from here, right?
    word_count = []
    word = []
    for n in np.arange(0, top_n_words, 1):
        word.append(top_words[n][0])
        word_count.append(top_words[n][1])

    top_words_pos = np.arange(len(word))

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.margins(0.04, 0.0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.bar(top_words_pos, word_count, facecolor='#9999ff', edgecolor='white', alpha=0.5)

    plt.tick_params(axis="both", which="both", bottom="on", top="off",
                    labelbottom="on", left="off", right="off", labelleft="on")

    y_lowlim = min(word_count)
    y_highlim = max(word_count)
    plt.ylim([0, math.ceil(y_highlim + 0.25 * (y_highlim - y_lowlim))])

    plt.text(0.7, 0.8, 'Smog Index: %s' % textstat.smog_index(data),
             horizontalalignment='left',
             verticalalignment='center',
             transform=ax.transAxes, fontsize=9, color="grey")

    plt.text(0.7, 0.75, 'Flesch Reading Ease: %s' % textstat.flesch_reading_ease(data),
             horizontalalignment='left',
             verticalalignment='center',
             transform=ax.transAxes, fontsize=9, color="grey")

    plt.text(0.7, 0.85, 'Flesch Kincaid Grade: %s' % textstat.flesch_kincaid_grade(data),
             horizontalalignment='left',
             verticalalignment='center',
             transform=ax.transAxes, fontsize=9, color="grey")

    plt.text(0.7, 0.7, 'Text Standard: %s' % textstat.text_standard(data),
             horizontalalignment='left',
             verticalalignment='center',
             transform=ax.transAxes, fontsize=9, color="grey")

    for x, y in zip(top_words_pos, word_count):
        plt.text(x + 0.4, y + 0.05, '%.0f' % y, ha='center', va='bottom', fontsize=6)


    plt.tick_params(axis='both', which='major', labelsize=8)
    plt.xticks(top_words_pos, word, rotation=50, size=7)
    plt.xlabel('Word', size=9)
    plt.ylabel('Usage', size=9)
    plt.title('Top %s Favorite Words \n @%s' % (top_n_words, username), size=10)
    plt.tight_layout()
    plt.savefig('./plots/top_%s_words_%s.png' % (top_n_words, username), dpi=750)


if __name__ == '__main__':
    # File to save parsed tweets
    tweet_file = './output/%s_tweets.txt' % username
    # Load User tweets
    user_tweets = loadTweets(username, consumer_key, consumer_secret, access_token, access_token_secret)
    # Save parsed tweets to text file
    saveTweets(user_tweets, tweet_file)
    # Calculate readability stats and plot top words
    readability(tweet_file, top_n_words, username)
