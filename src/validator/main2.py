

# samples per second
SAMPLE_RATE = 22050

AUDIO_PATH_IN = "../../dataSets/conversation/0.wav"
AUDIO_PATH_OUT = "../../dataSets/conversation/B_0.wav"

from pydub import AudioSegment
sound = AudioSegment.from_file(AUDIO_PATH_IN)

print("----------Before Conversion--------")
print("Frame Rate", sound.frame_rate)
print("Channel", sound.channels)
print("Sample Width",sound.sample_width)

# Change Frame Rate
sound = sound.set_frame_rate(SAMPLE_RATE)

# Change Channel
sound = sound.set_channels(1)

# Change Sample Width

# 1 : “8 bit Signed Integer PCM”,
# 2 : “16 bit Signed Integer PCM”,
# 3 : “32 bit Signed Integer PCM”,
# 4 : “64 bit Signed Integer PCM”

sound = sound.set_sample_width(3)

# Export the Audio to get the changed content
sound.export(AUDIO_PATH_OUT, format ="wav")




# import librosa
# output_istft, sr = librosa.load(AUDIO_PATH_IN, SAMPLE_RATE)
# import pysndfile
# pysndfile.sndio.write(AUDIO_PATH_OUT, output_istft, rate=SAMPLE_RATE, format='wav', enc='pcm16')
#
#
import speech_recognition as sr

print(sr.__version__)

r = sr.Recognizer()


harvard = sr.AudioFile(AUDIO_PATH_OUT)
with harvard as source:
    audio = r.record(source)
    o = r.recognize_google(audio, language='fr-FR')

print(o)
