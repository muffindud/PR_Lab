from player import Player


class PlayerFactory:
    def to_json(self, player: Player):
        ...

    def from_json(self, json_str: str):
        ...

    def from_xml(self, xml_str: str):
        ...

    def to_xml(self, list_of_players: List[Player]):
        ...

    def from_protobuf(self, binary_str: str):
        ...

    def to_protobuf(self, list_of_players: List[Player]):
        ...
