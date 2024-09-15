import Mood
import Details
import Spotify
import tkinter as tk
import pywhatkit as kit
import webbrowser as wb


CLIENT_ID = "9f62e5458a89475c97f49bc8bc3a3fa5"
CLIENT_SECRET = "c67ebc4709df4232a8430b682c9ebb7b"
redirect_uri = "http://localhost:8080/callback"

root = tk.Tk()
moodDetect = Mood.MoodDetectorApp(root)
root.mainloop()
mood = moodDetect.retMood()



root = tk.Tk()
detailObj = Details.DetailsApp(root)


root.mainloop()
details = detailObj. ret_details()

# working
# print(mood, details)

spotify = Spotify.SpotifyPlaylistGenerator("9f62e5458a89475c97f49bc8bc3a3fa5", "c67ebc4709df4232a8430b682c9ebb7b", redirect_uri, mood, details[1], details[0])
spotify.generate_playlist()
link = spotify.get_link()
print(link)

# SEND LINK 
kit.sendwhatmsg_instantly(phone_no=("+91"+details[2]), message=link, tab_close=True)
# OPEN SPOTIFY
wb.open(link)
