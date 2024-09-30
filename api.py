from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from main import main


templates = Jinja2Templates(directory=".")
app = FastAPI()
list_of_titles = ["Linje", "Mot", "Planerad Avgång", "Avgång", "Avgår"]


@app.get("/")
def get(request: Request):
    return templates.TemplateResponse(
        name="landing_page.html", 
        context={"request": request}
    )

@app.get("/{stop}")
def get(request: Request, stop: str, municipality: str):
    my_list, curr_time = main(stop=stop, municipality=municipality)
    year = curr_time["year"]
    month = curr_time["month_no"]
    month_name = curr_time["month_name"]
    day_no = curr_time["day_no"]
    day_name = curr_time["day_name"]
    hour = curr_time["hour"]
    minute = curr_time["minute"]
    return templates.TemplateResponse(
        "board_template.html", 
        {
            "request": request, 
            "my_list": my_list, 
            "titles_list": list_of_titles, 
            "departure_stop": stop.title(), 
            "year": year, 
            "month": month, 
            "month_name": month_name,
            "day_no": day_no, 
            "day_name": day_name, 
            "hour": hour, 
            "minute": minute
        }
    )



# Global variables to store data
# data = {"dep_data": [], "curr_time": []}


# # Function to update data periodically
# async def update_data_periodically():
#     while True:
#         data["dep_data"], data["curr_time"] = main()
#         await asyncio.sleep(30)  # wait 30 seconds before updating again

# # Start the periodic update task when the application starts
# @app.on_event("startup")
# async def start_periodic_update():
#     asyncio.create_task(update_data_periodically())

# @app.get("/")
# def get(request: Request):
#     # year, month, month_name, week, day_no, day_name, hour, minute = curr_times
#     return templates.TemplateResponse("template.html", {
#         "request": request,
#         "my_list": data["dep_data"],
#         "titles_list": list_of_titles,
#         "departure_stop": stop,
#         "year": data["curr_time"]["year"],
#         "month_no": data["curr_time"]["month_no"],
#         "month_name": data["curr_time"]["month_name"],
#         "day_no": data["curr_time"]["day_no"],
#         "day_name": data["curr_time"]["day_name"],
#         "hour": data["curr_time"]["hour"],
#         "minute": data["curr_time"]["minute"],
#     })