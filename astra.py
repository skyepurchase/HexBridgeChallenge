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
        print(f"An error has occurred for '{cmd}'")
        return None


def test_connection():
    rows = run_command("select release_version from system.local")
    if rows:
        print("Connection ok.")


def save_user(id, data):
    data_string = base64.b64encode(pickle.dumps(data)).decode("ascii")
    run_command(f"INSERT INTO \"HexBridge\".tbl (twitter, reddit, pickle) VALUES('{id['twitter']}', '{id['reddit']}', textAsBlob('{data_string}'))")


def load_user(id):
    rows = run_command(f"select pickle from \"HexBridge\".tbl where twitter = '{id['twitter']}' and reddit = '{id['reddit']}';")
    data = pickle.loads(base64.b64decode(rows[0][0]))
    return data


def load_all_users():
    rows = run_command("select * from \"HexBridge\".tbl;")
    return [({'twitter': row[0], 'reddit': row[1]}, pickle.loads(base64.b64decode(row[2]))) for row in rows]


if __name__ == "__main__":
    test_connection()
    # save_user({'twitter': 'asdf', 'reddit': 'qwer'}, [1, 2, 3, 4])
    # save_user({'twitter': 'test', 'reddit': 'test'}, [9, 8, 7, 6])
    print(load_user({'twitter': 'test', 'reddit': 'test'}))
    print(load_all_users())
