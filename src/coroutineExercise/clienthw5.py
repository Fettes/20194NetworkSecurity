import asyncio
import playground


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.sendindex = 0

    def connection_made(self, transport):
        print("*")
        self.transport = transport
        self.transport.write(("<EOL>\n").encode())

    def data_received(self, data):
        print(data)
        readytosent = [
            # "RESULT,34ce2a7d2d148a610784b2d83bc0a99496995a9e617192ee9fdc42219df84f7a",
            "SUBMIT, Zichen Wang, zwang216@jhu.edu, 6, 3456",
            "look<EOL>\n",
            "look mirror<EOL>\n",
            "get hairpin<EOL>\n",
            "look chest<EOL>\n",
            "unlock chest with hairpin<EOL>\n",
            "open chest<EOL>\n",
            "look in chest<EOL>\n",
            "get hammer from chest<EOL>\n",
            'hit flyingkey with hammer<EOL>\n',
            'get key<EOL>\n',
            "unlock door with key<EOL>\n",
            "open door<EOL>\n"
        ]
        if (self.sendindex < 13):
            if (self.sendindex == 8):
                if ((data == b'The flyingkey flies from the floor to the wall<EOL>\n') or (
                        data == b'The flyingkey flies from the ceiling to the wall<EOL>\n')):
                    self.transport.write(readytosent[self.sendindex].encode())
                    self.sendindex = self.sendindex + 1
            else:
                self.transport.write(readytosent[self.sendindex].encode())
                self.sendindex = self.sendindex + 1


loop = asyncio.get_event_loop()

conn = playground.create_connection(lambda: EchoClientProtocol(loop), '20194.0.0.19000', 19005)

loop.run_until_complete(conn)
loop.run_forever()
loop.close()
