# package webradio_metadata/webradio_metadata.py

# Scraps webradio metadatas

import sys
import requests
import time
import json
#import subprocess
from streams_url import streamsurl

def main():
  name = sys.argv[1]
  url = streamsurl[name]['url']
  parser =  streamsurl[name]['parser']

  while True:
      try:
          data = requests.get(url).json()
          func = globals()[parser]
          metadata = func(data)
          print( json.dumps(metadata) )
          return
      except Exception:
          time.sleep(2)
          continue

def fip(data):
    level = data['levels'][0]
    uid = level['items'][level['position']]
    metadata = data['steps'][uid]
    return { 'title': metadata['title'], 'artist': metadata['authors'], 'annee': metadata['anneeEditionMusique'], 'cover': metadata['visual'] }

def france_inter(data):
    seconds = time.time()
    metadata = {'artist': None, 'title': None, 'annee': None, 'cover': None}
    for item in data:
        if seconds > item['start'] and seconds < item['end']:
            if 'conceptParentTitle' in item:
                 metadata['artist'] = item["conceptParentTitle"];

            metadata['title'] = item['conceptTitle']
            if 'expressionTitle' in item :
                metadata['title'] += " - " + item['expressionTitle']

            return metadata

if __name__== "__main__":
  import traceback
  try:
      main()
  except:
      with open('/tmp/fip-crash.log', 'w') as f:
          traceback.print_exc(file=f)
