import asyncio, time
import playground
from autograder_ex6_packets import AutogradeStartTest
from autograder_ex6_packets import AutogradeTestStatus
from packet import GameResponsePacket
from packet import GameCommandPacket
from playground.network.packet import PacketType


class EchoClient(asyncio.Protocol):
    def __init__(self):
        self.index = 0
        self.deserializer = PacketType.Deserializer()

    def connection_made(self, transport):
        self.transport = transport
        packet1 = AutogradeStartTest()
        packet1.name = "Haolin Yuan"
        packet1.team = 4
        packet1.email = "hyuan4@jh.edu"
        packet1.port = 8080
        with open("packet.py", "rb") as f:
            packet1.packet_file = f.read()
        self.transport.write(packet1.__serialize__())

    def data_received(self, data):
        self.deserializer.update(data)
        for item_packet in self.deserializer.nextPackets():
            if isinstance(item_packet, AutogradeTestStatus):
                print(item_packet.submit_status)
                print(item_packet.client_status)
                print(item_packet.server_status)
                print(item_packet.error)

            if isinstance(item_packet, GameResponsePacket):
                data1 = item_packet.res
                print(item_packet.res)

                message = [
                    "look mirror",
                    "get hairpin",
                    "unlock chest with hairpin",
                    "open chest",
                    "look in the chest",
                    "get hammer from chest",
                    "hit flyingkey with hammer",
                    "get key",
                    "unlock door with key",
                    "open door"]

                if self.index <= 9:
                    if data1 == "You can't hit that!":
                        self.index -= 1
                        self.send(message[self.index])
                        self.index += 1
                    else:
                        self.send(message[self.index])
                        self.index += 1
                time.sleep(1)

    def send(self, message):
        packet2 = GameCommandPacket()
        package = packet2.create_game_command_packet(message)
        self.transport.write(package.__serialize__())
        print("66666")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.set_debug(enabled=True)
    from playground.common.logging import EnablePresetLogging, PRESET_DEBUG
    EnablePresetLogging(PRESET_DEBUG)


    coro = playground.create_connection(EchoClient, '20194.0.0.19000', 19006)
    client = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.close()

