# departure_board_v2
Departure board for any station in the Västtrafik network

NOTICE:
This under construction project is based on an older API. 
This has recentry been changed, and I have not had the time to test it on the new API yet.
python_jwt module is deprecated. Working on a solution with another library.


This app accesses the Västtrafik API to generate a departure board for a chosen stop within the Västtrafik network, and allows you to displyu the results in a web-app, using for example Uvicorn.
You must have a Västtrafik developer avvount. Register for free here: https://developer.vasttrafik.se/

Contents:<p>
1: api.py<p>
- Creates the app that allows you to host using eg. Uvicorn<p><p>
2: connection_details.py<p>
- Handles details about connecting to the right url.<p><p>
3: main_functions.py<p>
- These functions are imported into main.py<p><p>
4: main.py<p>
- This is where you enter the name of the stop and how many departures you would like returned<p>
- Make sure spelling is correct. (Not case sensitive)<p><p>

Gitignore:<p>
1: token.txt<p>
- Textfile that stores the token generated by the API. Before running the code for the first time, create token.txt in the same directory as the other files, and everything should work fine.<p><p>
2: account_details.py<p>
- Contains personal keys to grant access to the API.<p><p>
- Create an account here: https://developer.vasttrafik.se/<p><p>
