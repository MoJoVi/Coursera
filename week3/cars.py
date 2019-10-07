"""
Задача:
Создать иерархию классов для сортировки и удобочитаемого отображения
данных об автомобилях.
"""


import os
import csv


class CarBase:
    """
    Базовый класс
    """
    def __init__(self, brand, photo_file_name, carrying):
        """
        Присваеваем базовые характеристики, которые есть у всех авто
        :param brand: Фирма авто.
        :param photo_file_name: имя файла с фото авто
        :param carrying: Грузободъемность
        """
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying

    def get_photo_file_ext(self):
        """
        :return: разрешение файла с фото авто
        """
        return os.path.splitext(self.photo_file_name)[-1]

    def __str__(self):
        """
        Перегрузил метод __str__ для удобства отображения, хоть этого и нет
        в задании, но так намного проще отображать данные о машинах
        :return:
        """
        res_string = ''
        for key, value in self.__dict__.items():
            res_string += f'{key}: {value}, '
        return res_string[:-2] + '.\n'


class Car(CarBase):
    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        """
        :param passenger_seats_count: Количество мест.
        """
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        """
        :param body_whl: Характеристики кузова.
        """
        super().__init__(brand, photo_file_name, carrying)

        if body_whl:
            self.body_length, self.body_width, self.body_height \
                = [float(whl) for whl in body_whl.split('x')]
        else:
            self.body_length = self.body_width = self.body_height = 0.0

    def get_body_volume(self):
        return self.body_height * self.body_length * self.body_width


class SpecMachine(CarBase):
    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        """
        :param extra: Назначение авто.
        """
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def sorting_args(args, ix):
    """
    :param args: агрументы
    :param ix: Индекс специального аргумента
    :return: список аргументов для данного вида авто
    """
    return [args[0], args[2], float(args[4]), args[ix]]


def get_car_list(csv_filename):
    """
    :param csv_filename: csv-файл из которого необходимо взять параметры авто
    :return: словарь с объектами классов автомобилей
    """
    cars = {
        'car': [1, Car],
        'truck': [3, Truck],
        'spec_machine': [5, SpecMachine]
    }  # Словарь создан для сортировки авто и вызова необходимых классов и
    # чтобы избежать большого количества if-ов
    car_list = []  # список с итоговым результатом

    try:
        with open(csv_filename, encoding='utf8') as csv_fd:
            reader = csv.reader(csv_fd, delimiter=';')
            next(reader)  # пропускаем заголовок
            for row in reader:
                if [elem for elem in row if elem]:  # Проверяем не является ли список пустым
                    model = row.pop(0)
                    args = sorting_args(row, cars[model][0])  # Сортируем аргументы
                    car_list.append(cars[model][1](*args))

    except FileNotFoundError:
        return None
    else:
        return car_list


if __name__ == '__main__':
    cars = get_car_list('coursera_week3_cars.csv')
    for car in cars:
        print(car)
