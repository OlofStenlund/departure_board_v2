# departure_board_v2

Departure board for any station in the Västtrafik network
<br><br>

<br><br>
This app accesses the Västtrafik API to generate a departure board for a chosen stop within the Västtrafik network, and allows you to display the results in a web-app, using for example Uvicorn.<p>
You must have a Västtrafik developer account. Register for free here: https://developer.vasttrafik.se/<p>
This project uses handling of sensitive information using the python-dotenv package.
More info can be found here: https://pypi.org/project/python-dotenv/<p>
<br>
TODO:<p>
~~1: Create automatic updating~~<p>
2: Add features such as "Läge" and "Handikapsanpassad"<p>
~~3: Add colour coding to routes<p>~~
<br><br>
Contents:<p>
**1: api.py<p>**
Creates the app that allows you to host using eg. Uvicorn<p>
**2: departure_requests<p>**
Contains the functions used to access information about stops and departures<p>
**3: env_handling.py<p>**
Contains functions handling envorinment variables using the python-dotenv package.<p>
**4: token_handling.py<p>**
Contains functions handling the access-token needed. A token is valid for 24 hours, and these functions make sure the token is valid, and requests a new one if not.<p>
**5: main.py<p>**
The main program that is run when the app in api.py is run.<p>
**6: landing_page.html<p>**
HTML-template for landning page for selecting initial stop.<p>
**7: board_template.html<p>**
HTML-template for the actual departure board.<p>
<br><br>
Gitignore:<p>
**1: .env<p>**
Contains envorinment variables that should be hidden from others, <p>
ie. sensitive user information.<p>
**2: template.html<p>**
Deprecated frontend template.<p>
