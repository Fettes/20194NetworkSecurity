import asyncio
import time
import playground

from autograder_ex6_packets import AutogradeStartTest
from autograder_ex6_packets import AutogradeTestStatus
from escape_room_packets import GameCommandPacket
from escape_room_packets import GameResponsePacket



class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.flag = 0
        self.loop = loop
        self.deserializer1 = AutogradeTestStatus.Deserializer()
        self.deserializer2 = GameResponsePacket.Deserializer()
        self.command_list = ["look mirror", "get hairpin","unlock chest with hairpin", "open chest",
                             "get hammer in chest", "hit flyingkey with hammer", "get key", "unlock door with key", "open door"]
        self.flag = 0

    def connection_made(self, transport):
        self.transport = transport
        packetClient = AutogradeStartTest()
        packetClient.name = "Tianshi Feng"
        packetClient.team = 4
        packetClient.email = "tfeng7@jhu.edu"
        packetClient.port = 1024
        with open("escape_room_packets.py", "rb") as f:
            packetClient.packet_file = f.read()
        self.transport.write(packetClient.__serialize__())
        self.transport.write("<EOL>\n".encode())

    def data_received(self, data):
        self.deserializer1.update(data)
        for echoPacket in self.deserializer1.nextPackets():
            print(echoPacket.client_status)
        response = GameResponsePacket.response()
        print(response)




        # print(data.decode())
        # respond = data.decode().split("<EOL>\n")
        #
        # # Define the command list
        # command_list = ["SUBMIT,Tianshi Feng,tfeng7@jhu.edu,team 4,1024", "look mirror", "get hairpin","unlock chest with hairpin",
        #                 "open chest", "get hammer in chest", "hit flyingkey with hammer", "get key", "unlock door with key",
        #                 "open door"]
        #
        # if self.flag <= len(command_list) - 1:
        #     if respond[0] == "You can't hit that!":
        #         self.flag = self.flag - 1
        #         command = self.send_message(command_list[self.flag])
        #         self.transport.write(command.encode())
        #         self.flag = self.flag + 1
        #     else:
        #         command = self.send_message(command_list[self.flag])
        #         self.transport.write(command.encode())
        #         self.flag = self.flag + 1
        # time.sleep(1)

    def send_message(self, message):
        command = message + "<EOL>\n"
        return command

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


loop = asyncio.get_event_loop()

coro = playground.create_connection(lambda: EchoClientProtocol(loop), '20194.0.0.19000', 19006)
#coro = loop.create_connection(lambda: EchoClientProtocol(loop), 'localhost', 1024)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
