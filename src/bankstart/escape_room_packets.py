from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING, UNIT32, BUFFER


class GameCommandPacket(PacketType):
    DEFINITION_IDENTIFIER = "20194.exercise6.gameclient"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("command_line", STRING),
    ]

    @classmethod
    def create_game_command_packet(cls, s):
        return cls(command_line=s)

    def command(self):
        return self.command_line


class GameResponsePacket(PacketType):
    DEFINITION_IDENTIFIER = "20194.exercise6.gameserver"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("res", STRING),
        ("sta", STRING),
    ]

    @classmethod
    def create_game_response_packet(cls, response, status):
        return cls(res=response, sta=status)

    def game_over(self):
        return self.sta != "playing"

    def status(self):
        return self.sta

    def response(self):
        return self.res


class GameInitRequestPacket(PacketType):
    DEFINITION_IDENTIFIER = "20194.exercise7.gameinit"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("username_string", STRING),
    ]


class GamePaymentRequestPacket(PacketType):
    DEFINITION_IDENTIFIER = "20194.exercise7.gamepaymentrequest"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("unique_id", STRING),
        ("account", STRING),
        ("amount", UNIT32)
    ]


class GamePaymentResponsePacket(PacketType):
    DEFINITION_IDENTIFIER = "20194.exercise7.gamepaymentresponse"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("receipt", BUFFER),
        ("receipt_sig", BUFFER),
    ]


def create_game_init_packet(username):
    return GameInitRequestPacket(username_string=username)


def process_game_init(pkt):
    return "tianshi"


def create_game_require_pay_packet(unique_id, account, amount):
    return GamePaymentRequestPacket(unique_id=unique_id, account=account, amount=amount)


def process_game_require_pay_packet(pkt):
    return pkt.unique_id, pkt.account, pkt.amount


def create_game_pay_packet(receipt, receipt_signature):
    return GamePaymentResponsePacket(receipt=receipt, receipt_sig=receipt_signature)


def process_game_pay_packet(pkt):
    return pkt.receipt, pkt.receipt_sig


def create_game_response(response, status):
    return GameResponsePacket(res=response, sta=status)


def process_game_response(pkt):
    return pkt.res


def create_game_command(command):
    return GameCommandPacket(command_line=command)


def process_game_command(pkt):
    return pkt.command_line
