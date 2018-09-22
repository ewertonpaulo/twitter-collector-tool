# tweepy
## Environment:
```
$ pip install tweepy
```
```
$ pip install psycopg2
```
twitter-collector works with postgresSQL, before run, configure the connection in the file db.py line 14.
## How to use:
Create a file named auth.py with your own twitter api keys by the following script:
### auth.py
```py
# Authentications
consumer_key = 'your_consumer_key_here'
consumer_secret = 'your_consumer_secret_here'
access_token = 'your_access_token_here'
access_token_secret = 'your_access_token_secret_here'
```
### example.py
```py
from coletor import collect

collect('amor')
```
As paramter for collect function you can put the key word you expect to search.
main.py is a example of script, you can run on your prompt by the following command int the directory of the aplication:
```
python main.py
```
A message as 'collecting tweets with key amor' will confirm the correct run.
