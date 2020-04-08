from flask import Flask
from app.scheduling import run_extreme_scheduler

app = Flask(__name__)

# todo: run config checker
run_extreme_scheduler()
# todo: run_regular_scheduler()
