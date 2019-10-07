import asyncio


class Server(asyncio.Protocol):
    metrics_dict = dict()  # для этой задачи вполне достаточно использовать
    # словарь, позже можно будет осуществить долговременое хранение в
    # файле, а лучше с помощью СУБД

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        ans = self.sort_requests(data.decode().strip('\r\n'))
        self.transport.write(ans.encode())

    def sort_requests(self, command):
        client_req = {
            'get': self.get,
            'put': self.put
        }
        request = command.split()
        return client_req.get(request[0], self.wrong_request)(*request[1:])

    @staticmethod
    def get(key):
        res = 'ok\n'
        if key == '*':
            for key, value in Server.metrics_dict.items():
                res += ''.join([f'{key} {t} {val}\n' for val, t in value])
        else:
            for value in Server.metrics_dict.get(key, list()):
                res += f'{key} {value[1]} {value[0]}\n'
        return res + '\n'

    @staticmethod
    def put(key, value, timestamp):
        if Server.metrics_dict.get(key, False):
            if not (timestamp, value) in Server.metrics_dict[key]:
                Server.metrics_dict[key].append((timestamp, value))
        else:
            Server.metrics_dict[key] = [(timestamp, value)]
        return 'ok\n\n'

    @staticmethod
    def wrong_request(*args):
        return 'error\nwrong command\n\n'


def run_server(host, port):

    loop = asyncio.get_event_loop()
    coro = loop.create_server(Server, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server('127.0.0.1', 8888)
