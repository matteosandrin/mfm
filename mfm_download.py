import json
import requests
import time

episodes = json.load(open('mfm-feed.json'))

for i,e in enumerate(episodes):
    print('[{:03}/{:03}] Downloading episode "{}"'.format(
        i,
        len(episodes),
        e['title']))
    with open('episodes/'+e['audio_file'], 'wb') as f:
        audio_file = requests.get(e['audio_url'])
        f.write(audio_file.content)
    print("Done")
    time.sleep(1)