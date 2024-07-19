import textwrap
import json
import os
import keyboard
import time
import pathlib

from IPython.display import display
from IPython.display import Markdown

from speech import SpeechToTextManager

import google.generativeai as genai


BACKUP_FILE = "ChatHistoryBackup.txt"


with open('key.json') as f:
    keys = json.load(f)

# Access individual keys
gemini = keys['gemini']

genai.configure(api_key=gemini)


model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])


speechtotext_manager = SpeechToTextManager()


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



response = chat.send_message("make all the response concise and in less than 5 sentences unless asked for")



print("[green]Starting the loop, press F4 to begin")
while True:
    # Wait until user presses "f4" key
    if keyboard.read_key() != "f4":
        time.sleep(0.1)
        continue

    print("[green]User pressed F4 key! Now listening to your microphone:")

    # Get question from mic
    mic_result = speechtotext_manager.speechtotext_from_mic_continuous()
    
    if mic_result == '':
        print("[red]Did not receive any input from your microphone!")
        continue

    # Send question to OpenAi
    response = chat.send_message(mic_result, stream=True)
    
    response.resolve()
    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(response))
    to_markdown(response.text)
    print(response.text)
    speech_synthesis_result = speechtotext_manager.speech_synthesizer.speak_text_async(response.text)
    

    print("[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")
    