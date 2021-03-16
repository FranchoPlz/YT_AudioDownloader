import urllib.request
import re
import pafy

song_list = ['purpurina', 'stand by me']
#video = pafy.new(url) 
for search_query in song_list:
    #prepare string to be used in query
    search_query = search_query.replace(' ', '_')
    #Query for the first vid in search engine
    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' +search_query)
    video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
    vid_to_download = 'https://www.youtube.com/watch?v=' + video_ids[0]
    #select video
    vid = pafy.new(vid_to_download)
    #select best audio
    bestaudio = vid.getbestaudio(preftype="mp3, wav", ftypestrict=False)
    #download audio file
    bestaudio.download(f'./downloads/')