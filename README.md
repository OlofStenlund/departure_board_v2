# departure_board_v2

Departure board for any station in the Västtrafik network

NOTICE:
This repo is under construction

This app accesses the Västtrafik API to generate a departure board for a chosen stop within the Västtrafik network, and allows you to display the results in a web-app, using for example Uvicorn.
You must have a Västtrafik developer account. Register for free here: https://developer.vasttrafik.se/
This project uses handling of sensitive information using the python-dotenv package.
More info can be found here: https://pypi.org/project/python-dotenv/

Contents:<p>
1: api.py<p>
Creates the app that allows you to host using eg. Uvicorn<p><p>
2: departure_requests<p>
Contains the functions used to access information about stops and departures<p><p>
3: env_handling.py<p>
Contains functions handling envorinment variables using the python-dotenv package.<p><p>
4: toke_handling.py<p>
Contains functions handling the access-token needed. A token is valid for 24 hours, and these functions make sure the token is valid, and requests a new one if not.<p><p>
5: main.py<p>
The main program that is run when the app in api.py is run.

Gitignore:<p>
1: .env<p>
Contains envorinment variables that should be hidden from others, <p>
ie. sensitive user information.
