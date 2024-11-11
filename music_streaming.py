# Song class
class Song:
    def __init__(self, song_id, title, artist, album, duration):
        self.id = song_id
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_artist(self):
        return self.artist

    def get_album(self):
        return self.album


# Album class
class Album:
    def __init__(self, album_id, title, artist, songs):
        self.id = album_id
        self.title = title
        self.artist = artist
        self.songs = songs

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_artist(self):
        return self.artist

    def get_songs(self):
        return self.songs


# Artist class
class Artist:
    def __init__(self, artist_id, name, albums):
        self.id = artist_id
        self.name = name
        self.albums = albums

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_albums(self):
        return self.albums


# Playlist class
class Playlist:
    def __init__(self, playlist_id, name, owner):
        self.id = playlist_id
        self.name = name
        self.owner = owner
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def remove_song(self, song):
        self.songs.remove(song)

    def get_songs(self):
        return self.songs


# User class
class User:
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password
        self.playlists = []

    def add_playlist(self, playlist):
        self.playlists.append(playlist)

    def remove_playlist(self, playlist):
        self.playlists.remove(playlist)

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password
    
    def get_playlists(self):
        return self.playlists


# UserManager class (Singleton)
class UserManager:
    _instance = None

    def __init__(self):
        self.users = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register_user(self, user):
        self.users[user.get_id()] = user

    def login_user(self, username, password):
        for user in self.users.values():
            if user.get_username() == username and user.get_password() == password:
                return user
        return None


# MusicLibrary class (Singleton)
class MusicLibrary:
    _instance = None

    def __init__(self):
        self.songs = {}
        self.albums = {}
        self.artists = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_song(self, song):
        self.songs[song.get_id()] = song

    def add_album(self, album):
        self.albums[album.get_id()] = album
        for song in album.get_songs():
            self.add_song(song)

    def add_artist(self, artist):
        self.artists[artist.get_id()] = artist
        for album in artist.get_albums():
            self.add_album(album)

    def get_song(self, song_id):
        return self.songs.get(song_id)

    def get_album(self, album_id):
        return self.albums.get(album_id)

    def get_artist(self, artist_id):
        return self.artists.get(artist_id)

    def search_songs(self, query):
        matching_songs = []
        for song in self.songs.values():
            if query in song.get_title() or query in song.get_artist() or query in song.get_album():
                matching_songs.append(song)
        return matching_songs


# MusicPlayer class
class MusicPlayer:
    def __init__(self):
        self.current_song = None
        self.is_playing = False
        self.current_time = 0

    def play_song(self, song):
        self.current_song = song
        self.is_playing = True
        self.current_time = 0
        print(f"Playing: {song.get_title()} by {song.get_artist()}")

    def pause_song(self):
        self.is_playing = False
        print("Song paused.")

    def seek_to(self, time):
        self.current_time = time
        print(f"Seeking to: {time} seconds.")


# MusicRecommender class (Singleton)
class MusicRecommender:
    _instance = None

    def __init__(self):
        self.user_recommendations = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def recommend_songs(self, user):
        return self.user_recommendations.get(user.get_id(), [])


# MusicStreamingService class
class MusicStreamingService:
    def __init__(self):
        self.music_library = MusicLibrary.get_instance()
        self.user_manager = UserManager.get_instance()
        self.music_recommender = MusicRecommender.get_instance()

    def start(self):
        print("Music Streaming Service started.")

    def get_music_library(self):
        return self.music_library
    
    def get_user_manager(self):
        return self.user_manager
    
    def get_music_recommender(self):
        return self.music_recommender


# MusicStreamingServiceDemo class to run the demo
class MusicStreamingServiceDemo:
    @staticmethod
    def run():
        music_streaming_service = MusicStreamingService()

        # Create users
        user1 = User("1", "john@example.com", "password123")
        user2 = User("2", "jane@example.com", "password456")

        # Create songs
        song1 = Song("1", "Song 1", "Artist 1", "Album 1", 180)
        song2 = Song("2", "Song 2", "Artist 2", "Album 2", 200)
        song3 = Song("3", "Song 3", "Artist 3", "Album 3", 210)

        # Create albums
        album1 = Album("1", "Album 1", "Artist 1", [song1])
        album2 = Album("2", "Album 2", "Artist 2", [song2])
        album3 = Album("3", "Album 3", "Artist 3", [song3])

        # Create artists
        artist1 = Artist("1", "Artist 1", [album1])
        artist2 = Artist("2", "Artist 2", [album2])
        artist3 = Artist("3", "Artist 3", [album3])

        # Add artists to the music library
        music_streaming_service.get_music_library().add_artist(artist1)
        music_streaming_service.get_music_library().add_artist(artist2)
        music_streaming_service.get_music_library().add_artist(artist3)

        # User registration
        music_streaming_service.get_user_manager().register_user(user1)
        music_streaming_service.get_user_manager().register_user(user2)

        # User login
        logged_in_user = music_streaming_service.get_user_manager().login_user("john@example.com", "password123")
        if logged_in_user:
            print(f"User logged in: {logged_in_user.get_username()}")
        else:
            print("Invalid username or password.")

        # Search for songs
        search_results = music_streaming_service.get_music_library().search_songs("Song")
        print("Search Results:")
        for song in search_results:
            print(f"Song: {song.get_title()} - {song.get_artist()}")

        # Create a playlist
        playlist = Playlist("1", "My Playlist", logged_in_user)
        playlist.add_song(song1)
        playlist.add_song(song2)
        logged_in_user.add_playlist(playlist)

        # Get song recommendations
        recommendations = music_streaming_service.get_music_recommender().recommend_songs(logged_in_user)
        print("Recommended Songs:")
        for song in recommendations:
            print(f"Song: {song.get_title()} - {song.get_artist()}")

        # Play a song
        music_player = MusicPlayer()
        music_player.play_song(song1)

        # Pause the song
        music_player.pause_song()

        # Seek to a specific time
        music_player.seek_to(60)

        # Get user's playlists
        user_playlists = logged_in_user.get_playlists()
        print("User Playlists:")
        for user_playlist in user_playlists:
            print(f"Playlist: {user_playlist.name}")
            print("Songs:")
            for song in user_playlist.get_songs():
                print(f"- {song.get_title()}")


if __name__ == "__main__":
    MusicStreamingServiceDemo.run()
