import urllib.request
import re
import pafy

class YTDownloader():
    def __init__(self, download_folder='./downloads/'):
        self.download_folder = download_folder
        self.ytq_url = 'https://www.youtube.com/results?search_query='
        self.ytw_url = 'https://www.youtube.com/watch?v='

    def get_video_info(self, query):
        #prepare string to be used in query
        query = query.replace(' ', '_')
        #Query for the first vid in search engine
        html = urllib.request.urlopen(self.ytq_url + query)
        video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
        vid_id = self.ytw_url + video_ids[0]
        return vid_id

    def download_best_audio(self, vid_id):
        #select video
        vid = pafy.new(vid_id)
        #select best audio
        bestaudio = vid.getbestaudio(preftype="mp3, wav", ftypestrict=False)
        #download audio file
        bestaudio.download(self.download_folder)

    def download_song_list(self, song_list):
        for query in song_list:
            vid_id = self.get_video_info(query)
            self.download_best_audio(vid_id)