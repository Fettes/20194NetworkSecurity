from CipherUtil import loadCertFromFile
from BankCore import LedgerLineStorage, LedgerLine
from OnlineBank import BankClientProtocol, OnlineBankConfig
import playground, time
import getpass, os, asyncio
import sys

from playground.network.packet import PacketType
from autograder_ex6_packets import AutogradeStartTest
from autograder_ex6_packets import AutogradeTestStatus
import escape_room_packets
from escape_room_packets import *

bankconfig = OnlineBankConfig()
bank_addr = "20194.0.0.19004"
bank_port = 777
bank_stack = "default"
bank_username = "tfeng7"
certPath = os.path.join(bankconfig.path(), "bank.cert")
bank_cert = loadCertFromFile(certPath)


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.flag = 0
        self.loop = asyncio.get_event_loop()
        self.deserializer = PacketType.Deserializer()
        self.command_list = ["look mirror", "get hairpin", "unlock chest with hairpin", "open chest",
                             "get hammer in chest", "hit flyingkey with hammer", "get key", "unlock door with key",
                             "open door"]
        self.flag = 0

    def connection_made(self, transport):
        self.transport = transport
        packetClient = AutogradeStartTest()
        packetClient.name = "Tianshi Feng"
        packetClient.team = 4
        packetClient.email = "tfeng7@jhu.edu"
        packetClient.port = 1026
        with open("escape_room_packets.py", "rb") as f:
            packetClient.packet_file = f.read()
        self.transport.write(packetClient.__serialize__())

        self.command_packet = escape_room_packets.GameCommandPacket.create_game_command_packet("Submit")
        self.transport.write(self.command_packet.__serialize__())

        username = bank_username  # could override at the command line
        password = getpass.getpass("Enter password for {}: ".format(username))
        self.bank_client = BankClientProtocol(bank_cert, username, password)

        # ini_game = create_game_init_packet("Fettes")
        # self.transport.write(ini_game.__serialize__())

    def data_received(self, data):
        print(data)
        self.deserializer.update(data)
        for clientPacket in self.deserializer.nextPackets():
            if isinstance(clientPacket, AutogradeTestStatus):
                print(clientPacket.client_status)
                print(clientPacket.server_status)
                print(clientPacket.error)

            if isinstance(clientPacket, GamePaymentRequestPacket):
                print(clientPacket.unique_id)
                print(clientPacket.account)
                print(clientPacket.amount)
                self.loop.create_task(self.example_transfer(self.bank_client,"tfeng7",clientPacket.account,clientPacket.amount,clientPacket.unique_id))

            if isinstance(clientPacket,GamePaymentResponsePacket):
                print(clientPacket.receipt)
                print(clientPacket.receipt_sig)
                # example_verify(bank_client, result.Receipt, result.ReceiptSignature, dst, amount, memo)


            if isinstance(clientPacket, GameResponsePacket):
                res_temp = clientPacket.res
                print(clientPacket.res)
                if self.flag <= len(self.command_list) - 1:
                    if res_temp.split()[-1] == "wall" or res_temp.split()[-1] == "floor" or res_temp.split()[
                        -1] == "ceiling":
                        continue
                    if res_temp == "You can't hit that!":
                        self.flag = self.flag - 1
                        game_packet = GameCommandPacket()
                        command = game_packet.create_game_command_packet(self.command_list[self.flag])
                        self.transport.write(command.__serialize__())
                        print(self.command_list[self.flag])
                        self.flag = self.flag + 1
                    else:
                        game_packet = GameCommandPacket()
                        command = game_packet.create_game_command_packet(self.command_list[self.flag])
                        self.transport.write(command.__serialize__())
                        print(self.command_list[self.flag])
                        self.flag = self.flag + 1
                time.sleep(1)

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

    async def example_transfer(self, src, dst, amount, memo):
        await playground.create_connection(
            lambda: self,
            bank_addr,
            bank_port,
            family='default'
        )
        print("Connected. Logging in.")

        try:
            await self.loginToServer()
        except Exception as e:
            print("Login error. {}".format(e))
            return False

        try:
            await self.switchAccount(src)
        except Exception as e:
            print("Could not set source account as {} because {}".format(
                src,
                e))
            return False

        try:
            result = await self.transfer(dst, amount, memo)
        except Exception as e:
            print("Could not transfer because {}".format(e))
            return False

        return result




if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)
    from playground.common.logging import EnablePresetLogging, PRESET_DEBUG

    EnablePresetLogging(PRESET_DEBUG)
    coro = playground.create_connection(lambda: EchoClientProtocol(loop), '20194.0.0.19000', 19007)
    # coro = loop.create_connection(lambda: EchoClientProtocol(loop), 'localhost', 1024)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

