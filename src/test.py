import asyncio


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.flag = 0
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print(data.decode())
        command = "RESULT,"
        self.transport.write(command.encode())

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


loop = asyncio.get_event_loop()

coro = loop.create_connection(lambda: EchoClientProtocol(loop), '192.168.200.52', 19004)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
