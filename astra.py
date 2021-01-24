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
        session.default_timeout = 60

        rows = session.execute(cmd).all()
        return rows
    except:
        print(f"An error has occurred for '{cmd}'")
        return None


def test_connection():
    rows = run_command("select release_version from system.local")
    if rows:
        print("Connection ok.")


def save_user(id, data):
    data_string = base64.b64encode(pickle.dumps(data)).decode("ascii")
    if 'reddit' in id:
        run_command(f"INSERT INTO \"HexBridge\".wordcount (social, username, pickle) VALUES(0, '{id['reddit']}', textAsBlob('{data_string}'))")
    if 'twitter' in id:
        run_command(f"INSERT INTO \"HexBridge\".wordcount (social, username, pickle) VALUES(1, '{id['twitter']}', textAsBlob('{data_string}'))")


def load_all_users():
    rows = run_command("select * from \"HexBridge\".wordcount;")
    if not rows:
        print("An error has occured. No rows fetched.")
        return []
    ret = [({'reddit' if row[0] == 0 else 'twitter': row[1]}, pickle.loads(base64.b64decode(row[2]))) for row in rows]
    print(f"{len(ret)} rows fetched from database.")
    return ret

if __name__ == "__main__":
    test_connection()
    # save_user({'twitter': 'test', 'reddit': 'test1'}, [9, 8, 7, 6])
    # save_user({'twitter': 'test'}, [1, 2, 3, 4])
    # save_user({'reddit': 'test'}, [2, 0, 2, 1])
    print(load_all_users())
