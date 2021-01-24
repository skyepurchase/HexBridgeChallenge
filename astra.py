import pickle
import base64

from scipy.sparse.csr import csr_matrix

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


storage = [
        ({}, csr_matrix([1, 0, 0, 0, 0, 0, 0, 0])),
        ({}, csr_matrix([0, 0, 1, 0, 0, 0, 0, 0]))
]



def run_command(cmd):
    try:
        cloud_config = {
                'secure_connect_bundle': './secure-connect-hexbridgechallenge.zip'
        }
        auth_provider = PlainTextAuthProvider('hexbridge', 'password1')
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect()

        rows = session.execute(cmd).all()
        return rows
    except:
        print("An error has occurred")
        return None


def test_connection():
    rows = run_command("select release_version from system.local")
    if rows:
        print("Connection ok.")


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
    print(load_user('test'))
    print(load_all_users())
