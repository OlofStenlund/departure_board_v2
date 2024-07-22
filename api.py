from fastapi import FastAPI, Request, Depends
import jwt
import requests
import pandas as pd
from datetime import datetime, time, timedelta
import time
from fastapi.templating import Jinja2Templates
from main import main, stop


templates = Jinja2Templates(directory=".")

app = FastAPI()

# my_list, curr_time = main()

# print(type(my_list))


list_of_titles = ["Linje", "Mot", "Planerad Avgång", "Avgång", "Avgår Om"]


@app.get("/")
def get(request: Request):
    my_list, curr_time = main()
    year = curr_time["year"]
    month = curr_time["month_no"]
    month_name = curr_time["month_name"]
    day_no = curr_time["day_no"]
    day_name = curr_time["day_name"]
    hour = curr_time["hour"]
    minute = curr_time["minute"]
    return templates.TemplateResponse(
        "template.html", 
        {
            "request": request, 
            "my_list": my_list, 
            "titles_list": list_of_titles, 
            "departure_stop": stop, 
            "year": year, 
            "month": month, 
            "month_name": month_name,
            "day_no": day_no, 
            "day_name": day_name, 
            "hour": hour, 
            "minute": minute
        }
    )
