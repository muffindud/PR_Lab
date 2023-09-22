import xml.etree.ElementTree as ET
from typing import List
import player_pb2 as PlayerProto

from player import Player


class PlayerFactory:
    def to_json(self, players: List[Player]):
        dump = []
        for player in players:
            dump.append(
                {
                    "nickname": player.nickname,
                    "email": player.email,
                    "date_of_birth": player.date_of_birth.strftime("%Y-%m-%d"),
                    "xp": player.xp,
                    "class": player.cls
                }
            )
        return dump

    def from_json(self, dicts: List[dict]):
        dump = []
        for dict in dicts:
            dump.append(
                Player(
                    nickname=dict["nickname"],
                    email=dict["email"],
                    date_of_birth=dict["date_of_birth"],
                    xp=dict["xp"],
                    cls=dict["class"]
                )
            )
        return dump

    def to_xml(self, players: List[Player]):
        dump = []
        for player in players:
            dump.append(
                {
                    "nickname": player.nickname,
                    "email": player.email,
                    "date_of_birth": player.date_of_birth.strftime("%Y-%m-%d"),
                    "xp": player.xp,
                    "class": player.cls
                }
            )
        root = ET.Element("data")
        for player in dump:
            child = ET.SubElement(root, "player")
            for key, value in player.items():
                subchild = ET.SubElement(child, key)
                subchild.text = str(value)
        return ET.tostring(root, encoding="unicode")

    def from_xml(self, xml_str: str):
        root = ET.fromstring(xml_str)
        dicts = []
        dump = []
        for child in root:
            dict = {}
            for subchild in child:
                dict[subchild.tag] = subchild.text
            dicts.append(dict)
        for dict in dicts:
            dump.append(
                Player(
                    nickname=dict["nickname"],
                    email=dict["email"],
                    date_of_birth=dict["date_of_birth"],
                    xp=int(dict["xp"]),
                    cls=dict["class"]
                )
            )
        return dump

    def from_protobuf(self, binary_str: bytes):
        player_list = PlayerProto.PlayersList()
        player_list.ParseFromString(binary_str)

        dump = []
        for player in player_list.player:
            dump.append(
                Player(
                    nickname=player.nickname,
                    email=player.email,
                    date_of_birth=player.date_of_birth,
                    xp=player.xp,
                    cls=PlayerProto.Class.Name(player.cls)
                )
            )

        return dump

    def to_protobuf(self, list_of_players: List[Player]):
        player_list = PlayerProto.PlayersList()
        # classes = {value: key for key, value in PlayerProto.Class.items()}

        for player in list_of_players:
            player_proto = player_list.player.add()
            player_proto.nickname = player.nickname
            player_proto.email = player.email
            player_proto.date_of_birth = player.date_of_birth.strftime("%Y-%m-%d")
            player_proto.xp = player.xp
            # player_proto.cls = classes[player.cls]
            player_proto.cls = PlayerProto.Class.Value(player.cls)

        return player_list.SerializeToString()
