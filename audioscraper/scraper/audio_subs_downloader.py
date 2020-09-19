import youtube_dl
import os

YOUTUBE_PREFIX_LINK = 'https://www.youtube.com/watch?v='


def get_main_info_video(info_video, link, lang):
    video = {'title': info_video['title'],
             'id': info_video['id'],
             'automatic_captions_lang': False,  # True if video has subs in the desired lang
             'link': link}
    try:
        if len(info_video['automatic_captions'][lang]) > 0:
            video['automatic_captions_lang'] = True
    except KeyError as e:
        print('Exception catch: KeyError: ', e)
    return video


def get_videos_infos_list_from_link(link, lang):
    video_infos_list = []
    ydl_opts = {'outtmpl': '%(id)s%(ext)s',
                'writeautomaticsub': True,
                'subtitlesformat': 'vtt',
                'subtitleslangs': [lang],
                'postprocessors': [{'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'wav',
                                    'preferredquality': '0'}],
                'format': 'bestaudio/best'}
    print("\n\n--------------------- Getting info from link: ", link)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_object = ydl.extract_info(link, download=False)
        if '_type' in info_object.keys():
            if info_object['_type'] == 'playlist':
                # link passed is a playlist from Youtube
                print('total videos in playlist: ', len(info_object['entries']))
                for info_video in info_object['entries']:
                    video_infos_list.append(get_main_info_video(info_video, YOUTUBE_PREFIX_LINK+info_video['id'], lang))
        else:
            video_infos_list.append(get_main_info_video(info_object, link, lang))
    return video_infos_list


def download_audios_and_subs(link, lang, downloads_path):
    """
    from the youtube link it extracts audio in wav format
    and subtitles in .vtt format
    """
    ydl_opts = {'outtmpl': '%(id)s%(ext)s',
                'writeautomaticsub': True,
                'subtitlesformat': 'vtt',
                'subtitleslangs': [lang],
                'outtmpl': downloads_path+'/%(id)s',
                'postprocessors': [{'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'wav',
                                    'preferredquality': '0'}],
                'format': 'bestaudio/best'}
    # 1. Download video, audio and subs
    print("\n--------------------- Downloading audio and subs from link: ", link)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_video = ydl.extract_info(link, download=True)
        video_title = info_video["title"]
        video_id = info_video["id"]
    print("\n----------Downloaded audio subs-----------")
    print("Video link: ", link)
    print("Video title: ", video_title)
    print("Video id: ", video_id)
    print("---------------------------------------\n")

    # 2. Returning download paths for subs and audio files
    wav_file_path_destination = os.path.join('./.wav')
    sub_file_path_destination = os.path.join(downloads_path, video_id + "." + lang + ".vtt")

    print("\n----------Downloaded audio subs Paths-----------")
    print("wav_file_path_destination: ", wav_file_path_destination)
    print("sub_file_path_destination: ", sub_file_path_destination)
    print("---------------------------------------\n")

    return wav_file_path_destination, sub_file_path_destination


def old_download_audios_and_subs(link, lang, audios_path, subs_path):
    """
    from the youtube link it extracts audio in wav format
    and subtitles in .vtt format
    """

    ydl_opts = {
        'outtmpl': '%(id)s%(ext)s',
        'writeautomaticsub': True,
        'subtitlesformat': 'vtt',
        'subtitleslangs': [lang],

        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '0',
        }],

    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # 1. Just extract the info
        info_video = ydl.extract_info(
            link,
            download=False
        )
        video_title = info_video["title"]
        video_id = info_video["id"]

        # 2. Download video, audio and subs
        ydl.download([link])

    print("Video link: ", link)
    print("Video title: ", video_title)
    print("Video id: ", video_id)

    # 3. Move generated files to the correct dirs

    # 3.1. moving wav file
    wav_file_path_origin = "./wav"
    wav_file_path_destination = os.path.join(audios_path, video_id + ".wav")
    os.rename(wav_file_path_origin, wav_file_path_destination)

    # 3.2. moving subtitles file
    for dirpath, dirnames, filenames in os.walk("."):
        found_flag = False
        for file_name in filenames:
            if video_id in file_name and ".fr.vtt" in file_name:
                sub_file_path_origin = file_name
                found_flag = True
                break
        if found_flag:
            break
    sub_file_path_destination = os.path.join(subs_path, video_id + "." + lang + ".vtt")
    os.rename(sub_file_path_origin, sub_file_path_destination)

    return video_title, video_id
