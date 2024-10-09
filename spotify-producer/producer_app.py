# -*-coding:Utf-8 -*s

#--------------- IMPORTS ---------------#
import os
import json
from kafka import KafkaProducer
from time import sleep
import get_playlist as g_pl


ls_spotify_playlist = os.environ.get('SPOTIFY_PLAYLISTS').split(',')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
SPOTIFY_TOPIC = os.environ.get('SPOTIFY_TOPIC')


# Création du producer pour l'envoi des messages
if __name__ == '__main__':
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL, value_serializer=lambda value: json.dumps(value).encode("utf-8"))
    while True:
        for p in ls_spotify_playlist:
            message = g_pl.get_playlist_data(p)
            producer.send(SPOTIFY_TOPIC, value=message)
            print(message)
            sleep(10)
