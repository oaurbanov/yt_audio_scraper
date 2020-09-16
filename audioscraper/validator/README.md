# Validator project

It validates with external APIs the audios_word generated are correct.

## Deps

```
conda install --name audio_env -c conda-forge SpeechRecognition

#1.  I need to install and init the google cloud sdk
# https://cloud.google.com/sdk/docs/quickstart
conda install --name audio_env -c conda-forge google-cloud-sdk
gcloud init

#2. TODO: for using recognizer_instance.recognize_google_cloud
conda install --name audio_env -c conda-forge google-cloud-speech

conda install --name audio_env -c conda-forge google-cloud-texttospeech
conda install --name audio_env -c conda-forge google-api-python-client

---------------------

# Creating new env with python3.7, For being able to install google-cloud-speech, 
# For using recognizer_instance.recognize_google_cloud

conda create --name audio_py37 python=3.7
conda activate audio_py37

conda install -c conda-forge pydub
conda install -c conda-forge SpeechRecognition
conda install -c conda-forge google-api-python-client

conda install -c conda-forge google-cloud-sdk
gcloud init

conda install -c conda-forge oauth2client

# TODO: Exception when using the r.recognize_google_cloud API:
# googleapiclient.errors.UnknownApiNameOrVersion: name: speech  version: v1beta1
# https://stackoverflow.com/questions/60527135/google-speech-googleapiclient-errors-unknownapinameorversion-name-speech-ver

# Versions conflict, but Anyway I dont need it for now
conda install --name audio_py37 -c orc0 google-cloud-speech
```

## Issues

- Issue 001:
Problem when calling the Google Cloud Speech API.
During call to validator.recognize(api_number=2)
```
 Traceback (most recent call last):
   File "main.py", line 17, in <module>
     word_predicted = vl.recognize(AUDIO_PATH_OUT, GOOGLE_API_CREDENTIALS, api_number=2)
   File "/home/oscar/Mastering/AudioP_data/yotubeData/yt_audio_scraper/src/validator/validator.py", line 37, in recognize
     prediction = r.recognize_google_cloud(audio, json_dump, language=lang)
   File "/home/oscar/anaconda3/envs/audio_py37/lib/python3.7/site-packages/speech_recognition/__init__.py", line 832, in recognize_google_cloud
     speech_service = build("speech", "v1beta1", credentials=api_credentials, cache_discovery=False)
   File "/home/oscar/anaconda3/envs/audio_py37/lib/python3.7/site-packages/googleapiclient/_helpers.py", line 134, in positional_wrapper
     return wrapped(*args, **kwargs)
   File "/home/oscar/anaconda3/envs/audio_py37/lib/python3.7/site-packages/googleapiclient/discovery.py", line 294, in build
     raise UnknownApiNameOrVersion("name: %s  version: %s" % (serviceName, version))
 googleapiclient.errors.UnknownApiNameOrVersion: name: speech  version: v1beta1
```




