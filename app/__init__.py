from flask import Flask
from app.scheduling import run_min_max_scheduler, run_regular_scheduler

app = Flask(__name__)

# todo: run config checker
run_min_max_scheduler()
run_regular_scheduler()
