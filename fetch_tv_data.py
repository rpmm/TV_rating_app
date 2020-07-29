import requests
import json

def get_tv_series_ratings(titleName):

    myKey = 'XXXX' # OMDb API-key
    URL = 'http://www.omdbapi.com/?apikey={}&t={}'.format(myKey, titleName)
    json_data = requests.get(URL).text
    show_data = json.loads(json_data) # Parsed JSON

    if show_data['Response']=='False':
        return False

    # Series info
    amount_of_seasons = int(show_data['totalSeasons'])
    series_title = show_data['Title']
    poster = show_data['Poster']
    
    # For parsing seasons
    episode_index = 1
    seasons_list = []
    
    for season_num in range(1, amount_of_seasons+1):

        # Get season data
        URL = 'http://www.omdbapi.com/?apikey={}&t={}&Season={}'.format(myKey, titleName, season_num)
        json_data = requests.get(URL).text
        season_data = json.loads(json_data) # Parsed json
        
        # Season info
        episodes = season_data['Episodes']
        episodes_in_season = len(episodes)
        season_ratings = {}

        # Parse episodes in season
        for episode_number in range(episodes_in_season):
            episode_rating = episodes[episode_number]['imdbRating']
            season_ratings[str(episode_index)] = episode_rating
            episode_index += 1
        
        seasons_list.append(season_ratings)
    
    return series_title, seasons_list, poster