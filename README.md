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
