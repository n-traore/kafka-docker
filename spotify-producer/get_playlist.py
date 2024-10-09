# -*-coding:Utf-8 -*s

"""
Script permettant les appels à l'API Spotify afin de récupérer
les données de playlists
"""

import os
import time
import json
import base64
import requests



#--------------- VARIABLES D'ENVIRONNEMENT ---------------#
### Client
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

### API spotify
SPOTIFY_TOKEN_URL = os.environ.get('SPOTIFY_TOKEN_URL')
SPOTIFY_API_BASE_URL = os.environ.get('SPOTIFY_API_BASE_URL')
API_VERSION = os.environ.get('API_VERSION')
ENDPOINT_TO_REACH = os.environ.get('ENDPOINT_TO_REACH')
SPOTIFY_API_URL = "{}/{}/{}/".format(SPOTIFY_API_BASE_URL, API_VERSION, ENDPOINT_TO_REACH)
GRANT_TYPE = os.environ.get('GRANT_TYPE')

base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode()).decode()
AUTORISATION = "Basic {}".format(base64encoded)

HEADER_AUTH_PARAMS = {"grant_type": GRANT_TYPE}
AUTH_PARAMS = {"Authorization": AUTORISATION}


# Demande d'autorisation au serveur spotify : renvoie un token d'accès
reponse = {}

def request_access_token():
    global reponse

    requete_auth = requests.post(SPOTIFY_TOKEN_URL, data=HEADER_AUTH_PARAMS, headers=AUTH_PARAMS)
    req_time = time.time()

    # Vérification du statut de la requête
    if requete_auth.status_code == 200:
        reponse = json.loads(requete_auth.text)
        reponse["req_time"] = req_time
        return reponse
    return "Erreur Statut {} : raison {}".format(requete_auth.status_code, requete_auth.reason)


# Vérifier la validité du token
def is_expired_access_token():
    token_expired = time.time() - reponse["req_time"] >= reponse["expires_in"]
    return token_expired


# Récupérer les informations (type et token d'accès)
def get_access_token():
    """
    Vérifier si un token est en mémoire, si oui vérifier qu'il est encore valide
    et le retourner si c'est le cas
    Sinon, récupérer un nouveau token d'accès à partir de la fonction 1 et le retourner
    """

    if reponse and not is_expired_access_token():
        access_token = reponse["access_token"]
        token_type = reponse["token_type"]
        return token_type, access_token

    access_token = request_access_token()["access_token"]
    token_type = request_access_token()["token_type"]

    return token_type, access_token


# Récupérer les données de la playlist
def get_playlist_data(PLAYLIST_ID):
    info_token = get_access_token()
    TOKEN_PARAMS = {"Authorization": "{} {}".format(info_token[0], info_token[1])}

    requete_playlist = requests.get(SPOTIFY_API_URL+"{}".format(PLAYLIST_ID), headers=TOKEN_PARAMS)
    playlist_data_full = json.loads(requete_playlist.text)

    playlist_data_vf = {"collaborative": playlist_data_full["collaborative"],
                        "description": playlist_data_full["description"],
                        "followers": playlist_data_full["followers"]["total"],
                        "id": playlist_data_full["id"],
                        "name": playlist_data_full["name"],
                        "owner": playlist_data_full["owner"]["display_name"],
                        "public": playlist_data_full["public"],
                        "snapshot_id": playlist_data_full["snapshot_id"],
                        "tracks": playlist_data_full["tracks"]["items"],
                        "nbTracks": playlist_data_full["tracks"]["total"],
                        "uri": playlist_data_full["uri"]
                        }
    return playlist_data_vf
