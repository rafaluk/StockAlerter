from flask import Flask
from app.scheduling import run_scheduler
from app.stock_value import StockValue
from app.history_manager import HistoryManager

app = Flask(__name__)

run_scheduler()
