# Twitter Tools


A collection of scripts and utilities that rely on the Twitter's API to conduct parsing and analytics


### User Readability Stats

* Python based script that relies on the TwitterSearch and textstat libraries to download, parse, and conduct a battery of readability statistics for a specified users most recent tweets. The script can also count and plot the top n most common words a user tweets with optional filtering to ignore the top 100 most common English words and tweets with certain characters.


*Usage*

~~~
$ python user_readability_stats.py
~~~
<br>
*User options (set in script)*

~~~
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

~~~

<br>
*Example Output*
<br>
<br>
![LamaTweets](https://github.com/awentland90/TwitterTools/blob/master/plots/top_20_words_DalaiLama.png)
<br>
<br>
<br>
![ObamaTweets](https://github.com/awentland90/TwitterTools/blob/master/plots/top_20_words_BarackObama.png)
<br>
<br>
<br>
![TrumpTweets](https://github.com/awentland90/TwitterTools/blob/master/plots/top_20_words_realDonaldTrump.png)
