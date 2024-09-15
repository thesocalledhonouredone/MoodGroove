import spotipy
import random
from spotipy.oauth2 import SpotifyOAuth

class SpotifyPlaylistGenerator:
    def __init__(self, client_id, client_secret, redirect_uri, mood, language, num_songs):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.mood = str.lower(mood)
        self.language = str.lower(language)
        self.num_songs = int(num_songs)
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope="playlist-modify-public"))
        self.link = ""

    def get_search_query(self):
        mood_queries = {
            'angry': 'angry',
            'disgust': 'disgust',
            'fear': 'fear',
            'happy': 'happy',
            'neutral': 'chill',
            'sad': 'sad',
            'surprise': 'surprise'
        }
        language_queries = {
            'telugu': 'tollywood',
            'tamil': 'tamil',
            'hindi': 'bollywood',
            'english': 'english'
        }
        mood_query = mood_queries.get(self.mood, 'happy')
        language_query = language_queries.get(self.language, 'english')
        return f"{mood_query} {language_query}"

    def get_top_artists(self, search_query):
        artist_uris = []
        limit = 50
        offset = 0

        while len(artist_uris) < 100:
            results = self.sp.search(q=search_query, type='artist', limit=limit, offset=offset)
            artist_uris += [artist['uri'] for artist in results['artists']['items']]
            if len(results['artists']['items']) < limit:
                break
            offset += limit

        return artist_uris[:100]

    def get_random_tracks_from_artists(self, artist_uris):
        track_uris = []
        while len(track_uris) < self.num_songs:
            for artist_uri in artist_uris:
                top_tracks = self.sp.artist_top_tracks(artist_uri)
                if top_tracks['tracks']:
                    track = random.choice(top_tracks['tracks'])
                    if track['uri'] not in track_uris:
                        track_uris.append(track['uri'])
                if len(track_uris) >= self.num_songs:
                    break

        return track_uris

    def generate_playlist(self):
        search_query = self.get_search_query()
        print(f"Search query: {search_query}")
        artist_uris = self.get_top_artists(search_query)
        
        if not artist_uris:
            print("No artists found for the given criteria.")
            return
        
        track_uris = self.get_random_tracks_from_artists(artist_uris)
        playlist_name = f"{self.mood} {self.language} Playlist"
        user_id = self.sp.me()['id']
        playlist = self.sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
        
        if track_uris:
            self.sp.playlist_add_items(playlist['id'], track_uris)
        
        print(f"Playlist '{playlist_name}' with {self.num_songs} songs created successfully!")
        print(f"Link to the playlist: {playlist['external_urls']['spotify']}")
        self.link = playlist

    def get_link(self):
        return self.link['external_urls']['spotify']

# TESTING CODE
# if __name__ == "__main__":
#     client_id = "your_client_id"
#     client_secret = "your_client_secret"
#     redirect_uri = "http://localhost:8080/callback"
#     playlist_generator = SpotifyPlaylistGenerator(
#         client_id=client_id,
#         client_secret=client_secret,
#         redirect_uri=redirect_uri,
#         mood='sad',
#         language='telugu',
#         num_songs=10
#     )
#     playlist_generator.generate_playlist()
