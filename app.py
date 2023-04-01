from dotenv import load_dotenv
import os
import json
import requests
import base64
import time

load_dotenv()
commands = ["Show Top 10 Songs of an artist", "Show all albums of an artist", "Get Track's audio analysis", "Get Artist's information"]

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_base64 = str(base64.b64encode((client_id + ':' + client_secret).encode()), "utf-8")
    url = 'https://accounts.spotify.com/api/token'

    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    body = {
        'grant_type':'client_credentials'
    }

    response  = requests.post(url, headers=headers, data=body)
    results = json.loads(response.content)
    token = results["access_token"]
    return token

def get_headers(token):
    header = {
        'Authorization': 'Bearer ' + token
    }
    return header

def get_artist_info(token, artist, action):
    url = 'https://api.spotify.com/v1/search'
    header = get_headers(token)

    query = f'?q={artist}&type=artist&limit=1'
    full_query = url + query

    response = requests.get(full_query, headers=header)
    result = json.loads(response.content)
    data = result['artists']['items']
    if len(data) == 0:
        print('Such an artist was not found')
        return None
    else:
        if action == 2 or action == 1:
            return data[0]['id']
        elif action == 4:
            return data[0]

def get_all_albums(token, id):
    header = get_headers(token)
    url = f'https://api.spotify.com/v1/artists/{id}/albums?market=US'

    respone = requests.get(url, headers=header)
    result = json.loads(respone.content)['items']
    for inx, item in enumerate(result):
        time.sleep(0.5)
        print(f'\n{inx + 1}. "{item["name"]}" Release Date: {item["release_date"]}\n')
        get_songs(header, item['id'])

def get_artist():
    artist = input("Input artist's name: ")
    return artist

def get_songs(header, id):
    url = f'https://api.spotify.com/v1/albums/{id}/tracks'

    response = requests.get(url, headers=header)
    result = json.loads(response.content)['items']
    for inx, item in enumerate(result):
        time.sleep(0.25)
        print(f"    {inx + 1}. {item['name']}")
    print("\n")

def get_song_id(song, token):
    url = 'https://api.spotify.com/v1/search'
    header = get_headers(token)

    query = f'?q={song}&type=track&limit=1'
    full_query = url + query

    response = requests.get(full_query, headers=header)
    result = json.loads(response.content)['tracks']['items']
    return result[0]['id']
    
def get_song_name():
    song = input("Input song's name: ")
    return song

def get_song_analysis(token, id):
    url = f'https://api.spotify.com/v1/audio-features/{id}'
    header = get_headers(token)

    response = requests.get(url, headers=header)
    result = json.loads(response.content)
    for item, feature in result.items():
        time.sleep(0.25)
        if item == 'analysis_url' or item == 'duration_ms' or item == 'time_signature' or item == 'mode' or item == 'id' or item == 'uri' or item == 'track_href':
            pass
        else:
            print(f'{item}: {feature}')

def get_top_songs(token, id):
    url = f'https://api.spotify.com/v1/artists/{id}/top-tracks?country=US'
    header = get_headers(token)

    response = requests.get(url, headers = header)
    result = json.loads(response.content)["tracks"]
    for inx, item in enumerate(result):
        time.sleep(0.25)
        print(f"{inx + 1}. {item['name']}")           

while True:
    token = get_token()
    print("\n")
    for inx, command in enumerate(commands):
        print(f"{inx + 1}. {command}")
        time.sleep(0.5)
    print("\n")
    action = input("What do yo want to do? ")

    try:
        action = int(action)
    except:
        print("Please input on of the given digits")
        exit()
    
    if action == 1:
        artist = get_artist()
        id = get_artist_info(token, artist, action)
        get_top_songs(token, id)
    elif action == 2:
        artist = get_artist()
        id = get_artist_info(token, artist, action)
        get_all_albums(token, id)
    elif action == 3:
        song = get_song_name()
        print('\n')
        id = get_song_id(song, token)
        get_song_analysis(token, id)
    elif action == 4:
        artist = get_artist()
        data = get_artist_info(token, artist, action)
        time.sleep(1)
        print(f"\nArtist: {data['name']}\nNumber of followers: {data['followers']['total']}\nGenres: {data['genres']}\nImage: {data['images'][0]['url']}\nPopularity: {data['popularity']}\nSpotify page: {data['external_urls']['spotify']}\n")
    else:
        print("Choose one of the given commands")
        exit()