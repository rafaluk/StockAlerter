# StockAlerter
> Send me an email, when a price on my GPW stock reaches global max or min.

Python 3.7

## General description
Every given time interval StockAlerter **downloads stock price**. It compares it with global mininum and maximum, and if one of them is reached an **email is sent**.

## Details
### Scheduler
To specify intervals a scheduler from `APScheduler` has been used (https://pypi.org/project/APScheduler/). Since the logic is initialized once the `flask` server is started, it's implemented inside `app/__init__.py` file. 
### Downloading stock price
Since GPW (*Giełda Papierów Wartościowych*, main polish stock exchange) doesn't share its API for free (actually it's very expensive!), webscraping of **bankier.pl** has been used. Although it works fine, it has two main disadvantages:
* it's harder to implement and maintain than an API.
* it has a delay of approx. 20 minutes.

For webscraping `requests` and `BeautifulSoup` have been used.

See `app/stock_value.py`.
### History
The history is being searched and updated on every call. It's being kept in `history.csv` file. `HistoryManager` is responsible for reading the file, searching for global minimums and global maximums, saving to the file. 

An assumption has been made to save only values fetched by webscraping (described above). 

It'd possible to download a full history with shorter intervals (what would be more accurate), but it wouldn't make any difference after all, because the scheduler decides, when the email is sent.
### Sending an email
`smtplib` has been used, with `TLS` protocol.
> How about email account details, such as login and password? Where are they being kept?

They are only referenced from code as environmental variables.
**!!!** In order to make this project work, you have to set up these three env variables:

```
LOGIN = os.environ.get('STOCK_ALERTER_LOGIN')
PASSWORD = os.environ.get('STOCK_ALERTER_PASSWORD')
MY_EMAIL = os.environ.get('MY_GMAIL')
```

### Utils
Some of static utils function have been extracted to `app/utils.py`, e.g. `calc_time` wrapper, which can be used as a decorator:
```
@calc_time
def function():
    ....
```
Example output:
```
Execution of 'function' done in 1.87 seconds.
```
