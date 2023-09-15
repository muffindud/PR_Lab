from typing import List

from player import Player
import xml.etree.ElementTree as ET


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

    def from_protobuf(self, binary_str: str):
        ...

    def to_protobuf(self, list_of_players: List[Player]):
        ...
