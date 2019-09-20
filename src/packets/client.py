import asyncio
import time
import playground

from src.packets.autograder_ex6_packets import AutogradeStartTest


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.flag = 0
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport
        # self.transport.write("<EOL>\n".encode())
        packetClient = AutogradeStartTest()
        packetClient.name = "Tianshi Feng"
        packetClient.team = 4
        packetClient.email = "tfeng7@jhu.edu"
        packetClient.port = 1024
        packetClient.packet_file = b""
        self.transport.write(packetClient.__serialize__())

    def data_received(self, data):
        print(data.decode())
        respond = data.decode().split("<EOL>\n")

        # Define the command list
        command_list = ["SUBMIT,Tianshi Feng,tfeng7@jhu.edu,team 4,1024", "look mirror", "get hairpin","unlock chest with hairpin",
                        "open chest", "get hammer in chest", "hit flyingkey with hammer", "get key", "unlock door with key",
                        "open door"]

        if self.flag <= len(command_list) - 1:
            if respond[0] == "You can't hit that!":
                self.flag = self.flag - 1
                command = self.send_message(command_list[self.flag])
                self.transport.write(command.encode())
                self.flag = self.flag + 1
            else:
                command = self.send_message(command_list[self.flag])
                self.transport.write(command.encode())
                self.flag = self.flag + 1
        time.sleep(1)

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
