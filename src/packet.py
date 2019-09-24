from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING


class GameCommandPacket(PacketType):
    DEFINITION_IDENTIFIER = "command.packet"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("command", STRING),
        # whatever you want here
    ]

    @classmethod
    def create_game_command_packet(cls, s):
        return cls(command=s)

    def command(self):
        return self.command


class GameResponsePacket(PacketType):
    DEFINITION_IDENTIFIER = "response.packet"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("response", STRING),
        ("game_status", STRING),
        # whatever you want here
    ]

    @classmethod
    def create_game_response_packet(cls, response, status):
        return cls(response=response, game_status=status)

    def game_over(self):
        return self.game_status != "playing"

    def status(self):
        # MUST RETURN game.status (as a string)
        return self.game_status

    def response(self):
        # MUST return game response as a string
        return self.command
