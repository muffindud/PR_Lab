# main.py
import sys

from src.FlaskInstance import FlaskInstance, app
from src.RAFT import RAFT


flask_configs = [
    {
        "host": "127.0.0.1",
        "port": 5001,
        "db_uri": "postgresql://postgres:postgres@localhost:5432/scooters1",
    },
    {
        "host": "127.0.0.1",
        "port": 5002,
        "db_uri": "postgresql://postgres:postgres@localhost:5432/scooters2",
    },
    {
        "host": "127.0.0.1",
        "port": 5003,
        "db_uri": "postgresql://postgres:postgres@localhost:5432/scooters3",
    }
]

raft_config = {
    "host": "127.0.0.1",
    "port": 5000,
    "instance_ct": 3
}


def main(flask_instance: int):
    raft = RAFT(
        raft_config["host"],
        raft_config["port"],
        raft_config["instance_ct"],
        flask_configs[flask_instance]
    )

    flask_params = raft.server_params
    # print(flask_params)

    role = "main" if "token" in flask_params.keys() else "backup"
    token = None if "token" not in flask_params.keys() else flask_params["token"]
    token = token if token is not None else raft.main_params["token"]

    follower_instances = None
    if role == "main":
        follower_instances = raft.backup_params
        # print(follower_instances)

    flask_app = FlaskInstance(
        flask_configs[flask_instance]["host"],
        flask_configs[flask_instance]["port"],
        flask_configs[flask_instance]["db_uri"],
        role,
        token,
        follower_instances
    )


if __name__ == "__main__":
    main(int(sys.argv[1]))
