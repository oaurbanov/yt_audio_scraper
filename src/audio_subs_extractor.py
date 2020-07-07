
import youtube_dl
import os


def download_audios_and_subs(link, lang, audios_path, subs_path) :
    '''
    from the youtube link it extracts audio in wav format 
    and subtitles in .vtt format
    '''

    ydl_opts = {
        'outtmpl': '%(id)s%(ext)s',
        'writeautomaticsub' : True,
        'subtitlesformat' : 'vtt',
        'subtitleslangs' : [lang],

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
    wav_file_path_destination = os.path.join(audios_path, video_id+".wav" )
    os.rename(wav_file_path_origin,wav_file_path_destination)

    # 3.1. moving subtitles file
    for dirpath, dirnames, filenames in os.walk(".") :
        found_flag = False
        for file_name in filenames:
            if video_id in file_name and ".fr.vtt" in file_name :
                sub_file_path_origin = file_name
                found_flag = True
                break
        if found_flag :
            break
    sub_file_path_destination = os.path.join(subs_path, video_id+".fr.vtt" )
    os.rename(sub_file_path_origin,sub_file_path_destination)


    return video_title, video_id