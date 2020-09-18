import youtube_dl
import pprint

ydl_opts = {
    'outtmpl': '%(id)s%(ext)s',
    'writeautomaticsub': True,
    'subtitlesformat': 'vtt',
    'subtitleslangs': ['fr'],

    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '0',
    }]
}

link = 'https://www.youtube.com/watch?v=fFb4zm5D0Hg'
# title : Conversation in Slow French - Learn French
# id : fFb4zm5D0Hg
# automatic_captions len : 109
# automatic_captions fr len : 5

# link = 'https://www.youtube.com/watch?v=zJ43u9ca8kc'
# title : Discover Strasbourg | Easy French 55
# id : zJ43u9ca8kc
# automatic_captions len : 109
# automatic_captions fr len : 5

link_playlist = 'https://www.youtube.com/playlist?list=PLA5UIoabheFMYWWnGFFxl8_nvVZWZSykc'

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    # 1. Just extract the info
    info_video = ydl.extract_info(
        link,
        download=False
    )
    video_title = info_video["title"]
    video_id = info_video["id"]
    # display_id
    #

    # print("\n-------------------\n")
    # print(video_title)
    # print(video_id)
    # print("\n-------------------\n")
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(info_video)

    # 2. for playlist
    if '_type' in info_video.keys():
        if info_video['_type'] == 'playlist':
            print('total videos in playlist: ', len(info_video['entries']))
            for i, video in enumerate(info_video['entries']):
                print("\n------------------- ", i)
                print("title :", video['title'])
                print("id :", video['id'])
                print("automatic_captions len :", len(video['automatic_captions']))
                # if len(video['automatic_captions']) > 0 :
                try:
                    print("automatic_captions fr len :", len(video['automatic_captions']['fr']))
                except KeyError as e:
                    print('KeyError: ', e)
                print("-------------------")
    else:
        video = info_video
        print("\n------------------- ")
        print("title :", video['title'])
        print("id :", video['id'])
        print("automatic_captions len :", len(video['automatic_captions']))
        # if len(video['automatic_captions']) > 0 :
        try:
            print("automatic_captions fr len :", len(video['automatic_captions']['fr']))
        except KeyError as e:
            print('KeyError: ', e)
        print("-------------------")
