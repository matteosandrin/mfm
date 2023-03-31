from datetime import datetime
from pyannote.audio import Pipeline
import json
import os
import requests
from mfm_xml import get_mfm_feed

PUSHOVER_TOKEN = os.getenv('PUSHOVER_TOKEN')
PUSHOVER_USER = os.getenv('PUSHOVER_USER')
START_EP_ID = os.getenv('START_EP_ID')
HF_ACCESS_TOKEN = os.getenv('HF_ACCESS_TOKEN')

if PUSHOVER_TOKEN is None or \
   PUSHOVER_USER is None or \
   START_EP_ID is None or \
   HF_ACCESS_TOKEN is None:
    print("ERROR: missing environment variables")
    exit(1)

START_EP_ID = int(START_EP_ID, 10)

def notify(message):
    params = {
        "token" : PUSHOVER_TOKEN,
        "user" : PUSHOVER_USER,
        "message" : message
    }
    requests.post("https://api.pushover.net/1/messages.json", params=params)

episodes = get_mfm_feed()
print("[+] There are {} episodes in the feed".format(len(episodes)))
print("[+] Starting with episode {}...".format(START_EP_ID))

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                    use_auth_token=HF_ACCESS_TOKEN)

for i, ep in enumerate(episodes):

    if i+1 < START_EP_ID:
        continue

    filename = ep['audio_file']

    start = datetime.now()
    print("[+] Starting on episode {} at: {}".format(i+1, start.isoformat()))
    
    print("[+] Downloading episode {}".format(i+1))
    os.system('wget "{}" -nv -O {}.mp3'.format(ep['audio_url'], filename))

    print("[+] Converting episode {}".format(i+1))
    os.system('ffmpeg -i {}.mp3 -acodec pcm_s16le -ac 1 -ar 16000 -y -hide_banner -loglevel error {}.wav'.format(
        filename, filename))

    print("[+] Analyzing episode {}".format(i+1))

    diarization = pipeline(
        "{}.wav".format(filename),
        min_speakers=1,
        max_speakers=4)

    result = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        result.append({
            "speaker" : speaker,
            "start" : turn.start,
            "end" : turn.end,
        })
        # print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")

    output_filename = "out/{}.json".format(filename)

    with open(output_filename, "w") as f:
        print("[+] Writing result to", output_filename)
        f.write(json.dumps(result, indent=4, sort_keys=True))

    os.system('rm {}.mp3'.format(filename))
    os.system('rm {}.wav'.format(filename))

    delta = datetime.now() - start
    print("[+] End episode {}. Time delta: {}".format(i+1, delta))
    print("[+]")

    if i % 25 == 0:
        notify("MFM GPU has finished episode {}/{}".format(i+1, len(episodes)))

print("[+] All done!")
notify("MFM GPU is all done!")