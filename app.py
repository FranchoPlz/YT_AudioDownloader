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








"""
    #download vid info
    video_info = youtube_dl.YoutubeDL().extract_info(url=vid_to_download, download=False)
    video_title = video_info['title']
    #download options
    options = {
        'format' : 'bestaudio/best',
        'outtmpl' : f'./downloads/{video_title}.mp3',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
        }]
    }
    #download vid
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([vid_to_download])
"""