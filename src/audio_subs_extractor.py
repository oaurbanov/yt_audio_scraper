import pprint

import youtube_dl


def download_audios_and_subs(link, lang, audios_path, subs_path) :

    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    with ydl:
        info_video = ydl.extract_info(
            link,
            download=False # We just want to extract the info
        )

    # print(type(info_video))
    # pprint.pprint(info_video)

    print(link)
    print(info_video["title"])

    return info_video["title"]