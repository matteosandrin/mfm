from datetime import datetime
import json
import os.path
import requests
import xml.etree.ElementTree

def get_mfm_feed(writeToFile=False):

    feed_data = requests.get("https://feeds.megaphone.fm/HS2300184645")

    tree = xml.etree.ElementTree.fromstring(feed_data.text)
    episodes = tree.findall('./channel/item')

    episodes = episodes[::-1]

    result = []

    for i, episode in enumerate(episodes):
        air_date = datetime.strptime(
            episode.find('pubDate').text,
            '%a, %d %b %Y %H:%M:%S %z')
        episode_json = {
            'title' : episode.find('title').text,
            'audio_url' : episode.find('enclosure').get('url'),
        }
        episode_json['audio_file'] = "mfm_{:04}_{}".format(
            i+1,
            air_date.strftime("%Y_%m_%d"))
        episode_json['date'] = air_date.isoformat()
        result.append(episode_json)

    if writeToFile:
        with open('mfm-feed.json', 'w') as f:
            json.dump(result, f, sort_keys=True, indent=4)
    return result

if __name__ == "__main__":
    get_mfm_feed(True)