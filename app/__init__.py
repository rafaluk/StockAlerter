from flask import Flask
from app.scheduling import run_min_max_scheduler

app = Flask(__name__)

# todo: run config checker
run_min_max_scheduler()
# todo: run_regular_scheduler()
