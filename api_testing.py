import requests
import pprint
import csv
from bs4 import BeautifulSoup

#TODO:
#One issue is that the export csv from letterboxd can contain films removed from their website, need to make sure the URL is valid

#Use TMDB and TMDB ID to access JustWatch data and find if the film is streaming for free or on a paid service
def is_streaming(movie_id):
    api_key = ""
    response = requests.get("https://api.themoviedb.org/3/movie/"+ movie_id + "/watch/providers?api_key="+api_key)
    if 'US' in response.json()['results']:
        if 'free'in response.json()['results']['US']:
             for provider in response.json()['results']['US']['free']:
                 pprint.pprint("Free: " + provider['provider_name'])

        elif 'flatrate'in response.json()['results']['US']:
             for provider in response.json()['results']['US']['flatrate']:
                 pprint.pprint("Stream: " + provider['provider_name'])

        elif 'ads'in response.json()['results']['US']:
             for provider in response.json()['results']['US']['ads']:
                 pprint.pprint("Ads: " + provider['provider_name'])
        else:
            print("Not available")
    else:
        print("Not available")

#scape the letterboxd page of the film for the TMDB id
def get_tmdb_id(letterboxd_url):
    req = requests.get(letterboxd_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    html_class = soup.find('body',{'class': 'film backdropped'}) or soup.find('body',{'class': 'film'})
    id = html_class['data-tmdb-id']

    return(id)


#open our letterboxd watchlist csv and grab the names and urls to pull from
def open_csv(letterboxd_csv):
    ids = []
    with open(letterboxd_csv,newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ids.append([row['Letterboxd URI'], row['Name']])
    return ids


letterboxd_csv = ''
letterboxd_ids = open_csv(letterboxd_csv)
#letterboxd_ids = [['https://boxd.it/XyU','Vengeance Is Mine'], ['https://boxd.it/1RSc','High and Low']]
for film in letterboxd_ids:
    print(film[1])
    tmdb_id = get_tmdb_id(film[0])
    is_streaming(tmdb_id)
