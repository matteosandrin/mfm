import json
import os.path

episodes = json.load(open('mfm-feed.json'))

print(len(episodes))

for e in episodes:
    if not os.path.exists('episodes/'+e['audio_file']):
        print(e)