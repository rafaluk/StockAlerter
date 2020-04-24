# StockAlerter
StockAlerter is **a simple helper** for all, who **invest their money** on a stock exchange! It **alerts you with an email**, when the prices are extremely low/high and **sends you a daily summary**. All these with **detailed calculations**.

StockAlerter can operate **multiple stocks** for **multiple users** with different emails.

You just have to modify the config file with your transactions details! 

## Preparation
1. Clone the repo.
2. Install required packages (`pip install -r requirements.txt`), use an env with `Python 3.7`.
3. Create a config.json file (you can find `config_sample.json` in repo; see **Config file** chapter) with all required details.
4. Create two environmental variables with your email account details (see **Sending an email** chapter).
5. `flask run`

## Details
### Scheduler
The stocks are being checked in two ways:
* `min_max_mail`: **every given interval** (specified in `config.json`) StockAlerter downloads the stocks and compares them with mininum and maximum values for a given trade.
* `daily_mail`: **from Monday to Friday at 6 pm.** StockAlerter downloads all the stocks and sends a summary email to recipient.

Both ways are being called from schedulers (`APScheduler` has been used): `Interval` and `Cron`.

Both **can be enabled/disabled** in `config.json`.

See `app/scheduling.py`.
### Downloading stock price
Since GPW (*Giełda Papierów Wartościowych*, main polish stock exchange) doesn't share its API for free (actually it's very expensive!), webscraping of **bankier.pl** has been used. Although it works fine, it has two main disadvantages:
* it's harder to implement and maintain than an API.
* it has a delay of approx. 20 minutes comparing to current GPW data.

For webscraping `requests` and `BeautifulSoup` have been used.

See `app/stock_value.py`.
### Sending an email
Before an email is sent, it must be properly prepared. Since the email is the final product for the user, the email must contain every imporant information in readable form. This is where `EmailPreparer` comes in.

`EmailPreparer` handles all logic in terms of choosing right recipients and preparing email message. It's the last step before actual email shipment.

See: `app/email_preparer.py`.

For logic of sending mail `EmailSender` is responsible. It uses `smtplib` with `TLS` security protocol. A specific host and port could be specified in `config.json`.

**All email account details, such as login and password, are only referenced from the code as environmental variables.**

**IMPORTANT:** In order to make this project work, you have to set up these env variables:

`STOCK_ALERTER_LOGIN` - your email login from which the emails will be sent
`STOCK_ALERTER_PASSWORD` - your email password from which the emails will be sent

See: `app/email_sender.py`.
### History
The history is kept in `history.csv` file. It's being updated on every call. `HistoryManager` class is responsible for reading the file, searching for global minimums and global maximums and saving to the file. 

See: `app/history_manager.py`.
### Config file
The `config.json` file allows to manage things like:
* recipients (`address`)
* consent for a daily mail (`daily_mail`)
* transactions details (`symbol`, `buy_price`, `buy_quantity`)
* consent for a min/max mail within every transaction (`min_max_mail`)
* `smtp` details (`host`, `port`)
* data sources 

You **must have** a proper `config.json` file for the app to run!

**See a sample config file: `config_sample.json`.** 
### Calculator
The `Calculator` calculates revenues, costs and profits taking under consideration commissions and taxes.

Assumptions:
* An investment tax rate: **19%** (Polish *podatek Belki*).
* A commision rate: **0,39%**.
### Utils
Some of static utils function have been extracted to `app/utils.py`, e.g. `calculate_time` wrapper, which can be used as a decorator:
```
@calculate_time
def function():
    ....
```

Example output:
```
Execution of 'function' done in 1.87 seconds.
```
See: `app/utils.py`.
### Technology stack
* `python 3.7`
* `flask`
* `APScheduler` (https://pypi.org/project/APScheduler/)
* `BeautifulSoup`
