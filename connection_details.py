connection_url_1 = "/locations/by-text?q="
connection_url_2 = "&limit="
connection_url_3 = "&offset=0"

connection_base_url = "https://ext-api.vasttrafik.se/pr/v4"

def generate_connetion_url(stop, num):
    from account_details import connection_url_1, connection_url_2
    connection_url = connection_url_1+stop+connection_url_2+num+connection_url_3
    return connection_url