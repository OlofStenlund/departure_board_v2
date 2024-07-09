from fastapi import FastAPI, Request, Depends
# import jwt
import requests
# import pandas as pd
from datetime import datetime, time, timedelta
import time
from fastapi.templating import Jinja2Templates
from main import stop, main

app = FastAPI()


app.get("/")
def get(request: Request):
    deps, current_time = main()
    year, day, month, hour, minute = []