#!/usr/bin/python

import sys, getopt
from google.cloud import storage
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.oauth2 import service_account
from google.cloud import texttospeech
import youtube_dl
import ffmpeg
import glob,os
import wave
from pydub import AudioSegment

def cleangoogleStorage(storage_client,bucket):
   
   print("listing files in the bucket..")

   files = bucket.list_blobs()
   fileList = [file.name for file in files if '.' in file.name]
   for filename in fileList:
      print("deleting file..",filename)
      bucket.delete_blob(filename)
   return bucket

def uploadgooglestorage(bucket,filewav):
   blob = bucket.blob(filewav)
   print("uploading wave file to google storage bucket..")
   blob.upload_from_filename(filewav)
   print("file succesfuly uploaded")
   return

def youtubedownload(youtubeurl):

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtubeurl])

def converttomono(audio_file_name):
    print("converting to mono audiofile..")
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav") 
    return

def getfilewav():

   for file in glob.glob("*.wav"):
      print(file)
      filewav=file

      print("calculation frame_rate and channels..")

      with wave.open(filewav, "rb") as wave_file:
         frame_rate = wave_file.getframerate()
         channels = wave_file.getnchannels()
      
      if channels > 1:
         converttomono(filewav)

   
   return filewav,frame_rate,channels


def speechtotext(bucketname,filewav,frame_rate,language):
   gcs_uri ="gs://"+bucketname+"/"+filewav
   print("gcs_uri",gcs_uri)

   transcript = ''

   client = speech.SpeechClient.from_service_account_json('google.json')

   audio = types.RecognitionAudio(uri=gcs_uri)

   config = types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
   sample_rate_hertz=frame_rate,enable_word_time_offsets=True,
   language_code=language)

   f= open("output.json","w+")

   print("Recognizing:")

   operation = client.long_running_recognize(config, audio)
   response = operation.result(timeout=10000)

   print("Recognized")

   for result in response.results:
      alternative = result.alternatives[0]
      print('Transcript: {}'.format(alternative.transcript))
      print('Confidence: {}'.format(alternative.confidence))


      for word_info in alternative.words:
         word = word_info.word
         start_time = word_info.start_time
         end_time = word_info.end_time
         if len(word)>=4:
            print("{\"word\":\"%s\",\"start\":%4.1f}" % (word,start_time.seconds + start_time.nanos * 1e-9),file=f)



   f.close()

def cleanlocalfiles():
   for file in glob.glob("*.wav"):
      print("deleting intermediate files..",file)
      os.remove(file)


def main(argv):
   inputfile = ''
   language = ''
   try:
      opts, args = getopt.getopt(argv,"hi:l:",["ifile=","llannguage="])
   except getopt.GetoptError:
      print ('transcribe.py -i <inputfile> -l <language>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('transcribe.py -i <inputfile> -l <language>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-l", "--llanguage"):
         language = arg

   if not inputfile or not language:
      print ('usage: transcribe.py -i <inputfile> -l <language>')
      quit()

   print ('Input file is :', inputfile)
   print ('Language is :', language)

   bucketname='smartlab'
   storage_client = storage.Client.from_service_account_json('google.json')
   bucket = storage_client.get_bucket(bucketname)
   cleangoogleStorage(storage_client,bucket)
   youtubedownload(inputfile)
   filewav,frame_rate,channels=getfilewav()
   uploadgooglestorage(bucket,filewav)
   speechtotext(bucketname,filewav,frame_rate,language)
   cleangoogleStorage(storage_client,bucket)
   cleanlocalfiles()
   



if __name__ == "__main__":
   main(sys.argv[1:])