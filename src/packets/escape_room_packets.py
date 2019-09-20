from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT8, STRING, BUFFER, UINT16, BOOL, LIST[STRING]
from playground.network.packet.fieldtypes.attributes import Optional



class GameCommandPacket(PacketType):
    DEFINITION_IDENTIFIER =  # whatever you want
    DEFINITION_VERSION =  # whatever you want

    FIELDS = [
        # whatever you want here
    ]

    @classmethod
    def create_game_command_packet(cls, s):
        return cls(  # whatever arguments needed to construct the packet)

    def command(self):
        return  # whatever you need to get the command for the game


class GameResponsePacket(PacketType):
    DEFINITION_IDENTIFIER =  # whatever you want
    DEFINITION_VERSION =  # whatever you want

    FIELDS = [
        # whatever you want here
    ]

    @classmethod
    def create_game_response_packet(cls, response, status):
        return cls(  # whatever you need to construct the packet )

    def game_over(self):
        return  # whatever you need to do to determine if the game is over

    def status(self):
        return  # whatever you need to do to return the status

    def response(self):
        return  # whatever you need to do to return the response