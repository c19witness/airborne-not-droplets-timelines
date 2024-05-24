import os
import json
import sys
from datetime import datetime

def parse_event_file(file_path):
    title = {}
    event = {
        "media": {},
        "start_date": {},
        "end_date": {},
        "text": {}
    }
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if ': ' in line:
                key = line.strip().split(':')[0]
                value = line[len(key)+1:].strip()
                key = key.strip()

                if key == 'start_date_year':
                    if value != "":
                        event["start_date"]["year"] = int(value)
                elif key == 'start_date_month':
                    if value != "":
                        event["start_date"]["month"] = int(value)
                elif key == 'start_date_day':
                    if value != "":
                        event["start_date"]["day"] = int(value)
                elif key == 'end_date_year':
                    if value != "":
                        event["end_date"]["year"] = int(value)
                elif key == 'end_date_month':
                    if value != "":
                        event["end_date"]["month"] = int(value)
                elif key == 'end_date_day':
                    if value != "":
                        event["end_date"]["day"] = int(value)
                elif key.startswith('text_'):
                    if key[5:] == "text":
                        value = value + " <a href='https://github.com/c19witness/airborne-not-droplets-timelines/edit/main/./" + "/".join(file_path.split("/")[-2:]) + "'>&#9998;</a>"

                    event['text'][key[5:]] = value

                elif key.startswith('media_'):
                    event['media'][key[6:]] = value
                else:
                    event[key] = value
        if event["end_date"] == {}:
            event.pop("end_date")
        if event["start_date"] == {}:
            event.pop("start_date")
    return event

def parse_title_file(file_path):

    title = { "media": {}, "text": {} }
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if ': ' in line:
                key = line.strip().split(': ')[0]
                try:
                    value = line.strip().split(': ')[1]
                except IndexError:
                    value = None
                if key == 'title_media_url':
                    title["media"]["url"] = value
                elif key == 'title_media_caption':
                    title["media"]["caption"] = value
                elif key == 'title_media_thumbnail':
                    title["media"]["thumbnail"] = value
                elif key == 'title_media_credit':
                    title["media"]["credit"] = value
                elif key == 'title_text_headline':
                    title["text"]["headline"] = value
                elif key == 'title_text_text':
                        title["text"]["text"] = value
                else:
                    if value is not None:
                        title[key] = value
    return title

def convert_files_to_json(directory):
    title = {}
    events = []
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if file_name == '0.txt':
            title = parse_title_file(file_path)
        elif file_name.endswith('.txt'):
            event = parse_event_file(file_path)
            events.append(event)

    timeline_json = {"title": title, "events": events}
    with open(sys.argv[2], 'w', encoding='utf-8') as json_file:
        json.dump(timeline_json, json_file, indent=2)


# Set the directory containing the text files
directory = sys.argv[1]

# Convert the text files to JSON
convert_files_to_json(directory)
