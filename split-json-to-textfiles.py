import os
import json
import re
import sys
from datetime import datetime

translation_table = str.maketrans({
        "\n": "_",
        " ": "_",
        "/": "_",
        "[": "_",
        "]": "_",
        ":": "_",
        "'": "",
        "\"": "",
        "(": "",
        ")": "",
        ".": "",
        ",": ""
    })

def convert_date(event_date):
    year = event_date.get("year", "")
    month = ("0" + str(event_date.get("month", "0")))[-2:]
    day = ("0" + str(event_date.get("day", "00")))[-2:]
    return (f"{year}-{month}-{day}").replace("-00", "")


def remove_last_anchor_tag(text):
    # Define the regular expression pattern to find the last <a> tag with &#9998;
    pattern = r'<a [^>]*>&#9998;</a>'

    # Find all matches
    matches = list(re.finditer(pattern, text))

    if matches:
        # Get the last match
        last_match = matches[-1]
        # Remove the last match from the string
        text = text[:last_match.start()] + text[last_match.end():]

    return text.strip();


def sort_cr_delimited_string(input_string):
    # Split the input string by carriage returns
    lines = input_string.split('\n')

    # Remove blank lines
    lines = [line for line in lines if line.strip()]

    # Sort the lines alphabetically
    sorted_lines = sorted(lines)

    # Join the sorted lines back into a single string with CR delimiters
    sorted_string = '\n'.join(sorted_lines)

    return sorted_string

def create_text_file(event, directory):
    start_date = convert_date(event.get('start_date', {}))
    title = event.get('title', {}).get('text', {}).get('headline', 'untitled').replace(' ', '-').lower()

    file_content = ""
    for key, value in event.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, dict):
                    for sub_sub_key, sub_sub_value in sub_value.items():
                        file_content += f"{key}_{sub_key}_{sub_sub_key}: {sub_sub_value}\n"
                else:
                    if sub_key == 'text':
                        sub_value = remove_last_anchor_tag(sub_value.replace("\n", " "))
                    file_content += f"{key}_{sub_key}: {sub_value}\n"

                if f"{key}_{sub_key}" == "text_headline":
                    title = sub_value.translate(translation_table)
                    # Replace consecutive underscores with a single underscore
                    title = "_".join(filter(None, title.split("_")))
        else:
            file_content += f"{key}: {value}\n"

    if start_date == "":
        file_name = f"0.txt"
    else:
        file_name = f"{start_date}-{title}.txt"
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(sort_cr_delimited_string(file_content))

def split_json_to_files(json_path, directory):
    with open(json_path, 'r', encoding='utf-8') as json_file:
        timeline_data = json.load(json_file)

    events = timeline_data.get('events', [])
    if not os.path.exists(directory):
        os.makedirs(directory)

    for event in events:
        create_text_file(event, directory)

    # Handling the "title" field at the peer level of "events"
    title = timeline_data.get('title', {})
    if title:
        create_text_file({"title": title}, directory)

# Path to the JSON file
json_path = sys.argv[1]

# Directory to store the text files
directory = sys.argv[2]

# Split the JSON file into text files
split_json_to_files(json_path, directory)
