# -*-coding:Utf-8 -*s

import os
import json
import datetime
from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from check_playlist import date_dernier_ajout


KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
SPOTIFY_TOPIC = os.environ.get('SPOTIFY_TOPIC')
CASSANDRA_CLUSTER_IPS = os.environ.get('CASSANDRA_CLUSTER_IPS').split(',')


# Connexion au cluster cassandra
cluster = Cluster(CASSANDRA_CLUSTER_IPS)
session = cluster.connect("sink")
insertion_cass = session.prepare('INSERT INTO spotify_playlist JSON ?')
verif_playlist_existante = session.prepare('SELECT id FROM spotify_playlist WHERE id = ?')


# Consumer : lit les messages du topic et les envoie dans cassandra
if __name__ == '__main__':
    consumer = KafkaConsumer(SPOTIFY_TOPIC, bootstrap_servers=KAFKA_BROKER_URL, group_id="spotify-group-1", value_deserializer=lambda value: json.loads(value))

    for message in consumer:
        p = message.value
        print(p)
        p_id = p["id"]

        if (session.execute(verif_playlist_existante, [p_id]) == p_id
        and date_dernier_ajout(p) < datetime.datetime.utcnow().replace(hour=0,minute=0,second=0,microsecond=0).timestamp()
        ):
            continue
        else:
            #### Insertion dans Cassandra
            session.execute(insertion_cass, [json.dumps(p)])
