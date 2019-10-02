from playground.network.packet import PacketType
import playground, time
import getpass, os, asyncio
import sys

from autograder_ex8_packets import *
from escape_room_packets import *
from payProcedure import *


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self):
        self.flag = 0
        self.loop = asyncio.get_event_loop()
        self.deserializer = PacketType.Deserializer()
        self.command_list = ["look mirror", "get hairpin", "unlock chest with hairpin", "open chest",
                             "get hammer in chest", "hit flyingkey with hammer", "get key", "unlock door with key",
                             "open door"]

    def connection_made(self, transport):
        self.transport = transport
        packetClient = AutogradeStartTest()
        packetClient.name = "Tianshi Feng"
        packetClient.team = 4
        packetClient.email = "tfeng7@jhu.edu"
        packetClient.port = 1026
        # with open("escape_room_packets.py", "rb") as f:
        #     packetClient.packet_file = f.read()
        self.transport.write(packetClient.__serialize__())

        user_packet = create_game_init_packet("tfeng7")
        self.transport.write(user_packet.__serialize__())

    def data_received(self, data):
        self.deserializer.update(data)
        print(data)
        for clientPacket in self.deserializer.nextPackets():
            if isinstance(clientPacket, AutogradeTestStatus):
                print(clientPacket.submit_status)
                print(clientPacket.client_status)
                print(clientPacket.server_status)
                print(clientPacket.error)


            if isinstance(clientPacket, GameRequirePayPacket):
                unique_id, account, amount = process_game_require_pay_packet(clientPacket)
                print(unique_id)
                print(account)
                print(amount)
                self.loop.create_task(self.CreatePayment(account, amount, unique_id))

            if isinstance(clientPacket, GameResponsePacket):
                res_temp = clientPacket.response
                print(clientPacket.response)
                if self.flag <= len(self.command_list) - 1:
                    if res_temp.split()[-1] == "wall" or res_temp.split()[-1] == "floor" or res_temp.split()[-1] == "ceiling":
                        continue
                    if res_temp == "You can't hit that!":
                        self.flag = self.flag - 1
                        command = create_game_command(self.command_list[self.flag])
                        self.transport.write(command.__serialize__())
                        print(self.command_list[self.flag])
                        self.flag = self.flag + 1
                    else:
                        command = create_game_command(self.command_list[self.flag])
                        self.transport.write(command.__serialize__())
                        print(self.command_list[self.flag])
                        self.flag = self.flag + 1
                time.sleep(1)

    async def CreatePayment(self, account, amount, unique_id):
        result = await paymentInit("tfeng7_account", account, amount, unique_id)
        print(result)
        receipt, receipt_sig = result
        game_packet = create_game_pay_packet(receipt, receipt_sig)
        self.transport.write(game_packet.__serialize__())

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)
    from playground.common.logging import EnablePresetLogging, PRESET_DEBUG

    EnablePresetLogging(PRESET_DEBUG)
    coro = playground.create_connection(lambda: EchoClientProtocol(), '20194.0.0.19000', 19008)

    # coro = loop.create_connection(lambda: EchoClientProtocol(loop), 'localhost', 1024)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
