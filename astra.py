import pickle
import base64

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


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
    data_string = base64.b64encode(pickle.dumps(data)).decode("ascii")
    run_command(f"INSERT INTO \"HexBridge\".wordcounts (id, pickle) VALUES('{twitter_id}', textAsBlob('{data_string}'))")


def load_user(twitter_id):
    rows = run_command(f"select pickle from \"HexBridge\".wordcounts where id = '{twitter_id}';")
    data = pickle.loads(base64.b64decode(rows[0][0]))
    return data


def load_all_users():
    rows = run_command("select * from \"HexBridge\".wordcounts;")
    return {row[0]: pickle.loads(base64.b64decode(row[1])) for row in rows}


if __name__ == "__main__":
    test_connection()
    print(load_user('test'))
    print(load_all_users())
