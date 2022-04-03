import os
import requests
from requests.sessions import Session
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread,local
import json
import random
import sys

url = "https://cemantix.herokuapp.com/score"
words = "liste.de.mots.francais.frgut.txt"
limit = 900
message = ""

with open(words, "r") as file:
    word_list = file.readlines()
    #random.shuffle(word_list)

thread_local = local()

def get_session() -> Session:
    if not hasattr(thread_local,'session'):
        thread_local.session = requests.Session()
    return thread_local.session

def submit_word(word:str):
    global message
    session = get_session()
    with session.post(url, data={'word': word.strip()}) as response:
        try:
            if json.loads(response.text)['percentile'] > limit:
                print(f"{word.strip()}: {response.text}")
                if json.loads(response.text)['percentile'] == 1000:
                    end = time.time()
                    message = f"The word is {word.strip()}, founded in {end - start} seconds"
        except:
            pass
        # print(f"{word.strip()}: {response.text}")
        if response.status_code != 200:
            print(f"{word.strip()}: {response.text}")


def submit_all(words:list) -> None:
    with ThreadPoolExecutor(max_workers=200) as executor:
        executor.map(submit_word,words)

start = time.time()
submit_all(word_list)
end = time.time()
print(message)
print(f"Total time: {end - start} seconds")
