import io
import numpy as np
import pickle
import base64

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from scipy.sparse.csr import csr_matrix


storage = [
        ({}, csr_matrix([1, 0, 0, 0, 0, 0, 0, 0])),
        ({}, csr_matrix([0, 0, 1, 0, 0, 0, 0, 0]))
]



def run_command(cmd):
    cloud_config = {
            'secure_connect_bundle': './secure-connect-hexbridgechallenge.zip'
    }
    auth_provider = PlainTextAuthProvider('hexbridge', 'password1')
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()

    row = session.execute(cmd).one()
    return row


def test_connection():
    row = run_command("select release_version from system.local")
    if row:
        print(row[0])
    else:
        print("An error has occured")


def save_user(twitter_id, data):
    #data_string = base64.b64encode(pickle.dumps(data)).decode("ascii")
    #run_command(f"INSERT INTO \"HexBridge\".wordcounts (id, pickle) VALUES('{twitter_id}', textAsBlob('{data_string}'))")
    storage.append((twitter_id, data))


def load_user(twitter_id):
    #row = run_command(f"select pickle from \"HexBridge\".wordcounts where id = '{twitter_id}';")
    #data = pickle.loads(base64.b64decode(row[0]))
    #print(data)
    #return data
    pass

def load_all_users():
    return storage

if __name__ == "__main__":
    test_connection()
    load_user('test')
