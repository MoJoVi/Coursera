"""
Задача:
написать сетевую программу - клиент, которая будет уметь отправлять данные
различных метрик на сервер, запрашивать информацию хранящихся на сервере
и обрабатывать его ответы.
"""
import socket
import time


class ClientError(socket.error):
    """Пользовательский класс исключений."""
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        try:
            self.sock = socket.create_connection((host, port), timeout)
        except socket.error as err:
            self._save_log_and_raise_err(err, "Error create connection")

    def _push(self, data):
        """
        внутренний метод для отправуи данных на сервер, при ошибке
        отправки данных - выбрасывает пользовательское исключение.
        :param data: данные которые необходимо отправить.
        :return: None.
        """
        try:
            self.sock.sendall(data)
        except socket.error as err:
            self._save_log_and_raise_err(err, 'Error sending data to server')

    def _save_log_and_raise_err(self, error, description):
        """
        Внутренний метод для записи ошибок в лог файл, после чего
        вызывает клиентский класс исключений с заданным текстом описания
        ошибки.
        :param error: сама ошибка для сохранения в лог файл.
        :param description: описание ошибки для пользователя.
        :return: None
        """
        with open('client_log', 'a') as log_file:
            log_file.write(str(error))
            raise ClientError(description)

    def _server_ans(self):
        """
        Внутренний метод считывающий ответ сервера.
        :return: Данные полученные с сервера.
        """
        data = ''
        while data[-2:] != '\n\n':
            try:
                data += self.sock.recv(1024).decode()
            except socket.error as er:
                self._save_log_and_raise_err(er, 'Error receiving response from server')
        if data.startswith('err'):
            raise ClientError('Wrong command')
        return data

    def put(self, key, value, timestamp=time.time()):
        """
        Метод для отправки данных на сервер.
        :param key: наименование метрики.
        :param value: значение данной метрики.
        :param timestamp: время замера.
        :return: None.
        """
        self._push(f'put {key} {value} {timestamp}\n'.encode())
        self._server_ans()

    def get(self, key):
        """
        метод для запроса данных с сервера, при необходимости запроса
        всех данных используется символ "*"
        :param key: наименование метрики данные по которой необходимо получить
        :return: словарь со всеми значениями метрики, которые хранятся на сервере
        """
        self._push(f'get {key}\n'.encode())
        data = self._server_ans().split('\n')
        data = [line for line in data[1:] if line]
        res_dict = {}
        for metric in data:
            key, value, timestamp = metric.split()
            res_dict[key] = res_dict.get(key, list()) + [(int(timestamp), float(value))]
        return res_dict

    def __del__(self):
        """
        Перегруженный метод закрывает соединение при закрытии программы
        или удалении объекта класса
        :return: None
        """
        self.sock.close()


if __name__ == '__main__':
    client = Client("127.0.0.1", 8888, timeout=5)
    client.put("test", 0.5, timestamp=1)
    client.put("test", 2.0, timestamp=2)
    client.put("test", 0.5, timestamp=3)
    client.put("load", 3, timestamp=4)
    client.put("load", 4, timestamp=5)
    print(client.get("*"))
