from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING


class GameCommandPacket(PacketType):
    DEFINITION_IDENTIFIER = "20194.exercise6.gameclient"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("command", STRING),
    ]

    @classmethod
    def create_game_command_packet(cls, s):
        print("15:" +s)
        return cls(command=s)

    def command(self):
        return self.command


class GameResponsePacket(PacketType):
    DEFINITION_IDENTIFIER = "20194.exercise6.gameserver"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("response", STRING),
        ("status", STRING),
    ]

    @classmethod
    def create_game_response_packet(cls, response, status):
        return cls(response=response, status=status)

    def game_over(self):
        return "Game over 36"

    def status(self):
        return self.status

    def response(self):
        return self.response
