import sqlite3
import requests

def create_database():
    conn = sqlite3.connect('anime_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weekly_anime (
            week TEXT PRIMARY KEY,
            top_anime TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_anime_data(query):
    url = 'https://graphql.anilist.co'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json={'query': query}, headers=headers)
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.text)
    if response.status_code == 200:
        return response.json()
    return None

def get_weekly_top_anime():
    query = '''
    {
      Page(perPage: 10) {
        media(sort: POPULARITY_DESC, type: ANIME, season: WINTER, seasonYear: 2024) {
          title {
            romaji
            english
          }
          id
        }
      }
    }
    '''
    data = fetch_anime_data(query)
    if data and 'data' in data and 'Page' in data['data']:
        return data['data']['Page']['media']
    return None

def get_trending_anime():
    query = '''
    {
      Page(perPage: 10) {
        media(sort: TRENDING_DESC, type: ANIME) {
          title {
            romaji
            english
          }
          id
        }
      }
    }
    '''
    data = fetch_anime_data(query)
    if data and 'data' in data and 'Page' in data['data']:
        return data['data']['Page']['media']
    return None

def get_top_anime_list():
    query = '''
    {
      Page(perPage: 10) {
        media(sort: SCORE_DESC, type: ANIME) {
          title {
            romaji
            english
          }
          id
        }
      }
    }
    '''
    data = fetch_anime_data(query)
    if data and 'data' in data and 'Page' in data['data']:
        return data['data']['Page']['media']
    return None
