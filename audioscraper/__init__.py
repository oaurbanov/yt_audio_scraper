from .scraper.audio_subs_downloader import old_download_audios_and_subs
from .scraper.audio_subs_downloader import download_audios_and_subs
from .scraper.audio_subs_downloader import get_main_info_video
from .scraper.audio_subs_downloader import get_videos_infos_list_from_link

from .scraper.audio_words_generator import generate_audio_words_per_link
from .scraper.audio_words_generator import get_not_yet_scraped_videos
from .scraper.audio_words_generator import generate_audio_words_per_file

# from .scraper.audio_analyser import store_audio_file
# from .scraper.audio_analyser import load_audio_signal
from .scraper import audio_analyser
from .dictionary import white_list

from .validator.validator import recognize_audio_file
