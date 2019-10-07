"""
Задача:
Написать сетевую программу - Сервер, которая будет хранить отправляемые
клиентом метрики и по запросу отправлять данные клиенту
"""

import asyncio


class Server(asyncio.Protocol):
    metrics_dict = dict()  # для этой задачи вполне достаточно использовать
    # словарь, позже можно будет осуществить долговременое хранение в
    # JSON, а лучше с помощью СУБД

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):

        ans = self.sort_requests(data.decode().strip('\r\n'))
        self.transport.write(ans.encode())

    def sort_requests(self, command):
        """
        Метод сортирует запросы клиента и перенаправляет на методы
        "get" b "put" и "wrong command" при ошибочном запросе.
        :param command: данные отправленные клиентом.
        :return: Ответ Сервера для клиента.
        """
        client_req = {
            'get': self.get,
            'put': self.put
        }
        request = command.split()
        return client_req.get(request[0], self.wrong_request)(*request[1:])

    @staticmethod
    def get(key):
        """
        Возвращает клиенту данные хранящиеся на сервере по ключу и формирует
        верный ответ сервера.
        :param key: ключ.
        :return: Запрошенные данные клиента.
        """
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
        """
        Метод записывает отправленные клиентом данные на сервер.
        :param key: ключ.
        :param value: значение.
        :param timestamp: время замера.
        :return: сформированный ответ сервера
        """
        if Server.metrics_dict.get(key, False):
            if not (timestamp, value) in Server.metrics_dict[key]:
                Server.metrics_dict[key].append((timestamp, value))
        else:
            Server.metrics_dict[key] = [(timestamp, value)]
        return 'ok\n\n'

    @staticmethod
    def wrong_request(*args):
        """
        Метод вызывается при неверном запросе со стороны клиента
        :param args: запрос клиента
        :return: Сформированный ответ сервера
        """
        print(args)
        return 'error\nwrong command\n\n'


def run_server(host, port):
    """
    Функция запускающая и закрывающая сервер
    :param host:
    :param port:
    :return:
    """
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
