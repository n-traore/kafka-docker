# -*-coding:utf-8 -*s

import socket
import platform as p
import time
import datetime



# Date d'ajout de titre la plus récente dans la playlist

def date_dernier_ajout(playlist):
    dt_dernier_ajout = []

    for d in range(0, playlist["nbTracks"]):
        dt_dernier_ajout.append(playlist["tracks"][d]["added_at"])

    dt_dernier_ajout_max = max(dt_dernier_ajout)

    return dt_dernier_ajout_max
